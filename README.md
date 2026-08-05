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
- `InventoryItemSoftware` — software actually running on an InventoryItem
  (e.g. a Cisco CIMC or Dell iDRAC modeled as a legacy InventoryItem)
- `InventoryItemRolePlatform` — maps an InventoryItemRole to the Platform
  whose SoftwareVersions apply to it
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
│                                        # SoftwareImageFile, DeviceSoftware, InventoryItemSoftware,
│                                        # InventoryItemRolePlatform, ValidatedSoftware,
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
│   ├── inventoryitem_lifecycle_panel.html
│   └── devicetype_lifecycle_panel.html
├── api/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── migrations/
    ├── __init__.py
    └── 0001_initial.py                   # generated against NetBox v4.6.4 (see below)
```

## Installation

1. Install the package into the same Python environment as NetBox — from
   PyPI:

   ```bash
   pip install netbox-dlm
   ```

   or, for local development, editable from a checkout via the included
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

3. **Apply migrations:**

   ```bash
   cd /opt/netbox/netbox   # your NetBox root
   python3 manage.py migrate
   ```

   The shipped `0001_initial` migration was generated against NetBox v4.6.4.
   If your host runs a different NetBox version, run
   `python3 manage.py makemigrations netbox_dlm` first and check the output
   for unexpected diffs before migrating — field/constraint behavior on
   NetBox's core models (`dcim.Device`, `dcim.Platform`, etc.) can shift
   between versions.

4. Restart NetBox (`systemctl restart netbox netbox-rq` or your equivalent).
   You should see "Device Lifecycle" in the left nav, and Scripts under
   Operations > Scripts grouped by this plugin.

5. If you're serving static files separately behind a reverse proxy, run
   `python manage.py collectstatic --no-input`.

### Docker (netbox-docker)

Nothing about this plugin is Docker-incompatible — it's pure Python (only
dependency is `requests`, which NetBox core already pulls in), has no
compiled extensions, and doesn't use `FileField`/`ImageField` anywhere, so
it doesn't care whether media storage is local disk or S3. The steps just
differ from the bare-metal instructions above because of how
[netbox-docker](https://github.com/netbox-community/netbox-docker) itself
works, not because of anything specific to this plugin:

1. `netbox-docker`'s base image doesn't ship third-party plugins, so you
   need a custom image. Add a `plugin_requirements.txt` next to your
   `docker-compose.yml`:

   ```
   netbox-dlm
   ```

   and a `Dockerfile-Plugins` (see netbox-docker's
   [plugins documentation](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins)
   for the current template) that `RUN`s
   `pip install -r /opt/netbox/plugin_requirements.txt` on top of the base
   image. Point your compose file's `build` at it instead of pulling the
   stock image.

2. Configure the plugin via netbox-docker's dedicated config file,
   `/etc/netbox/config/plugins.py` (typically mounted from
   `configuration/plugins.py` in your compose repo), rather than editing
   `configuration.py` directly:

   ```python
   PLUGINS = ["netbox_dlm"]

   PLUGINS_CONFIG = {
       "netbox_dlm": {
           "nist_api_key": None,
           "eos_warning_days": 180,
       },
   }
   ```

3. Rebuild and restart: `docker compose build && docker compose up -d`.
   netbox-docker runs `migrate` and `collectstatic` automatically on
   container startup, so no separate migration step is needed — just watch
   the `netbox` container's startup logs to confirm the migration applied
   cleanly.

4. The same version-match caveat from step 3 above still applies: check
   that the NetBox image tag you're pinned to is compatible with the
   shipped migrations before rolling this out to a production stack.

## Using it

- **Providers / Contracts** — track who supports what, and which devices a
  contract covers, either explicitly (`Contract.devices` M2M) or by
  `Contract.platforms` (any device on a covered platform). Unlike
  `ValidatedSoftware`, an empty scope covers nothing — `covers_device()`
  and `covered_devices` do the lookup, so a contract can't silently apply to
  devices nobody scoped it to.
- **Hardware Notices** — one row per `DeviceType` *or* `ModuleType` (not
  both — enforced in `clean()`), with EoS/EoL/EoSecurity/EoSW dates.
- **Software Versions / Images** — per `Platform`. `SoftwareVersion.release_designation`
  optionally marks a version as N-1/N/N+1 in that platform's release train (at
  most one version per platform per designation, enforced by a DB constraint).
  `DeviceSoftware` is a 1:1 to `Device` recording what's actually running
  (populate this from your existing sync tooling — e.g. alongside
  `aci_netbox_sync` runs, or a Golden Config compliance pass).
  `InventoryItemSoftware` is the same idea for a `dcim.InventoryItem` — useful
  for management controllers (Cisco CIMC, Dell iDRAC, HPE iLO, etc.) modeled
  as inventory items rather than as their own `Device`. Since `InventoryItem`
  has no `platform` field of its own, `InventoryItemRolePlatform` declares
  which `Platform`'s `SoftwareVersion`s apply to a given `InventoryItemRole`
  (e.g. "Management Controller" → a "Cisco CIMC" platform); once that mapping
  exists, the `InventoryItemSoftware` add form narrows its version picker to
  that platform, and `clean()` rejects a mismatched selection.
- **Validated Software** — approval rules scoped by `device_types`,
  `device_roles`, specific `devices`, `platforms`, and/or
  `inventory_item_roles` (all M2M). A rule with no scope at all applies to
  any device or inventory item running that software version.
  `preferred=True` marks the target version for a given scope;
  `covers_device()`/`covers_inventory_item()` and `valid_now` do the
  compliance-check heavy lifting.
- **CVE / Vulnerability** — `CVE.affected_software` M2M links a CVE to one or
  more `SoftwareVersion`s; `Vulnerability` narrows that down to (optionally) a
  specific `Device` *or* `InventoryItem` (at most one of the two), with its
  own `status` workflow (open → mitigated/resolved).
- **Scripts** (Operations > Scripts > Device Lifecycle Management):
  - `Check Hardware Notices` — flags past-due and upcoming EoS.
  - `Run Software Validation` — flags devices and inventory items whose
    recorded software has no currently-valid `ValidatedSoftware` rule, or
    isn't the preferred version.
  - `Sync CVEs from NIST NVD` — placeholder; wire up the actual NVD API 2.0
    HTTP calls once your NetBox host has outbound access to
    `services.nvd.nist.gov`.

Device, InventoryItem, and DeviceType pages get a right-hand panel (via
`template_content.py`) summarizing running software, compliance status, and
open vulnerabilities at a glance (the Device panel also shows the
`HardwareNotice` for its `DeviceType`, since hardware EoL notices are still
`DeviceType`/`ModuleType`-scoped only — see below).

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
- **Inventory item hardware notices** — `InventoryItemSoftware` and its
  `ValidatedSoftware`/`Vulnerability` scoping now cover `InventoryItem`, but
  `HardwareNotice` (EoS/EoL dates) is still scoped to `DeviceType`/`ModuleType`
  only. If you're using NetBox's legacy `InventoryItem` model for non-modular
  gear and want EoL tracking for it too, that's a straightforward additional
  FK to add to `HardwareNotice`.
- **VM software tracking** — `DeviceSoftware` only covers `Device`, not
  `VirtualMachine`. Trivial to mirror if needed.
- **Automated CVE ingestion** — `SyncCVEs` is a stub; NVD API 2.0
  request/response handling needs to be written against whatever
  auth/rate-limit setup you use.
