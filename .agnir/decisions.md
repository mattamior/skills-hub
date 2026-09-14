# Decisions

- Keep each reusable skill independent under `skills/<skill-name>/` with `SKILL.md` as the entry point.
- Keep formal public documentation synchronized between English and Chinese.
- Do not commit credentials, user data, generated caches, virtual environments, or local installation links.
- Use Agnir `repository-filesystem/0.1` with project-owned continuity memory under `.agnir/` and repository `main` as the authoritative ref.
- Retire the legacy `.chatgpt/` continuity files so Agnir is the single repository-managed durable Project truth.
- Host the public skill gallery on Cloudflare Pages, use `https://skills-hub.hkooii.com/` as the canonical public URL, retain the provider-assigned `pages.dev` address as the underlying Pages endpoint, and deploy only revisions that have passed repository validation and production acceptance; the previous `skills-hub` Cloudflare Worker remains retired.
- Keep `ZEROLOCAL.yaml` aligned with the active Cloudflare Pages runtime and Pages-scoped deployment permissions; do not preserve Worker-specific runtime or token guidance after Worker retirement.
- Generate public catalog metadata and per-skill detail pages from each skill's `SKILL.md` and `agents/openai.yaml`; do not hand-maintain duplicate skill descriptions, invocation prompts, or source provenance in site code.
- Keep bilingual gallery localization layered over canonical skill sources: static UI copy may be dual-language in site assets, structured Simplified Chinese per-skill summaries and invocation examples live in `locales/zh-CN.json`, and the rendered `SKILL.md` operating contract remains source-English instead of maintaining translated duplicate instructions. Formal `README.zh.md` copy must be validated against the structured localization source rather than parsed as build data.
- Use maintained parsers for build-time YAML and Markdown semantics instead of repository-specific scalar/Markdown parsers; keep Markdown raw HTML disabled when rendering skill contracts.
- Keep the gallery build deterministic apart from revision-bearing health metadata; do not add wall-clock timestamps to catalog data when no consumer requires them.
- Keep validation, installer exercises, production catalog acceptance, localization coverage, and browser smoke tests data-driven over the complete skill set; adding a skill must not require editing CI or deployment allowlists.
- Use a committed npm lockfile and `npm ci` in validation/deployment so parser, browser-test, and deployment tooling resolve reproducibly.
