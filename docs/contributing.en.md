# Contributor Guide (Version 0.1.0)

Thank you for improving Insight UI. This guide explains how to add components, documentation, and tests while staying consistent with the project’s conventions.

## Prerequisites
- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) for dependency management
- Node.js if you plan to extend the Tailwind build

Install everything locally:

```bash
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py runserver
```

## Development Workflow
1. Create a feature branch.
2. Run `uv run ruff format` and `uv run ruff check --fix` on the files you touch.
3. Execute the test suite with `uv run --extra test pytest`.
4. Update documentation and demos before opening a pull request.

## Adding or Extending Components
- Follow the [naming conventions](guides/naming_conventions.md) for templates, assets, and context helpers.
- Place new templates in `insight_ui/templates/insight_ui/components/…` and register an inclusion tag inside `insight_ui/templatetags/insight_tags.py`.
- Store component-specific JS/CSS under `insight_ui/static/insight_ui/`.
- Add demo data in `insight_ui/demo_context.py` so the showroom and docs render your component.

## Documentation Expectations
- Each new component or significant change needs a page under `docs/en/components/` and `docs/de/components/`.
- Update the example partial in `insight_ui/templates/insight_ui/docs/partial/` if the demo output changes.
- Keep both language variants in sync: update the German (`docs/de/...`) and English (`docs/en/...`) files in the same commit.

## Testing Checklist
- Template tag or Python changes: add or update tests in `insight_ui/tests/test_template_tags.py` or a new test module.
- Frontend behaviour: add regression coverage using HTMX or screenshot references when applicable.
- Demo scripts (`utils/`) should log through the structured logger and avoid global state.

## Pull Request Guidelines
- Use Conventional Commit prefixes (`feat:`, `fix:`, `chore:`, `docs:`, …).
- Reference related issues and describe user-facing impact.
- Include evidence of testing (command output, screenshots, or links to preview builds).
- Request review once lint and tests pass and documentation is updated.

By following these steps you help keep Insight UI predictable and approachable for every team member.
