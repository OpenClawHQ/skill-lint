# openclaw-cli

The developer toolkit for building OpenClaw plugins.

`openclaw-cli` provides a streamlined workflow for OpenClaw plugin developers—from scaffolding to testing, validation, and local development. Built for the OpenClaw community: we build hands for AI that moves first.

## Features

- **Init** — Scaffold a new plugin with a complete project structure, config, tests, and boilerplate code
- **Validate** — Check plugin structure, config schema, and imports for correctness
- **Test** — Run plugin tests with OpenClaw-specific settings and reporting
- **Dev** — Start local development mode with hot-reload and plugin runtime

## Quick Start

### Installation

```bash
pip install openclaw-cli
```

### Create a New Plugin

```bash
openclaw init my-plugin
cd my-plugin
```

This generates:
```
my-plugin/
├── src/my_plugin/
│   ├── __init__.py
│   ├── plugin.py
│   └── config.py
├── tests/
│   └── test_plugin.py
├── pyproject.toml
├── README.md
└── LICENSE
```

### Validate Your Plugin

```bash
openclaw validate
```

Checks:
- Required files and directories exist
- `pyproject.toml` is valid
- Plugin config schema is correct
- All imports can be resolved

### Run Tests

```bash
openclaw test
```

Runs pytest with OpenClaw-specific settings.

### Start Development Mode

```bash
openclaw dev
```

Watches source files and automatically reloads your plugin in dev mode.

## Command Reference

| Command | Usage | Description |
|---------|-------|-------------|
| `init` | `openclaw init <name>` | Scaffold a new plugin project |
| `validate` | `openclaw validate [path]` | Validate plugin structure and config |
| `test` | `openclaw test [path]` | Run plugin tests with pytest |
| `dev` | `openclaw dev [path]` | Start local development mode |

All commands (except `init`) accept an optional `[path]` argument to target a specific plugin directory. Defaults to current directory (`.`).

## Links

- [OpenClawHQ](https://github.com/OpenClawHQ)
- [OpenClaw Plugins](https://github.com/OpenClawHQ/openclaw)
- [Contributing](./CONTRIBUTING.md)
- [License](./LICENSE)

## Principles

**Build First** — Rapid iteration with real tools.
**Ship Loud** — Celebrate launches and share progress.
**Open by Default** — Transparent, community-driven development.

---

Built by the OpenClaw community. We move first.
