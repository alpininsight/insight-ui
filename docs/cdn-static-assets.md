# Insight UI CDN Static Assets

Insight UI ships browser assets as package data and can publish them to
`https://cdn.alpininsight.ai/insight-ui/` for production delivery.

## Build Contract

The readable source files stay in:

- `insight_ui/static/insight_ui/js/*.js`
- `insight_ui/static/insight_ui/css/*.css`
- `insight_ui/static/insight_ui/font/*`
- `insight_ui/static/insight_ui/favicon/*`
- `insight_ui/static/insight_ui/svg/*`
- `insight_ui/utils/input.css`

Generated distributable files are committed next to them:

- `*.min.js`
- `*.min.css`

`insight_ui/utils/input.css` is the Tailwind source of truth. When it changes,
regenerate the packaged stylesheet first:

```bash
npm run build:tailwind
```

Then regenerate minified distributable assets:

```bash
npm run build:static
```

For local convenience, run both steps with:

```bash
npm run build:static-all
```

`build:static` intentionally only minifies existing assets. It does not compile
Tailwind from `input.css`, because the shared `.github-private` CDN workflow is
Node-only and must be able to rebuild/upload distributable files without
requiring Python, Django, or the Tailwind CLI at CDN publication time.

CI verifies the generated files are current with:

```bash
npm run check:static-build
```

The check first compares generated Insight UI theme tokens in `tailwind.css`
against `input.css`, then verifies the committed `.min.js` and `.min.css` files.
This catches stale `tailwind.css` before assets are uploaded to the CDN.

## CDN Upload

The `Static Assets` workflow runs on protected branch pushes and uploads the
generated assets via the shared `.github-private` workflow into branch-specific
mutable aliases:

- development alias: `https://cdn.alpininsight.ai/insight-ui/develop/`
- production alias: `https://cdn.alpininsight.ai/insight-ui/main/`

These branch aliases are intentionally separate. `develop` must not update the
production-facing `main/` alias and must not update `latest/`.

The upload includes all runtime browser assets that packaged CSS or templates
can reference directly: JavaScript, CSS, SVGs, favicons, web manifests, fonts,
and common image formats. This is required because CSS font URLs are resolved
relative to the CDN stylesheet path.

The `CDN Deploy` workflow runs on GitHub Release publication and uploads the
generated assets via the same shared `.github-private` workflow:

- immutable version path: `https://cdn.alpininsight.ai/insight-ui/vX.Y.Z/`
- mutable latest alias: `https://cdn.alpininsight.ai/insight-ui/latest/`

Production consumers should use the immutable version path. `latest/` is only a
convenience alias for demos and development checks.

The repository release is created by the `Release (Alpine Insight)` workflow.
Because GitHub does not reliably start a second workflow from a release event
created by another workflow token, `CDN Deploy` also listens for a successful
release workflow completion. It then resolves the matching release tag from the
completed commit SHA and calls the shared `.github-private` static asset
publisher with that explicit version.

Runtime deployments must not rely on `latest/` for application rendering. New
paths can be negatively cached at the Cloudflare edge before the first upload,
so a deployment that points at `latest/` can keep seeing a stale `404` until the
edge TTL expires. Use a versioned `INSIGHT_UI_CDN_VERSION` value for runtime
deployments and reserve `latest/` for manual smoke checks.

Required GitHub secrets:

- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_ENDPOINT`

## Runtime Settings

The Django templates resolve Insight UI-owned CSS/JS assets through the
`insight_asset` template tag. Local development keeps using Django staticfiles.
Production uses minified local staticfiles by default. It can switch to
CDN-backed minified assets only when the matching versioned CDN path has already
been published and verified:

```env
IS_PROD=True
INSIGHT_UI_USE_MINIFIED_ASSETS=True
INSIGHT_UI_CDN_ENABLED=True
INSIGHT_UI_CDN_BASE_URL=https://cdn.alpininsight.ai
INSIGHT_UI_CDN_PREFIX=insight-ui
INSIGHT_UI_CDN_VERSION=1.2.3
```

`INSIGHT_UI_CDN_VERSION` may be passed with or without the leading `v` for
SemVer versions. Branch aliases such as `develop`, `main`, and `latest` are
used as-is.
