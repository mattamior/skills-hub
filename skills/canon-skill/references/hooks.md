# Hook Lifecycle

A Subject Pack owns hook implementation and subject-specific semantics. Canon Skill selects and invokes only resolved, authorized handlers; never evaluate code, shell commands or network instructions merely because they occur in a pack.

## Stages

| Stage | Permitted role | Boundary |
| --- | --- | --- |
| PRE_GENERATION | Capability, source, mask and declared preflight checks | No change to frozen semantic fields or unapproved input pixels |
| POST_GENERATION | Declared deterministic/local candidate finalization | Keep construction provenance; validate resulting pixels |
| PRE_VALIDATION | Final candidate preparation and read-only checks | Freeze exact candidate hash before full validation |
| POST_VALIDATION | Read-only audit or reporting | Any pixel mutation invalidates validation; never silently accept |
| PRE_DELIVERY | Derive final export from accepted master | Modify derivative only, never master or continuity |

Image preparation that changes reference pixels beyond already approved variants must be resolved before packet freeze. New crop/mask semantics are not a transport-only retry change.

## Declarations and execution records

Freeze hook ID, stage, handler/version, required output kinds, permitted scope, mutation flag, input/output provenance classes and preconditions. Choose applicable hooks before freeze. Record invocation order, input/output hashes, version, outcome, and actual execution evidence. Declaration-only fixtures do not supply handlers.

Execute in stage order, preserving declaration order within a stage. A handler must be deterministic for declared input and parameters when so required; use idempotency keys based on packet, attempt, hook and input hash. Do not apply a pigment, decal, watermark or similar transformation repeatedly to an already transformed result.

A missing required handler or failed required hook blocks acceptance. Optional absence must be recorded, not reported as a pass. PRE_DELIVERY failure blocks that delivery only; it does not retrospectively invalidate an unchanged accepted master.

## Construction-stage validation

A pack may declare a construction intermediate with temporarily deferred invariant groups, scoped precheck validators and required finalization hooks. Validate the non-deferred identity/structure and operation constraints before finalization. Do not try to repair a fundamental failure with a detail hook.

Only the explicitly declared construction checks may defer those groups. The intermediate cannot be accepted as a final clean master, continuity source or canonical authority. After finalization, run full V1/V2/V3 against final Canon with no implicit deferrals. A failed finalization remains blocked; removing the hook is not recovery.

A preview may deliberately stop at an authorized construction stage for shot selection. Its success remains preview-scoped and never promotes its temporary omissions into final Canon. Calibration may declare different construction/finalization and Principal-gate semantics without any named-subject branch in the runtime.
