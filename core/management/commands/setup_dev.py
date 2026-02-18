"""Management command to set up the development environment."""

from typing import Any

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Set up the development environment (migrate + create admin user)."""

    help = "Set up the development environment (migrate + create admin user)"

    def handle(self, *_args: Any, **options: Any) -> None:  # noqa: ANN401
        """Run migrations and create a default admin superuser."""
        self.stdout.write("Running migrations...")
        call_command("migrate", verbosity=options["verbosity"])

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        if not user_model.objects.filter(**{username_field: "admin"}).exists():
            kwargs = {username_field: "admin", "password": "admin"}  # noqa: S106
            if username_field != "email":
                kwargs["email"] = "admin@localhost"
            user_model.objects.create_superuser(**kwargs)
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin"))
        else:
            self.stdout.write(
                self.style.WARNING("Superuser 'admin' already exists, skipping.")
            )

        self.stdout.write(self.style.SUCCESS("Dev setup complete!"))
