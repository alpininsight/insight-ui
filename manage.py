#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Django's command-line utility for administrative tasks."""

import os
import sys

from logging_config import setup_logging

if __name__ == "__main__":
    """Run administrative tasks."""
    setup_logging()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devtools.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        msg = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(msg) from exc
    execute_from_command_line(sys.argv)
