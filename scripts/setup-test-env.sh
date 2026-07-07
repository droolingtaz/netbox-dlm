#!/usr/bin/env bash
# Bootstraps a local NetBox checkout + venv for template-compile checks.
# No database or Redis is required: this only exercises django.setup()
# and template compilation, never model queries or migrations.
set -euo pipefail

NETBOX_VERSION="v4.6.4"  # keep in sync with the production host
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEV_DIR="$REPO_ROOT/.dev"
NETBOX_SRC="$DEV_DIR/netbox-src"
VENV="$DEV_DIR/venv"

mkdir -p "$DEV_DIR"

if [ ! -d "$NETBOX_SRC" ]; then
    echo "Cloning netbox-community/netbox @ $NETBOX_VERSION ..."
    git clone --quiet --depth 1 --branch "$NETBOX_VERSION" \
        https://github.com/netbox-community/netbox.git "$NETBOX_SRC"
else
    echo "NetBox checkout already present at $NETBOX_SRC (skipping clone)"
fi

if [ ! -d "$VENV" ]; then
    echo "Creating venv at $VENV ..."
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install -q --upgrade pip
    # psycopg[c] needs local libpq headers to compile; we never connect to a
    # real database here, so the pure-binary wheel is sufficient.
    sed 's/psycopg\[c,pool\]/psycopg[binary,pool]/' "$NETBOX_SRC/requirements.txt" \
        > "$DEV_DIR/requirements-test.txt"
    "$VENV/bin/pip" install -q -r "$DEV_DIR/requirements-test.txt"
else
    echo "venv already present at $VENV (skipping dependency install)"
fi

cat > "$NETBOX_SRC/netbox/netbox/configuration.py" <<'PYEOF'
# Minimal configuration for template-compile checks only.
# No database or Redis connection is ever made by this config -
# django.setup() just needs these keys to exist.

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'unused',
        'USER': 'unused',
        'PASSWORD': 'unused',
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 300,
    }
}

REDIS = {
    'tasks': {
        'HOST': 'localhost',
        'PORT': 6379,
        'USERNAME': '',
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': 'localhost',
        'PORT': 6379,
        'USERNAME': '',
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    },
}

SECRET_KEY = 'template-check-only-not-for-production-use-0123456789abcdefghij'

PLUGINS = ['netbox_dlm']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
PYEOF

echo "Test environment ready."
