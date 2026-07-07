#!/usr/bin/env python3
"""Compile every plugin template through NetBox's real template engine.

Catches TemplateSyntaxError / TemplateDoesNotExist (undefined filters/tags,
bad {% load %}, missing includes) without needing a database - Django
compiles templates without touching models or issuing queries.

Run via: scripts/test-templates.sh (sets up the venv/checkout first).
"""
import glob
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netbox.settings')
django.setup()

from django.template import engines  # noqa: E402
from django.template.exceptions import TemplateDoesNotExist, TemplateSyntaxError  # noqa: E402


def main():
    django_engine = engines['django']
    templates = sorted(glob.glob('netbox_dlm/templates/netbox_dlm/*.html'))
    failures = []

    for path in templates:
        name = 'netbox_dlm/' + os.path.basename(path)
        try:
            django_engine.get_template(name)
            print(f'OK   {name}')
        except (TemplateSyntaxError, TemplateDoesNotExist) as e:
            failures.append((name, str(e)))
            print(f'FAIL {name}: {e}')

    if failures:
        print(f'\n{len(failures)} template(s) failed to compile', file=sys.stderr)
        return 1

    print(f'\nAll {len(templates)} templates compiled cleanly.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
