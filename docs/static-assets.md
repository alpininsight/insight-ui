# Static Assets

Insight UI ships CSS, JavaScript, fonts, SVGs, favicons, and other browser
assets as package data. Host applications can serve these assets with Django
staticfiles or from their own CDN.

This page describes the public package contract only. Organization-specific
deployment, CDN upload, object storage, cache purge, and platform routing
procedures belong in the operating organization's private platform
documentation.

## Packaged Assets

Readable source assets live under:

| Asset type | Package location |
|------------|------------------|
| CSS | `insight_ui/static/insight_ui/css/` |
| JavaScript | `insight_ui/static/insight_ui/js/` |
| Fonts | `insight_ui/static/insight_ui/font/` |
| Favicons | `insight_ui/static/insight_ui/favicon/` |
| SVGs | `insight_ui/static/insight_ui/svg/` |
| Tailwind source | `insight_ui/utils/input.css` |

Generated distributable files are deliberately not committed or packaged:

- `*.min.css`
- `*.min.js`

The centralized static-assets workflow regenerates these files from the
readable sources for CDN publication. Django staticfiles always use the
readable package assets, so package consumers do not need a JavaScript build
step or generated minified files.

## Local Staticfiles

For most Django projects, use Django staticfiles:

```python
STATIC_URL = "/static/"
```

For production, collect static files as part of your own deployment process:

```bash
uv run python manage.py collectstatic --noinput
```

If you use the Insight UI base template, assets are resolved through Insight
UI's asset helper and can use local staticfiles or a configured CDN.

## Web App Icons

The base template resolves the manifest path from `settings.INSIGHT_UI`, which
lets each Django consumer provide its own app identity:

```python
INSIGHT_UI = {
    "webmanifest": "my_app/favicon/site.webmanifest",
    "apple_touch_icon": "my_app/favicon/apple-touch-icon.png",
}
```

The Apple touch icon covers iOS and iPadOS home-screen bookmarks. Android and
installable PWAs use the icons declared in the webmanifest. Include dedicated
192x192 and 512x512 PNGs with `purpose: "maskable"`; keep important artwork in
the central safe zone and use an opaque background. Manifest icon URLs should
be relative to the manifest file so they remain valid below a static URL prefix.

## Build Commands For Contributors

When `insight_ui/utils/input.css` changes, rebuild the packaged stylesheet:

```bash
npm run build:tailwind
```

To validate the minified CDN build locally, generate the ignored artifacts:

```bash
npm run build:static
```

For convenience, both steps can be run together:

```bash
npm run build:static-all
```

Before opening a pull request, validate the tracked Tailwind output and the
CDN asset build:

```bash
npm run verify:static-build
```

This command leaves generated `*.min.css` and `*.min.js` files ignored. Do not
add them to a commit.

## CDN Configuration

Host applications may opt into CDN-backed asset URLs through
`settings.INSIGHT_UI`:

```python
INSIGHT_UI = {
    "assets": {
        "use_minified": True,
        "cdn_enabled": True,
        "cdn_base_url": "https://cdn.example.com",
        "cdn_prefix": "insight-ui",
        "cdn_version": "1.2.3",
    }
}
```

The resulting asset URL is assembled from:

```text
<cdn_base_url>/<cdn_prefix>/<cdn_version>/<asset-path>
```

For example:

```text
https://cdn.example.com/insight-ui/1.2.3/css/tailwind.min.css
```

Use immutable version paths for production where possible. Mutable aliases such
as `latest` are convenient for development checks, but they can make browser
and CDN cache behavior harder to reason about.

## Public Boundary

This repository intentionally does not document any organization's private CDN
bucket layout, upload credentials, cache-purge process, deployment automation,
or runtime deployment path. Keep those details in the private repository or
platform runbook that owns the deployment.
