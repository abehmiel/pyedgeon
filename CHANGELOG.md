# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-07-22

### Security

- Upgraded Pillow from `^10.0.0` (locked 10.4.0) to `^12.3.0` (locked 12.3.0) to
  remediate four vulnerabilities:
  - **CVE-2026-25990** — out-of-bounds write in PSD parsing (RCE), fixed in Pillow 12.1.1
  - **CVE-2026-40192** — FITS GZIP decompression bomb (DoS), fixed in Pillow 12.2.0
  - **CVE-2026-42311** — out-of-bounds write from PSD tile integer overflow, fixed in Pillow 12.2.0
  - **CVE-2026-54060** — excessive allocation in `FontFile.compile()`, fixed in Pillow 12.3.0

### Changed

- **BREAKING: minimum supported Python is now 3.10.** Pillow 12.x dropped support for
  Python 3.8 and 3.9, and no patched Pillow release exists for those interpreters, so
  clearing the CVEs above requires dropping them. Python 3.8/3.9 users must stay on
  pyedgeon 0.4.0 (which remains vulnerable) or upgrade their Python.
- Updated tooling targets to match: mypy `python_version = 3.10`, ruff `target-version = py310`,
  black `target-version = [py310, py311, py312]`.

### Fixed

- Declared `numpy` as a required dependency. It was previously listed as an optional
  "optimization" extra, but the core rendering path imports and uses it unconditionally,
  so any install without numpy failed at import. numpy is now a core dependency.
