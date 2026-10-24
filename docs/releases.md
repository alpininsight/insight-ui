<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Releases And Consumer Upgrades

Insight UI is a production-supported MVP with a defined feature scope. The
`Production/Stable` package classifier describes project maturity, not feature
completeness. Alpha versions from `develop` are prereleases of the next change;
they do not downgrade the maturity of an existing stable release.

## One Python Publisher

Contributor CI automatically builds and tests changes. Python uploads belong
only to the organization's central `insight-ui-publish-python.yml` workflow:

| Package source | Destination | Upload trigger |
| --- | --- | --- |
| Exact reviewed `develop` commit | TestPyPI prerelease | Explicit dispatch and artifact approval. |
| Exact reviewed `main` commit and matching stable release tag | Production PyPI | Explicit dispatch and artifact approval. |

The publisher executes from its protected control repository's `main` branch
for either destination. Its source-channel input selects the package branch;
do not confuse executor branch and source branch. Neither a green CI run nor a
merge uploads a Python package automatically. The retired source-repository
`main-publish-pypi.yml` must not be restored as a second token-based publisher.
GitHub release/tag and CDN publication are separate private maintainer operations,
not Python uploads. Public workflows only validate contributions and produce
short-lived CI artifacts; they must not call private reusable workflows, even
when they run only on `main`, manually, or on a schedule. Contributor tests check
every workflow file, including those without a pull-request trigger.

The former source-repository release, version, CDN, changelog and scheduled
pre-commit callers are retired. Changelog changes and pre-commit hook updates
remain ordinary reviewed contributor PRs; neither needs a publishing credential.
Maintainers perform release and CDN operations from the protected control
repository using the exact source commit that passed Contributor CI. This does
not automatically update consumer dependencies or redeploy the reference website.

## Five Release Gates

1. Make a bounded correction on a worktree branch from current `develop`, add
   regression tests and review the PR. Include already-integrated changes in
   the release review; do not silently call a feature release a patch.
2. Pass Contributor CI, including supported Python/Django series, JavaScript,
   static assets, built metadata and isolated wheel/sdist installation. Verify
   the complete default page using production staticfiles settings.
3. Promote through a `develop` to `main` PR. GitVersion determines the final
   version; check that the stable tag resolves to the exact approved source.
   Do not force a requested patch number over incompatible changes.
4. Build the exact source using the central publisher's non-publishing mode.
   Obtain the normal independent approval for the exact version and both file
   hashes, then explicitly publish via Trusted Publishing. Prior exceptions or
   approvals for different bytes are not reusable release permission.
5. Verify the public index hashes and install the released version in a fresh
   environment. Update consumers through their own dependency/lockfile PRs,
   integration tests and deployment gates. A published package does not update
   any running application automatically.

Published files are immutable. Compatible fixes use a new patch release;
compatible additions use a minor release and incompatible public API changes
need a major release with migration guidance. Do not delete and re-upload a
release to correct its description or classifier.

## Bounded v1.15.2 Maintenance Backport

The failed-state icon in v1.15.1's `minimal_stepper` references the removed
`danger` icon. Develop already corrects it, but also changes the public step
status API and other interfaces. Do not publish that integration backlog as a
patch or copy the reusable template into a consumer.

For this correction only, `hotfix/v1.15.2-minimal-stepper` may target `main`
from the exact v1.15.1 commit `24787fc561d5d60d970c129d6a8eae4f5fd5c1ed`.
The metadata-only branch policy limits the diff to the stepper template, its
render regression, this release guide, the policy workflow and its tests.
Both the template and render regression are mandatory; renamed/deleted files,
other source/API changes, forks and other hotfix branch names are rejected.
The exception expires automatically once Main advances beyond that base.

Review the policy bootstrap separately on Develop, then inspect the bounded
Main backport. It requires an independent repository reviewer's approval of
the exact head; self-approval, bot reviews and stale approvals do not count.
Submitted/dismissed reviews rerun the read-only policy. Do not self-approve,
use an administrator bypass or merge the full Develop backlog to unblock it.
This is preparation until that independent review and all normal Contributor
CI checks pass, not permission to merge or publish automatically.

The maintenance diff must retain the v1.15.1 `items` and status API. Only the
failed icon changes to `x-mark`; the regression renders every supported old
state. Keep the existing Develop implementation and its new API unchanged.
GitVersion still determines the final stable version after reviewed Main
integration; `v1.15.2` is the intended patch, not a forced override.

All remaining release gates above still apply: supported Python/Django,
JavaScript/static and isolated distribution checks; exact Main/tag identity;
central non-publishing build; independent approval of version and both file
hashes; explicit Trusted Publishing; public-index hash/fresh-install checks;
and separate consumer PRs and deployment acceptance. No source-repository
publisher, publication credentials or live application changes are added.

## Reference Application

`insight-ui` owns generic components and package tests. `insight-ui-docs` owns
the reference website, catalog, editorial examples and application-level
browser tests. Review both source contracts when changing a public component,
but do not copy reference-application code into this package.

The reference application's Git pin and `uv.lock` are explicit dependencies.
A package release does not update them. Replacing a Git source with a PyPI
dependency is a separate approved consumer change, followed by Django checks,
strict staticfiles collection, browser tests and the container/GitOps rollout.
Keep unrelated Docs changes in their own PRs.

[Testing](testing.md) | [Guide index](README.md)
