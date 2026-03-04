# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-04

### Added

- **Init Command**: Scaffold new OpenClaw plugins with complete project structure
  - Generates src/, tests/, pyproject.toml, README.md, and LICENSE
  - Creates boilerplate plugin code with PluginConfig class
  - Starter test suite with pytest integration
  - Automatic package name conversion (hyphens to underscores)

- **Validate Command**: Check plugin structure and configuration
  - Verifies required files and directories exist
  - Validates pyproject.toml syntax and structure
  - Checks source package structure and __init__.py files
  - Validates test structure
  - Tests Python import resolution
  - Clear pass/fail reporting with detailed output

- **Test Command**: Run plugin tests with pytest
  - Wraps pytest with OpenClaw-specific settings
  - Supports custom pytest arguments via --args flag
  - Targets tests directory with proper path resolution

- **Dev Command**: Start local development mode
  - File watching and auto-reload support (with watchfiles)
  - Fallback basic file watching without watchfiles
  - Automatic module reloading on code changes
  - Clear development feedback and tips

- **CLI Infrastructure**
  - Typer-based command structure with Rich formatting
  - Professional colored output and progress indicators
  - --version flag for version reporting
  - Comprehensive help text for all commands
  - Proper exit codes and error handling

- **Documentation**
  - Professional README with feature list and quick start
  - Command reference table
  - Links to OpenClawHQ organization
  - CHANGELOG with versioning

- **Testing**
  - Comprehensive test suite for scaffold module
  - Validation tests for validator module
  - Tests cover directory structure, file creation, imports, and TOML parsing
  - Test fixtures and pytest integration

- **CI/CD**
  - GitHub Actions workflow for linting, type checking, and testing
  - Matrix testing across Python 3.10, 3.11, 3.12
  - Ruff linting and mypy type checking
  - Pytest test runner with coverage support

### Project Structure

- Modular design: scaffold.py, validator.py, main.py
- Entry point: openclaw-cli command via setuptools
- Modern Python packaging with pyproject.toml
- Development dependencies: pytest, ruff, mypy
- MIT License

### Features Enabled

- OpenClaw-compliant plugin generation
- Real working CLI with actual file I/O and validation
- Production-ready code quality
- Community-focused messaging (Build First, Ship Loud, Open by Default)

---

**OpenClawHQ** — An open community building plugins, connectors, and tools for proactive AI.
We build hands for AI that moves first.
