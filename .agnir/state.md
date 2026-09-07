# Current State

- Project: `mattamior/skills-hub`, a repository for developing and maintaining reusable Agent Skills for ChatGPT and Codex.
- Skills live under `skills/<skill-name>/` and use `SKILL.md` as their entry point.
- The currently documented reusable skills are `brand-design-system` and `pet-avatar-generation`.
- The public gallery is deployed with Cloudflare Pages and exposed canonically at `https://skills-hub.hkooii.com/`; the provider-assigned `https://skills-hub-ea7.pages.dev/` address remains the underlying Pages URL, and the superseded `skills-hub` Cloudflare Worker has been retired.
- The public gallery is now a repository-generated skill catalog: each skill gets a dedicated `/skills/<skill-name>/` detail page generated from `SKILL.md` and `agents/openai.yaml`, including source links, a Codex install command, and a ready-to-copy invocation prompt.
- The public gallery supports English and Simplified Chinese across the catalog shell and generated skill detail pages, and the browser remembers the selected language. Chinese per-skill summaries and invocation examples are derived at build time from `README.zh.md`, while the rendered `SKILL.md` operating contract remains the canonical English source.
- Repository validation uses `./scripts/validate-skills.py`; GitHub Actions also checks skill compatibility and install behavior before deploying the validated revision to Cloudflare Pages, then accepts both the provider Pages URL and the canonical custom domain.
- Agnir Core `0.1` with discovery profile `repository-filesystem/0.1` is initialized, with colocated durable continuity under `.agnir/`.
- The Agnir operational package is upgraded compatibly to published `v0.1.1`, applied from immutable revision `e9712357ab590e5c1e5357b3cf3219d07d789aff`; Project identity and all declared memory locators/content were preserved.
