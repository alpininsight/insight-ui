# Deployment Contract

This repository is prepared for deployment behind the `management-cloud`
platform contract and the repo-side runtime contract.

Canonical references:

- Platform side:
  - `insight-lima-k8s-capi/docs/PLATFORM.md`
  - `insight-lima-k8s-capi/docs/runbooks/management-cloud-application-namespace-contract.md`
- Repo side:
  - `.github-private/docs/repo-runtime-contract.md`
  - `docs/blue-green-ci-cd-handover.md`

## Runtime contract

The container now exposes the canonical HTTP runtime endpoints required by the
repo contract:

- `GET /healthz`
- `GET /readyz`
- `GET /api/info`

`/api/info` returns stable runtime identity fields for service name, service
namespace, artifact version, runtime instance, deployment environment, lane,
blue/green slot, platform namespace, and git revision.

## Production and demo targets

The production canonical host for the public Insight UI package website is:

- host: `insight-ui.com`
- namespace class: `demo`
- service name: `insight-ui`

The previous production demo host remains a transition alias while DNS,
Cloudflare Tunnel, Istio, oauth2-proxy, and monitoring are cut over:

- transition alias: `insight-ui.demo.alpininsight.ai`

The develop lane remains separate and is not changed by production promotion:

- develop host: `insight-ui.dev.alpininsight.ai`

## Blue/Green model

The repo is prepared for slot-neutral images and platform-side promotion.

Rules:

- `develop` is the deploy-relevant container build lane.
- `main` must not introduce a new deploy-relevant image digest.
- The same tested digest is promoted from the candidate slot to the live slot.
- The platform decides which color is currently live and which color receives
  the next candidate rollout.
- `/api/info` exposes both the logical lane (`develop` or `main`) and the
  physical slot (`blue` or `green`) so the running pod can be identified
  during cutover and rollback.

Example candidate/develop slot:

```env
SERVICE_NAMESPACE=alpininsight
SERVICE_NAME=insight-ui
PLATFORM_NAMESPACE=demo
DEPLOYMENT_ENVIRONMENT=develop
DEPLOYMENT_LANE=develop
DEPLOYMENT_SLOT=green
PUBLIC_BASE_URL=https://insight-ui.dev.alpininsight.ai
ALLOWED_HOSTS=insight-ui.dev.alpininsight.ai
CSRF_TRUSTED_ORIGINS=https://insight-ui.dev.alpininsight.ai
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
PUBLIC_BASE_URL=https://insight-ui.com
ALLOWED_HOSTS=insight-ui.com,insight-ui.demo.alpininsight.ai,.demo.alpininsight.ai
CSRF_TRUSTED_ORIGINS=https://insight-ui.com,https://insight-ui.demo.alpininsight.ai
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
- The deploy-relevant container image is built once on `develop`, published
  with moving aliases such as `develop`, `candidate`, and `edge`, and also
  with a stable tree-content alias `tree-<git-tree-sha>`.
- `main` performs a protocol validation build in GitHub Actions, but stable
  aliases such as `main` and `latest` are promoted from the already tested
  `tree-<git-tree-sha>` image instead of pushing a newly rebuilt digest.
- The platform decides which slot/lane receives which digest and runtime env
  values.
- Production canonical cutover to `insight-ui.com` also requires platform-side
  Cloudflare DNS/Tunnel routing, Istio host routing, and oauth2-proxy redirect
  allowlist changes; the app repository only declares the expected runtime
  contract.
- Promotion means switching the tested digest from the candidate lane/slot to
  the live lane/slot. It does not require a new `main` container build.
- Rollback means switching traffic back to the previous slot while keeping the
  new image available for analysis.
- `SECRET_KEY` must be provided explicitly for production-style deployments;
  the repo no longer carries a production fallback.
- Build metadata is baked into the image through `ARTIFACT_VERSION` and
  `GIT_COMMIT_SHA`, and also surfaced in `/api/info`.

## CI expectation

`.github/workflows/container-build.yml` now acts as a thin caller into the
central reusable workflow in `.github-private@main` and validates:

- container build
- management commands for migrations and collectstatic
- production-style Django deploy checks
- runtime smoke checks against `/healthz`, `/readyz`, and `/api/info`
- candidate runtime identity with `develop/green`
- promoted runtime identity with `main/blue`

On branch pushes, the workflow then behaves as follows:

- `develop`: publish the candidate digest to GHCR
- `main`: promote the previously published `tree-<git-tree-sha>` digest to the
  stable aliases without creating a new deploy-relevant image
- generated GitOps PRs pin the image digest and matching CDN runtime version
  together: `develop` for the green slot and the GitVersion release version for
  the blue slot

That keeps the repo-side runtime contract explicit before the K8s repo wires
the actual ArgoCD, ingress, secret, and namespace manifests.
