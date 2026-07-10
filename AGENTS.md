# AGENTS.md

Instructions for AI coding agents (Claude Code, Copilot, Cursor, Codex, etc.)
working in this repo. See [README.md](README.md) first for what this plugin
models and why — this file covers things the README doesn't: workflow
gotchas, CI shape, and constraints that aren't visible from reading the code.

## What this is

A real NetBox plugin (Django app), not a standalone service. It only makes
sense loaded inside a NetBox instance's Python environment — there is no
`manage.py`, database, or Redis in this repo itself.

## Commands

```bash
./scripts/test-templates.sh   # only automated check that exists today
python -m build                # build sdist/wheel (mirrors CI's package-build-sanity job)
```

There is no unit test suite, linter, or formatter configured yet — don't
assume `pytest`, `ruff`, `flake8`, or `black` exist here; check
`pyproject.toml` before adding a command that depends on one.

`test-templates.sh` compiles every template in
`netbox_dlm/templates/netbox_dlm/` through NetBox's real template engine
(`scripts/check_templates.py`). First run clones `netbox-community/netbox`
(pinned version, see below) into `.dev/netbox-src` and builds a venv under
`.dev/venv` (~150MB, gitignored); later runs reuse both. This only proves
templates *parse* — it never touches the ORM, so it won't catch a template
referencing a model field that silently resolves to nothing at render time.

## Things that will bite you if missed

- **NetBox version pin**: `scripts/setup-test-env.sh` hardcodes
  `NETBOX_VERSION="v4.6.4"`. If you bump this, it must track whatever NetBox
  version is actually running in production — a mismatch means the template
  checks pass against a NetBox that doesn't match reality. Delete `.dev/` to
  force a re-clone after bumping it.
- **Shipped migration tracks the NetBox version pin**: `netbox_dlm/migrations/0001_initial.py`
  was generated against NetBox v4.6.4 (see README's Installation section).
  If you change a model or bump the NetBox version pin, regenerate it —
  `makemigrations` needs a real NetBox checkout with the plugin importable;
  the same `.dev/netbox-src` + `.dev/venv` used by `test-templates.sh` works
  for this (add the plugin to `PLUGINS` in its `configuration.py` and set
  `DEVELOPER = True`, since NetBox's `makemigrations` command refuses to run
  otherwise). Field/constraint behavior on NetBox's core models
  (`dcim.Device`, `dcim.Platform`, etc.) is sensitive to NetBox version, so
  always verify the regenerated migration against the version actually
  running in production before shipping it.
- **CI's package-build-sanity job runs from `/tmp`** (see
  `.github/workflows/test.yml`) specifically so `import netbox_dlm` resolves
  to the *installed wheel*, not this checkout's source tree. If you touch
  that job, preserve the `cd /tmp` — removing it silently defeats the check.
- **Release tags must match `pyproject.toml`**: `.github/workflows/release.yml`
  fails the build if a pushed `vX.Y.Z` tag doesn't match
  `project.version` in `pyproject.toml`. Bump the version in `pyproject.toml`
  (and `netbox_dlm/__init__.py`'s `version = "..."`, which is separate and
  not currently checked against the tag) before tagging.

## Conventions

- Models follow NetBox's plugin patterns: `NetBoxModel` base class, one
  `NetBoxModelForm`/`FilterSetForm` per model in `forms.py`, one
  `NetBoxTable` in `tables.py`, one `NetBoxModelFilterSet` in
  `filtersets.py`, generic CRUD views in `views.py`. Follow the existing
  model in each file rather than introducing a new pattern.
- Compliance/reporting logic belongs in `scripts.py` as an on-demand
  `Script`, not a stored `*Result` model — see README's "What I didn't
  build" section for why, and don't add historical-trend models without
  raising it first, since that's a deliberate scope cut.
- `netbox_dlm/__init__.py`'s `PluginConfig.version` and `pyproject.toml`'s
  `project.version` should be bumped together even though nothing enforces
  it automatically today.
