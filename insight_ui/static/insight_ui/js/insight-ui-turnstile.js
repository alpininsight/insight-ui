// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/** Optional Turnstile widget lifecycle for forms and HTMX fragments. */

const API_URL = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
let apiPromise = null;

function loadTurnstile() {
    if (window.turnstile) return Promise.resolve(window.turnstile);
    if (apiPromise) return apiPromise;

    apiPromise = new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = API_URL;
        script.async = true;
        script.onload = () => {
            if (window.turnstile) resolve(window.turnstile);
            else {
                script.remove();
                reject(new Error("Turnstile API did not initialize"));
            }
        };
        script.onerror = () => {
            script.remove();
            reject(new Error("Turnstile API could not be loaded"));
        };
        document.head.appendChild(script);
    }).catch(error => {
        apiPromise = null;
        return Promise.reject(error);
    });
    return apiPromise;
}

export class Turnstile {
    static instances = new WeakMap();

    constructor(element) {
        if (Turnstile.instances.has(element)) return Turnstile.instances.get(element);

        this.element = element;
        this.widget = element.querySelector("[data-insight-turnstile-widget]");
        this.error = element.querySelector("[data-insight-turnstile-error]");
        this.form = element.closest("form");
        this.widgetId = null;
        this.destroyed = false;
        this.resetTimer = null;
        this.boundReset = () => this.scheduleReset();
        this.boundAfterRequest = event => {
            if (event.detail?.elt === this.form) this.scheduleReset();
        };

        this.form?.addEventListener("reset", this.boundReset);
        this.form?.addEventListener("htmx:afterRequest", this.boundAfterRequest);
        element.__insightInstance = this;
        Turnstile.instances.set(element, this);

        loadTurnstile().then(api => {
            if (this.destroyed || !this.element.isConnected) return;
            const options = {
                sitekey: element.dataset.sitekey,
                theme: element.dataset.theme || "auto",
                size: element.dataset.size || "normal",
                callback: () => { if (this.error) this.error.hidden = true; },
                "error-callback": () => { if (this.error) this.error.hidden = false; },
            };
            if (element.dataset.action) options.action = element.dataset.action;
            this.widgetId = api.render(this.widget, options);
        }).catch(() => {
            if (!this.destroyed && this.error) this.error.hidden = false;
        });
    }

    scheduleReset() {
        clearTimeout(this.resetTimer);
        this.resetTimer = setTimeout(() => {
            if (!this.destroyed && this.widgetId !== null) window.turnstile?.reset(this.widgetId);
        }, 0);
    }

    destroy() {
        this.destroyed = true;
        clearTimeout(this.resetTimer);
        this.form?.removeEventListener("reset", this.boundReset);
        this.form?.removeEventListener("htmx:afterRequest", this.boundAfterRequest);
        if (this.widgetId !== null) window.turnstile?.remove(this.widgetId);
        Turnstile.instances.delete(this.element);
        delete this.element.__insightInstance;
        this.element = null;
    }

    static initAll() {
        document.querySelectorAll("[data-insight-turnstile]").forEach(element => new Turnstile(element));
    }
}
