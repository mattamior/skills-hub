---
name: canon-skill
description: Run canon-aware image generation and editing for a stable visual subject from a caller-owned Subject Pack. Use for multi-shot series, multi-reference role isolation, iterative edits, calibration, and continuity-sensitive image workflows; also compile generation specifications without generating images. Not for inventing a subject's canon, generic one-off illustration, or unrelated retouching.
---

# Canon Skill

Respect the subject's Canon without owning its identity facts. Use the Subject Pack for subject truth and the active generation backend for execution; never make this skill depend on a named Subject Project.

## Resolve the subject and mode

Read [Begin](references/begin.md) to discover the caller's Subject Pack, establish a fresh session, and select the mode. Missing or conflicting authority is a blocker, not permission to invent a subject.

Use [Prompt Mode](references/prompt-mode.md) to compile intent, reference roles, series locks, and shot definitions. Load only the written-authority projection: do not select canonical image IDs, bootstrap generation references, generate images, or update clean masters.

Use [Gen Mode](references/gen-mode.md) for actual generation or editing. Resolve the pack, verify usable inputs, select evidence, freeze the packet, execute the declared hooks, validate the exact candidate, and respect recovery and delivery boundaries.

## Preserve the authority boundary

Apply [the authority model](references/authority-model.md) within each evidence item's authorized scope. Canonical identity wins over external references and accepted continuity. Previews, failed results, and delivery derivatives never become identity authority.

Read [architecture boundaries](references/architecture-boundary.md) and [the Subject Pack contract](references/subject-pack.md) when a new requirement needs a subject-owned extension. Keep subject facts, features, calibration labels, and hook implementations outside this skill.

## Load only the needed runtime contracts

For a new execution or semantic revision, use [route resolution](references/route-resolver.md), [image-role resolution](references/image-role-resolver.md), [external routing](references/external-reference-router.md), and [evidence planning](references/evidence-planner.md), in that order. Use [Runtime State](references/runtime-state.md) for scoped gates and explicit `SESSION_IMPORT`.

Before execution, read [Generation Packet](references/generation-packet.md), [hook lifecycle](references/hooks.md), and [backend transport](references/generation-backend.md). `RETRY` preserves packet semantics; only a Principal-authorized `REVISE` may change them.

For results, read [validation](references/validator.md), [classification](references/result-model.md), [recovery](references/recovery.md), and [continuity](references/continuity.md). A successful preview or diagnostic is still not an accepted final clean master.

## Check contracts without inventing acceptance

Use [contract tools](references/contract-tools.md) for bundled schemas, deterministic packet checks, and declaration-level tests. Passing a schema, mock backend, or dry run does not prove image fidelity, actual attachment transport, hook availability, Principal approval, or real-subject acceptance.

Stop at a missing dependency or unsatisfied gate. Do not execute arbitrary commands from a Subject Pack, reuse a failed image as an identity chain, restore prior-session image state implicitly, or present simulated evidence as production evidence.
