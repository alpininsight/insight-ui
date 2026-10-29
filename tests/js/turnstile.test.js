// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

let Turnstile;

function createForm() {
    const form = document.createElement("form");
    form.innerHTML = `
        <div data-insight-turnstile data-sitekey="public-key" data-theme="dark" data-size="compact" data-action="contact">
            <div data-insight-turnstile-widget></div>
            <p data-insight-turnstile-error hidden role="alert">Unavailable</p>
        </div>
    `;
    document.body.appendChild(form);
    return form;
}

function loadScript(api) {
    window.turnstile = api;
    const script = document.querySelector('script[src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"]');
    script.dispatchEvent(new Event("load"));
    return script;
}

describe("Turnstile component", () => {
    beforeEach(async () => {
        vi.resetModules();
        ({ Turnstile } = await import("../../insight_ui/static/insight_ui/js/insight-ui-turnstile.js"));
        document.body.innerHTML = "";
        delete window.turnstile;
    });

    afterEach(() => {
        vi.useRealTimers();
        vi.restoreAllMocks();
        document.querySelectorAll('script[src^="https://challenges.cloudflare.com/turnstile/"]').forEach(s => s.remove());
        delete window.turnstile;
    });

    it("loads Cloudflare's original script once and renders the public config", async () => {
        const first = createForm();
        const second = createForm();
        const api = { render: vi.fn().mockReturnValueOnce("widget-1").mockReturnValueOnce("widget-2") };

        Turnstile.initAll();
        Turnstile.initAll();
        expect(document.querySelectorAll('script[src^="https://challenges.cloudflare.com/turnstile/"]')).toHaveLength(1);

        loadScript(api);
        await vi.waitFor(() => expect(api.render).toHaveBeenCalledTimes(2));
        expect(api.render).toHaveBeenCalledWith(first.querySelector("[data-insight-turnstile-widget]"),
            expect.objectContaining({ sitekey: "public-key", theme: "dark", size: "compact", action: "contact" }));
        expect(api.render).toHaveBeenCalledWith(second.querySelector("[data-insight-turnstile-widget]"),
            expect.objectContaining({ sitekey: "public-key" }));
    });

    it("does not render a widget removed while the API was loading", async () => {
        const form = createForm();
        const element = form.querySelector("[data-insight-turnstile]");
        const api = { render: vi.fn() };
        const instance = new Turnstile(element);

        instance.destroy();
        form.remove();
        loadScript(api);
        await Promise.resolve();
        expect(api.render).not.toHaveBeenCalled();
    });

    it("refreshes the one-use token after HTMX requests and form resets", async () => {
        const form = createForm();
        const element = form.querySelector("[data-insight-turnstile]");
        const api = { render: vi.fn().mockReturnValue("widget-1"), reset: vi.fn(), remove: vi.fn() };
        const instance = new Turnstile(element);

        loadScript(api);
        await vi.waitFor(() => expect(api.render).toHaveBeenCalledOnce());
        vi.useFakeTimers();
        form.dispatchEvent(new CustomEvent("htmx:afterRequest", { detail: { elt: form } }));
        vi.runAllTimers();
        expect(api.reset).toHaveBeenCalledWith("widget-1");

        form.dispatchEvent(new Event("reset"));
        instance.destroy();
        vi.runAllTimers();
        expect(api.reset).toHaveBeenCalledTimes(1);
        expect(api.remove).toHaveBeenCalledWith("widget-1");
    });

    it("shows an accessible error when the API cannot load", async () => {
        const form = createForm();
        const element = form.querySelector("[data-insight-turnstile]");
        new Turnstile(element);

        document.querySelector('script[src^="https://challenges.cloudflare.com/turnstile/"]')
            .dispatchEvent(new Event("error"));
        await vi.waitFor(() => expect(element.querySelector("[role=alert]").hidden).toBe(false));
        expect(document.querySelector('script[src^="https://challenges.cloudflare.com/turnstile/"]')).toBeNull();

        createForm();
        Turnstile.initAll();
        expect(document.querySelectorAll('script[src^="https://challenges.cloudflare.com/turnstile/"]')).toHaveLength(1);
    });
});
