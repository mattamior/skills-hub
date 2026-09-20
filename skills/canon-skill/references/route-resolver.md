# Route Resolver

Route Resolver chooses the v1 runtime route before image roles, external-reference routing, or evidence planning. A route identifies the workflow context; it does not decide which image is authoritative.

## Route set

The v1 routes are fixed:

- `SERIES` — create or update a multi-shot series or series-wide specification.
- `EXISTING_SERIES_SHOT` — operate on a named shot already present in `shot_registry`.
- `STANDALONE_SHOT` — create or operate on one shot that is not part of a registered series.
- `PREVIEW_ONLY` — produce or update preview material without promoting it to a final clean master.
- `CURRENT_SHOT_OPERATION` — operate on the currently selected shot without requiring the principal to repeat its identifier.
- `CALIBRATION` — run an explicit calibration or diagnostic workflow declared by the Subject Pack.

Do not introduce new routes merely to encode a backend feature, image role, validator result, or subject-specific concept.

## Inputs

Resolve from explicit task language and session state:

```yaml
current_subject:
shot_registry:
selected_shot:
current_revision:
series_lock:
preview_gate:
identity_gate:
explicit_operation:
explicit_shot_id:
explicit_series_intent:
explicit_preview_intent:
explicit_calibration_intent:
```

An image attachment by itself does not establish the route. Route selection uses task semantics and registered state, then Image Role Resolver determines what attached images mean.

## Resolution precedence

Apply these rules in order:

1. Choose `CALIBRATION` only when the task explicitly requests calibration or a declared calibration operation. Never infer calibration from an unusual view or a low-confidence generation.
2. Choose `CURRENT_SHOT_OPERATION` when the principal explicitly operates on the selected current shot, such as retrying, revising, refining, editing, validating, or delivering it without naming another shot.
3. Choose `EXISTING_SERIES_SHOT` when the principal names a shot identifier that exists in `shot_registry`, even if a preview image for that shot is also attached.
4. Choose `PREVIEW_ONLY` when preview output is explicitly requested and no current-shot or named existing-shot operation takes precedence.
5. Choose `SERIES` when the task creates, revises, or manages multiple shots or series-wide locks.
6. Choose `STANDALONE_SHOT` for a single non-series shot after the earlier cases are excluded.

If two earlier rules both appear applicable, prefer the one tied to the more explicit registered target. Do not use image recency or attachment order as a tiebreaker.

## Existing-shot semantics

A request such as "generate B3" resolves to `EXISTING_SERIES_SHOT` when `B3` is present in `shot_registry`.

A preview image associated with B3 remains a `PREVIEW_SHOT_REFERENCE`. The route does not convert that preview into an edit target or an implicit upscale source.

A request such as "retry this" may resolve to `CURRENT_SHOT_OPERATION` only when `selected_shot` is unambiguous. Otherwise stop with `SPEC_UNRESOLVED` instead of guessing which shot "this" means.

## Preview semantics

`PREVIEW_ONLY` is a delivery-stage limitation, not a lower canon standard. Preview work still respects canonical identity, structure, external-reference roles, and series locks appropriate to the preview.

Preview output cannot become an accepted clean master or continuity auxiliary without a later final-generation path and validation.

## Calibration semantics

`CALIBRATION` requires:

- a Subject Pack with `calibration.enabled: true`;
- a matching declared calibration profile or an explicitly supported generic calibration operation;
- any required authority assets.

Diagnostic-only calibration may inspect or compare evidence but must not be passed to generation when its profile has `generation_eligible: false`.

If calibration is requested but the pack does not support it, return `BLOCKED` with `SPEC_UNRESOLVED` or the more specific missing-dependency code available to the caller.

## Output contract

Route Resolver produces a stable routing record:

```yaml
route: EXISTING_SERIES_SHOT
operation: GENERATE
series_id: series-01
shot_id: B3
target_revision: 2
required_gates: [identity_gate, preview_gate]
reason:
  source: explicit_shot_id
  evidence: B3 exists in shot_registry
```

The `reason` is runtime provenance, not prompt prose. It should make conflicts auditable.

Route Resolver may identify required gates, but it does not satisfy them, select image roles, or choose canonical evidence.

## Block rather than reinterpret

Return `SPEC_UNRESOLVED` when the task cannot be mapped to one route without inventing a target.

Do not repair ambiguity by:

- treating the newest image as the current shot;
- assuming a preview image is a final shot;
- turning a named shot into a standalone shot because its clean master is missing;
- choosing calibration because canonical evidence is weak;
- creating a new series entry from an unknown identifier without explicit intent.
