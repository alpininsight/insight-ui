<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Static Assets

This is the public package asset contract. It explains local development and
generic host settings, not an organization's upload service or deployment.
You do not need private CDN access to develop or use local Insight UI assets.

## Source And Output

| Item | Source / output | Ownership |
| --- | --- | --- |
| Design tokens and component styles | [utils/input.css](../insight_ui/utils/input.css) | Edit this source for shared styling changes. |
| Readable stylesheet | [css/tailwind.css](../insight_ui/static/insight_ui/css/tailwind.css) | Compiled package CSS; shipped in wheel and sdist. |
| Browser modules | [js/](../insight_ui/static/insight_ui/js/) | Readable source modules, including relative imports. |
| Fonts | [font/](../insight_ui/static/insight_ui/font/) | Font files and their license. |
| SVGs and app icons | [svg/](../insight_ui/static/insight_ui/svg/) and [favicon/](../insight_ui/static/insight_ui/favicon/) | Generic package media. |
| Minified CSS/JS | Adjacent `*.min.css` / `*.min.js` | Ignored generated CDN artifacts, not shipped package files. |

## Local Staticfiles Is The Default

In the host application's settings, use Django staticfiles and keep package CDN
delivery disabled:

```python
STATIC_URL = "/static/"
INSIGHT_UI = {
    "assets": {"cdn_enabled": False, "use_minified": False},
    "safari_mask_icon": "insight_ui/svg/insight-ui-logo.svg",
}
```

Use the base template or the `insight_asset` tag for package-owned assets:

```django
{% load insight_assets %}
<link rel="stylesheet" href="{% insight_asset 'insight_ui/css/tailwind.css' %}">
<script type="module" src="{% insight_asset 'insight_ui/js/insight-ui-init.js' %}"></script>
```

Do not add this block again when extending the base template, which already
loads the assets. Ordinary project-owned files should use Django's `static`
tag; the Insight UI helper applies package-specific CDN rules.

Local asset resolution uses readable package files, even when `use_minified`
is true. It does not require Node on the deployed host when using a built wheel.
Run the **host project's** `manage.py collectstatic --noinput` for production and
serve `STATIC_ROOT` through that host's chosen static-file service. `collectstatic`
collects existing files; it neither compiles Tailwind nor publishes to a CDN.
The package itself has no `manage.py`, container, or production static server.

### Host App Icons

Provide a host-owned manifest and icons when branding an application. For
example, add these paths to the host's existing `INSIGHT_UI` mapping:

```python
INSIGHT_UI.update({
    "webmanifest": "myapp/favicon/site.webmanifest",
    "apple_touch_icon": "myapp/favicon/apple-touch-icon.png",
})
```

Supply the actual files under the host app's `static/myapp/favicon/` directory.
The Apple touch icon serves iOS/iPadOS home-screen bookmarks; installable PWAs
use the manifest. Follow the packaged manifest's separate regular and maskable
icon entries and use paths relative to that manifest. Keep meaningful artwork
inside the maskable safe area. These assets describe application identity, not
the navbar's BrandMark Config; see [host branding](getting-started.md#brand-defaults-and-explicit-composition).

## Build In An Insight UI Source Checkout

Install the development groups with uv, then Node dependencies using `npm ci`.
The [package scripts](../package.json) define these distinct steps:

| Command | What it does |
| --- | --- |
| `npm run build:tailwind` | Compile package sources and `input.css` into readable `tailwind.css`. |
| `npm run build:static` | Minify existing CSS/JS; rewrite relative module imports for minified output. **Does not compile Tailwind.** |
| `npm run build:static-all` | Run both steps in that order. |
| `npm run verify:static-build` | Check generated-file policy and theme synchronization, then validate minification. Not a CDN upload. |

```bash
uv sync --frozen --all-groups
npm ci
npm run build:static-all
npm run verify:static-build
```

Rebuild after modifying tokens, templates, JS or class-generating Python code.
Commit intended changes to tracked readable output, but do not force-add ignored
minified files. Publication automation can rebuild the artifacts; local tests
must still inspect the CSS that the package will actually ship.

The Tailwind source explicitly scans package templates, configs, JS and tags.
It does not scan this Markdown or the separate documentation application's
templates. Dynamically assembled classes need explicit build coverage.
`use_tailwind_cli=False` selects packaged CSS at runtime; it does not mean the
source build can skip Tailwind compilation.

## Optional Host-Owned CDN

Only enable a CDN when the exact package assets have already been published.
For an **illustrative** published version `1.2.3`:

```python
INSIGHT_UI = {
    "assets": {
        "cdn_enabled": True,
        "use_minified": True,
        "cdn_base_url": "https://cdn.example.com",
        "cdn_prefix": "insight-ui",
        "cdn_version": "1.2.3",
    },
}
```

The resolver produces
`https://cdn.example.com/insight-ui/v1.2.3/css/tailwind.min.css` for the stylesheet.
Bare `X.Y.Z` receives a `v` prefix; an already prefixed version is preserved.
Use the version corresponding to the installed package, not an unrelated newer
asset set. This setting constructs URLs; it does not upload missing files or
prove their availability.

Keep relative JS imports, CSS font URLs and media paths working together. Verify
HTTP status, content types and CORS for cross-origin modules/fonts, including
imports fetched after the entry point. The [package CDN manifest](../insight_ui/cdn_manifest.json)
lists required verification assets, not every file that must be published.
Check browser layout and interactions, not only a HEAD request for one CSS file.

For an immutable production release, verify every required asset and each
enabled conditional asset before switching the runtime:

- Require HTTP 200, the correct content type, and the selected package version.
- Check the stylesheet's `must_contain_selectors` from the manifest as well as
  the JavaScript entry point and its imports. A successfully downloaded but
  incomplete stylesheet can still break the page.
- Serve immutable public release files with the release cache policy, for
  example `Cache-Control: public, max-age=31536000, immutable`. Do not use this
  policy for changing aliases such as `develop` or `latest`.
- Provide CORS for the consuming origin. Public, credential-free package
  modules can use `Access-Control-Allow-Origin: *`; that is not an authorization
  policy for private extension assets.

The version and publish process are host-owned; matching URL strings or a local
build do not prove that a remote publication completed.

Host favicons and logos still need valid Django static paths. The base template
also references external HTMX and optional third-party libraries independently
of package CDN settings. No bucket, credential, tunnel or private publication
procedure is required by this public guide.

[All package guides](README.md) | [Design system](design-system.md)
