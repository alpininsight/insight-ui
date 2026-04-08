# Guidelines for contributors

Are you interested in helping us further develop Insight UI? 

Welcome! 

We appreciate every helpful contribution to further expanding Insight UI so that it is as useful and versatile as possible. First, here is some information about how the project is structured and how we work. This document explains how you can help us and what guidelines we have in place to avoid any misunderstandings.

## Prerequisites

First of all, the requirements for working with Insight UI:

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) for dependency management

Lokales Setup:

```bash
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py runserver
```

This should enable Insight UI to run locally.

## Our workflow

This section describes our traditional workflow. We ask that you adhere to it so that everything can run smoothly and no unnecessary effort is required.

We always work with feature branches, so the first step is to create a new branch with a suitable name, e.g., `feat/accordion`, or if it involves improving a component by fixing a bug, for example, `fix/accordion`.

Then you can work on the branch in peace. If everyone follows the rules, no one should work on your branch without asking.

Once all changes are complete and the runners have run through the tests and linting, you can create a pull request and add someone from the review team.

### Summary

1. Create feature branch
2. Develop
3. Update documentation and demos if necessary
4. Wait for green light from CI runner
5. Open pull request.

## Add components

In this section, we explain all the steps necessary to add a new component.

### Part 1: Creating a component

1. Create a new template for the component under `insight_ui/templates/insight_ui/components`, e.g., `accordion.html`. If necessary, you can also create multiple templates.
2. If required, create a new JavaScript file under `insight_ui/static/insight_ui/js`.
    - We use classes for all components that are exported as modules.
    - Corresponding instances are found and created in the DOM using `data attributes`.
3. Implement the new component.
    - We use TailwindCSS for styling.
4. Create a new inclusion tag in `insight_ui/templatetags/insight_tags.py`.

### Part 2: Documenting New Components

1. Document the new component for future users. Our component documentation is context-based and is divided into several files in this directory: `insight_ui/component_details/`
    - `a11y_context.py`: Contains documentation for all accessibility topics related to the component.
    - `description_context.py`: Contains a summary description of the component.
    - `parameter_context.py`: Contains an explanation of the component's parameters.
    - `related_components_context.py`: Contains a list of all components that are similar or related to the topic.
    - `usage_context.py`: Contains an example of the source code required to integrate the component.
    - `git_path_mapping.py`: Contains the URL to the component file(s) and, if applicable, the script file(s) in the Git repository.
2. Insert demo
    - Extend component demo file `insight_ui/templates/insight_ui/docs/component_demo.html`
        - Disable padding in the view if necessary
    - Add demo context function `insight_ui/demo_context.py

> Please note our [Naming Conventions](naming_conventions.md) for Templates, Assets and Context-helper.

## Test checklist

- Template tags or Python logic: Add tests in `insight_ui/tests/test_template_tags.py` or your own test module.
- Frontend behavior: Add regression tests (e.g., HTMX requests or screenshots) if necessary.

## Pull request guidelines

- We use conventional commits (`feat:`, `fix:`, `chore:`, `docs:`, etc.) for both commit messages and branch names. For branch name use `/` instead of `:`.
- Refer to issues if necessary.
- Only request a review once the CI runners for linting and testing are green and the documentation has been updated.

This ensures that Insight UI remains easy to understand and can be easily maintained by all team members.

Thank you for your interest. We look forward to receiving your ideas and suggestions for improvement.
