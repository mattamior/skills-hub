# Agent Skills

这是 `mattamior` 的个人 Agent Skills 集合，用于开发和维护可在 ChatGPT 与 Codex 中复用的工作流。仓库中的每个 skill 都独立存放在 `skills/<skill-name>/`，并以 `SKILL.md` 作为入口。

线上画廊：[skills-hub.lapplax.com](https://skills-hub.lapplax.com/)

## Skills

| Skill | 用途 |
| --- | --- |
| [`brand-design-system`](skills/brand-design-system/SKILL.md) | 从品牌探索、过程留档和母版确认推进到生产资产、网站接入与视觉验收。 |
| [`pet-avatar-generation`](skills/pet-avatar-generation/SKILL.md) | 将真实宠物照片转成保持辨识度的风格化头像，探索明显不同的视觉方向，并精修选中的方案，包括透明背景输出。 |

## 安装

Codex 会从用户级 `$HOME/.agents/skills` 目录发现 skills，本仓库使用符号链接保持已安装版本与源码一致：

```bash
git clone https://github.com/mattamior/skills-hub.git
cd skills-hub
./scripts/link-skills.sh --check brand-design-system
./scripts/link-skills.sh brand-design-system
./scripts/link-skills.sh pet-avatar-generation
```

无参数时，脚本会处理仓库中的全部 skills。可使用 `--target DIR` 指定其他安装目录。脚本不会覆盖已有文件或指向其他位置的符号链接。

## 使用

安装到用户级 `$HOME/.agents/skills` 后，无需将 skill 复制到其他仓库。在任意 Codex 项目中，在请求开头显式调用所需 skill：

```text
$brand-design-system 审查这个项目现有的 Logo、favicon 和 PWA 图标，先做只读检查并报告证据、缺口和待决策项。
```

```text
$pet-avatar-generation 把源图里的宠物做成三个明显不同的头像风格，同时保留它的花纹和辨识特征。
```

Codex CLI 或 IDE 扩展中也可先运行 `/skills` 确认已发现 skills，再输入 `$` 选择。在 ChatGPT 桌面版中，从 Skills 选择器选择对应 skill。当请求与某个 skill 的描述匹配时，ChatGPT 或 Codex 也可能自动选择它。

## 开发与验证

新增或修改 skill 时：

1. 将 skill 放入 `skills/<skill-name>/`，并保持目录名与 `SKILL.md` 的 `name` 一致。
2. 把通用工作流和关键约束写在 `SKILL.md`；按需细节放入 `references/`，输出模板放入 `assets/`。
3. 同步维护 `agents/openai.yaml`，其默认提示必须显式包含 `$<skill-name>`。
4. 将简体中文目录摘要和调用示例写入 `locales/zh-CN.json`，并保持 `README.zh.md` 中对应的正式文案一致。
5. 运行仓库与网站验证：

```bash
./scripts/validate-skills.py
npm ci
npm run check
```

画廊构建会直接读取 `SKILL.md`、`agents/openai.yaml` 与 `locales/zh-CN.json`。`README.zh.md` 会与结构化本地化事实源做一致性校验，但不会再被解析为构建数据。

GitHub Actions 还会使用固定 revision 的 Agent Skills `skills-ref` 检查规范兼容性，针对完整 skill 集合验证安装脚本的检查、安装、幂等与冲突拒绝路径，并使用真实 Chromium 浏览器执行双语画廊 smoke test。本地如需运行浏览器测试，可先通过 Playwright 安装 Chromium：

```bash
npx playwright install chromium
npm run test:browser
```

当 skill 的路由发生实质变化时，复核 `tests/*-trigger-cases.md` 下对应的场景。

正式用户文档保持 `README.zh.md` 与 `README.en.md` 同步。仓库只分发独立 skills，不打包 plugin，也不发布 GitHub Release。

## 许可证

[Apache License 2.0](LICENSE)
