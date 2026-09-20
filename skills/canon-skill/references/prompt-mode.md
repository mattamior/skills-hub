# Prompt Mode

Compile a self-contained Generation Spec, not a Generation Packet. Prompt Mode has no generation side effects.

## Allowed inputs and output

Read the subject's written-authority projection, the current Principal instruction, explicitly supplied external references, and current-session shot definitions. Do not load canonical generation images, select anchor IDs, resolve transport, invoke image tools or hooks, mark gates passed, or modify accepted-master/continuity state.

The machine-readable handoff follows [Generation Spec schema](../schemas/generation-spec.schema.json). Record subject ID, written revision, Gen-pack locator, route, operation, output kind, effective spec, series lock, shot registry, selected shot, external role map, preserve constraints, required gates, and unresolved fields.

## Compilation

Separate observed reference information, Principal instructions, and unknowns. Scope each external reference before translating pose, camera, composition, lighting, environment, wardrobe, objects, or declared extensions. Never import another subject's primary identity.

Preserve exact reference shots as separate shot definitions; do not average incompatible poses or cameras. Give each shot a stable ID and revision. Keep shared variables in a series lock and shot-specific changes in the registry. Defaults come from the pack's written/runtime policy, not human anatomy assumptions inside this skill.

Write explicit descriptions instead of relying on 'as in the reference'. Preserve meaningful uncertainty; do not invent occluded details. Compile intentional construction-stage omissions as deferred final invariants with required finalization, never as a change to final Canon.

## Handoff QA

Confirm one selected target, explicit ratio or declared ratio source, reference scopes, preserve constraints, and unresolved gates. A series handoff can describe multiple shots; each actual Gen call still gets a separate target packet. Preview outer layout and inner-shot ratios are distinct.

A Prompt Spec may be handed off with unresolved generation dependencies, but must label them. It cannot claim `PACKET_FROZEN`, loaded references, validated images, or approved gates. Preserve a fingerprint of the spec. Gen Mode may fill execution dependencies, but may not silently redesign photography or identity.

## Mode transition

An explicit request to generate routes to [Gen Mode](gen-mode.md). Reload current Subject Canon; a revision mismatch requires reconciliation, not silent use of stale written facts. Cross-session transfer of the spec does not transfer old preview images, approval state, clean masters, or edit targets.
