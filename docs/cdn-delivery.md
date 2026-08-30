# CDN Delivery & Entitlement Contract

This document describes two related concerns for serving Insight UI assets from
a CDN:

1. **Public asset versioning and pre-flight verification** (issue #314) — which
   immutable CDN URLs must exist and be checked before runtime CDN delivery is
   enabled.
2. **Target state: license-bound, tenant-scoped access** (issue #259) — how
   access to licensed `insight-ui-*` assets is modeled against the tenant /
   OIDC tree.

It complements, and does not replace, [`static-assets.md`](static-assets.md),
which defines the public package contract. As stated there, this repository
does **not** document any organization's private CDN bucket layout, upload
credentials, or cache-purge automation.

## Required CDN URLs

The canonical, machine-readable list lives in
[`insight_ui/cdn_manifest.json`](../insight_ui/cdn_manifest.json). Each full URL
is assembled as:

```text
<cdn_base_url>/<cdn_prefix>/<version>/<path>
# e.g. https://cdn.alpininsight.ai/insight-ui/v1.12.0/css/tailwind.min.css
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

Before Kubernetes (or any runtime) enables CDN delivery for a version, every
`required` URL for that exact version must:

- return HTTP 200,
- send an immutable `Cache-Control` (`public, max-age=31536000, immutable`),
- send `Access-Control-Allow-Origin: *`, and
- for `css/tailwind.min.css`, contain the responsive selectors listed under
  `must_contain_selectors` in the manifest (guards against the template/asset
  version skew that motivated #314).

The runtime image version and the CDN `version` it references must match. K8s
must not point runtime delivery at a mutable alias.

## Target State: License-Bound, Tenant-Scoped Access (issue #259)

> Status: **design proposal for #259.** The public `insight_ui` base package
> stays open and unauthenticated. The model below governs the licensed
> `insight-ui-*` extension packages only. Items marked _(open)_ need a decision.

### Principle

Licenses are **bound to tenants**, not to individual users. Assignment mirrors
the **OIDC tree**: a license is granted to a tenant node — the company (tree
root) **or any node below it** (org unit / group / project) — depending on the
scope that was sold. Access to a licensed asset is therefore an **entitlement
lookup against the tenant node in that tree**, resolved at request time.

### Model

```text
Tenant (tree node; mirrors OIDC org/group hierarchy)
  └── may hold 0..n License grants
License
  ├── package        e.g. "insight-ui-charts"
  ├── version_range  e.g. ">=2.0,<3.0"
  ├── granted_to     Tenant node id (root company OR a descendant node)
  └── scope          "node_only" | "node_and_descendants"
Asset (CDN object)
  └── belongs to a package + immutable version
```

- A grant at an **ancestor** node with scope `node_and_descendants` covers all
  child tenants (company-wide license). A grant at a **descendant** node with
  scope `node_only` limits the license to that subtree/node (e.g. a single
  department bought the add-on).
- Entitlement check for a request: authenticate via OIDC → map the subject to
  its tenant node → walk **up** the tree from that node → the request is
  entitled if any visited node holds a `License` whose `package`/`version_range`
  matches and whose `scope` reaches the requesting node.

### Enforcement options at the CDN edge _(open — pick one)_

- **Cloudflare Access** in front of licensed paths, with the tenant/entitlement
  claim carried in the OIDC identity.
- **Signed URLs / tokens** minted by the app after it resolves entitlement.
- **Worker proxy** that validates the OIDC token and the tenant→license lookup
  before serving from R2.

### Open questions carried from #259

- Which OIDC claim identifies the tenant node, and is inheritance strictly
  down-only?
- Signed URLs vs. Access vs. Worker proxy as the single central mechanism.
- How immutable versions, cache-purge, and rollback are governed for licensed
  assets.
- How apps reference the add-on packages (PyPI, staticfiles, CDN-only, hybrid),
  and which build/release artifacts each `insight-ui-*` repo must produce.
- CI guard that no private/licensed asset is ever published unprotected.
