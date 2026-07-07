from pathlib import Path


def test_container_build_compiles_german_translations() -> None:
    dockerfile = Path("Dockerfile").read_text()

    assert "apt-get install -y --no-install-recommends gettext" in dockerfile
    assert "python manage.py compilemessages --locale de" in dockerfile
    assert "python manage.py compilemessages --locale de" in dockerfile.split("python manage.py collectstatic", 1)[0]
