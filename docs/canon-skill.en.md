# Canon Skill 0.1.0 — experimental

Canon Skill is a subject-agnostic operating contract with deterministic supporting helpers for stable, Canon-aware image generation and editing. It is not an image model, a bundled Subject Pack, a visual-recognition service or a provider-specific generation client.

## Ownership and use

The Subject Project owns who or what the subject is: written Canon, invariant groups, visual references, calibration, specialized validators, hooks and delivery. Canon Skill owns how that authority is respected. The execution host owns actual tools, asset access, visual inspection and authorization.

Install `skills/canon-skill` with the repository's existing installer. Invoke it with an available Subject Pack:

```text
$canon-skill use this Subject Pack to compile three shots. Keep canonical identity and use my external references only for pose and lighting. Do not generate yet.
```

Prompt Mode compiles written intent without reading canonical generation inventories or transporting their images. Gen Mode separately resolves route, image roles, scoped external references, minimum canonical evidence, capabilities and gates; then freezes and executes one packet. Missing prerequisites block rather than produce a weaker workflow.

## Implementation map

The thin [SKILL.md](../skills/canon-skill/SKILL.md) routes to begin, Prompt Mode and Gen Mode. Conditional contracts live in `references/`. Six JSON Schemas cover Subject Pack, references, calibration, runtime state, generation packet and result. `scripts/contract_runtime.py` provides deterministic building blocks for route/role resolution, minimum cover, packet immutability, scoped gates, classification, recovery, hook invocation, transport checks and continuity/import rules.

The helpers use Python's standard library. Schema and fixture tests use pinned jsonschema and PyYAML dependencies in CI. Schema ids under `schemas.canon-skill.invalid` are local registry identifiers, not live network endpoints. Register all six schema resources locally.

The optional exact-cover helper is bounded to 24 already-relevant candidate assets. Larger inventories require prior scoping or an equivalent host planner. No helper performs image-model inference, verifies a person's identity automatically or treats caller-supplied evidence as self-authenticating.

## Verification

The repository includes 63 executable generic contract tests, including three explicitly simulated Human/Pet/Virtual end-to-end paths. They cover negative boundaries as well as successful metadata paths. The original Markdown trigger/runtime/validation scenarios remain forward-test specifications, not counted as executed visual tests.

```bash
python -m pip install 'jsonschema==4.26.0' 'PyYAML==6.0.3'
python -m unittest discover -s tests -p 'test_*.py' -v
./scripts/validate-skills.py
npm ci --ignore-scripts --no-audit --no-fund
npm run check
npx playwright install chromium
npm run test:browser
```

CI additionally validates every skill with pinned Agent Skills `skills-ref` and the official upstream skill-creator quick validator, exercises check/install/repeat/collision behavior, verifies full Chinese localization and versioned gallery assets, and runs Chromium smoke tests.

Synthetic byte strings, simulated receipts, supplied PASS reports and fixture manifests are never real image-generation or visual-fidelity evidence. The host must materialize actual references and inspect actual candidates before acceptance.

## Release gates

| Milestone | Required evidence | Status of this distribution |
| --- | --- | --- |
| 0.1.0 experimental | generic contracts, three subject classes, Prompt/Gen, routing, evidence, packets, validation/recovery, continuity and hooks | implemented with executable contract verification |
| 0.2.0 | a real consumer pack with complete source-bound legacy parity, calibration/hook behavior and generation-semantics preservation | gated; private consumer development and scoped shadow checks are not full cutover proof |
| 1.0.0 | at least two distinct real Subject Projects successfully consuming the runtime | not established by anonymous fixtures or one consumer's metadata tests |

Private consumer facts and assets stay outside the public skill. Do not publish a production-readiness claim, perform a cutover, or count a fixture as an adopted project merely because CI is green. Record integration conflicts, unsupported capabilities, actual visual QA and Principal approvals in the owning Subject Project.
