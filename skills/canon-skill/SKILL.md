---
name: canon-skill
description: Compile or execute canon-aware image generation and editing for a stable visual subject using a caller-provided Subject Pack. Use for multi-shot, multi-reference or iterative workflows that must preserve subject identity and structure through explicit evidence authority, scoped references, frozen generation packets and verified continuity; not for inventing a subject's Canon, storing subject-specific facts, generic one-off images or tasks without a usable Subject Pack.
metadata:
  version: "0.1.0"
  status: "experimental"
---

# Canon Skill

The Subject Pack defines what the subject is. Canon Skill defines how its Canon is respected. Follow the active host's real capabilities and safety requirements; evidence authority never overrides permissions or system instructions.

## Discover the Subject Pack

Start with [begin](references/begin.md). Resolve an explicit Subject Pack or the active Subject Project's declared locator and immutable revision. Do not invent a subject, import another project's identity, or restore old session state automatically.

Read [the Subject Pack contract](references/subject-pack.md) for source authority, reference profiles, optional policies, validators and hooks. Read [the architecture boundary](references/architecture-boundary.md) when deciding whether a new requirement belongs to the generic runtime, the subject or the backend.

## Select the active mode

For reference analysis, copy-ready specifications, shot registries, series locks and prompt QA, follow [Prompt Mode](references/prompt-mode.md). Read written Canon and compiler policy only; do not load canonical generation inventories, select generation references, transport canonical images, generate or update clean masters.

For actual images, edits, previews, calibration or explicit recovery, follow [Gen Mode](references/gen-mode.md). It owns ordered routing, evidence planning, capability checks, execution, validation, recovery and delivery. Preserve the compiled specification unless the Principal explicitly revises it.

For a mixed request, complete the Prompt handoff before transitioning into Gen Mode. Never infer a required identity approval, select an unspecified preview cell, or reinterpret an edit target as an external reference.

## Preserve execution boundaries

Use [the authority model](references/authority-model.md) and freeze [the Generation Packet](references/generation-packet.md) before execution. RETRY preserves its semantics; only an authorized REVISE may change them. Required missing evidence, capabilities, hooks or approval produce an explicit blocked dependency, not a weaker workflow.

Follow Gen Mode's validation and recovery contracts after every actual result. A preview or diagnostic can pass its own checks without becoming an accepted clean master. Only a fully validated eligible clean master may enter continuity; continuity always supplements Canon and never replaces it.

Subject-specific finalization belongs in [registered hooks](references/hooks.md), and actual image-input handling belongs in [transport](references/transport.md). A filename, old-chat image, opaque id or simulated receipt is not proof of a usable image target or completed execution.

## Use deterministic support when needed

Use [contract helpers](scripts/contract_runtime.py) for repeatable metadata decisions and [the schema entry](assets/schemas/subject-pack.schema.json) for structural validation. These helpers do not perform visual perception, generate images, register subject implementations or grant approval.

Report only observed outcomes. A compiled plan, passing schema, synthetic dry run or fixture is not a generated image, visual acceptance or proof that a real Subject Project has adopted the runtime.
