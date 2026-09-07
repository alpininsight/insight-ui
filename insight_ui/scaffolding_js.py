# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Optional JavaScript skeleton following the package's lifecycle convention."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from insight_ui.scaffolding import ComponentScaffold

HEADER = (
    "// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG\n"
    "// SPDX-License-Identifier: AGPL-3.0-only\n"
)


def javascript_changes(root: Path, spec: ComponentScaffold) -> list[tuple[str, str, bool]]:
    """Wire imports, initialization and cleanup instead of emitting an orphan file."""
    class_name = spec.class_name.removesuffix("Config")
    slug = spec.slug.replace("_", "-")
    module = f"insight-ui-{slug}.js"
    entry_path = "insight_ui/static/insight_ui/js/insight-ui-init.js"
    entry = (root / entry_path).read_text(encoding="utf-8")
    replacements = {
        "import { Accordion }": f'import {{ {class_name} }} from "./{module}";\n\nimport {{ Accordion }}',
        "Object.assign(window.InsightUI, {": f"Object.assign(window.InsightUI, {{\n\t{class_name},",
        "function initAll() {": f"function initAll() {{\n\t{class_name}.initAll();",
    }
    for marker, replacement in replacements.items():
        if entry.count(marker) != 1:
            message = "The JS initializer changed; cannot safely register this component. Nothing was written."
            raise ValueError(message)
        entry = entry.replace(marker, replacement, 1)
    source = (
        HEADER
        + f"""/** Lifecycle skeleton. Add behavior and matching tests before requesting review. */
export class {class_name} {{
    static instances = new WeakMap();

    constructor(element) {{
        if ({class_name}.instances.has(element)) {{
            return {class_name}.instances.get(element);
        }}
        this.element = element;
        this.controller = new AbortController();
        element.__insightInstance = this;
        {class_name}.instances.set(element, this);
    }}

    static initAll(root = document) {{
        root.querySelectorAll("[data-insight-{slug}]").forEach(element => new {class_name}(element));
    }}

    destroy() {{
        this.controller.abort();
        if (this.element.__insightInstance === this) {{
            delete this.element.__insightInstance;
        }}
        {class_name}.instances.delete(this.element);
    }}
}}
"""
    )
    test = (
        HEADER
        + f"""import {{ expect, test }} from "vitest";
import {{ {class_name} }} from "../../insight_ui/static/insight_ui/js/{module}";

test("{slug} initializes once and can be initialized again after cleanup", () => {{
    const root = document.createElement("div");
    root.innerHTML = '<div data-insight-{slug}></div>';
    const element = root.firstElementChild;
    {class_name}.initAll(root);
    const instance = element.__insightInstance;
    {class_name}.initAll(root);
    expect(element.__insightInstance).toBe(instance);
    instance.destroy();
    expect(instance.controller.signal.aborted).toBe(true);
    expect(element.__insightInstance).toBeUndefined();
    {class_name}.initAll(root);
    expect(element.__insightInstance).not.toBe(instance);
    element.__insightInstance.destroy();
}});
"""
    )
    return [
        (f"insight_ui/static/insight_ui/js/{module}", source, True),
        (f"tests/js/{slug}.test.js", test, True),
        (entry_path, entry, False),
    ]
