// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const script = fileURLToPath(new URL("../../scripts/check-generated-static-assets.mjs", import.meta.url));

function run(command, args, cwd, env = process.env) {
    return new Promise((resolve, reject) => {
        execFile(command, args, { cwd, env, encoding: "utf8" }, (error, stdout, stderr) => {
            if (error && error.code === "ENOENT") {
                reject(error);
                return;
            }
            const code = typeof error?.code === "number" ? error.code : 0;
            resolve({ code, stdout, stderr });
        });
    });
}

function envWithoutParentGit(dir) {
    const env = { ...process.env, GIT_CEILING_DIRECTORIES: dir };
    delete env.GIT_DIR;
    delete env.GIT_WORK_TREE;
    return env;
}

async function initRepo() {
    const dir = await mkdtemp(join(tmpdir(), "min-assets-"));
    const init = await run("git", ["init", "-q"], dir);
    assert.equal(init.code, 0, init.stderr);
    await writeFile(join(dir, "app.js"), "export {}\n");
    const add = await run("git", ["add", "--", "app.js"], dir);
    assert.equal(add.code, 0, add.stderr);
    return dir;
}

test("untracked minified files do not fail the check", async () => {
    const dir = await initRepo();
    try {
        await mkdir(join(dir, "nested"));
        await writeFile(join(dir, "app.min.js"), "min\n");
        await writeFile(join(dir, "nested", "app.min.css"), "body{}\n");

        const result = await run(process.execPath, [script], dir);

        assert.equal(result.code, 0, result.stderr);
    } finally {
        await rm(dir, { recursive: true, force: true });
    }
});

test("a tracked minified file fails, including from a subdirectory", async () => {
    const dir = await initRepo();
    try {
        await mkdir(join(dir, "nested", "deeper"), { recursive: true });
        await writeFile(join(dir, "nested", "deeper", "app.min.js"), "min\n");
        const add = await run("git", ["add", "-f", "--", "nested/deeper/app.min.js"], dir);
        assert.equal(add.code, 0, add.stderr);

        const fromRoot = await run(process.execPath, [script], dir);
        const fromSubdir = await run(process.execPath, [script], join(dir, "nested"));

        assert.equal(fromRoot.code, 1);
        assert.match(fromRoot.stderr, /nested\/deeper\/app\.min\.js/);
        assert.equal(fromSubdir.code, 1);
        assert.match(fromSubdir.stderr, /nested\/deeper\/app\.min\.js/);
    } finally {
        await rm(dir, { recursive: true, force: true });
    }
});

test("tracked names that only contain the minified suffix do not fail", async () => {
    const dir = await initRepo();
    try {
        await writeFile(join(dir, "notes.min.js.txt"), "not a script\n");
        await writeFile(join(dir, "already.min.js.bak"), "not a script\n");
        const add = await run("git", ["add", "--", "notes.min.js.txt", "already.min.js.bak"], dir);
        assert.equal(add.code, 0, add.stderr);

        const result = await run(process.execPath, [script], dir);

        assert.equal(result.code, 0, result.stderr);
    } finally {
        await rm(dir, { recursive: true, force: true });
    }
});

test("a temporary repository with no tracked minified assets passes", async () => {
    const dir = await initRepo();
    try {
        const result = await run(process.execPath, [script], dir, envWithoutParentGit(dir));

        assert.equal(result.code, 0, result.stderr);
        assert.match(result.stdout, /No minified CSS or JavaScript assets are tracked/);
    } finally {
        await rm(dir, { recursive: true, force: true });
    }
});

test("a directory without git metadata fails cleanly", async () => {
    const dir = await mkdtemp(join(tmpdir(), "min-assets-nogit-"));
    try {
        const result = await run(process.execPath, [script], dir, envWithoutParentGit(dir));

        assert.equal(result.code, 1);
        assert.match(result.stderr, /Could not list tracked files/);
        assert.match(result.stderr, /not a git repository/);
    } finally {
        await rm(dir, { recursive: true, force: true });
    }
});
