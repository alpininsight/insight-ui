# CDN Asset Verification Contract

This document defines the public package contract for verifying Insight UI
assets before a deployer enables CDN delivery:

- the template-required asset paths,
- immutable versioning, and
- the checks that prevent runtime and CDN asset versions from drifting.

It complements, and does not replace, [`static-assets.md`](static-assets.md),
which defines the public package contract. As stated there, this repository
does **not** document any organization's private CDN bucket layout, upload
credentials, or cache-purge automation.

## Required CDN URLs

**Publish vs. verify — one source of truth each, no overlap.** What actually
gets uploaded is decided by the deployer's release automation. That remains the
single source of truth for *publishing*, and this document does not duplicate or
override it. The manifest below is the complementary *verification* subset: the
specific template-required URLs that must be checked before runtime CDN delivery
is enabled (#314). It is a strict subset of what the release publishes, never a
competing publish list.

The canonical, machine-readable list of the required-for-verification subset
lives in [`insight_ui/cdn_manifest.json`](../insight_ui/cdn_manifest.json). Each
full URL is assembled as:

```text
<cdn_base_url>/<cdn_prefix>/<version>/<path>
# e.g. https://cdn.example.com/insight-ui/v1.12.0/css/tailwind.min.css
```

`version` is an immutable release tag (`vX.Y.Z`) for production. Mutable
aliases (`develop`, `main`, `latest`) are for development checks only and must
**not** back production runtime delivery.

### Required for every version (break the page if missing or skewed)

| Path | Loaded by |
|------|-----------|
| `css/tailwind.min.css` | base template stylesheet |
| `js/insight-ui-init.min.js` | base template |
| `js/insight-ui-utils.min.js` | base template |
| `js/insight-ui-state.min.js` | base template |
| `js/insight-ui-websocket.min.js` | base template |
| `js/insight-ui-debug.min.js` | base template |
| `js/insight-ui-toc-generator.min.js` | base template |

### Conditional (only when the feature is enabled)

| Path | Enabled by |
|------|------------|
| `css/prism.min.css` | `INSIGHT_UI.load_prism = True` |
| `js/insight-ui-demo-sandbox.min.js` | component demo / sandbox pages |

## Verification Gate (issue #314)

Before an application runtime enables CDN delivery for a version, every
`required` URL for that exact version must:

- return HTTP 200,
- send an immutable `Cache-Control` (`public, max-age=31536000, immutable`),
- send `Access-Control-Allow-Origin: *`, and
- for `css/tailwind.min.css`, contain the responsive selectors listed under
  `must_contain_selectors` in the manifest (guards against the template/asset
  version skew that motivated #314).

The runtime version and the CDN `version` it references must match. Production
runtime delivery must not point at a mutable alias.

## Public Boundary

This manifest is intentionally limited to package-owned asset paths and their
verification requirements. It does not choose a CDN provider, configure a
hosted endpoint, publish assets, or describe authentication for separately
licensed extension packages. Those operational and commercial decisions belong
to the deployment owner's private platform contract.
