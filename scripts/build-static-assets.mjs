import { readdir, readFile, unlink, writeFile } from "node:fs/promises";
import { basename } from "node:path";
import { fileURLToPath } from "node:url";
import { minify } from "terser";

const assetRoot = new URL("../insight_ui/static/insight_ui/", import.meta.url);
const checkMode = process.argv.includes("--check");

const assetGroups = [
    {
        directory: new URL("js/", assetRoot),
        extension: ".js",
        minExtension: ".min.js",
        build: minifyJavaScript,
        label: "JavaScript",
    },
    {
        directory: new URL("css/", assetRoot),
        extension: ".css",
        minExtension: ".min.css",
        build: minifyCss,
        label: "CSS",
    },
];

function toMinifiedName(sourceFile, extension, minExtension) {
    return sourceFile.slice(0, -extension.length) + minExtension;
}

function toMinifiedJavaScriptSpecifier(specifier) {
    if (!specifier.startsWith("./") && !specifier.startsWith("../")) {
        return specifier;
    }
    if (!specifier.endsWith(".js") || specifier.endsWith(".min.js")) {
        return specifier;
    }

    return specifier.slice(0, -".js".length) + ".min.js";
}

function rewriteJavaScriptModuleSpecifiers(sourceFile, code) {
    const rewriteStaticSpecifier = (_match, prefix, quote, specifier) => {
        const rewrittenSpecifier = toMinifiedJavaScriptSpecifier(specifier);
        return `${prefix}${quote}${rewrittenSpecifier}${quote}`;
    };
    const rewriteDynamicSpecifier = (_match, prefix, quote, specifier, suffix) => {
        const rewrittenSpecifier = toMinifiedJavaScriptSpecifier(specifier);
        return `${prefix}${quote}${rewrittenSpecifier}${quote}${suffix}`;
    };

    const rewritten = code
        .replace(/\b(from\s*)(["'])([^"']+)\2/g, rewriteStaticSpecifier)
        .replace(/\b(import\s*)(["'])([^"']+)\2/g, rewriteStaticSpecifier)
        .replace(/\b(import\s*\(\s*)(["'])([^"']+)\2(\s*\))/g, rewriteDynamicSpecifier);

    const remainingUnminifiedImports = [
        ...rewritten.matchAll(/\b(?:from\s*|import\s*|import\s*\(\s*)(["'])(\.{1,2}\/[^"']+\.js)\1/g),
    ].filter((match) => !match[2].endsWith(".min.js"));

    if (remainingUnminifiedImports.length > 0) {
        const specifiers = remainingUnminifiedImports.map((match) => match[2]).join(", ");
        throw new Error(`Unminified relative module imports remain in ${sourceFile}: ${specifiers}`);
    }

    return rewritten;
}

async function minifyJavaScript(sourceFile, source) {
    const isModule = /\b(?:import|export)\b/.test(source);
    const result = await minify({ [sourceFile]: source }, {
        module: isModule,
        ecma: 2022,
        compress: true,
        mangle: true,
        format: { comments: false },
    });

    if (!result.code) {
        throw new Error(`Terser produced empty output for ${sourceFile}`);
    }

    return isModule ? rewriteJavaScriptModuleSpecifiers(sourceFile, result.code) : result.code;
}

async function minifyCss(sourceFile, source) {
    const minified = source
        .replace(/\/\*[\s\S]*?\*\//g, (comment) => comment.startsWith("/*!") ? comment : "")
        .replace(/\s+/g, " ")
        .replace(/\s*([{};,])\s*/g, "$1")
        .replace(/:\s+/g, ":")
        .replace(/;}/g, "}")
        .trim();

    if (!minified) {
        throw new Error(`CSS minifier produced empty output for ${sourceFile}`);
    }

    validateCssOutput(sourceFile, source, minified);

    return minified;
}

function validateCssOutput(sourceFile, source, output) {
    const missingLicenseComments = [...source.matchAll(/\/\*![\s\S]*?\*\//g)]
        .map((match) => match[0].replace(/\s+/g, " ").trim())
        .filter((comment) => !output.includes(comment));

    if (missingLicenseComments.length > 0) {
        throw new Error(`Minified ${sourceFile} is missing required license comments`);
    }

    if (sourceFile !== "tailwind.css") {
        return;
    }

    const requiredPatterns = [
        [".bg-insight-primary", /\.bg-insight-primary\{[^}]*background-color:\s*var\(--color-insight-primary\)/],
        [".fill-insight-primary", /\.fill-insight-primary\{[^}]*fill:\s*var\(--color-insight-primary\)/],
        [".text-insight-primary", /\.text-insight-primary\{[^}]*color:\s*var\(--color-insight-primary\)/],
        ["--color-insight-primary-foreground", /--color-insight-primary-foreground:\s*#fff/],
        ["--insight-shadow-button", /--insight-shadow-button:\s*none/],
        [".btn-primary foreground", /\.btn-primary\{[^}]*color:\s*var\(--color-insight-primary-foreground\)/],
        [".btn-secondary foreground", /\.btn-secondary\{[^}]*color:\s*var\(--color-insight-secondary-foreground\)/],
        [".btn-secondary border", /\.btn-secondary\{[^}]*--insight-button-border-color:\s*var\(--color-insight-button-border/],
        [".insight-surface-page", /\.insight-surface-page\{[^}]*background-color:\s*var\(--color-insight-surface-page\)/],
        [".insight-surface-base", /\.insight-surface-base\{[^}]*background-color:\s*var\(--color-insight-surface-base\)/],
        [".insight-radius-control", /\.insight-radius-control\{[^}]*border-radius:\s*var\(--insight-radius-sm\)/],
        [".insight-radius-surface", /\.insight-radius-surface\{[^}]*border-radius:\s*var\(--insight-radius-md\)/],
        [".insight-shadow-surface", /\.insight-shadow-surface\{[^}]*box-shadow:\s*var\(--insight-shadow-surface\)/],
        [".btn-white", /\.btn-white\{/],
        [".lg:flex-row", /\.lg\\:flex-row\{/],
        [".lg:hidden", /\.lg\\:hidden\{/],
        [".xl:block", /\.xl\\:block\{/],
    ];
    const missingTokens = requiredPatterns.filter(([, pattern]) => !pattern.test(output)).map(([label]) => label);

    if (missingTokens.length > 0) {
        throw new Error(`Minified ${sourceFile} is missing required selectors: ${missingTokens.join(", ")}`);
    }
}

async function processAssetGroup({ directory, extension, minExtension, build, label }) {
    const entries = await listAssetFiles(directory);
    const sourceFiles = entries
        .filter((name) => name.endsWith(extension) && !name.endsWith(minExtension))
        .sort();

    if (sourceFiles.length === 0) {
        throw new Error(`No ${label} source files found in ${fileURLToPath(directory)}`);
    }

    const generatedFiles = new Set();
    const staleFiles = [];

    for (const sourceFile of sourceFiles) {
        const sourceUrl = new URL(sourceFile, directory);
        const source = await readFile(sourceUrl, "utf8");
        const outputFile = toMinifiedName(sourceFile, extension, minExtension);
        const outputUrl = new URL(outputFile, directory);
        const minified = await build(sourceFile, source);
        const output = [
            `/* Generated from ${sourceFile}; do not edit directly. Run npm run build:js. */`,
            minified,
            "",
        ].join("\n");

        if (checkMode) {
            try {
                const existingOutput = await readFile(outputUrl, "utf8");
                if (existingOutput !== output) {
                    staleFiles.push(outputFile);
                }
            } catch (error) {
                if (error.code !== "ENOENT") {
                    throw error;
                }
                staleFiles.push(outputFile);
            }
        } else {
            await writeFile(outputUrl, output, "utf8");
        }

        generatedFiles.add(outputFile);

        const sourceBytes = Buffer.byteLength(source, "utf8");
        const outputBytes = Buffer.byteLength(output, "utf8");
        const ratio = Math.round((outputBytes / sourceBytes) * 100);
        console.log(`${basename(sourceFile)} -> ${outputFile} (${outputBytes}/${sourceBytes} bytes, ${ratio}%)`);
    }

    for (const entry of entries) {
        if (entry.endsWith(minExtension) && !generatedFiles.has(entry)) {
            if (checkMode) {
                staleFiles.push(entry);
            } else {
                await unlink(new URL(entry, directory));
                console.log(`Removed stale generated file ${entry}`);
            }
        }
    }

    return staleFiles;
}

async function listAssetFiles(directory, relativeDirectory = "") {
    const files = [];
    const entries = await readdir(new URL(relativeDirectory, directory), { withFileTypes: true });

    for (const entry of entries) {
        const relativePath = `${relativeDirectory}${entry.name}`;
        if (entry.isDirectory()) {
            files.push(...await listAssetFiles(directory, `${relativePath}/`));
        } else if (entry.isFile()) {
            files.push(relativePath);
        }
    }

    return files;
}

const staleFiles = [];
for (const group of assetGroups) {
    staleFiles.push(...await processAssetGroup(group));
}

if (staleFiles.length > 0) {
    console.error(`Generated static assets are stale: ${staleFiles.join(", ")}`);
    console.error("Run npm run build:js and commit the generated .min.js/.min.css files.");
    process.exit(1);
}

if (checkMode) {
    console.log("generated static assets are current");
}
