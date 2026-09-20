# Result Model

Every generation or edit attempt receives exactly one top-level runtime classification:

```text
ACCEPT
HARD_RESET
RETRY_REQUIRED
REFINE_ELIGIBLE
BLOCKED
```

The classification is deterministic from required dependencies and validator outcomes. It is not a subjective quality score.

## Classification precedence

Apply this precedence:

```text
BLOCKED
  >
HARD_RESET
  >
RETRY_REQUIRED
  >
REFINE_ELIGIBLE
  >
ACCEPT
```

The precedence is logical, not an authority ranking. It prevents a lower-severity condition from masking a more fundamental failure.

## ACCEPT

Use `ACCEPT` only when:

- all required dependencies and gates are satisfied;
- V1 has no hard failure;
- V2 has no operation failure;
- no required local defect remains;
- all required post-generation and pre-validation hooks have completed successfully;
- the exact candidate being accepted is the one that was validated.

An accepted result may be promoted from `CLEAN_MASTER_CANDIDATE` to `ACCEPTED_CLEAN_MASTER`.

Acceptance does not make the image Subject Canon. It may become continuity auxiliary evidence only through the continuity-admission contract.

## HARD_RESET

Use `HARD_RESET` only for:

```text
WRONG_SUBJECT_IDENTITY
MAJOR_STRUCTURAL_DRIFT
MAJOR_ANATOMY_OR_GEOMETRY_FAILURE
EXTERNAL_IDENTITY_CONTAMINATION
```

The failing result is discarded as a continuity, refinement, or identity source.

A `HARD_RESET` may trigger one automatic fresh retry under [the recovery contract](recovery.md). The fresh retry reuses frozen packet semantics and starts again from its authorized canonical, external, continuity, and edit-target inputs. It must not use the failed result as a new reference.

Do not broaden `HARD_RESET` to cover camera, pose, composition, edit-contract, or ordinary local-quality failures.

## RETRY_REQUIRED

Use `RETRY_REQUIRED` when the canonical subject and major structure are basically correct but V2 shows that the operation did not execute as frozen.

Examples include:

- wrong camera or view;
- wrong pose;
- wrong composition or framing;
- shot geometry mismatch;
- external role not followed;
- preserve constraint violated without major canonical drift;
- edit contract not followed;
- wrong aspect ratio;
- series consistency miss.

`RETRY_REQUIRED` never causes an automatic retry.

The principal or an explicitly authorized controller may later request `RETRY`, which reuses the same packet semantics, or `REVISE`, which changes authorized semantics and freezes a new packet.

The failed result does not become continuity evidence or a clean master.

## REFINE_ELIGIBLE

Use `REFINE_ELIGIBLE` only when:

- V1 confirms canonical identity and major structure;
- V2 confirms the requested shot/operation;
- remaining defects are bounded and local.

The result remains a `CLEAN_MASTER_CANDIDATE`, not an accepted clean master.

A refinement must preserve every V1/V2-passed scope and target only the declared local defects. Refinement is a new edit/generation attempt with explicit preserve constraints and must be revalidated before acceptance.

A refine-eligible candidate cannot enter continuity until a later result reaches `ACCEPT`.

## BLOCKED

Use `BLOCKED` when execution or trustworthy validation cannot proceed because a required dependency is unavailable or unresolved.

Baseline codes include:

```text
SPEC_UNRESOLVED
SUBJECT_PACK_UNAVAILABLE
CANONICAL_EVIDENCE_UNAVAILABLE
EDIT_TARGET_UNAVAILABLE
PREVIEW_REFERENCE_UNAVAILABLE
GATE_NOT_SATISFIED
VALIDATOR_UNAVAILABLE
REQUIRED_HOOK_FAILED
PROVENANCE_UNVERIFIED
```

`BLOCKED` is not a failed generation quality judgment. It means the runtime lacks the authority or dependency needed to continue safely.

Do not automatically retry a blocked state. Resolve the dependency first.

## Mixed failures

If one result has multiple failures, classify using the precedence above.

Examples:

- identity contamination plus wrong camera -> `HARD_RESET`;
- correct subject plus wrong pose plus edge artifact -> `RETRY_REQUIRED`;
- correct subject and shot plus edge artifact -> `REFINE_ELIGIBLE`;
- validator unavailable even if the image looks correct -> `BLOCKED`.

Record all observed reasons even when one higher-precedence class controls recovery.

## Result record

Each attempt should produce:

```yaml
result_id:
packet_revision:
attempt_index:
classification:
reason_codes: []
validator_report:
hook_execution_record:
candidate_provenance:
automatic_action:
```

`automatic_action` is one of `NONE` or `FRESH_RETRY_ONCE`. Result classification itself never mutates the frozen Generation Packet.
