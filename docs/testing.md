<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Testing The Package

Run these commands from an Insight UI source checkout. Use
[CONTRIBUTING.md](../CONTRIBUTING.md) for setup and generation. No private
documentation application, credentials or running deployment is needed.

## Focused Checks

| Change | Check |
| --- | --- |
| Config/tag/template | Python tests under [tests/insight_ui/](../tests/insight_ui/); render real tags. |
| Browser behavior | [Vitest/jsdom](../tests/js/); events, focus, state, repeated initialization and cleanup. |
| Generated component | Its generated Python test; optional JS stub must be expanded. |
| Tokens/assets | Tailwind build, semantic-token check, readable and minified asset checks. |
| Public guides | Link, token, example-rendering and package-boundary regression tests. |
| Packaging | Build wheel/sdist and run the archive boundary checker. |

```bash
uv run pytest tests/insight_ui/unit/components/test_button.py
npm test -- tests/js/tabs.test.js
uv run pytest tests/insight_ui/unit/test_contributor_docs.py
```

The [existing button tests](../tests/insight_ui/unit/components/test_button.py)
and [tabs tests](../tests/js/tabs.test.js) are working examples. Test the public
contract rather than copying assertions from a different component blindly.

## Before Opening A PR

```bash
uv sync --frozen --all-groups
npm ci
uv run ruff check --no-fix
uv run ruff format --check
uv run python -m django check --settings=tests.settings
uv run pytest
npm test
npm run build:static-all
npm run verify:static-build
uv build
uv run python scripts/check_distribution.py
uv run --no-project python scripts/smoke_distribution.py
git diff --check
```

The minimal host is [tests/settings.py](../tests/settings.py), not a removed
Docs `core.settings`. Package Python tests and all Vitest behavior tests stay
here. Do not replace a failing required check with a skipped test or an ignored
shell exit code. Report commands, versions and known limits in the PR.

Use `uv run pytest --cov=insight_ui --cov-report=term-missing` and
`npm run test:coverage` to inspect coverage; a percentage is not proof that the
important behavior is tested. Do not introduce an arbitrary coverage promise.

## Contributor CI

Pull requests run the same public package checks on disposable GitHub-hosted
runners. Fork contributors need no organization token, SSH key, private
documentation checkout, CDN account or running cluster.

| Check | Evidence |
| --- | --- |
| Python 3.12, 3.13 and 3.14 | Locked dependencies, exported requirements, lint, formatting, Django system checks and package tests against Django 5.2 and 6.1. |
| JavaScript and static assets | Vitest/jsdom behavior tests and the package's existing static-build verification. No CDN upload. |
| Contributor hygiene | The repository's public pre-commit hooks, with secret scanning performed once separately. |
| Wheel and sdist | Both archives are inspected, installed separately outside the checkout, then checked for Django rendering and staticfiles. |
| PR metadata | Conventional Commit title and branch routing, using read-only GitHub access and no source checkout. |

The required quality gate fails if any package check fails or is skipped. It
retains the existing protected status names. PR title validation reads the
current title from GitHub, including when an older run is retried.

The [local PR policy](../.github/workflows/pr-branch-guard.yml) already owns
title validation. Do not add the private organization PR-title caller alongside
it: that would duplicate the check and require private workflow access and write
permissions from contributors. A failure of
`test_pull_request_workflows_have_no_private_access` in every Python matrix leg
is a workflow-boundary failure, not evidence of a Python/Django runtime defect.
Keep that guard enabled and fix the caller, not the supported Python versions.

The tested wheel and sdist are downloadable from the run as
`package-dist-<commit SHA>` for seven days. These are CI artifacts, not a PyPI
release or an internal storage boundary: artifacts follow the repository's
visibility. A private reference application must keep its own integration-test
results in its private repository; these package artifacts contain no such
evidence.

The [contributor workflow](../.github/workflows/feature-ci.yml) is deliberately
self-contained so it also works in public forks. Organization-specific release,
CDN publication and application evidence are separate from contributor tests.
The existing maintainer-only publication workflows are not converted by this
change; moving their execution to a private repository is a remaining
maintainer gate before changing repository visibility. Passing Contributor CI
does not authorize that visibility change or a package publication.

## Behavior And Visual Checks

- Test defaults, supported overrides and nested Configs through the actual tag.
- Test missing optional values, long text, escaping and repeated component IDs.
- Cover keyboard/focus/ARIA states as well as pointer interaction.
- Exercise both light and dark, RTL where relevant, and narrow layouts in the
  local component preview after rebuilding assets.
- Compare component-specific runtime behavior before and after your change.
  Vitest/jsdom does not implement browser layout or replace rendered checks.

The separate reference application owns its Playwright/axe and application-level
audit evidence. Package tests protect reusable behavior; neither they nor a
successful screenshot establish WCAG conformance. See [accessibility](accessibility.md).
Commit screenshots only when a guide references them or an actual visual
regression test uses them as a baseline. Keep debugging captures outside Git.

## Documentation And Distribution Boundaries

Public Markdown under `docs/` is allowed in the Git repository. The current wheel
and sdist omit it; the [archive checker](../scripts/check_distribution.py) still
rejects Docs application, enterprise and host-project payloads. It also keeps
`devtools` out of the runtime wheel. Do not weaken those gates to restore the
old self-documentation application.

Guide changes should keep relative links, example Configs and token names valid.
Update implementation-linked examples when an API changes rather than preserving
an obsolete command because it once passed CI.

[All package guides](README.md)
