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

Generated distributable files are committed next to their readable sources:

- `*.min.css`
- `*.min.js`

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

## Build Commands For Contributors

When `insight_ui/utils/input.css` changes, rebuild the packaged stylesheet:

```bash
npm run build:tailwind
```

Then regenerate minified distributable assets:

```bash
npm run build:static
```

For convenience, both steps can be run together:

```bash
npm run build:static-all
```

Before opening a pull request, verify that generated files are current:

```bash
npm run check:static-build
```

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
