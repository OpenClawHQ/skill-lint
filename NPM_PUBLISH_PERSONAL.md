# 用个人 npm 账号发布 skill-lint

包名已设为 `@afkv/skill-lint`，用你的 npm 账号发布后，别人即可 `npx @afkv/skill-lint`。

---

## 第一步：改包名

打开 `package.json`，把 `name` 从：

```json
"name": "@openclawHQ/skill-lint"
```

改成（已按你的 npm 用户名 `afkv` 配置）：

```json
"name": "@afkv/skill-lint"
```

保存文件。

---

## 第二步：登录 npm

在终端执行（会提示输入 Username、Password、Email、OTP 等）：

```bash
npm login
```

按提示用你在 https://www.npmjs.com 的账号登录。

---

## 第三步：发布

在项目根目录执行（scoped 包必须加 `--access public`，否则会变成私有包）：

```bash
cd /Users/dujiayi/Desktop/OpenClawHQ/skill-lint
npm publish --access public
```

成功后会看到类似：`+ @afkv/skill-lint@0.1.0`

---

## 第四步：别人怎么用

任何人（包括你自己）可以：

```bash
npx @afkv/skill-lint
```

或先安装再运行：

```bash
npm install -g @afkv/skill-lint
skill-lint
```

---

## 可选：以后要改成 org 包

如果之后在 npm 上创建了 **openclawHQ** 组织，并把你的账号加进去，可以把 `package.json` 的 `name` 改回 `@openclawHQ/skill-lint`，改一下版本号（例如 `0.1.1`），再执行一次 `npm publish --access public`。两个包名可以并存（一个是你个人的，一个是 org 的）。
