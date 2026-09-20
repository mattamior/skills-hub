# Route Resolver

Keep the six routes: `SERIES`, `EXISTING_SERIES_SHOT`, `STANDALONE_SHOT`, `PREVIEW_ONLY`, `CURRENT_SHOT_OPERATION`, `CALIBRATION`. A route is workflow context, not an evidence rank.

## Resolve explicit intent

Explicit calibration selects CALIBRATION only when the pack supports the requested operation. A named existing shot selects EXISTING_SERIES_SHOT. An operation on an unambiguously selected current shot selects CURRENT_SHOT_OPERATION. Explicit preview-only intent otherwise selects PREVIEW_ONLY; multi-shot/series intent selects SERIES; a complete single non-series request selects STANDALONE_SHOT.

A named target overrides a conflicting implicit current selection. Unknown shot IDs do not create new shots without explicit intent. An attachment by itself is not a route or a current-shot selection. Ambiguous 'retry this' is `SPEC_UNRESOLVED`.

## Route versus frozen operation

CURRENT_SHOT_OPERATION is a command-dispatch context. A RETRY dispatched through it executes the original frozen packet's route and operation unchanged; do not rewrite packet.route merely to reflect the command. A semantic REVISE re-resolves affected decisions and freezes a new revision.

'Generate B3' executes B3's registered definition. Its preview is geometry evidence, not an implicit edit/upscale source. A preview request for a named shot may retain EXISTING_SERIES_SHOT with output_kind PREVIEW; output kind controls promotion eligibility independently of route.

## Gates and execution

SERIES coordinates separately frozen identity checks, previews, and final targets. Required gates are pack- and target-scoped; do not rerun a satisfied gate for an unchanged scope or bypass it due to an attachment. A generic 'continue' is not an unrequested preview selection.

PREVIEW_ONLY respects Canon and role isolation but cannot create final-master continuity. CALIBRATION uses pack-specific views and Principal gates, not the ordinary series preview workflow. Pack calibration policy may disable automatic retries; do not reopen already approved views without a task requiring it.

Record route, operation, output kind, target ID/revision, required gates and the explicit resolution basis. Do not invent dozens of routes to encode individual subject features or backend capabilities.
