# Validator Model

Inspect the actual candidate produced by one frozen packet. A validator is not a prompt rewrite or a source of new Canon.

## Layers

V1 checks canonical identity, fixed structure, major anatomy/geometry, silhouette/proportion invariants and external identity contamination. Only WRONG_SUBJECT_IDENTITY, MAJOR_STRUCTURAL_DRIFT, MAJOR_ANATOMY_OR_GEOMETRY_FAILURE or EXTERNAL_IDENTITY_CONTAMINATION map to HARD_FAIL.

V2 checks camera, pose, composition, shot geometry, image/external roles, edit contract, preserved regions, ratio and series consistency. An operation miss with fundamentally correct identity is OPERATION_FAIL, not HARD_FAIL.

V3 checks bounded local artifacts, edges, surface/wardrobe/background defects, unwanted text, local realism and small appendage detail. Major anatomy or mechanical geometry failure belongs in V1, not a cosmetic refinement bucket.

Each required validator reports ID, layer, scope, outcome, reason and evidence. Outcomes are PASS, HARD_FAIL, OPERATION_FAIL, LOCAL_DEFECT or BLOCKED. Subject-owned validators extend declared scopes without changing the five result classes. Unknown, unavailable, duplicate or contradictory required reports fail closed.

## Candidate binding

Bind a complete report to packet digest, exact candidate checksum, hook record and resolved dependencies. Validate the post-finalization, unwatermarked candidate, not its delivery derivative. Any later pixel mutation requires new validation. Never infer visual PASS from a schema test, successful tool return or an image that was not inspected.

Construction prechecks may defer only the pack-declared groups at a non-final stage under [hook lifecycle](hooks.md). Such a precheck cannot produce final acceptance. Restore all final required invariants after finalization.

A small missing canonical detail may be LOCAL_DEFECT only when identity and major structure remain valid; it is never silently waived for final acceptance. Operation failures take precedence over local defects, hard failures over operation failures, and unresolved dependencies block trustworthy classification.

## Implementation boundary

The bundled helper aggregates externally supplied inspection evidence; it is not a visual identity/anatomy detector. The host must run real V1/V2/V3 inspection and resolve any Subject Pack validators before claiming a real result. See [Result Model](result-model.md).
