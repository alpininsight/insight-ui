// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

function isTrackedMinifiedAsset(path) {
    return path.endsWith(".min.css") || path.endsWith(".min.js");
}

// Index only. `build:static` writes ignored, untracked siblings next to the
// sources; those local artifacts must not fail this check.
async function trackedMinifiedAssets() {
    const { stdout: toplevel } = await execFileAsync("git", ["rev-parse", "--show-toplevel"], {
        encoding: "utf8",
    });
    const repoRoot = toplevel.trim();
    const { stdout } = await execFileAsync("git", ["-C", repoRoot, "ls-files", "-z"], {
        cwd: repoRoot,
        encoding: "utf8",
    });

    return stdout.split("\0").filter(isTrackedMinifiedAsset);
}

try {
    const trackedAssets = await trackedMinifiedAssets();

    if (trackedAssets.length > 0) {
        console.error("Tracked minified assets must not be committed:");
        console.error(trackedAssets.map((asset) => `- ${asset}`).join("\n"));
        console.error("Minified CSS and JavaScript are generated CDN artifacts.");
        console.error(".gitignore does not stop git add -f; remove them from the index.");
        process.exit(1);
    }

    console.log("No minified CSS or JavaScript assets are tracked.");
} catch (error) {
    const detail = `${error.stderr ?? ""}`.trim() || error.message;
    console.error(`Could not list tracked files: ${detail}`);
    process.exit(1);
}
