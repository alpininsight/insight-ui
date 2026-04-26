# Blue/Green CI/CD Handover

This document is the concrete handover note for `alpininsight/insight-ui`.
It describes which workflow builds the candidate container, which step promotes
the already tested digest, and which runtime endpoints must be checked during
rollout.

## Scope

- Repository: `alpininsight/insight-ui`
- Service name: `insight-ui`
- Target host: `https://insight-ui.demo.alpininsight.ai`
- Target namespace class: `demo`
- Promotion model: build once on `develop`, promote the same digest on `main`

## Authoritative references

- Runtime/deployment contract: [deployment.md](./deployment.md)
- Runtime endpoints and identity payload:
  - [core/runtime_views.py](../core/runtime_views.py)
  - [core/runtime_contract.py](../core/runtime_contract.py)
- Workflow implementation: [container-build.yml](../.github/workflows/container-build.yml)

## GitHub URLs

- Service repository: <https://github.com/alpininsight/insight-ui>
- Current implementation PR: <https://github.com/alpininsight/insight-ui/pull/189>
- Workflow page: <https://github.com/alpininsight/insight-ui/actions/workflows/container-build.yml>
- Workflow file on GitHub:
  <https://github.com/alpininsight/insight-ui/blob/feat/bluegreen-cicd/.github/workflows/container-build.yml>

## Build and promotion behavior

### Pull requests

PRs validate the container contract only:

- container build
- `migrate` smoke run
- `collectstatic` smoke run
- Django `check --deploy`
- runtime endpoint checks for:
  - candidate profile: `develop` + `green`
  - promoted profile: `main` + `blue`

No deploy-relevant image is pushed on PRs.

### Push to `develop`

`develop` is the deploy-relevant candidate lane.

The workflow:

- builds the image
- validates runtime and management commands
- publishes the candidate digest to GHCR

Candidate aliases:

- branch alias: `develop`
- moving aliases: `candidate`, `edge`
- commit alias from `docker/metadata-action`
- tree-content alias: `tree-<git-tree-sha>`

The `tree-<git-tree-sha>` alias is the stable promotion source.

### Push to `main`

`main` still runs the validation build for protocol and developer comparison,
but it must not replace the deploy-relevant artifact.

The workflow:

- validates the repository state locally
- resolves the already published `tree-<git-tree-sha>` image
- promotes that existing digest to the stable aliases:
  - `main`
  - `latest`

No new deploy-relevant digest is published on `main`.

## Runtime contract

The container exposes:

- `GET /healthz`
- `GET /readyz`
- `GET /api/info`

Expected `api/info` rollout signals:

- candidate slot:
  - `deployment.environment.name=develop`
  - `deployment.lane=develop`
  - `deployment.slot=green`
- promoted slot:
  - `deployment.environment.name=production`
  - `deployment.lane=main`
  - `deployment.slot=blue`

## GHCR usage

Recommended deployment source:

- deploy the candidate slot from `tree-<git-tree-sha>` or the immutable digest
- do not deploy `latest` into the candidate slot
- after `main` promotion, `main` and `latest` should reference the same digest

## End-to-end test sequence

1. Merge the central reusable workflow change in `alpininsight/.github-private`.
2. Merge this `insight-ui` CI/CD change.
3. Push or merge to `develop` in `insight-ui`.
4. Confirm on the workflow page that the `develop` run published the candidate image.
5. Deploy the `tree-<git-tree-sha>` alias or digest into the candidate slot in the K8s repo.
6. Verify `/healthz`, `/readyz`, and `/api/info` on the candidate rollout.
7. Merge `develop` into `main`.
8. Confirm on the workflow page that `main` promoted the existing `tree-<git-tree-sha>` digest to `main` and `latest`.
9. Switch traffic on the platform side with ArgoCD/Istio.
10. Verify `/api/info` on the live slot after cutover.

## Platform-side responsibilities

This repo does not switch traffic itself.

The platform side must:

- choose the live slot and candidate slot
- deploy the chosen digest to the correct slot
- set `DEPLOYMENT_ENVIRONMENT`, `DEPLOYMENT_LANE`, and `DEPLOYMENT_SLOT`
- route traffic during promotion and rollback

Those steps belong to `insight-lima-k8s-capi`, not to this repository.
