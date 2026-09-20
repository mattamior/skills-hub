# Canon Skill Validation and Recovery Cases

Use these cases to forward-test Day 3 validator, classification, recovery, clean-master, and continuity contracts.

## V1 Canon / Structure

| Case | Expected result |
| --- | --- |
| Output depicts a different primary subject from Canon. | V1 `HARD_FAIL / WRONG_SUBJECT_IDENTITY` -> `HARD_RESET`. |
| Canonical robot helmet and limb geometry are substantially deformed. | V1 `HARD_FAIL / MAJOR_STRUCTURAL_DRIFT` or `MAJOR_ANATOMY_OR_GEOMETRY_FAILURE` -> `HARD_RESET`. |
| External pose reference causes the external person's face to replace the canonical subject. | V1 `HARD_FAIL / EXTERNAL_IDENTITY_CONTAMINATION` -> `HARD_RESET`. |
| Subject identity and structure are correct but a small canonical surface mark is missing. | V1 may report `LOCAL_DEFECT`; if V2 passes, classify `REFINE_ELIGIBLE`, not `HARD_RESET`. |

## V2 Operation Compliance

| Case | Expected result |
| --- | --- |
| Subject identity is correct but requested side camera is rendered front-on. | `RETRY_REQUIRED / CAMERA_NONCOMPLIANCE`; no automatic retry. |
| Subject identity is correct but external POSE role was ignored. | `RETRY_REQUIRED / REFERENCE_ROLE_EXECUTION_FAILURE`. |
| Background-only edit changes protected subject pixels but does not cause major canonical drift. | `RETRY_REQUIRED / EDIT_CONTRACT_FAILURE` or `PRESERVE_CONSTRAINT_FAILURE`. |
| Correct subject and pose but wrong target ratio. | `RETRY_REQUIRED / ASPECT_RATIO_FAILURE`. |

## V3 Local Quality

| Case | Expected result |
| --- | --- |
| Canon and shot pass; there is a small edge halo. | `REFINE_ELIGIBLE / EDGE_DEFECT`. |
| Canon and shot pass; unwanted text appears in the background. | `REFINE_ELIGIBLE / UNWANTED_TEXT`. |
| A local appendage detail is malformed but major body structure is still canonical. | `REFINE_ELIGIBLE / LOCAL_APPENDAGE_DEFECT`. |
| Appendage failure changes major anatomy or mechanical geometry. | Escalate to V1 hard failure and `HARD_RESET`; do not hide it as local quality. |

## Classification precedence

| Combined findings | Expected result |
| --- | --- |
| External identity contamination + wrong camera + edge artifact. | `HARD_RESET`; retain all reason codes. |
| Correct identity + wrong pose + background artifact. | `RETRY_REQUIRED`; V2 controls recovery. |
| Correct identity + correct shot + local artifact. | `REFINE_ELIGIBLE`. |
| Image appears correct but a required validator is unavailable. | `BLOCKED / VALIDATOR_UNAVAILABLE`. |
| All required validators and hooks pass. | `ACCEPT`. |

## HARD_RESET one-safe-retry

| Case | Expected result |
| --- | --- |
| Attempt 1 is `HARD_RESET`; packet has not used automatic hard-reset recovery. | Discard result and perform exactly one fresh retry with the same packet semantics. |
| Attempt 2 after automatic fresh retry is `ACCEPT`. | Accept attempt 2 and stop automatic execution. |
| Attempt 2 is another `HARD_RESET`. | Stop; report `HARD_RESET`; do not auto-retry a second time. |
| Attempt 2 is `RETRY_REQUIRED` or `REFINE_ELIGIBLE`. | Stop; report that classification; no further automatic generation. |
| Automatic retry would require changing pose, camera, evidence roles, or preserve constraints. | Do not call it retry; require `REVISE` and a newly frozen packet. |
| First hard-reset result is visually close to correct. | It still cannot be fed back as identity, continuity, preview, or refine evidence. |

## RETRY_REQUIRED

| Case | Expected result |
| --- | --- |
| Result misses composition but identity is correct. | No automatic retry. Principal/controller may explicitly `RETRY` the same packet. |
| Principal asks to change composition after the miss. | `REVISE`, re-run affected planning, freeze a new packet. |
| Retry-required image is the newest generated result. | It still cannot become continuity or clean-master evidence. |

## REFINE_ELIGIBLE

| Case | Expected result |
| --- | --- |
| Only a small local surface defect remains. | Candidate may become explicit `EDIT_TARGET` for bounded refinement with all passed V1/V2 scopes preserved. |
| Refinement fixes defect but changes camera framing. | V2 fails on revalidation; do not accept. |
| Refine-eligible image is needed as continuity for the next shot. | Reject continuity admission until a refined result reaches `ACCEPT`. |

## BLOCKED

| Case | Expected result |
| --- | --- |
| Canonical evidence required by the shot is missing. | `BLOCKED / CANONICAL_EVIDENCE_UNAVAILABLE`; do not substitute continuity. |
| Required identity validator cannot run. | `BLOCKED / VALIDATOR_UNAVAILABLE`. |
| Required post-generation hook fails. | `BLOCKED / REQUIRED_HOOK_FAILED`; candidate is not accepted. |
| Clean-master provenance cannot be verified during session import. | `BLOCKED / PROVENANCE_UNVERIFIED` for operations that depend on accepted provenance. |

## Clean-master provenance

| Case | Expected result |
| --- | --- |
| Candidate receives `ACCEPT`. | Promote that exact validated candidate to a new immutable `ACCEPTED_CLEAN_MASTER` record. |
| Candidate is `REFINE_ELIGIBLE`. | Keep it a candidate; do not create an accepted clean master. |
| Accepted master is watermarked for delivery. | Watermarked file is `DELIVERY_DERIVATIVE`; source accepted clean master remains authoritative. |
| An accepted master is later edited and accepted. | Create a new clean master identifier; retain prior provenance rather than overwriting history. |

## Continuity admission

| Case | Expected result |
| --- | --- |
| Accepted clean master contains useful approved environment state for the next series shot. | May admit as `ACCEPTED_CONTINUITY` with environment role and provenance link. |
| Preview looks perfect but has never been accepted. | Reject continuity admission. |
| Delivery derivative is the only visible copy but source accepted master exists. | Use the source master for continuity; never the derivative. |
| Continuity image conflicts with Canon. | Canon wins; continuity cannot override the canonical invariant. |
| Next shot uses accepted continuity. | Evidence Planner must still include all required canonical evidence. |
