# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.3] - 2026-07-15

### Added

- `requirements.txt` mirroring `pyproject.toml`'s runtime dependencies, for
  `pip install -r requirements.txt`.

### Changed

- The CVE detail view's "Vulnerability Instances" panel now renders through
  the existing `VulnerabilityTable`/`RequestConfig` machinery instead of a
  raw HTML loop, so it paginates instead of listing every instance on one
  page.

## [0.3.2] - 2026-07-13

### Security

- SHA-pinned every third-party GitHub Action referenced in
  `.github/workflows/` (with a version comment) instead of trusting
  mutable major-version tags, since the release workflow's jobs hold
  PyPI trusted-publishing and GitHub release write permissions.
- Added Dependabot config (`pip` + `github-actions` ecosystems) to keep
  the dependency and pinned action SHAs current.
- Capped `requests` to `<3.0` instead of an unbounded lower-bound-only
  pin.

## [0.3.1] - 2026-07-13

### Fixed

- `SoftwareVersionTable.device_count`, `ContractTable.device_count`, and
  `CVETable.vulnerability_count` raised `FieldError: Unsupported lookup
  'count'` when sorted, because their django-tables2 accessors
  (e.g. `devices_running__count`) only worked for rendering, not for the
  `ORDER BY` NetBox builds from the same accessor. Replaced with
  queryset-level `Count(..., distinct=True)` annotations.

## [0.3.0] - 2026-07-13

### Added

- Software Version list and detail page now show a count of devices
  running that version (`SoftwareVersionTable.device_count`, and a
  "Devices Running" panel on the detail page).

## [0.2.0] - 2026-07-09

### Added

- Shipped `0001_initial` migration covering all models, generated against
  NetBox v4.6.4.

## [0.1.0] - 2026-07-07

Initial release.

### Added

- Core models: `HardwareNotice`, `SoftwareVersion`, `SoftwareImageFile`,
  `DeviceSoftware`, `ValidatedSoftware`, `Contract`, `Provider`, `CVE`,
  `Vulnerability`.
- On-demand Scripts: `CheckHardwareNotices`, `RunSoftwareValidation`,
  `SyncCVEs` (stub).
- Device/DeviceType page panels summarizing lifecycle and compliance status.
- Packaging, CI (package-build sanity + template-compile checks), and PyPI
  release workflow.

[Unreleased]: https://github.com/droolingtaz/netbox-dlm/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/droolingtaz/netbox-dlm/releases/tag/v0.3.2
[0.3.1]: https://github.com/droolingtaz/netbox-dlm/releases/tag/v0.3.1
[0.3.0]: https://github.com/droolingtaz/netbox-dlm/releases/tag/v0.3.0
[0.2.0]: https://github.com/droolingtaz/netbox-dlm/releases/tag/v0.2.0
[0.1.0]: https://github.com/droolingtaz/netbox-dlm/releases/tag/v0.1.0
