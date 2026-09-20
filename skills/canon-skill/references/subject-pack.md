# Subject Pack Contract

The normative v1 wire shape is [subject-pack.schema.json](../schemas/subject-pack.schema.json); shared definitions are in [contracts.schema.json](../schemas/contracts.schema.json). Resolve a caller-owned pack, never embed a real subject in this skill.

## Required blocks

Require `subject`, `canon`, `references`, `calibration`, `validators`, `postprocess`, and `delivery`. Use `subject.id` and a resolvable revision for provenance. `subject.type` is descriptive, not an anatomy switch. Empty optional capability lists are valid.

`canon.written_authority` records facts or written-source locators, revision and invariant scope. `invariant_groups` uses generic IDs, classes, regions and constraints. Do not require face, hair, coat, marks, or any particular anatomy as generic fields.

## References and profiles

The [reference schema](../schemas/references.schema.json) separates authority, visible regions, explicit invariant `covers`, view, generation eligibility and diagnostic-only status. Experimental older fixtures using invariant IDs in `visible_regions` remain readable, but new packs should use `covers` explicitly. Real execution must resolve asset bytes and checksums; a placeholder locator does not satisfy it.

A profile matches generic shot attributes and requires invariant groups. `require.assets` may declare an irreducible complementary set whose order is meaningful; minimization cannot remove or reorder it. `prefer_assets` is a preference, not a substitute for coverage. Profiles may be `PRIMARY` or `SUPPLEMENT`. With `runtime_policy.profile_selection = SINGLE_PRIMARY`, select exactly one primary; matching conditional supplements remain separate. Otherwise merge compatible matching requirements, never contradictory shot definitions.

`bootstrap_policy` may declare `GEN_ONLY`, required bootstrap IDs and permitted fallback order. Bootstrapping availability is not the same as attaching every bootstrapped image to every call.

Approved `transports` retain source identity, checksum and approval provenance. Their kind is `ORIGINAL` or `APPROVED_TRANSPORT`; delivery-only or unverified generated derivatives are not authorized transport variants.

## Calibration and optional behavior

Use [calibration.schema.json](../schemas/calibration.schema.json). Profiles declare purpose, visible regions, authority assets, view matching, approval, generation eligibility and diagnostic-only status. Diagnostic eligibility is independent of ordinary generation eligibility for a shared underlying asset. Never feed a diagnostic-only board to the generator just because it exists in the inventory.

Subject validators report through generic V1/V2/V3 outcomes. Resolve required handler availability before generation. Hooks declare stage, required output kinds, handler/version, scope and mutation constraints under [the hook contract](hooks.md). Declare missing capabilities rather than inventing no-op implementations.

`runtime_policy` may supply ratio defaults, single-primary selection, bounded retry policy, route-specific gates, a continuity limit, construction stages and external-role extensions. Extensions use `extension:<name>` and an explicit non-identity influence definition. Do not convert pack-defined policy into a hard-coded subject exception in the core.

`delivery.policies` constrain derivatives from accepted clean masters. Optional calibration, custom hooks, validators, or special delivery rules need not exist for every subject class. Preview/diagnostic presentation does not create final clean-master authority.

## Examples and validation

The [human](fixtures/human.yaml), [pet](fixtures/pet.yaml), and [virtual character](fixtures/virtual-character.yaml) fixtures share this contract. Their locators, checksums and hook handles are explicitly test-only declarations, not actual image assets or real-subject approvals.

Use [contract tools](contract-tools.md) to validate schema, duplicate IDs and cross-references. Schema-valid data can still be semantically contradictory or unavailable; Gen Mode must resolve those dependencies before execution.
