# skill-lint

[![npm](https://img.shields.io/npm/v/@openclawHQ/skill-lint?color=E03E3E&logo=npm&logoColor=white)](https://www.npmjs.com/package/@openclawHQ/skill-lint) [![CI](https://github.com/OpenClawHQ/skill-lint/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenClawHQ/skill-lint/actions) [![Node.js ≥ 18](https://img.shields.io/badge/node-%3E%3D18-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

**[English →](./README.md)**

一个轻量级 Node.js CLI 工具，用于在发布到 ClawHub 前 lint 并验证 OpenClaw SKILL.md 文件。

## 概述

`skill-lint` 确保你的 OpenClaw skill 遵循最佳实践并已准备好发布。它验证 SKILL.md 文件结构、必填字段、metadata 完整性和 markdown 内容质量。

## 功能

- **Frontmatter 验证** — 检查 YAML 结构和必填字段（name、description）
- **Metadata 检查** — 验证 `metadata.openclaw` 结构和安装方式
- **安装方式验证** — 确保 install 条目格式正确（brew、apt、manual、npm、pip）
- **内容验证** — 检查 markdown body 是否包含必要章节（Purpose、When to Use、Setup）
- **Emoji 验证** — 如缺少展示用 emoji 则发出警告（影响 ClawHub 可发现性）
- **描述质量检查** — 验证 description 长度（20-200 字符）
- **彩色输出** — 带错误/警告/信息分级的人类可读终端输出
- **JSON 输出** — 通过 `--json` flag 输出机器可读的 JSON
- **零外部依赖** — 仅使用 Node.js 内置模块构建

## 安装

```bash
npm install -g @openclawHQ/skill-lint
```

或本地安装：

```bash
npm install --save-dev @openclawHQ/skill-lint
```

## 使用

### 基础验证

验证当前目录下的 SKILL.md 文件：

```bash
skill-lint
```

验证指定文件：

```bash
skill-lint path/to/SKILL.md
```

### 选项

```
-h, --help         显示帮助信息
-v, --version      显示版本号
-q, --quiet        抑制 info 消息（只显示错误和警告）
--json             以 JSON 格式输出结果，适合程序化使用
```

### 示例

最小化输出：

```bash
skill-lint -q SKILL.md
```

获取 JSON 输出（用于 CI/CD 集成）：

```bash
skill-lint --json path/to/SKILL.md
```

## 验证规则

### 错误（发布前必须修复）

- **required-fields** — frontmatter 中缺少 `name` 或 `description`
- **install-missing-id** — install 方式缺少必填 `id` 字段
- **install-missing-kind** — install 方式缺少必填 `kind` 字段
- **install-no-target** — install 方式缺少 target（formula/package/steps）
- **install-missing-formula** — brew 安装方式需要 `formula` 字段
- **install-missing-package** — APT 安装方式需要 `package` 字段
- **install-missing-steps** — manual 安装方式需要 `steps` 数组

### 警告（建议修复）

- **name-format** — skill name 应为 kebab-case（如 `my-skill`，而非 `MySkill`）
- **name-length** — skill name 超过 50 个字符
- **description-length** — description 少于 20 或超过 200 个字符
- **description-format** — description 应以大写字母开头
- **missing-emoji** — `metadata.openclaw.emoji` 中未设置 emoji
- **emoji-format** — emoji 应为单个字符
- **install-invalid-kind** — install kind 不在以下范围内：brew、apt、manual、npm、pip
- **missing-sections** — body 缺少推荐章节（Purpose、When to Use、Setup）
- **empty-body** — skill description body 为空
- **no-install** — 未指定安装方式
- **no-examples** — 建议添加 Examples 章节

### 信息（最佳实践）

- **metadata-structure** — 建议添加 `metadata.openclaw` 章节
- **no-examples** — 建议添加包含使用示例的 Examples 章节

## SKILL.md 格式

一个合法的 SKILL.md 文件需要：

```yaml
---
name: skill-name
description: "简短描述这个 skill 的功能"

# 可选：为 ClawHub 提供扩展 metadata
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
        label: "通过 Homebrew 安装"
      - id: manual
        kind: manual
        label: "手动安装"
        steps:
          - "第 1 步"
          - "第 2 步"
---

## Purpose

描述这个 skill 的功能及主要使用场景。

## When to Use

说明适合使用这个 skill 的场景。

## Setup

安装和配置说明。

## Commands / Actions

列出并描述可用的命令。

## Examples

提供可直接复制使用的示例。
```

## 退出码

- `0` — 未发现错误（可能有警告和信息）
- `1` — 发现一个或多个错误

## 集成示例

### Pre-commit Hook

添加到 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
skill-lint SKILL.md || exit 1
```

### GitHub Actions

推荐直接使用 [skill-lint-action](https://github.com/OpenClawHQ/skill-lint-action)——零配置，PR 行内标注：

```yaml
- uses: OpenClawHQ/skill-lint-action@v1
```

或手动集成 CLI：

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
- run: npm install -g @openclawHQ/skill-lint
- run: skill-lint SKILL.md
```

### npm script

添加到 `package.json`：

```json
{
  "scripts": {
    "validate": "skill-lint SKILL.md"
  }
}
```

## 开发

### 运行测试

```bash
npm test
```

所有测试使用 Node.js 内置 `test` runner（需要 Node 18+）。

### 添加新规则

1. 在 `src/rules.js` 中添加验证函数
2. 在 `test/rules.test.js` 中添加测试
3. 更新 README（本文件）中的规则说明
4. 运行测试验证：`npm test`

## 贡献

欢迎贡献！请：

1. Fork 本 repo
2. 创建 feature 分支
3. 为新功能添加测试
4. 确保所有测试通过：`npm test`
5. 提交 Pull Request

## License

MIT — 详见 [LICENSE](./LICENSE)

## 相关链接

- [OpenClaw](https://github.com/openclaw/openclaw) — 主项目
- [ClawHub](https://clawhub.com) — 官方 skill 注册中心
- [skill-lint-action](https://github.com/OpenClawHQ/skill-lint-action) — 本工具的 GitHub Action 封装版

---

由 OpenClaw 社区构建。We move first.
