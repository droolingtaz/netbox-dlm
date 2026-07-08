# Contributing

This is a young, single-maintainer plugin, so process is intentionally
light. AI agents working in this repo should also follow
[AGENTS.md](AGENTS.md).

## Getting set up

There's nothing to install in this repo standalone — it's a NetBox plugin
and only runs loaded inside a NetBox instance. To validate changes without a
full NetBox environment:

```bash
./scripts/test-templates.sh
```

See [README.md](README.md) for full installation instructions against a real
NetBox host, and the "Testing" section for what template-compile checks do
and don't catch.

## Before opening a PR

- Run `./scripts/test-templates.sh` if you touched anything under
  `netbox_dlm/templates/`.
- Run `python -m build && twine check dist/*` if you touched packaging
  (`pyproject.toml`, `MANIFEST.in`, package layout) — this mirrors CI's
  `package-build-sanity` job.
- If you bump the version, update it in **both**
  `pyproject.toml` (`project.version`) and `netbox_dlm/__init__.py`
  (`PluginConfig.version`), and add a `CHANGELOG.md` entry.
- If you touch `netbox_dlm/models.py`, don't commit a generated migration —
  see AGENTS.md for why migrations are intentionally not shipped.

## Releasing

Tag pushes matching `v*.*.*` trigger `.github/workflows/release.yml`, which
verifies the tag matches `pyproject.toml`'s version, builds, and publishes to
PyPI + GitHub Releases. Tagging a mismatched version fails CI before
anything publishes.
