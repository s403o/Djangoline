#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from utils.logging import setup_log
from utils.telemetry import setup_telemetry

import structlog
logger = structlog.stdlib.get_logger(__name__)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
    setup_log()
    setup_telemetry()
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            logger.exception("Couldn't import Django.")
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
