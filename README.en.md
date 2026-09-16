# Agent Skills

This is `mattamior`'s collection for developing and maintaining reusable Agent Skills for ChatGPT and Codex. Each skill lives independently under `skills/<skill-name>/` and uses `SKILL.md` as its entry point.

Public gallery: [skills-hub.lapplax.com](https://skills-hub.lapplax.com/)

## Skills

| Skill | Purpose |
| --- | --- |
| [`brand-design-system`](skills/brand-design-system/SKILL.md) | Establish brand foundations when needed, then move from identity exploration and approval to governed production assets, implementation, and visual/accessibility acceptance. |
| [`pet-avatar-generation`](skills/pet-avatar-generation/SKILL.md) | Turn a real pet photo into recognizable stylized profile avatars, explore distinct visual directions, and refine a selected result including transparent-background output. |

## Install

Codex discovers user-level skills from `$HOME/.agents/skills`. This repository uses symbolic links so installed skills stay aligned with their source:

```bash
git clone https://github.com/mattamior/skills-hub.git
cd skills-hub
./scripts/link-skills.sh --check brand-design-system
./scripts/link-skills.sh brand-design-system
./scripts/link-skills.sh pet-avatar-generation
```

With no skill arguments, the script processes every skill in the repository. Use `--target DIR` for another installation directory. It never overwrites an existing file or a symbolic link that points elsewhere.

## Use

After installing it in the user-level `$HOME/.agents/skills` directory, you do not need to copy the skill into other repositories. Invoke a skill explicitly at the start of a request in any Codex project:

```text
$brand-design-system audit this project's existing logo, favicon, and PWA assets. Start read-only and report evidence, gaps, and required decisions.
```

```text
$pet-avatar-generation turn the pet in my source image into three distinct profile-avatar styles while preserving its markings.
```

In Codex CLI or the IDE extension, you can also run `/skills` to confirm discovery and then type `$` to select a skill. In ChatGPT desktop, choose the matching skill from the Skills picker. ChatGPT or Codex may also select a skill automatically when the request matches its description.

## Develop and validate

When adding or changing a skill:

1. Put it in `skills/<skill-name>/` and keep the directory name equal to the `name` in `SKILL.md`.
2. Keep shared workflow and essential constraints in `SKILL.md`; put conditional detail in `references/` and output templates in `assets/`.
3. Keep `agents/openai.yaml` aligned and include `$<skill-name>` explicitly in its default prompt.
4. Add the Simplified Chinese display name, catalog summary, full scope description, invocation example, and complete website contract mirror to `locales/zh-CN.json`, then keep the matching formal summary and invocation copy in `README.zh.md` aligned.
5. Run repository and site validation:

```bash
./scripts/validate-skills.py
npm ci
npm run check
```

The gallery build reads `SKILL.md`, `agents/openai.yaml`, and `locales/zh-CN.json` directly. English `SKILL.md` remains the canonical agent instruction source; the Chinese `bodyMarkdown` field is a website display mirror whose section structure, code fences, and repository-relative references are validated against that canonical source. `README.zh.md` is validated against the structured localization source but is not parsed as build data.

GitHub Actions also validates Agent Skills specification compatibility with a pinned `skills-ref` revision, exercises the installer's check/install/idempotency/collision paths across the complete skill set, and runs real-browser Chromium smoke tests for the fully bilingual gallery. To run the browser smoke tests locally after installing Chromium with Playwright:

```bash
npx playwright install chromium
npm run test:browser
```

For material routing changes, review the matching scenarios under `tests/*-trigger-cases.md`.

Keep formal user documentation synchronized between `README.zh.md` and `README.en.md`. The repository distributes standalone skills only; it does not package a plugin or publish a GitHub Release.

## License

[Apache License 2.0](LICENSE)
