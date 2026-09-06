# Contributing

Welcome! We appreciate every helpful contribution to Insight UI.

> Before your first pull request can be merged you need to sign the
> [Contributor Licence Agreement](../CLA.md) once — Insight UI is
> dual-licensed and that is what makes the commercial edition possible.
> See [CONTRIBUTING.md](../CONTRIBUTING.md#licensing-and-the-cla).

## Prerequisites

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) for dependency management

Local setup:

```bash
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py runserver
```

## Workflow

1. Create a feature branch with a suitable name:
   - `feat/accordion` for new features
   - `fix/accordion` for bug fixes
   - `docs/readme` for documentation
   - `refactor/sidebar` for refactoring

2. Develop your changes

3. Update documentation and demos if necessary

4. Wait for CI to pass (linting and tests)

5. Open a pull request

## Adding Components

Use the scaffolding command to create the boilerplate:

```bash
uv run python manage.py create_component --name "My Component" --category input --js
```

Categories: `layout`, `navigation`, `input`, `popup`, `util`, `list`, `filter`, `card`, `form`

**Important:** Before opening a PR for a new component, complete the [New Component Checklist](new-component-checklist.md). This checklist is mandatory for all reusable UI components.

The checklist covers:
- Template tag API
- Component template
- JavaScript module (if interactive)
- Self-documentation (description, usage, parameters, accessibility)
- Demo context and presentation
- Tests

## Contract Documentation Rule

If you change a token, semantic class, template tag signature, or `data-insight-*` hook, update the corresponding documentation in the same pull request:

| Change | Update |
|--------|--------|
| Token or semantic class | `input.css` and [Design System](design-system.md) |
| Template tag signature | `insight_tags.py` and `documentation/component_details/parameter_context.py` |
| `data-insight-*` hook | JS module, template, and [Conventions](conventions.md) |

## Testing

See the [Testing Guide](testing.md) for full details.

Quick reference:

```bash
# Python tests
uv run pytest

# JavaScript tests (requires Docker)
docker run --rm -v "$(pwd):/app" -w /app node:25-alpine sh -c "npm install && npx vitest run"

# All tests
make test
```

### Test Checklist

- Template tags or Python logic: Add tests in `tests/` directory
- Frontend behavior: Add JavaScript tests if the component is interactive
- Coverage targets: 80% Python, 70% JavaScript

## GitHub Issue Labels

Labels are used as a taxonomy:

| Axis | Purpose | Examples |
|------|---------|----------|
| Type | What kind of work? | `bug`, `enhancement`, `documentation`, `chore`, `ci` |
| Area | Which part affected? | `area: component-api`, `area: design-system`, `area: responsive` |
| Component | Which component? | `component: sidebar`, `component: footer` |
| Impact | Who is affected? | `impact: public-api`, `impact: consumer-compatibility` |
| Status | Process state? | `status: split` |

For most issues: one type label, at least one area label, and a component label when applicable.

## Pull Request Guidelines

- Use conventional commits (`feat:`, `fix:`, `chore:`, `docs:`, etc.)
- PR titles must follow the same format: `docs: update contributing guide`
- Branch names must start with an allowed prefix: `feat/`, `fix/`, `docs/`, `chore/`, `ci/`, `test/`
- Refer to issues if applicable
- Only request review once CI is green and documentation is updated

Thank you for contributing!
