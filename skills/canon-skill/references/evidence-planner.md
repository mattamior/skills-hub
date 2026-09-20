# Evidence Planner

Evidence Planner selects the minimum role-relevant canonical evidence required for the resolved route, shot, operation, and Subject Pack. It also carries already-routed external and continuity evidence into separate packet channels.

The planner answers "what evidence does this shot actually need?" It must not attach the entire Subject Pack by default.

## Inputs

Consume only resolved inputs:

```yaml
subject_pack:
route:
operation:
series_lock:
shot:
edit_contract:
image_role_bindings:
external_reference_plan:
continuity_candidates:
```

The shot specification should expose generic requirements such as view, framing, visible regions, and required invariant groups. Evidence Planner must not infer human-specific anatomy or feature names.

## Required canonical coverage

Build `required_invariant_groups` from:

1. invariant groups explicitly required by the shot;
2. canon-bearing groups locked by `series_lock`;
3. groups visible in the output whose stability is required by the effective spec;
4. groups intersecting changed or risk-adjacent regions of an edit;
5. any Subject Pack profile requirements for the matched view and framing.

A group may be required for validation even when the edit contract says its pixels should remain unchanged.

Do not allow external or continuity evidence to remove a required canonical group.

## Candidate filtering

Canonical candidates come from Subject Pack reference inventory and approved calibration profiles.

Exclude from generation selection when:

- `generation_eligible: false`;
- `diagnostic_only: true`;
- the asset does not cover a required group and adds no declared operation value;
- its view is incompatible with a stricter matching-view requirement;
- its provenance cannot be resolved.

Diagnostic-only evidence may still be carried separately for validation when the applicable validator declares it.

## Profile matching

Match `references.profiles` against the resolved shot's generic attributes such as:

```yaml
view:
framing:
visible_regions:
operation:
```

A matching profile may:

- require invariant groups;
- prefer specific assets;
- encode matching-view authority needs.

If multiple profiles match, combine required groups, then select the smallest asset set that covers them without violating profile constraints.

## Deterministic selection

Select the minimum number of eligible assets that covers all required canonical groups.

When multiple subsets have equal size, break ties in this order:

1. exact view match;
2. asset explicitly preferred by the matched profile;
3. higher evidence authority;
4. narrower role-relevant coverage over unrelated broad coverage;
5. stable asset identifier ordering.

This makes evidence selection auditable and avoids "send every reference" behavior.

## Calibration evidence

Approved calibration may be selected when:

- the Subject Pack declares calibration enabled;
- a matching calibration profile covers a required region or diagnostic need;
- the asset is eligible for the intended use.

Matching-view approved calibration may supplement canonical visuals. It does not override contradictory written canon or canonical visuals.

Diagnostic-only calibration remains outside generation transport.

## External evidence

Carry External Reference Router output as `external_evidence` without changing roles or authority.

External evidence can satisfy operation requirements such as camera, pose, composition, lighting, wardrobe, environment, object, or secondary-subject definition.

It cannot satisfy missing primary-subject canonical identity or structure.

## Continuity evidence

Select continuity only from `continuity_candidates` that are accepted clean masters and relevant to the current series or shot.

Prefer no continuity evidence when canonical evidence and the effective spec are sufficient. Include continuity when it materially supports accepted series consistency such as environment state, wardrobe state, camera language, or prior accepted staging.

Continuity always remains a separate packet channel:

```text
canonical_evidence
external_evidence
continuity_evidence
```

Never collapse these arrays into one unordered reference list.

## Edit evidence

For an edit, preserve the `EDIT_TARGET` separately from canonical evidence.

The planner must include canonical evidence needed to validate canon-bearing visible regions and any region at risk from the edit. A background-only edit may use a minimal identity reference rather than a full body/reference inventory when the Subject Pack profile allows it.

The edit target itself does not become canonical evidence merely because it already depicts the subject.

## Planning output

Produce a plan with explicit coverage:

```yaml
required_invariant_groups:
  - primary-identity
matched_profiles:
  - front-closeup

canonical_evidence:
  - id: canonical-front
    authority: CANONICAL_VISUAL
    covers: [primary-identity]
    selected_because: exact-view minimal coverage

external_evidence:
  - id: external-pose
    roles: [POSE]

continuity_evidence: []

coverage:
  primary-identity: canonical-front

uncovered: []
risk_guards:
  - NO_EXTERNAL_IDENTITY_TRANSFER
```

The selection rationale is runtime provenance and should be available to validation and debugging.

## Block on missing coverage

If any required canonical group remains uncovered, stop with `CANONICAL_EVIDENCE_UNAVAILABLE`.

Do not recover by:

- promoting an external reference to canonical identity;
- using an unverified generated image;
- using preview pixels as identity authority;
- treating continuity as a replacement for canon;
- dropping the invariant from the effective spec;
- silently switching to a different route.

A later principal-authorized revision may change the shot, Subject Pack, or required invariants and then re-run Evidence Planner.
