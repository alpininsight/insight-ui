from dataclasses import fields, is_dataclass

import pytest
from django.utils.translation import activate
from docstring_parser import DocstringStyle, parse

from insight_ui import configs


def validate_config_docs(cls) -> None:  # noqa: ANN001
    """Verify that all members of the component Config Dataclass are documented consistently.

    To ensure consistent documentation, the following is checked:
    - A docstring is present for each member.
    - metadata["doc"] is present for each member.
    - The description is exactly the same for both (for consistency).

    Args:
        cls: The dataclass config class to validate.
    """
    parsed = parse(cls.__doc__ or "", style=DocstringStyle.GOOGLE)
    doc_params = {attr.arg_name: (attr.description or "").strip() for attr in parsed.meta if attr.args[0] == "attribute"}
    field_names = {field.name for field in fields(cls)}

    # Verify that every field is documented
    missing_in_docstring = field_names - doc_params.keys()
    if missing_in_docstring:
        raise AssertionError(f"{cls.__name__}: Missing in Docstring: {', '.join(sorted(missing_in_docstring))}")  # noqa: TRY003

    # Check that there are no typos in the docstring
    extra_in_docstring = doc_params.keys() - field_names
    if extra_in_docstring:
        raise AssertionError(  # noqa: TRY003
            f"{cls.__name__}: Appears in Docstring without related field: {', '.join(sorted(extra_in_docstring))}"
        )

    # Compare descriptions
    for field in fields(cls):
        metadata_doc = field.metadata.get("doc")

        if metadata_doc is None:
            raise AssertionError(f"{cls.__name__}.{field.name}: metadata['doc'] is missing")  # noqa: TRY003

        metadata_doc = str(metadata_doc).strip()
        docstring_doc = doc_params[field.name]

        if metadata_doc != docstring_doc:
            raise AssertionError(  # noqa: TRY003
                f"{cls.__name__}.{field.name}: "
                f"Docstring and metadata['doc'] diverge.\n\n"
                f"Docstring: {docstring_doc!r}\n"
                f"Metadata : {metadata_doc!r}"
            )


def get_config_classes() -> list:
    """Retrieve all component config dataclasses."""
    return [getattr(configs, name) for name in configs.__all__ if is_dataclass(getattr(configs, name))]


@pytest.mark.parametrize("config_cls", get_config_classes())
def test_config_docs(config_cls) -> None:  # noqa: ANN001
    """
    Verify that all members of the component Config Dataclass are documented consistently.

    To ensure consistent documentation, the following is checked:
    - A docstring is present for each member.
    - metadata["doc"] is present for each member.
    - The description is exactly the same for both (for consistency).
    """
    activate("en")
    validate_config_docs(config_cls)
