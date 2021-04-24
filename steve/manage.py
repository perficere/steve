#!/usr/bin/env python
"""Django’s command-line utility for administrative tasks."""

import sys

from core.set_settings_module import set_settings_module


def main():
    set_settings_module()
    try:
        # pylint: disable=import-outside-toplevel
        from django.core.management import execute_from_command_line
    except ImportError as exception:
        raise ImportError("Couldn’t import Django.") from exception
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
