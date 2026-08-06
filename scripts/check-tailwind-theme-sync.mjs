import { readFile } from "node:fs/promises";

const sourceUrl = new URL("../insight_ui/utils/input.css", import.meta.url);
const compiledUrl = new URL("../insight_ui/static/insight_ui/css/tailwind.css", import.meta.url);

const REQUIRED_COMPILED_TOKENS = [
    "--color-insight-bg-base",
    "--color-insight-bg-surface",
    "--color-insight-bg-raised",
    "--color-insight-bg-overlay",
    "--color-insight-border-surface",
    "--color-insight-border-raised",
    "--color-insight-border-overlay",
    "--color-insight-primary",
    "--color-insight-secondary",
    "--color-insight-text-primary",
    "--color-insight-text-secondary",
    "--radius-insight-control",
    "--radius-insight-surface",
    "--radius-insight-raised",
    "--radius-insight-overlay",
    "--shadow-insight-subtle",
    "--shadow-insight-surface",
    "--shadow-insight-raised",
    "--shadow-insight-overlay",
];

const COMPARABLE_TOKEN_PREFIXES = [
    "--color-insight-",
    "--insight-surface-",
    "--insight-border-",
    "--insight-radius-",
    "--insight-shadow-",
    "--insight-nav-",
    "--insight-sidebar-",
    "--insight-user-dropdown-",
    "--insight-progress-",
    "--insight-chat-",
    "--insight-table-",
    "--insight-form-",
    "--insight-control-",
];

function stripCssComments(css) {
    return css.replace(/\/\*[\s\S]*?\*\//g, "");
}

function extractCompiledThemeLayer(css) {
    const themeStart = css.indexOf("@layer theme");
    const baseStart = css.indexOf("@layer base", themeStart);

    if (themeStart === -1 || baseStart === -1) {
        return css;
    }

    return css.slice(themeStart, baseStart);
}

function extractCustomProperties(css) {
    const declarations = new Map();
    const declarationPattern = /(--[a-zA-Z0-9_-]+)\s*:\s*([^;{}]+);/g;

    for (const match of stripCssComments(css).matchAll(declarationPattern)) {
        const [, name, value] = match;
        if (!declarations.has(name)) {
            declarations.set(name, normalizeValue(value));
        }
    }

    return declarations;
}

function normalizeValue(value) {
    return value
        .trim()
        .replace(/\s+/g, " ")
        .replace(/#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?/g, normalizeHex)
        .replace(/rgb\(0 0 0 \/ 0\.1\)/g, "#0000001a");
}

function normalizeHex(match, color, alpha = "") {
    const lowerColor = color.toLowerCase();
    const lowerAlpha = alpha.toLowerCase();

    if (
        !lowerAlpha &&
        lowerColor[0] === lowerColor[1] &&
        lowerColor[2] === lowerColor[3] &&
        lowerColor[4] === lowerColor[5]
    ) {
        return `#${lowerColor[0]}${lowerColor[2]}${lowerColor[4]}`;
    }

    return `#${lowerColor}${lowerAlpha}`;
}

function isComparableToken(name, sourceValue) {
    if (sourceValue.includes("color-mix(")) {
        // Tailwind emits a fallback value plus an @supports override for these.
        return false;
    }

    return COMPARABLE_TOKEN_PREFIXES.some((prefix) => name.startsWith(prefix));
}

function formatMismatch({ name, sourceValue, compiledValue }) {
    return [
        `- ${name}`,
        `  input.css:    ${sourceValue}`,
        `  tailwind.css: ${compiledValue ?? "<missing>"}`,
    ].join("\n");
}

const [sourceCss, compiledCss] = await Promise.all([
    readFile(sourceUrl, "utf8"),
    readFile(compiledUrl, "utf8"),
]);

const sourceTokens = extractCustomProperties(sourceCss);
const compiledTokens = extractCustomProperties(extractCompiledThemeLayer(compiledCss));
const missingRequiredTokens = REQUIRED_COMPILED_TOKENS.filter((token) => !compiledTokens.has(token));

const mismatches = [];
for (const [name, compiledValue] of compiledTokens) {
    const sourceValue = sourceTokens.get(name);
    if (!sourceValue || !isComparableToken(name, sourceValue)) {
        continue;
    }

    if (compiledValue !== sourceValue) {
        mismatches.push({ name, sourceValue, compiledValue });
    }
}

if (missingRequiredTokens.length > 0 || mismatches.length > 0) {
    if (missingRequiredTokens.length > 0) {
        console.error("tailwind.css is missing required Insight UI theme tokens:");
        console.error(missingRequiredTokens.map((token) => `- ${token}`).join("\n"));
    }

    if (mismatches.length > 0) {
        console.error("tailwind.css is stale against insight_ui/utils/input.css:");
        console.error(mismatches.map(formatMismatch).join("\n"));
    }

    console.error("Run `USE_TAILWIND_CLI=True uv run manage.py tailwind build --force --no-minify` and then `npm run build:static`.");
    process.exit(1);
}

console.log("tailwind.css theme tokens are current against input.css");
