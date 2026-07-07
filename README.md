# netbox-dlm

A NetBox plugin for hardware/software lifecycle management — built as a
real NetBox plugin (Django models, not Custom Objects), since this needs
background scripts, custom filtersets/API viewsets, and many-to-many
scoping that Custom Objects doesn't support well.

## What it models

- `HardwareNotice` (DeviceType or ModuleType) — EoS/EoL/EoSecurity/EoSW dates
- `SoftwareVersion` (per Platform)
- `SoftwareImageFile`
- `DeviceSoftware` — software actually running on a Device
- `ValidatedSoftware` — approval rules
- `Contract`
- `Provider`
- `CVE`
- `Vulnerability`

NetBox doesn't have native `SoftwareVersion`/`Contact` core models for
this, so those are built from scratch here rather than reused.

Reports are handled as **on-demand Scripts** (`scripts.py`) rather than
stored "*Result" models — `CheckHardwareNotices` and `RunSoftwareValidation`
compute compliance live against current data. This is a deliberate scope
simplification; add stored result models later as ordinary `NetBoxModel`s
if you want historical trending of compliance over time.

## Package layout

```
netbox_dlm/
├── __init__.py                          # PluginConfig
├── models.py                            # Provider, Contract, HardwareNotice, SoftwareVersion,
│                                        # SoftwareImageFile, DeviceSoftware, ValidatedSoftware,
│                                        # CVE, Vulnerability
├── choices.py                           # ChoiceSets
├── admin.py                             # Django admin registrations
├── forms.py                             # NetBoxModelForm / FilterSetForm classes
├── tables.py                            # NetBoxTable classes
├── filtersets.py                        # NetBoxModelFilterSet classes
├── views.py                             # Generic CRUD views
├── urls.py                              # UI URL routing
├── navigation.py                        # Nav menu ("Device Lifecycle")
├── template_content.py                  # Panels injected onto Device/DeviceType pages
├── scripts.py                           # CheckHardwareNotices, RunSoftwareValidation, SyncCVEs
├── templates/netbox_dlm/
│   ├── device_lifecycle_panel.html
│   └── devicetype_lifecycle_panel.html
├── api/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── migrations/
    └── __init__.py                       # run `manage.py makemigrations` in your env (see below)
```

## Installation

1. Copy `netbox_dlm/` onto your NetBox host inside the same
   Python environment as NetBox, or install it editable via the included
   `pyproject.toml`:

   ```bash
   pip install -e /path/to/netbox_dlm
   ```

2. Add to `configuration.py`:

   ```python
   PLUGINS = [
       "netbox_dlm",
       # ... your other plugins
   ]

   PLUGINS_CONFIG = {
       "netbox_dlm": {
           "nist_api_key": None,       # optional, raises NVD API rate limits
           "eos_warning_days": 180,
       },
   }
   ```

3. **Generate and apply migrations against your actual NetBox version** —
   this repo intentionally ships without a pre-built migration, since exact
   field/constraint behavior is sensitive to the NetBox version pinned in
   your venv:

   ```bash
   cd /opt/netbox/netbox   # your NetBox root
   python3 manage.py makemigrations netbox_dlm
   python3 manage.py migrate
   ```

4. Restart NetBox (`systemctl restart netbox netbox-rq` or your equivalent).
   You should see "Device Lifecycle" in the left nav, and Scripts under
   Operations > Scripts grouped by this plugin.

5. If you're serving static files separately behind a reverse proxy, run
   `python manage.py collectstatic --no-input`.

## Using it

- **Providers / Contracts** — track who supports what, and which devices a
  contract covers (`Contract.devices` M2M).
- **Hardware Notices** — one row per `DeviceType` *or* `ModuleType` (not
  both — enforced in `clean()`), with EoS/EoL/EoSecurity/EoSW dates.
- **Software Versions / Images** — per `Platform`. `DeviceSoftware` is a
  1:1 to `Device` recording what's actually running (populate this from your
  existing sync tooling — e.g. alongside `aci_netbox_sync` runs, or a Golden
  Config compliance pass).
- **Validated Software** — approval rules scoped by `device_types`,
  `device_roles`, and/or specific `devices` (M2M). A rule
  with no scope at all applies to any device running that software version.
  `preferred=True` marks the target version for a given scope; `covers_device()`
  and `valid_now` do the compliance-check heavy lifting.
- **CVE / Vulnerability** — `CVE.affected_software` M2M links a CVE to one or
  more `SoftwareVersion`s; `Vulnerability` narrows that down to (optionally) a
  specific `Device`, with its own `status` workflow (open → mitigated/resolved).
- **Scripts** (Operations > Scripts > Device Lifecycle Management):
  - `Check Hardware Notices` — flags past-due and upcoming EoS.
  - `Run Software Validation` — flags devices whose recorded software has no
    currently-valid `ValidatedSoftware` rule, or isn't the preferred version.
  - `Sync CVEs from NIST NVD` — placeholder; wire up the actual NVD API 2.0
    HTTP calls once your NetBox host has outbound access to
    `services.nvd.nist.gov`.

Device and DeviceType pages get a right-hand panel (via `template_content.py`)
summarizing running software, compliance status, hardware notice, and open
vulnerabilities at a glance.

## Testing

```bash
./scripts/test-templates.sh
```

First run clones `netbox-community/netbox` (pinned to the version this
plugin targets) and builds a venv under `.dev/` (gitignored, ~150MB);
subsequent runs reuse it. It compiles every template in
`netbox_dlm/templates/netbox_dlm/` through NetBox's real template engine —
no database or Redis needed, since template compilation never touches the
ORM. This catches `TemplateSyntaxError`/`TemplateDoesNotExist` (bad
`{% load %}`, filters used where a tag was needed, missing includes)
before they reach a deployed host. It won't catch bugs that only manifest
at render time against real data (e.g. a table column referencing a model
attribute that silently resolves to nothing) — there's no substitute for
exercising the view against a real NetBox + Postgres instance for that.

## What I didn't build (scope cuts, worth knowing about)

- **Stored compliance-result models / history** — this plugin computes
  compliance live via scripts rather than persisting result rows.
  Straightforward to add later as another `NetBoxModel` if you want a
  graphable history.
- **Inventory item lifecycle** — hardware notices are scoped to
  `Module`/`ModuleType` (NetBox's modern equivalent); if you're still
  using NetBox's legacy `InventoryItem` model for non-modular gear, that's a
  straightforward additional FK to add to `HardwareNotice`.
- **VM software tracking** — `DeviceSoftware` only covers `Device`, not
  `VirtualMachine`. Trivial to mirror if needed.
- **Automated CVE ingestion** — `SyncCVEs` is a stub; NVD API 2.0
  request/response handling needs to be written against whatever
  auth/rate-limit setup you use.
