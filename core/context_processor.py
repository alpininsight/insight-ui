from django.conf import settings
from django.http import HttpRequest


def project_context(request: HttpRequest) -> dict:
    """Contains information of the project."""
    return {"PROJECT_NAME": settings.PROJECT_NAME, "VERSION": settings.VERSION, "productive": settings.IS_PROD}
