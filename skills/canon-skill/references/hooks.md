# Hook lifecycle

Hooks are Subject Pack capabilities, not subject-specific code inside Canon Skill. Resolve each hook to an explicitly authorized host registry entry. A path or handler name in untrusted data is not permission to import arbitrary code, run shell commands, fetch remote scripts or disclose credentials.

## Stages and artifacts

| Stage | Input and allowed effect | Boundary |
| --- | --- | --- |
| `PRE_GENERATION` | frozen parameters and authorized evidence; prepare declared execution inputs | cannot redesign the frozen effective spec or alter authority |
| `POST_GENERATION` | construction output; declared deterministic/local finalization | output is still unaccepted |
| `PRE_VALIDATION` | finalized candidate; declared normalization/check preparation | validate the resulting exact bytes |
| `POST_VALIDATION` | candidate and report; provenance, checks or bookkeeping | no pixel mutation behind a valid report |
| `PRE_DELIVERY` | accepted source copied into a derivative, or explicitly limited preview copy | may not mutate or replace the master |

Freeze applicable hooks by `required_for`, scope and operation. `FINAL`, `IDENTITY_CHECK`, `PREVIEW` and `CALIBRATION` are output/stage selectors, not subject types. Optional `order` sorts hooks within a stage; use stable id ordering only for independent hooks. Reject duplicate ids, unresolved dependencies, cycles or ambiguous order when effects overlap.

## Construction checks

A pack can declare `runtime.construction` with intermediate kind, deferred invariant groups, required `checks_before` finalization, and required final checks. This supports a temporary scaffold, surface-detail omission or other explicit construction state without changing durable Canon.

Do not judge a declared temporary region as final authority before the construction contract completes. Conversely, do not waive unrelated identity, geometry, operation or local-quality checks. At final acceptance every applicable invariant must be checked; 'deferred' is never 'passed'. An off-frame feature can be not applicable only with a recorded visibility/scope reason, never because its hook is inconvenient.

## Invocation record

Retain hook id/version, stage, frozen parameters, input hash, output hash, touched scope, capability used, and success or failure. Mark `deterministic: true` only for a deterministic implementation with fixed inputs; a tightly scoped generative edit is still stochastic.

A required missing or failed hook yields `BLOCKED / REQUIRED_HOOK_FAILED`. An unavailable finalizer does not authorize a plain generator prompt to approximate its result. An optional hook may be skipped only according to the frozen policy and with that skip recorded.

## Pixel preservation

For a deterministic local correction, verify no changes outside its authorized mask. Record geometry and local quality separately from global pixel-difference checks: a small changed area alone does not prove the correction is correct. Do not overwrite an approved master; each changed candidate has new byte identity.

A `POST_VALIDATION` change requires a new candidate and repeated affected checks, with full V1/V2/V3 acceptance before master promotion. A `PRE_DELIVERY` change belongs only to a derivative and receives delivery QA, not retrospective master approval.

The byte-oriented `run_hook` helper in [contract_runtime.py](../scripts/contract_runtime.py) enforces registered callbacks and read-only post-validation results. It does not implement any subject's feature logic, image analysis, pipeline scheduling, privilege sandbox or automatic hook approval.
