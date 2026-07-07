#!/usr/bin/env bash
# Compile-checks every plugin template against a real (unconnected) NetBox
# instance. Bootstraps the local checkout/venv on first run (see
# setup-test-env.sh); subsequent runs just reuse it.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$REPO_ROOT/scripts/setup-test-env.sh"

cd "$REPO_ROOT"
PYTHONPATH="$REPO_ROOT/.dev/netbox-src/netbox:$REPO_ROOT" \
    "$REPO_ROOT/.dev/venv/bin/python" scripts/check_templates.py
