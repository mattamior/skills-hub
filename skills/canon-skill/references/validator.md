# Validator Model

Validate the exact candidate produced under one frozen packet. Validators inspect outputs; they do not modify the specification, relax Canon or silently reinterpret reference roles.

## Inputs and phases

Resolve core and required subject validators before execution. Retain the candidate's byte hash, packet hash, evidence scopes, edit contract, series lock and hook records. A missing required validator, authority, hook or necessary approval is a blocked dependency, not a visual pass.

For a declared construction intermediate, run its explicit pre-finalization checks against that stage's contract. A final-only invariant may be deferred, not passed or discarded. After required finalizers and PRE_VALIDATION processing, run the complete applicable V1/V2/V3 validation on the exact candidate. Do not validate a marked delivery derivative in place of its master.

## V1 — Canon and Structure

Check canonical identity, fixed structural invariants, major anatomy/geometry, canon-bearing silhouette/proportions and external identity contamination. Subject Packs define the regions and feature semantics.

Only these severe failures map to `HARD_FAIL`:

```text
WRONG_SUBJECT_IDENTITY
MAJOR_STRUCTURAL_DRIFT
MAJOR_ANATOMY_OR_GEOMETRY_FAILURE
EXTERNAL_IDENTITY_CONTAMINATION
```

A bounded small canonical surface defect can be `LOCAL_DEFECT` when identity and major structure remain intact. Do not classify missing small details as hard resets merely because a fresh sample might fix them, or hide major geometry failures as minor local defects.

## V2 — Operation Compliance

Check the frozen camera, pose/configuration, composition, framing, shot geometry, edit contract, external-role execution, preserve scopes, aspect ratio and series consistency. A fundamentally correct subject with a wrong operation produces `OPERATION_FAIL`, not a hard reset.

Typical reasons are `CAMERA_NONCOMPLIANCE`, `POSE_NONCOMPLIANCE`, `COMPOSITION_NONCOMPLIANCE`, `SHOT_GEOMETRY_NONCOMPLIANCE`, `EDIT_CONTRACT_FAILURE`, `REFERENCE_ROLE_EXECUTION_FAILURE`, `PRESERVE_CONSTRAINT_FAILURE`, `ASPECT_RATIO_FAILURE` and `SERIES_CONSISTENCY_FAILURE`.

## V3 — Local Quality

Check bounded artifacts, edges, local appendage/mechanical details, surface/wardrobe defects, backgrounds, unwanted text and local realism. Use `LOCAL_DEFECT` only where a bounded correction can preserve all passed identity, structure and operation scopes. V3 must not conceal a V1/V2 failure.

## Report contract

Each observation includes validator id, layer, scope, outcome, reason, supporting evidence and explicit uncertainty. Allowed outcomes are `PASS`, `HARD_FAIL`, `OPERATION_FAIL`, `LOCAL_DEFECT` and `BLOCKED`. Custom reasons must map to those generic outcomes. An optional validator's observed severe failure must not be silently ignored.

Do not infer confidence or report PASS without inspecting the required evidence. Duplicate ids, undeclared validators, invalid layer/outcome combinations and missing required checks cannot produce vacuous acceptance.

## Aggregation and short circuits

Unresolved real dependencies take precedence. Otherwise, after all required V1 observations exist, any valid V1 hard failure controls the result. Later layers may remain deliberately unrun after that decisive failure. With V1 non-decisive, require V2 observations; an operation failure controls recovery and may short-circuit V3. Acceptance or local refinement eligibility requires the remaining applicable checks.

A deliberately short-circuited later layer is different from an unavailable validator. Record why it was not run; never fabricate PASS entries. The result mapping is in [Result Model](result-model.md).

Any pixel mutation after validation creates a new candidate and requires revalidation. POST_VALIDATION bookkeeping cannot silently change accepted bytes. Delivery QA is separately scoped to derivatives.
