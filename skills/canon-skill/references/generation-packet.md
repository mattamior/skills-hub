# Generation Packet contract 0.1

A packet freezes one logical execution target. It is not a mutable prompt scratchpad or a flat unordered pile of image references.

## Required fields

```yaml
subject:
  id: subject-owned-id
  pack_revision: immutable-source-revision
route: STANDALONE_SHOT
operation: GENERATE
output_kind: FINAL
effective_spec: {}
series_lock: {}
shot: {}
canonical_evidence: []
external_evidence: []
continuity_evidence: []
preserve_constraints: []
risk_guards: []
preprocess_hooks: []
postprocess_hooks: []
validators: []
retry_policy:
  automatic_hard_reset: 1
delivery_policy: {}
```

The mappings above describe shape only; actual execution requires a resolved effective spec, adequate canonical evidence and required validators. Validate the [schema](../assets/schemas/generation-packet.schema.json) before using the deterministic helpers.

Optional fields include revision, gates, edit target/contract, preview reference, construction policy, validation phases and transport requirements. `output_kind` is separate from route: previews and diagnostics cannot become clean masters merely because a named-shot route produced them. `PREVIEW_ONLY` cannot produce a `FINAL` target.

## Freeze boundary

Resolve subject revision, effective spec, route/operation, selected shot, image roles, all evidence channels, preserve constraints, risk guards, hook implementations/parameters, core and custom validators, approval policies, retry limit and delivery policy. Missing dependencies block rather than freeze an executable-looking incomplete plan.

Evidence entries retain authority id, role/scope, source revision, selected transport variant and payload hash when bytes are bound, and admission/approval provenance as applicable. Protect canonical source identity separately from approved transport payload identity. Diagnostic-only references do not enter generation channels.

The Python helper serializes a detached JSON snapshot and hashes its sorted, compact, finite JSON form. This is a version-local semantic digest, not an interoperability claim for an external canonical-JSON standard. Do not expose mutable aliases to frozen input data.

## Approval phases

`PRE_EXECUTION` gates must be passed before submission. Their `scope_hash` binds subject, effective spec, series lock, shot and output kind; their approval evidence must correspond to that current scope.

A `POST_VALIDATION` gate declares an approval that can occur only after an image exists, such as calibration-master review. Freeze its id, requirement and phase, then stop with a candidate awaiting Principal approval. Do not require that future approval before generating its first candidate, and do not fake it after generation.

The realized approval receipt is session-local, outside immutable packet semantics. It binds gate id, approval evidence id, packet hash and exact candidate SHA-256. Master promotion must reject absent or mismatched approval. Until all required approval dependencies are satisfied, there is no accepted master, continuity admission or dependent diagnostics.

## RETRY and REVISE

`RETRY` retains all frozen semantics, evidence roles, selected authority/transport bindings, shot geometry, operation, masks/preserve scopes, hooks, validators and policies. Only allowed backend randomness or same-payload transport details may vary. The failed result never becomes a new input. A command routed through `CURRENT_SHOT_OPERATION` may locate an earlier packet without rewriting its original route.

`REVISE` applies only Principal-authorized semantic changes, invalidates affected approvals, replans affected dependencies and freezes a new revision. Reset packet-local retry counters for that new revision, not by changing a label on an old packet. Local refinement is an explicit bounded edit with new candidate provenance, not a covert rewrite of the old packet.

## Execution envelope and provenance

Keep ephemeral tool handles, job ids, timestamps, actual receipts, attempt index, observed results and approval receipts in an execution envelope linked to the packet digest. No credentials or private signed URLs belong in durable packets.

Record which evidence satisfied each invariant and why it was selected. Record which hook output was validated and the exact candidate hash. An actual pixel change after validation requires a new candidate and revalidation. Failed delivery processing does not retroactively alter an accepted master.

Every result links to this packet revision and receives one of the five [result classifications](result-model.md). A metadata plan or synthetic dry run does not prove images were materialized, a backend ran, or Canon was visually preserved.
