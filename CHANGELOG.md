# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/droolingtaz/netbox-dlm/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/droolingtaz/netbox-dlm/releases/tag/v0.2.0
[0.1.0]: https://github.com/droolingtaz/netbox-dlm/releases/tag/v0.1.0
