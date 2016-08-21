#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    print(__import__('django'))  # Should print the module information
    print(__import__('django').__file__)  # Should print the location of __init__.py file
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
