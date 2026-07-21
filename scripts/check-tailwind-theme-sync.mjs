import { readFile } from "node:fs/promises";

const sourceUrl = new URL("../insight_ui/utils/input.css", import.meta.url);
const compiledUrl = new URL("../insight_ui/static/insight_ui/css/tailwind.css", import.meta.url);

const REQUIRED_COMPILED_TOKENS = [
    "--color-insight-primary",
    "--color-insight-secondary",
    "--color-insight-text-primary",
    "--color-insight-text-secondary",
    "--insight-surface-page",
    "--insight-surface-page-dark",
    "--insight-surface-base",
    "--insight-surface-base-dark",
    "--insight-surface-muted",
    "--insight-surface-muted-dark",
    "--insight-surface-subtle",
    "--insight-surface-subtle-dark",
    "--insight-surface-raised",
    "--insight-surface-raised-dark",
    "--insight-border-subtle",
    "--insight-border-default",
    "--insight-radius-control",
    "--insight-shadow-surface",
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
    return value.trim().replace(/\s+/g, " ");
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
const compiledTokens = extractCustomProperties(compiledCss);
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

    console.error("Run `USE_TAILWIND_CLI=True uv run manage.py tailwind build --force` and then `npm run build:static`.");
    process.exit(1);
}

console.log("tailwind.css theme tokens are current against input.css");
