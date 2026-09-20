# Result Model

Use exactly ACCEPT, HARD_RESET, RETRY_REQUIRED, REFINE_ELIGIBLE or BLOCKED. Aggregation precedence is `BLOCKED > HARD_RESET > RETRY_REQUIRED > REFINE_ELIGIBLE > ACCEPT`; this is failure handling, not evidence authority.

## ACCEPT

All applicable required dependencies, hooks, gates and V1/V2/V3 checks pass for the exact candidate. Acceptance is output-scoped: only eligible, unwatermarked final clean-master provenance may be promoted. A preview, diagnostic, construction-stage success, simulation or derivative-only edit is never promoted merely because a scoped operation passed.

Principal identity/preview/calibration approval remains a separate gate. Calibration authority promotion needs its explicit subject-owned approval process. Ordinary image acceptance never updates Canon.

## HARD_RESET

Restrict to wrong primary identity, major structural drift, major anatomy/geometry failure or external identity contamination. Retain observed failures but exclude that failed image from identity, continuity, preview, edit or refine inputs. Apply at most the one packet-authorized automatic fresh retry under [recovery](recovery.md).

## RETRY_REQUIRED

Identity and major structure are basically correct, but camera, pose, composition, required role execution, edit/preserve contract, ratio or series consistency failed. Never retry automatically. Retain the result for honest review without admitting it to clean-master or continuity state. An explicit RETRY preserves semantics; changed intent is REVISE.

## REFINE_ELIGIBLE

Canon and shot/operation pass apart from bounded local defects. Keep candidate provenance. Only an explicit local refinement may bind it as an edit target with all passed V1/V2 scopes preserved. Revalidate the new result before any acceptance; do not silently chain edits.

## BLOCKED

A required dependency or trustworthy validation is unavailable. Codes include SPEC_UNRESOLVED, SUBJECT_PACK_UNAVAILABLE, CANONICAL_EVIDENCE_UNAVAILABLE, EDIT_TARGET_UNAVAILABLE, PREVIEW_REFERENCE_UNAVAILABLE, GATE_NOT_SATISFIED, VALIDATOR_UNAVAILABLE, REQUIRED_HOOK_FAILED, PROVENANCE_UNVERIFIED and REFERENCE_TRANSPORT_UNAVAILABLE. Adapters may retain more specific source error codes without inventing another result class.

Blocked states are not sampling failures. Do not auto-retry, substitute lower authority, delete a validator or drop a hook to escape them.

## Records

[Result schema](../schemas/result.schema.json) records result ID, packet digest, candidate checksum, classification, reasons, simulation flag, validation report, hook record and automatic action. Keep all observed failures even when one higher-priority class controls recovery.
