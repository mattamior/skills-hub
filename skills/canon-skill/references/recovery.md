# Recovery Model

Recovery changes execution state, not frozen meaning. The only automatic image-generation recovery is a single fresh retry after the initial HARD_RESET when the frozen policy permits it.

## Action table

| Result | Automatic generation | Reuse of result |
| --- | --- | --- |
| ACCEPT | none | eligible master only after verified promotion/admission |
| HARD_RESET | at most one fresh retry from the original packet | never as new evidence or edit base |
| RETRY_REQUIRED | none | not a clean master or continuity source |
| REFINE_ELIGIBLE | none | explicit bounded refinement edit target only |
| BLOCKED | none | resolve the dependency, not a new sample |

## One-safe-retry

The initial sample has attempt index 1 and packet-local hard-reset automatic retry count 0. On its HARD_RESET, a frozen allowance of 1 permits one fresh sample; an allowance of 0 forbids it. No allowance may exceed 1. Increment both retry count and the consumed automatic-hard-reset count before dispatch to avoid duplicate execution.

Reuse the same subject revision, effective spec, route, operation, shot, series lock, evidence bindings, preserve scopes, hooks, validators, gates and delivery policy. Vary only authorized backend randomness or same-payload transport details. Never attach the failed result as an identity, preview, continuity, edit or refinement input.

After that fresh sample is validated, stop automatic generation regardless of its result. ACCEPT may be promoted normally; every other result is reported without another automatic sample. A transport timeout with unknown job status is not proof that a generation failed; resolve its job/idempotency status before resubmission.

## Explicit operations

RETRY_REQUIRED needs an explicit Principal or authorized controller retry. Reusing the packet does not restore an already-consumed automatic allowance. A request to change camera, pose, framing, roles, evidence or another semantic field is REVISE and must replan, invalidate affected approvals and freeze a new revision.

REFINE_ELIGIBLE needs an explicit local correction contract and new candidate provenance. Preserve every passed V1/V2 scope; a resulting operation change is a new failure, not a successful refinement. Do not continue improving indefinitely without renewed bounded intent.

A new authorized semantic revision resets packet-local counters; changing only a revision label is not authorization to evade a retry cap. Fresh sessions do not automatically import old retry permissions or stale job handles.

## Preserve prior accepted state

A failed later candidate does not overwrite or demote an earlier accepted master. Clear or reject the current candidate pointer, retain its failure provenance separately, and keep the existing accepted master immutable. No rejected or refine-only result enters continuity.

Keep the last result id/classification, validation report, retry count and automatic-hard-reset count in session state. These records are audit evidence, never new Subject Canon.
