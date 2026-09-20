# Route Resolver

Resolve workflow context from current task semantics and registered session targets, before interpreting image roles. An attachment alone does not establish a route.

## Six routes

| Route | Purpose |
| --- | --- |
| `SERIES` | create or revise a multi-shot series or its shared specification |
| `EXISTING_SERIES_SHOT` | operate on an explicitly named registered shot |
| `STANDALONE_SHOT` | one complete non-series shot |
| `PREVIEW_ONLY` | produce preview material and stop before final generation |
| `CURRENT_SHOT_OPERATION` | operate on the unambiguous selected shot without repeating its id |
| `CALIBRATION` | explicitly requested, Subject Pack-supported calibration |

## Resolution order

Explicit calibration is first. Next resolve an explicitly named registered shot; it takes precedence over an implicit reference to the currently selected shot. Then resolve current-shot operations, explicit preview intent, series intent, and finally a single standalone shot.

An unknown named shot or an ambiguous 'retry this' is `BLOCKED / SPEC_UNRESOLVED`, not permission to select the newest image, create a hidden new shot or change to a standalone route. Calibration requires the pack's declared capability and applicable profile; do not infer calibration merely from unusual views or weak evidence.

## Operation and output kind

Record operation, target id/revision, series id, required gates and reason provenance with the route. Keep output kind and command semantics distinct. 'Generate B3' resolves a registered shot; its preview remains geometry evidence, not an upscale/edit source. An explicit edit of preview pixels may bind an edit target but remains preview-derived, not a final identity source.

An existing-shot operation reuses still-valid scoped approvals, but must not reuse approvals invalidated by a revision. A retry command can be resolved through the current-shot route while executing the original frozen packet unchanged. It does not mutate that packet's route or revision.

## Gates

Read gate policy from the Subject Pack and active specification. A new series may require identity-check approval, preview creation, then explicit shot selection. A standalone task is not silently expanded into a series. 'Continue' after a preview does not choose an unspecified cell.

Preview validity still requires Canon, operation and applicable quality checks, but preview acceptance never creates final-master provenance. Calibration may require clean-master-first Principal approval, deterministic diagnostics and board-last delivery; those are pack-owned policies, not generic calibration numbering.
