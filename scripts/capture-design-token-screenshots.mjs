import { execFileSync } from "node:child_process";
import { mkdir } from "node:fs/promises";
import { createRequire } from "node:module";
import { join } from "node:path";

const require = createRequire(import.meta.url);

function loadPlaywright() {
    try {
        return require("playwright");
    } catch {
        const globalRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
        return require(require.resolve("playwright", { paths: [globalRoot] }));
    }
}

const { chromium } = loadPlaywright();

const baseUrl = process.env.INSIGHT_UI_SCREENSHOT_BASE_URL || "http://127.0.0.1:8010";
const phase = process.env.INSIGHT_UI_SCREENSHOT_PHASE || "before";
const outputRoot =
    process.env.INSIGHT_UI_SCREENSHOT_OUTPUT ||
    "docs/assets/design-token-impact-map";

const viewport = { width: 1440, height: 1100 };
const themes = ["default", "brite"];
const pages = [
    ["overview", "/docs/components/"],
    ["buttons", "/docs/components/button/"],
    ["forms", "/docs/components/form/"],
    ["cards", "/docs/components/app_card/"],
    ["navigation", "/docs/components/sidebar/"],
    ["feedback", "/docs/components/alert/"],
    ["table", "/docs/components/table/"],
    ["range-slider", "/docs/components/range_slider/"],
];

const browser = await chromium.launch();
const context = await browser.newContext({ viewport });

await context.addInitScript((themeName) => {
    window.localStorage.setItem("insight-ui-design-theme", themeName);
}, themes[0]);

for (const theme of themes) {
    const themeDir = join(outputRoot, phase, theme);
    await mkdir(themeDir, { recursive: true });

    for (const [name, path] of pages) {
        const page = await context.newPage();
        await page.addInitScript((themeName) => {
            window.localStorage.setItem("insight-ui-design-theme", themeName);
        }, theme);
        await page.goto(new URL(path, baseUrl).toString(), { waitUntil: "networkidle" });
        await page.screenshot({
            path: join(themeDir, `${name}.png`),
            fullPage: true,
        });
        await page.close();
    }
}

await browser.close();
