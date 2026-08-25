# Contributing to Insight UI

Insight UI is a component framework for Django, built and maintained by
Alpin Insight Solutions. Contributions are welcome — code, documentation,
translations, bug reports and review are all useful, and not all of them require
writing Python.

This page covers what applies to every contribution. The developer guide with
setup, workflow, component rules and the test checklist is
**[docs/contributing.md](docs/contributing.md)**, and the code-level rules are in
[docs/conventions.md](docs/conventions.md). This page supersedes the
organisation-wide contributing guide for this repository.

## Ways to contribute

| | |
|---|---|
| **Report a bug** | Open an issue. A good report beats a vague patch — see [Reporting bugs](#reporting-bugs). |
| **Fix a bug** | Issues labelled `good first issue` are scoped small on purpose. |
| **Build a component** | The largest surface. See [Adding Components](docs/contributing.md#adding-components). |
| **Improve the docs** | Including the component reference pages, which are generated from docstrings. |
| **Translate** | Insight UI ships German and English; further locales are welcome. |
| **Review** | Reading someone else's pull request is a contribution, whether or not you can merge it. |

## Code of conduct

This project follows the
[Alpin Insight Solutions Code of Conduct](https://github.com/alpininsight/.github/blob/main/CODE_OF_CONDUCT.md).
Concerns go to security@alpininsight.com — that address is monitored, a personal
message to a maintainer is not.

## Licensing and the CLA

Insight UI is dual-licensed: AGPL-3.0 for everyone, and a commercial Enterprise
licence for organisations that cannot meet the AGPL's network-copyleft
obligation. [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) explains what that
means.

Because of that dual licence, **every contributor signs the
[Contributor Licence Agreement](CLA.md) once**, before their first pull request
can be merged.

> **Right now the agreement is still with our lawyers, and the signing bot is
> switched off.** Please open your pull request anyway — we will review it and
> work on it with you exactly as we normally would. Only the merge waits. When
> the CLA is in force, the bot will ask you to sign in your pull request and we
> take it from there. There is nothing for you to do in the meantime.

You keep the copyright in your work. What you grant us is the additional right
to license it commercially — and in exchange we are bound to keep licensing it
under the open source licence too. We cannot take your contribution
closed-source-only.

### Signing the CLA

A bot comments on your first pull request with a link to the agreement. Reply in
that thread with:

```text
I have read the CLA Document and I hereby sign the CLA
```

Your signature is recorded once and applies to every later pull request. If you
contribute on behalf of an employer, ask them to sign Part B of the agreement
instead and write to contact@alpininsight.com.

### Contributions you do not fully own

If part of what you are submitting was written by someone else — vendored code,
a snippet from a blog post, output you are not sure about — say so in the pull
request before it is reviewed. Name the source and its licence. This is much
cheaper to sort out before a merge than after one.

## Reporting bugs

A report that lets a maintainer reproduce the problem in one attempt is worth
several that do not. Include:

- Insight UI, Django and Python versions
- the component involved, and the template tag call that triggers it
- browser and viewport, for anything visual
- what you expected, and what happened instead

Screenshots help for layout problems. For a theme or contrast issue, say which
theme you were in — the same component can be correct in one and wrong in the
other.

## Security

Never open a public issue for a vulnerability. Report privately to
security@alpininsight.com, as described in the
[security policy](https://github.com/alpininsight/.github/blob/main/SECURITY.md).

## Contact

- Licensing, Enterprise, CLA questions: contact@alpininsight.com
- Security and Code of Conduct: security@alpininsight.com
- Everything else: open an [issue](https://github.com/alpininsight/insight-ui/issues)
  or a [discussion](https://github.com/alpininsight/insight-ui/discussions)
