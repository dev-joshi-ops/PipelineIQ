# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-04-13

### Removed
- **Documentation**: Removed visual architecture diagram from README.md.

## [0.1.0] - 2026-04-13

### Added
- **Security Hardening**: Implemented strict regex validation for Jenkins jobs, builds, and folders to prevent injection.
- **Fail-Safe Decorator**: Added `@safe_tool` to prevent internal infrastructure leakage (URLs, stack traces) to LLM clients.
- **Input Bounding**: Added size limits for log retrieval and build listing to prevent resource exhaustion.
- **Sanitizer Unit Tests**: Added regression tests for automated log redaction.

### Fixed
- **Thread Safety**: Refactored `JenkinsClient` as a thread-safe singleton.
- **Indentation & Syntax**: Resolved multiple syntax and indentation errors across tool implementations.
- **Test Assertions**: Fixed broken test assertions caused by Pydantic model migration.
- **Lifecycle Cleanup**: Fixed async client cleanup during server shutdown.

### Changed
- **Architectural Pivot**: Completely refactored the repository from a FastAPI/React web scaffold to a Python-based Model Context Protocol (MCP) server named **pipeline-iq**.
- **Tech Stack**: Switched to `antigravity` Python SDK, `httpx` for API requests, and `pytest` for testing.
- **Persona Updates**: Replaced web-centric developer personas with `@mcp-builder` and `@cicd-expert`.
- **Project Goal**: PipelineIQ is now focused on becoming a CI/CD Pipeline Debugger connecting to Jenkins and GitHub Actions.
- **Folder Structure**: Adopted PyPI-standard `src/` layout.
- **Packaging**: Updated `pyproject.toml` with detailed metadata, project URLs, and classifiers for PyPI.
- **Standard Layout**: Added missing `__init__.py` files across all subpackages.
- **PEP 561 Compliance**: Added `py.typed` for type-hint distribution.
- **Linter Alignment**: Full project alignment with `ruff` rules.
