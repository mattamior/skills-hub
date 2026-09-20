# Result Model

Each actual attempt or blocked execution receives exactly one top-level class: `ACCEPT`, `HARD_RESET`, `RETRY_REQUIRED`, `REFINE_ELIGIBLE`, or `BLOCKED`. A classifier consumes observed validation and dependencies; it is not itself visual perception.

## Precedence

```text
BLOCKED > HARD_RESET > RETRY_REQUIRED > REFINE_ELIGIBLE > ACCEPT
```

This is failure-handling precedence, not evidence authority. Keep all observed reasons even when one class controls the next action. Actual missing dependencies outrank apparent visual success. Later checks deliberately unrun after a decisive earlier failure are not invented dependency failures.

## ACCEPT

All applicable Canon/structure, operation, local quality, required hooks and required approval dependencies must pass for the exact candidate. Master promotion additionally requires eligible output provenance and byte/packet identity.

`ACCEPT` for a preview or diagnostic is limited to that artifact's purpose. It must not mint an accepted clean master. A post-validation Principal gate can leave an otherwise visually valid candidate awaiting approval; until that gate is satisfied, the dependent acceptance/promotion remains blocked. The frozen gate declaration is not mutated by the later approval receipt.

## HARD_RESET

Use only `WRONG_SUBJECT_IDENTITY`, `MAJOR_STRUCTURAL_DRIFT`, `MAJOR_ANATOMY_OR_GEOMETRY_FAILURE` or `EXTERNAL_IDENTITY_CONTAMINATION`. Discard the failed result as an identity, continuity, preview, edit or refinement source.

A packet may permit at most one automatic fresh retry after its initial hard failure. Subject policy may narrow that allowance to zero. Camera, pose, composition and ordinary local defects are not hard-reset reasons.

## RETRY_REQUIRED

The subject is fundamentally correct but the frozen operation failed: camera, pose, composition, roles, shot geometry, preserve scopes, edit contract, ratio or series consistency. Never retry automatically. A later explicit RETRY uses the same packet; changing intended semantics requires REVISE. This failed output is not a clean master or continuity input.

## REFINE_ELIGIBLE

Identity/major structure and operation are correct, with only bounded local defects remaining. The result remains a candidate. An explicit refinement may bind it as an edit target with all passed V1/V2 scopes protected. The new result requires complete applicable revalidation before acceptance; the refine-only candidate cannot enter continuity.

## BLOCKED

A required dependency or trustworthy validation is unavailable. Baseline reasons include `SPEC_UNRESOLVED`, `SUBJECT_PACK_UNAVAILABLE`, `CANONICAL_EVIDENCE_UNAVAILABLE`, `EDIT_TARGET_UNAVAILABLE`, `PREVIEW_REFERENCE_UNAVAILABLE`, `GATE_NOT_SATISFIED`, `VALIDATOR_UNAVAILABLE`, `REQUIRED_HOOK_FAILED`, `PROVENANCE_UNVERIFIED`, `TRANSPORT_UNAVAILABLE` and `BACKEND_CAPABILITY_UNAVAILABLE`.

Do not escape a blocker by weakening evidence, skipping required hooks, inventing approval or sampling again. Delivery can be blocked while its source master remains accepted; report the scope rather than retroactively changing master truth.

## Result record

Use the [result schema](../assets/schemas/result.schema.json): result id, packet revision, attempt index, classification, reason codes, validator and hook records, candidate provenance and automatic action (`NONE` or `FRESH_RETRY_ONCE`). Result metadata never changes the frozen packet retrospectively. Follow [recovery](recovery.md) and [continuity](continuity.md) for the allowed next transitions.
