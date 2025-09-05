from django.db.models import Q


def get_filter_settings_for_field(fields: list[dict], field: object) -> tuple[str, list[str], dict[str, str]]:
    """
    Retrieve the allowed operators based on the type of field.

    Arguments:
    ---------
        fields (list): A list of all available fields.
        field (object): The field to get the desired information from.

    Return:
    ------
        information (tuple): The desired information.

    """
    for f in fields:
        if f.get("field") == field:
            return f.get("type"), f.get("operations"), f.get("values")

    return "text", [], {}


def build_dynamic_query(filters: dict) -> tuple[Q, dict, dict]:
    """
    Build django query by the given filters.

    Arguments:
    ---------
        filters (dict): A dictionaries of filters used to generate the query.

    Returns:
    -------
        query (tuple): The generated query, a Dict with annotations and a Dict with the annotation filters.

    """
    if not filters:
        return Q(), {}, {}

    base_query = Q()
    annotations = {}
    annotation_filters = {}

    # Group filters by model field
    grouped_filters = {}
    for f in filters:
        field = f.get("field")
        # Ignore empty filters
        if field == "":
            continue
        grouped_filters.setdefault(field, []).append(f)

    for field, group in grouped_filters.items():
        # Normal fields
        for f in group:
            operator = f.get("operator", "exact")
            value = f.get("value")
            logic = f.get("logic", "AND")
            q = Q(**{f"{field}__{operator}": value})
            base_query = base_query & q if logic == "AND" else base_query | q

    return base_query, annotations, annotation_filters
