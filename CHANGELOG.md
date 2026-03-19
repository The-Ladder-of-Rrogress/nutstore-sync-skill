# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-03-18

### Added
- Complete type annotations for all methods
- Exception hierarchy: `NutstoreError`, `ConfigError`, `APIError`
- New methods: `delete()`, `exists()`
- `pyproject.toml` for modern Python packaging
- Bilingual README (Chinese/English)
- CHANGELOG.md following Keep a Changelog format
- Comprehensive .gitignore for Python projects

### Changed
- Refactored to single file structure
- Improved error handling with specific exception types
- Enhanced docstrings with Google style
- Optimized config validation

### Removed
- Split module structure (merged into single file)
- Redundant code and unused imports

## [1.0.0] - 2024-XX-XX

### Added
- Initial release
- Basic WebDAV operations: upload, download, list
- Command line interface
- JSON configuration support
