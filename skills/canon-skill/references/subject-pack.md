# Subject Pack contract 0.1

A Subject Pack defines durable subject truth and subject-owned capabilities. Canon Skill consumes it without assuming a human, animal, robot, product, or any mandatory anatomy.

## Required normal form

```yaml
subject:
  id: subject-owned-id
  type: subject-owned-class
canon:
  written_authority: []
  invariant_groups: []
references:
  inventory: []
  profiles: []
  bootstrap_policy: {}
calibration:
  enabled: false
  profiles: []
validators:
  identity: []
  structure: []
  local_quality: []
postprocess:
  hooks: []
delivery:
  policies: []
```

This is a field-shape example, not an executable pack with sufficient evidence. Validate resolved data with the [Subject Pack schema](../assets/schemas/subject-pack.schema.json). Optional `schema_version: "0.1"`, `runtime` policies and `extensions` are supported. Unsupported fields must not be silently ignored by an adapter.

A consumer may normalize its own entry manifest and current source metadata into this form. Keep a hash/revision over every consumed authority source. Do not duplicate mutable identity facts in the generic skill or use an unversioned URL as immutable provenance.

## Subject and written Canon

`subject.id` is stable; `subject.type` is descriptive, not a switch for mandatory body parts. `written_authority` entries identify source, id and scoped invariant groups, with optional inline facts. The consumer resolves authoritative sources and any conflicts before execution.

`invariant_groups` contain arbitrary ids, classes, regions and constraints. Generic classes include identity, structure, surface, silhouette, symbol and material; additional classes remain subject-owned. Optional `final_only` describes a construction-stage timing requirement, not an exemption from final Canon.

## References

The [reference schema](../assets/schemas/references.schema.json) requires each inventory item to declare id, asset locator, authority, views, covered invariant groups in `visible_regions`, `generation_eligible` and `diagnostic_only`. `CANONICAL_VISUAL` and `APPROVED_CALIBRATION` are distinct. Diagnostic-only items are never generation inputs.

Reference profiles match generic shot `view`, `framing` and `operation` using `match.views`, `match.framing` and `match.operations`. They declare `require.invariant_groups`, optional `require.assets`, and preferred assets. Required assets are hard constraints; preferences are tie-breaks. An adapter may add explicit shot-level `required_asset_ids` for declared matching-view or conditional support, with provenance for that selection.

Select the smallest adequate subset subject to all hard constraints. `runtime.defaults.profile_selection: EXPLICIT_SINGLE` requires one resolved `shot.reference_profile`; this forbids unintentional union of multiple primary profiles. Without that policy, compatible matching requirements may be combined. Unknown profiles/groups block rather than weaken coverage.

`bootstrap_policy` describes authorized session transport preparation. It never means all bootstrapped assets belong in every call. Optional `provenance` records source hashes and approved transport variants; see [transport](transport.md). A transport derivative can carry an authority id without becoming a new identity authority.

## Calibration

The [calibration schema](../assets/schemas/calibration.schema.json) defines enabled status plus profiles with id, purpose, visible regions, authority assets, generation eligibility and diagnostic-only status. The consumer owns view labels and approval evidence. Canon Skill does not interpret subject-specific calibration numbers.

Approved matching-view calibration supplements Canon within its regions. A body/structure authority does not gain identity authority over incidental features visible in it. Distinct generated views have their own approval workflow; crops/boards are deterministic diagnostic derivatives where required by policy.

## Validators and hooks

Pack validators reference explicitly registered host implementations or inspectable subject-owned instructions. Declare id, layer/scope, `required_for`, checks and failure mapping where needed. The host adds the generic V1/V2/V3 checks; empty custom lists never mean skip core validation.

Hooks declare id, lifecycle stage, `required_for`, and optionally handler, deterministic status, order, scope, parameters and `checks_before`. Resolve them before execution using [the hook lifecycle](hooks.md). A handler locator is not authority to execute arbitrary code. Required missing hooks block.

## Optional runtime policy

`runtime.defaults` carries subject-owned defaults such as ratio and single-primary-profile selection. `runtime.gates` declares approval scope, selectors and phase. `runtime.retry` may narrow automatic hard-reset recovery to zero for particular routes; it cannot expand the cap beyond one. `runtime.external_reference` may declare approved non-identity fallback dimensions and aliases. `runtime.transport` defines authorized transport variants, bootstrap and recovery policy.

`runtime.construction` may define temporary intermediates, deferred groups, pre-finalization checks and required finalizers. Resolve this into the packet's `construction_policy` and `validation_phases`; do not move final-only invariants into passed state before finalization. A temporary scaffold or feature-free base remains construction evidence, never continuity or final delivery.

Policy interpretation is performed by the authorized host/consumer adapter and frozen into the packet. A policy cannot bypass Canon, host safety, required approval or provenance. Unsupported required policy yields `BLOCKED`, not optimistic execution.

## Delivery and variability

`delivery.policies` defines subject-specific permitted outputs, mandatory delivery hooks, marks and derivative constraints. Delivery QA is separate from master acceptance. A pack may have no custom hooks, calibration, validators or export policy; feature-detect rather than assume all subjects share capabilities.

The same normal form describes [Human](fixtures/human.yaml), [Pet](fixtures/pet.yaml) and [Virtual](fixtures/virtual-character.yaml) fixtures. Their `fixture://` assets and validator ids are illustrative, not real image inputs or registered live implementations. They are never a substitute for real-consumer acceptance.

## Other data contracts

Use the [runtime-state schema](../assets/schemas/runtime-state.schema.json), [packet schema](../assets/schemas/generation-packet.schema.json) and [result schema](../assets/schemas/result.schema.json) with this pack. Schema `$id` values under `schemas.canon-skill.invalid` are local-registry identifiers, not hosted endpoints. Register all six schema resources locally; no network schema retrieval is required.
