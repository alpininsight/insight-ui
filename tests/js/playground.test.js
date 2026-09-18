// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
import { existsSync } from "node:fs";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

describe.skipIf(!existsSync(".git"))("source-only component playground", () => {
    let themeObserver;

    afterEach(() => { vi.unstubAllGlobals(); });

    beforeEach(async () => {
        vi.resetModules();
        document.documentElement.dataset.theme = "light";
        document.body.innerHTML = `
            <select id="viewport-select">
                <option value="desktop">Desktop</option>
                <option value="mobile">Mobile</option>
                <option value="full">Full Width</option>
            </select>
            <input id="rtl-toggle" type="checkbox">
            <iframe id="component-preview"></iframe>`;
        vi.stubGlobal("MutationObserver", class {
            constructor(callback) { themeObserver = callback; }
            observe() {}
        });
        await import("../../devtools/static/devtools/playground.js");
    });

    it("resizes the frame viewport, not just an inner component div", () => {
        const frame = document.getElementById("component-preview");
        const select = document.getElementById("viewport-select");
        expect(frame.style.width).toBe("1024px");
        select.value = "mobile";
        select.dispatchEvent(new Event("change"));
        expect(frame.style.width).toBe("375px");
        select.value = "full";
        select.dispatchEvent(new Event("change"));
        expect(frame.style.width).toBe("100%");
    });

    it("keeps RTL and dark mode in sync on changes and frame reloads", () => {
        const frame = document.getElementById("component-preview");
        const root = frame.contentDocument.documentElement;
        const rtl = document.getElementById("rtl-toggle");
        rtl.checked = true;
        rtl.dispatchEvent(new Event("change"));
        expect(root.dir).toBe("rtl");
        document.documentElement.dataset.theme = "dark";
        themeObserver();
        expect(root.dataset.theme).toBe("dark");
        expect(root.classList.contains("dark")).toBe(true);
        root.dir = "ltr";
        frame.dispatchEvent(new Event("load"));
        expect(root.dir).toBe("rtl");
        document.documentElement.dataset.theme = "light";
        themeObserver();
        expect(root.classList.contains("dark")).toBe(false);
    });
});
