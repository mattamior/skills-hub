---
name: brand-design-system
description: Create, refine, document, package, govern, or review a brand identity from optional brand foundations through approved production assets and optional web integration. Use for brand foundations tied to identity work, logo systems, process records, asset packs, favicon/PWA/social exports, machine-readable brand tokens or asset manifests, accessibility-aware implementation reviews, or governance handoffs; not for one-off illustrations or standalone product UI component-library/design-system work.
---

# Brand Design System

Create a brand identity that remains traceable and faithful from the initial evidence through approved production assets. Treat documented strategy when it exists, source material, approved artwork, and recorded decisions—not verbal recollection—as the source of truth.

## Invoke the skill

In Codex, invoke the skill from any repository by starting the request with `$brand-design-system`; a user-scoped installation does not need to be copied into each project. In ChatGPT desktop, select **Brand Design System** from the Skills picker. Both products may also select it automatically when the request matches the skill description.

```text
$brand-design-system audit this project's existing logo, favicon, and PWA assets. Start read-only and report evidence, gaps, and required decisions.
```

## Establish the assignment

Determine whether the request is exploration, refinement, historical reconstruction, production, integration, or review. Inspect existing assets, implementation, repository history, and prior records before asking questions they can answer.

Establish the brand or product name, audience, intended surfaces, required languages and scripts, visual constraints, target markets, available source material, and approval authority. Keep evidence, inference, and unknowns separate. Never invent missing design history or strategy.

For a new identity, repositioning, or a visual direction that depends on unresolved strategy, establish the minimum brand foundation needed to make design choices: positioning, audience, promise or value proposition, differentiators, personality, and any relevant values or non-values. For production or review of an already approved identity, reuse existing foundation evidence and do not force redundant strategy work.

Do not advance past this gate until the intended outcome, audience, surfaces, approver, and material blockers are clear enough to act without guessing. If a blocking unknown cannot be resolved from available evidence, report it explicitly and stop at the affected gate.

## Keep a durable process record

Read [process record guidance](references/process-records.md) for new identity work, historical reconstruction, or any task expected to produce a reusable handoff. Use the supplied [process log](assets/templates/brand-process-log.md) and [handoff](assets/templates/brand-handoff.md) templates when the project lacks an equivalent record; adapt an established project convention instead of creating a duplicate system.

Record materially distinct concept directions, the evidence behind them, selection and rejection reasons, approval checkpoints, clearance status, exceptions, and unresolved questions. A transient ideation request does not require a full dossier unless the user asks for one.

Treat naming or visual similarity checks as risk screening, not legal clearance. When clearance matters, record the status and evidence as `not requested`, `preliminary screen`, `specialist/legal review recorded`, or `unknown`, including jurisdiction, classes or scope, date, and source when those details exist. Never promote a preliminary screen to a legal conclusion.

## Explore and approve

For new identity exploration, create a small set of materially distinct, vector-friendly directions. Explain the visual idea, likely category associations, strategic fit, and important tradeoffs. Image generation is suitable for exploration, not as an automatic substitute for editable production artwork.

Do not treat aesthetic preference as approval. Once the user or named approver selects a direction, record that checkpoint before producing derivatives. Similarity review may flag visual or naming risk, but it is not legal or trademark clearance.

Do not leave the concept gate until the selected direction, approver, material rejected alternatives, known risks, and unresolved blockers are recorded at the level appropriate to the assignment.

## Lock the approved master

Record the master artwork location and visible invariants: geometry and proportions, palette, stroke behavior, typography and casing, backgrounds, negative space, and lockup relationships. Do not silently simplify, redraw, reinterpret, or substitute those decisions while producing derivatives.

Use editable SVG or another vector-native source for production logo work. Pathify final wordmarks when portability matters and licensing permits it. If only raster or incomplete evidence exists, report the fidelity limit before rebuilding anything. Localized wordmarks or script-specific lockups are separate approved variants rather than implicit transformations.

Do not leave the master gate until the editable source or fidelity limit, approved version, invariants, typography/licensing constraints, and required localized variants are identifiable. Machine-readable metadata may reference the master, but it does not replace the approved artwork.

## Produce only what the delivery needs

Read [production asset guidance](references/production-assets.md) when producing production assets, application icons, social images, machine-readable delivery, or a web-ready pack. Generate the minimum useful asset set and keep concept previews separate from approved production files.

When downstream automation needs structured brand data, prefer an established project token or asset-manifest format. If interoperable design tokens are explicitly requested and no project format exists, use the current stable Design Tokens Community Group format where compatible rather than a draft format. Keep tokens and manifests derived from approved decisions, include provenance or version references, and do not model logo geometry as design tokens merely because a token format exists.

Website integration requires explicit authorization. When authorized, inspect the project and follow its existing asset conventions. Update only the approved branding surface and required metadata; do not change product behavior or information architecture. Verify current platform-specific metadata or image requirements when possible; otherwise state any assumed defaults instead of presenting them as timeless requirements.

## Verify visible output

Read [visual QA guidance](references/visual-qa.md) whenever finalizing production assets or reviewing an implementation. Validate rendered output rather than SVG source alone, including transparency, color application, small-size readability, lockup proportions, localized typography when relevant, and actual favicon or manifest delivery.

When brand colors are applied to text, controls, states, or informational graphics, verify the target accessibility standard rather than assuming the logo exception applies to the whole interface. Record allowed application pairings and any decorative-only colors; do not rely on color alone to convey required meaning.

Finish by updating the process log and handoff with generated assets, machine-readable artifacts when any, integration changes, validation evidence, clearance and accessibility status, known limits, deprecations or replacements, and unresolved work. Report evidence and inference separately. Do not claim final acceptance until the required approval and QA gates for the assignment are satisfied.
