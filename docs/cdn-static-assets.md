# Insight UI CDN Static Assets

Insight UI ships browser assets as package data and can publish them to
`https://cdn.alpininsight.ai/insight-ui/` for production delivery.

## Build Contract

The readable source files stay in:

- `insight_ui/static/insight_ui/js/*.js`
- `insight_ui/static/insight_ui/css/*.css`

Generated distributable files are committed next to them:

- `*.min.js`
- `*.min.css`

Run:

```bash
npm run build:js
```

CI verifies the generated files are current with:

```bash
npm run check:js-build
```

## CDN Upload

The `CDN Deploy` workflow runs on GitHub Release publication and uploads the
generated assets via the shared `.github-private` workflow:

- immutable version path: `https://cdn.alpininsight.ai/insight-ui/vX.Y.Z/`
- mutable latest alias: `https://cdn.alpininsight.ai/insight-ui/latest/`

Production consumers should use the immutable version path. `latest/` is only a
convenience alias for demos and development checks.

Required GitHub secrets:

- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_ENDPOINT`

## Runtime Settings

The Django templates resolve Insight UI-owned CSS/JS assets through the
`insight_asset` template tag. Local development keeps using Django staticfiles.
Production can switch to CDN-backed minified assets with:

```env
IS_PROD=True
INSIGHT_UI_USE_MINIFIED_ASSETS=True
INSIGHT_UI_CDN_ENABLED=True
INSIGHT_UI_CDN_BASE_URL=https://cdn.alpininsight.ai
INSIGHT_UI_CDN_PREFIX=insight-ui
INSIGHT_UI_CDN_VERSION=1.2.3
```

`INSIGHT_UI_CDN_VERSION` may be passed with or without the leading `v`.
