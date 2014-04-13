#!/usr/bin/env python
import os, sys

if not os.getenv("VIRTUAL_ENV"):
    print >> sys.stderr, "Activate the virtual environment!"
    actpath = os.path.abspath('venv/bin/activate')
    if os.path.exists(actpath):
        print >> sys.stderr, "source %s" % actpath
    exit(1)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
