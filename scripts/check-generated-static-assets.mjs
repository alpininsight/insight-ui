import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const generatedAssetPatterns = [
    ":(glob)insight_ui/static/insight_ui/css/**/*.min.css",
    ":(glob)insight_ui/static/insight_ui/js/**/*.min.js",
];

const { stdout } = await execFileAsync("git", ["ls-files", "--", ...generatedAssetPatterns]);
const trackedAssets = stdout.split("\n").filter(Boolean);

if (trackedAssets.length > 0) {
    console.error("Generated minified assets must not be tracked in the package repository:");
    console.error(trackedAssets.map((asset) => `- ${asset}`).join("\n"));
    console.error("The central static-assets workflow generates and publishes these CDN artifacts.");
    process.exit(1);
}

console.log("No generated minified static assets are tracked.");
