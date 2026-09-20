# External Reference Router

Consume already resolved image roles. Do not reclassify protected Canon, edit bases, selected previews, or accepted continuity as ordinary external references.

## Scope

Baseline roles are `POSE`, `CAMERA`, `COMPOSITION`, `LIGHTING`, `WARDROBE`, `ENVIRONMENT`, `OBJECT`, `SECONDARY_SUBJECT`, `NON_HUMAN_SUBJECT`, and the operational fallback `ORIGINAL_PROMPT_REFERENCE`.

POSE changes articulated configuration, not fixed identity geometry. CAMERA/COMPOSITION change view and spatial arrangement. LIGHTING changes illumination. WARDROBE varies only permitted wearable state. ENVIRONMENT and OBJECT supply the authorized scene/prop. SECONDARY_SUBJECT supplies a separately requested additional subject; NON_HUMAN_SUBJECT retains its narrower original meaning. Neither may replace or blend the primary identity.

Additional reusable dimensions use pack-declared `extension:<name>` roles with explicit allowed influence. Core code does not interpret a particular subject feature. All roles retain primary identity/structural denial, including extensions.

## Explicit and fallback routing

Runtime modes are NONE, ROLE_SCOPED, or CONSERVATIVE_FALLBACK. 'Only lighting' removes other influence for that image. Resolve fallback from prompt-explicit dimensions or the pack's explicitly declared non-identity fallback policy; never grant unlimited influence from 'use this image'.

In an execution packet, expand ORIGINAL_PROMPT_REFERENCE into concrete allowed dimensions and retain the operational fallback label in image_roles. Keep source provenance and the expansion basis. Unresolved influence is `SPEC_UNRESOLVED`.

Preserve current effective-spec precedence over evidence. A reference helps execute the shot; it cannot silently change it. External evidence cannot cover missing primary canonical identity or structure. Add NO_EXTERNAL_IDENTITY_TRANSFER and protect canonical structure even when the reference contains another person, animal, robot or product.

## Transport

Select the minimum task-relevant external set, not every upload. Freeze which references are generation-critical. Each selected packet image must actually enter the call or execution blocks. Optional evidence excluded from the packet need not be transported.

Record id, authority, roles, allowed/denied influence, checksum, declared extension meanings and selection rationale. Keep external, canonical, preview/edit and continuity channels distinct. For edits, external influence is further limited by the frozen change/preserve contract.
