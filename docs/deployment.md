# Deployment Contract

This repository is prepared for deployment behind the `management-cloud`
platform contract and the repo-side runtime contract.

Canonical references:

- Platform side:
  - `insight-lima-k8s-capi/docs/PLATFORM.md`
  - `insight-lima-k8s-capi/docs/runbooks/management-cloud-application-namespace-contract.md`
- Repo side:
  - `.github-private/docs/repo-runtime-contract.md`

## Runtime contract

The container now exposes the canonical HTTP runtime endpoints required by the
repo contract:

- `GET /healthz`
- `GET /readyz`
- `GET /api/info`

`/api/info` returns stable runtime identity fields for service name, service
namespace, artifact version, runtime instance, deployment environment, lane,
blue/green slot, platform namespace, and git revision.

## Demo target

For the first public demo rollout, the intended platform-side target is:

- host: `insight-ui.demo.alpininsight.ai`
- namespace class: `demo`
- service name: `insight-ui`

## Blue/Green model

The repo is prepared for slot-neutral images and platform-side promotion.

Rules:

- `develop` and `main` do not need separate image builds.
- The same tested digest is promoted from the candidate slot to the live slot.
- The platform decides which color is currently live and which color receives
  the next candidate rollout.
- `/api/info` exposes both the logical lane (`develop` or `main`) and the
  physical slot (`blue` or `green`) so the running pod can be identified
  during cutover and rollback.

Example candidate slot for `insight-ui.demo.alpininsight.ai`:

```env
SERVICE_NAMESPACE=alpininsight
SERVICE_NAME=insight-ui
PLATFORM_NAMESPACE=demo
DEPLOYMENT_ENVIRONMENT=develop
DEPLOYMENT_LANE=develop
DEPLOYMENT_SLOT=green
PUBLIC_BASE_URL=https://insight-ui.demo.alpininsight.ai
ALLOWED_HOSTS=insight-ui.demo.alpininsight.ai
CSRF_TRUSTED_ORIGINS=https://insight-ui.demo.alpininsight.ai
USE_X_FORWARDED_HOST=true
TRUST_X_FORWARDED_PROTO=true
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=true
SECURE_HSTS_PRELOAD=true
RUN_MIGRATIONS=0
```

Example promoted live slot using the exact same image digest:

```env
SERVICE_NAMESPACE=alpininsight
SERVICE_NAME=insight-ui
PLATFORM_NAMESPACE=demo
DEPLOYMENT_ENVIRONMENT=production
DEPLOYMENT_LANE=main
DEPLOYMENT_SLOT=blue
PUBLIC_BASE_URL=https://insight-ui.demo.alpininsight.ai
ALLOWED_HOSTS=insight-ui.demo.alpininsight.ai
CSRF_TRUSTED_ORIGINS=https://insight-ui.demo.alpininsight.ai
USE_X_FORWARDED_HOST=true
TRUST_X_FORWARDED_PROTO=true
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=true
SECURE_HSTS_PRELOAD=true
RUN_MIGRATIONS=0
```

Notes:

- `RUN_MIGRATIONS=0` is the default for scaled web pods after a dedicated
  migration job or init step has completed.
- The container image is reused across `develop` and `main`; the platform
  decides which slot/lane receives which digest and runtime env values.
- Promotion means switching the tested digest from the candidate lane/slot to
  the live lane/slot. It does not require a new `main` container build.
- Rollback means switching traffic back to the previous slot while keeping the
  new image available for analysis.
- Build metadata is baked into the image through `ARTIFACT_VERSION` and
  `GIT_COMMIT_SHA`, and also surfaced in `/api/info`.

## CI expectation

`.github/workflows/container-build.yml` validates:

- container build
- management commands for migrations and collectstatic
- production-style Django deploy checks
- runtime smoke checks against `/healthz`, `/readyz`, and `/api/info`

That keeps the repo-side runtime contract explicit before the K8s repo wires
the actual ArgoCD, ingress, secret, and namespace manifests.
