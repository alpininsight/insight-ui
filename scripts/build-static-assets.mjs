import CleanCSS from "clean-css";
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

    return result.code;
}

async function minifyCss(sourceFile, source) {
    const result = new CleanCSS({ level: 2 }).minify(source);

    if (result.errors.length > 0) {
        throw new Error(`CleanCSS failed for ${sourceFile}: ${result.errors.join("; ")}`);
    }
    if (!result.styles) {
        throw new Error(`CleanCSS produced empty output for ${sourceFile}`);
    }

    return result.styles;
}

async function processAssetGroup({ directory, extension, minExtension, build, label }) {
    const entries = await readdir(directory, { withFileTypes: true });
    const sourceFiles = entries
        .filter((entry) => entry.isFile())
        .map((entry) => entry.name)
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
        if (entry.isFile() && entry.name.endsWith(minExtension) && !generatedFiles.has(entry.name)) {
            if (checkMode) {
                staleFiles.push(entry.name);
            } else {
                await unlink(new URL(entry.name, directory));
                console.log(`Removed stale generated file ${entry.name}`);
            }
        }
    }

    return staleFiles;
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
