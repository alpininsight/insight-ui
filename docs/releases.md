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
The existing GitHub release/tag and CDN workflows are not Python uploads and
remain separate.

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
