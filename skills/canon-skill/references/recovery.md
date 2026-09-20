# Recovery Model

Recovery decides what may happen after a classified result without changing the frozen Generation Packet semantics.

The runtime has one automatic recovery path: a single fresh retry after the first `HARD_RESET` for a packet revision.

## Recovery table

| Classification | Automatic action | Result may be reused as reference | Principal action |
| --- | --- | --- | --- |
| `ACCEPT` | promote validated candidate | only after continuity admission | deliver or continue |
| `HARD_RESET` | one fresh retry on first occurrence only | no | revise after automatic path stops |
| `RETRY_REQUIRED` | none | no | explicit `RETRY` or `REVISE` |
| `REFINE_ELIGIBLE` | none | only as explicit refine edit target, never as continuity | explicit local refinement |
| `BLOCKED` | none | not applicable | resolve dependency |

## One-safe-retry HARD_RESET rule

Track automatic hard-reset recovery per frozen packet revision.

On attempt 1:

1. validate the result;
2. if classification is `HARD_RESET` and `hard_reset_auto_retry_count == 0`, discard the failed candidate;
3. increment `hard_reset_auto_retry_count` to 1;
4. execute one fresh retry from the same frozen packet semantics.

"Fresh" means:

- reuse the same Subject Pack revision;
- reuse the same route, operation, effective spec, shot, series lock, evidence-role bindings, canonical evidence, external evidence, continuity evidence, preserve constraints, hooks, validators, retry policy, and delivery policy;
- allow only backend execution randomness or other packet-approved nondeterminism to differ;
- do not feed the hard-reset result back as identity, continuity, preview, edit, or refinement evidence.

After the fresh retry completes, stop automatic execution regardless of its classification.

If the second attempt is `ACCEPT`, accept it normally. If it is `HARD_RESET`, `RETRY_REQUIRED`, `REFINE_ELIGIBLE`, or `BLOCKED`, report that result and take no further automatic generation action.

A new `REVISE` packet starts a new packet revision and resets the packet-local hard-reset automatic retry counter.

## RETRY_REQUIRED

Do not automatically retry `RETRY_REQUIRED`.

This class means the semantic packet is still valid but execution did not comply. An explicit `RETRY` may sample the same packet again. If the requested camera, pose, composition, roles, or preserve constraints need to change, use `REVISE` instead.

A retry-required output is not eligible as:

- continuity evidence;
- identity evidence;
- a clean master;
- an implicit preview reference.

## REFINE_ELIGIBLE

Refinement is intentionally explicit.

The candidate may be bound as an `EDIT_TARGET` for a local refinement only when:

- the refinement contract names the local defects;
- all V1/V2-passed scopes become preserve constraints;
- no new external role is inferred;
- canonical evidence remains available for validation.

Refinement never means "keep improving until it looks good." Each refine attempt must be bounded, revalidated, and reclassified.

## BLOCKED

Blocked states require dependency repair, not sampling.

Examples:

- missing Subject Pack -> resolve the pack;
- missing canonical evidence -> repair the Subject Pack or revise the shot;
- missing edit target -> obtain the correct target;
- gate not satisfied -> satisfy or explicitly revise the workflow;
- validator unavailable -> restore the required validator;
- unverified provenance -> recover verified provenance or exclude the item.

Do not weaken authority, drop validators, or substitute lower-authority evidence to escape `BLOCKED`.

## Recovery provenance

Runtime State should retain:

```yaml
retry_count:
hard_reset_auto_retry_count:
last_result_classification:
last_result_id:
validation_report:
```

`retry_count` counts execution retries for the active packet revision. `hard_reset_auto_retry_count` is specifically capped at 1 for automatic hard-reset recovery.

An explicit principal retry after `RETRY_REQUIRED` may increment `retry_count`, but it does not grant another automatic hard-reset retry if the packet revision already consumed its one-safe-retry allowance.
