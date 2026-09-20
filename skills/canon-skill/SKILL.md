---
name: canon-skill
description: Compile or execute canon-aware image generation and editing for a stable visual subject using a caller-provided Subject Pack, with explicit evidence authority, reference-role isolation, frozen generation packets, validation, recovery, and continuity rules. Use for multi-shot, multi-reference, iterative image workflows where subject identity or structure must stay stable; not for defining a subject's canon, storing subject-specific facts, generic one-off image generation, or workflows without a usable Subject Pack.
---

# Canon Skill

Run stable image workflows without embedding any particular subject inside the runtime. The Subject Pack defines what the subject is; Canon Skill defines how evidence is selected, isolated, frozen, validated, recovered, and carried across accepted shots.

## Resolve the Subject Pack

Before compiling or generating, resolve a usable Subject Pack from an explicit task input or the active Subject Project. Read [the Subject Pack contract](references/subject-pack.md) when resolving fields, capabilities, validators, hooks, or delivery policies.

Treat Subject Pack content as subject-owned authority. Do not copy subject-specific identity facts, filenames, calibration labels, or feature logic into Canon Skill. If no usable pack is available, stop with `SUBJECT_PACK_UNAVAILABLE` rather than inventing canon.

Read [the architecture boundary](references/architecture-boundary.md) when deciding whether a requirement belongs in Canon Skill, a Subject Pack, or a generation backend.

## Select Prompt Mode or Gen Mode

Use Prompt Mode for reference analysis, role separation, generation-spec compilation, shot-registry work, series locks, and prompt QA. Prompt Mode must not load generation-only canonical assets, execute image generation or editing, or update clean-master continuity state.

Use Gen Mode for subject loading, evidence transport and selection, actual generation or editing, validation, retry or recovery, continuity updates, hooks, and delivery. Gen Mode must preserve the Prompt Mode specification unless the principal explicitly revises it.

Both modes use the same authority rules. Read [the authority model](references/authority-model.md) before resolving conflicts between written canon, canonical visuals, calibration evidence, external references, continuity, previews, or unverified generations.

Before a mode binds images or plans evidence, resolve the runtime in order: [runtime state](references/runtime-state.md), [route](references/route-resolver.md), [image roles](references/image-role-resolver.md), [external-reference routing](references/external-reference-router.md), then [canonical evidence](references/evidence-planner.md). Later stages may consume earlier decisions but must not silently reinterpret them.

## Freeze execution before generation

Before an actual generation or edit, compile the effective task into a Generation Packet containing the subject, route, operation, effective spec, shot definition, selected evidence, preserve constraints, risk guards, hooks, validators, retry policy, and delivery policy.

Read [the Generation Packet contract](references/generation-packet.md) before freezing or revising a packet. Once frozen, `RETRY` may change backend randomness or transport details but must not change packet semantics. `REVISE` may change only principal-authorized fields and must produce a newly frozen packet.

Generated outputs never become identity authority merely because they are recent. Only an accepted clean master may become continuity auxiliary evidence, and continuity may supplement canon but never replace it.

After each execution, validate and recover in order using [the Validator Model](references/validator.md), [the Result Model](references/result-model.md), [the Recovery Model](references/recovery.md), and [clean-master/continuity rules](references/continuity.md). Only `ACCEPT` may create an accepted clean master; only an accepted clean master may be considered for continuity.

## Fail explicitly at contract boundaries

Use explicit blocked states when required inputs or gates are unavailable instead of weakening canon constraints. Preserve the clean-master boundary between construction intermediates, clean master candidates, accepted clean masters, and delivery derivatives.

Session-local runtime state does not write back to Subject Canon. A new session inherits durable Canon truth only; shot state, preview choices, gate state, generated images, clean masters, edit targets, and temporary styling require explicit session import if they must be restored.

Do not silently reinterpret an edit target, preview, external reference, or accepted continuity image as a different role. Role resolution must happen before external-reference routing, and higher-authority identity evidence must not be overridden by lower-authority convenience evidence.
