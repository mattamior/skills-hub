# Validator Model

Validation runs against the exact result produced by one frozen Generation Packet revision. Validators inspect the output; they do not rewrite the packet, reinterpret evidence roles, or silently change the requested shot.

The runtime uses three ordered layers:

```text
V1 — CANON / STRUCTURE
V2 — OPERATION COMPLIANCE
V3 — LOCAL QUALITY
```

Subject Pack validators may extend any layer, but every validator must report through the generic outcome contract.

## Validation inputs

A validation run receives:

```yaml
result:
generation_packet:
subject_pack_revision:
canonical_evidence:
external_evidence:
continuity_evidence:
edit_contract:
series_lock:
hook_execution_record:
```

Validate the actual post-`POST_GENERATION` candidate that would become the clean master. Never validate a delivery derivative in place of the candidate.

If a required validator, required authority asset, or required hook result is unavailable, stop with a blocked outcome rather than pretending the corresponding check passed.

## Validator outcome contract

Each validator returns one outcome:

```text
PASS
HARD_FAIL
OPERATION_FAIL
LOCAL_DEFECT
BLOCKED
```

and a structured record such as:

```yaml
validator_id: primary-identity
layer: V1
outcome: HARD_FAIL
reason_code: WRONG_SUBJECT_IDENTITY
scope: [primary-identity]
evidence:
  - canonical-front
confidence: high
notes:
  - result depicts a different primary subject
```

A validator must report only within its declared scope. A local-quality validator cannot promote a structural failure to `PASS`, and an operation validator cannot redefine canonical identity.

## V1 — Canon / Structure

V1 answers whether the result is still the intended canonical subject with the required major structure.

Check the applicable Subject Pack invariants, including:

- canonical primary identity;
- fixed structural invariants;
- major anatomy or geometry;
- silhouette or proportion requirements when canon-bearing;
- subject-specific invariant groups;
- external identity contamination.

Use `HARD_FAIL` only for failures severe enough to invalidate the candidate as this subject or its required major structure.

The canonical hard-failure reason codes are:

```text
WRONG_SUBJECT_IDENTITY
MAJOR_STRUCTURAL_DRIFT
MAJOR_ANATOMY_OR_GEOMETRY_FAILURE
EXTERNAL_IDENTITY_CONTAMINATION
```

Do not use `HARD_FAIL` for a small, bounded defect when overall identity and major structure remain correct. A missing small canonical surface detail, minor edge defect, or localized rendering flaw may be `LOCAL_DEFECT` if it can be repaired without redesigning identity, shot geometry, or structure.

V1 must run before V2 and V3 classification is allowed to control recovery.

## V2 — Operation Compliance

V2 answers whether the frozen operation was actually executed as specified.

Check applicable fields such as:

- camera and view;
- pose or articulated configuration;
- composition and framing;
- shot geometry;
- edit contract;
- external-reference role execution;
- preserve constraints;
- aspect ratio;
- series locks and series consistency;
- requested object, environment, wardrobe, or secondary-subject behavior.

Use `OPERATION_FAIL` when the subject is fundamentally correct but the requested operation is not.

Typical reason codes include:

```text
CAMERA_NONCOMPLIANCE
POSE_NONCOMPLIANCE
COMPOSITION_NONCOMPLIANCE
SHOT_GEOMETRY_NONCOMPLIANCE
EDIT_CONTRACT_FAILURE
REFERENCE_ROLE_EXECUTION_FAILURE
PRESERVE_CONSTRAINT_FAILURE
ASPECT_RATIO_FAILURE
SERIES_CONSISTENCY_FAILURE
```

A V2 failure must not be relabeled as `HARD_FAIL` merely because another sample might execute the shot better.

## V3 — Local Quality

V3 runs only after Canon/Structure and operation compliance are good enough to preserve.

Check localized quality defects such as:

- small rendering artifacts;
- edge or masking defects;
- hands, paws, appendages, or mechanical details when they are local rather than major structural failures;
- wardrobe or surface defects;
- background defects;
- unwanted text or marks;
- local realism problems;
- small canonical details whose repair does not change identity or shot semantics.

Use `LOCAL_DEFECT` for bounded issues that can be refined while preserving all passed V1/V2 constraints.

Typical reason codes include:

```text
LOCAL_ARTIFACT
EDGE_DEFECT
LOCAL_APPENDAGE_DEFECT
SURFACE_DEFECT
BACKGROUND_DEFECT
UNWANTED_TEXT
LOCAL_REALISM_DEFECT
SMALL_CANONICAL_DETAIL_DEFECT
```

Do not use V3 refinement to hide a V1 or V2 failure.

## Subject Pack validators

A Subject Pack may declare additional validators in its `identity`, `structure`, or `local_quality` lists.

Each custom validator must declare or resolve to:

```yaml
id:
layer: V1 | V2 | V3
scope: []
required_for: []
failure_mapping:
  hard: []
  operation: []
  local: []
```

The implementation may understand subject-specific semantics. Canon Skill understands only the reported generic layer, scope, outcome, and reason code.

If a custom validator introduces a new reason code, it must map to one of the generic outcome classes without adding a subject-specific result class.

## Validation aggregation

Aggregate in strict order:

1. any unresolved required dependency -> `BLOCKED`;
2. any valid V1 `HARD_FAIL` -> hard-reset candidate;
3. after V1 has no hard failure, any V2 `OPERATION_FAIL` -> retry-required candidate;
4. after V1/V2 pass, any V1 or V3 `LOCAL_DEFECT` -> refine-eligible candidate;
5. otherwise -> accept candidate.

Warnings may be recorded, but they cannot override a failing required validator.

The final runtime result class is defined by [the result model](result-model.md).
