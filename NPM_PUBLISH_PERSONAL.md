# Publish skill-lint with a personal npm account

The package name is set to `@afkv/skill-lint`. After you publish with your npm account, others can run `npx @afkv/skill-lint`.

---

## Step 1: Set the package name

In `package.json`, set `name` from:

```json
"name": "@openclawHQ/skill-lint"
```

to (already set for npm user `afkv`):

```json
"name": "@afkv/skill-lint"
```

Save the file.

---

## Step 2: Log in to npm

In the terminal:

```bash
npm login
```

Enter your npm username, password, email, and one-time password (if 2FA is enabled) when prompted.

---

## Step 3: Publish

From the project root (scoped packages require `--access public` or they stay private):

```bash
cd /Users/dujiayi/Desktop/OpenClawHQ/skill-lint
npm publish --access public
```

On success you will see something like: `+ @afkv/skill-lint@0.1.0`

---

## Step 4: How others use it

Anyone (including you) can run:

```bash
npx @afkv/skill-lint
```

Or install globally then run:

```bash
npm install -g @afkv/skill-lint
skill-lint
```

---

## Optional: Switch to an org package later

If you create an **openclawHQ** organization on npm and add your account, you can change `package.json` `name` back to `@openclawHQ/skill-lint`, bump the version (e.g. to `0.1.1`), and run `npm publish --access public` again. Both package names can coexist (one under your user, one under the org).
