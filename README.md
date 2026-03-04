# skill-lint

A lightweight Node.js CLI tool for linting and validating OpenClaw SKILL.md files before publishing to ClawHub.

## Overview

`skill-lint` ensures that your OpenClaw skills follow best practices and are ready for publication. It validates SKILL.md file structure, required fields, metadata completeness, and markdown content quality.

## Features

- **Frontmatter Validation** - Checks YAML structure and required fields (name, description)
- **Metadata Inspection** - Validates metadata.openclaw structure and installation methods
- **Installation Validation** - Ensures install entries have correct format (brew, apt, manual, npm, pip)
- **Content Validation** - Checks markdown body for required sections (Purpose, When to Use, Setup)
- **Emoji Validation** - Warns if display emoji is missing for better ClawHub discoverability
- **Description Quality** - Validates description length (20-200 chars) for clarity
- **Colored Output** - Human-readable terminal output with errors, warnings, and info
- **JSON Output** - Machine-readable JSON output with `--json` flag
- **No External Dependencies** - Built with Node.js built-ins only

## Installation

```bash
npm install -g @openclawHQ/skill-lint
```

Or install locally:

```bash
npm install --save-dev @openclawHQ/skill-lint
```

## Usage

### Basic Validation

Validate a SKILL.md file in the current directory:

```bash
skill-lint
```

Validate a specific file:

```bash
skill-lint path/to/SKILL.md
```

### Options

```
-h, --help         Show help message
-v, --version      Show version number
-q, --quiet        Suppress info messages (errors and warnings only)
--json             Output results as JSON for programmatic use
```

### Examples

Validate with minimal output:

```bash
skill-lint -q SKILL.md
```

Get JSON output for CI/CD integration:

```bash
skill-lint --json path/to/SKILL.md
```

## Validation Rules

### Errors (must fix before publishing)

- **required-fields** - Missing `name` or `description` in frontmatter
- **install-missing-id** - Install method missing required `id` field
- **install-missing-kind** - Install method missing required `kind` field
- **install-no-target** - Install method missing target (formula/package/steps)
- **install-missing-formula** - Brew install method requires `formula` field
- **install-missing-package** - APT install method requires `package` field
- **install-missing-steps** - Manual install method requires `steps` array

### Warnings (recommended to fix)

- **name-format** - Skill name should be kebab-case (e.g., `my-skill`, not `MySkill`)
- **name-length** - Skill name longer than 50 characters
- **description-length** - Description shorter than 20 or longer than 200 characters
- **description-format** - Description should start with capital letter
- **missing-emoji** - No emoji in metadata.openclaw.emoji
- **emoji-format** - Emoji should be a single character
- **install-invalid-kind** - Install kind is not one of: brew, apt, manual, npm, pip
- **missing-sections** - Body missing recommended sections (Purpose, When to Use, Setup)
- **empty-body** - Skill description body is empty
- **no-install** - No installation methods specified
- **no-examples** - Consider adding Examples section

### Info Messages (best practices)

- **metadata-structure** - Consider adding metadata.openclaw section
- **no-examples** - Consider adding Examples section with usage patterns

## SKILL.md Format

A valid SKILL.md file requires:

```yaml
---
name: skill-name
description: "Brief description of what this skill does"

# Optional: Extended metadata for ClawHub
metadata:
  openclaw:
    emoji: 🔧
    requires:
      bins:
        - required-binary
      env:
        - REQUIRED_ENV_VAR
    install:
      - id: brew
        kind: brew
        formula: package-name
        label: "Install via Homebrew"
      - id: manual
        kind: manual
        label: "Manual installation"
        steps:
          - "Step 1"
          - "Step 2"
---

## Purpose

Describe what this skill does and its primary use cases.

## When to Use

Explain scenarios where this skill is appropriate.

## When NOT to Use

Explain scenarios where alternatives would be better.

## Setup

Installation and configuration instructions.

### Prerequisites

List required tools and dependencies.

### Local Testing

How to install and test the skill locally.

## Commands / Actions

List and describe available commands.

## Examples

Provide copy-paste-ready usage examples.

## Notes

- **Limitations**: Known limitations and edge cases
- **Performance**: Expected performance characteristics
- **Troubleshooting**: Common issues and solutions
- **Security**: Security considerations for API keys, etc.
```

## Exit Codes

- `0` - No errors found (warnings and info may still be present)
- `1` - One or more errors found

## Integration Examples

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
skill-lint SKILL.md || exit 1
```

### GitHub Actions

Add to `.github/workflows/validate.yml`:

```yaml
name: Validate SKILL.md
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install -g @openclawHQ/skill-lint
      - run: skill-lint SKILL.md
```

### npm script

Add to `package.json`:

```json
{
  "scripts": {
    "validate": "skill-lint SKILL.md"
  }
}
```

## Development

### Project Structure

```
.
├── bin/
│   └── skill-lint.js        # CLI entry point
├── src/
│   ├── parser.js            # SKILL.md parser
│   ├── rules.js             # Validation rules
│   └── reporter.js          # Output formatting
├── test/
│   ├── parser.test.js       # Parser tests
│   ├── rules.test.js        # Rules tests
│   ├── reporter.test.js     # Reporter tests
│   ├── integration.test.js  # Integration tests
│   └── fixtures/            # Test fixtures
├── package.json
└── README.md
```

### Running Tests

```bash
npm test
```

All tests use Node.js built-in `test` runner (Node 18+).

### Adding New Rules

1. Add validation function to `src/rules.js`
2. Add tests in `test/rules.test.js`
3. Update README with rule documentation
4. Run tests to verify: `npm test`

## Future Enhancements

- Auto-fix capabilities for common issues
- Support for skill templates and scaffolding
- Integration with ClawHub API for pre-publish checks
- Custom rule configuration
- Multiple file validation
- Watch mode for development

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `npm test`
5. Submit a pull request

## License

MIT - See LICENSE file

## Links

- [OpenClaw](https://github.com/OpenClawHQ/openclaw) - Main project
- [ClawHub](https://clawhub.com) - Official skill registry
- [SKILL.md Specification](https://github.com/OpenClawHQ/openclaw/docs/SKILL.md) - Full format documentation

---

Built by the OpenClaw community. We move first.
