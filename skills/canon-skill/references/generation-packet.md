# Generation Packet Contract

A Generation Packet is the frozen execution contract for one actual generation or edit. It captures the semantic decisions that must remain stable across safe retries.

## Minimum v1 shape

```yaml
subject:
  id: example-subject
  pack_revision: immutable-or-resolvable-revision

route: STANDALONE_SHOT
operation: GENERATE

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

retry_policy: {}
delivery_policy: {}
```

A packet may include backend transport metadata, but provider-specific fields must remain separable from the semantic contract.

## Freeze inputs

Freeze only after resolving:

- the Subject Pack and its revision;
- route and operation;
- effective user specification;
- shot definition and series lock;
- image roles;
- canonical evidence selected by Evidence Planner;
- role-scoped external evidence;
- eligible continuity auxiliaries;
- preserve constraints and contamination guards;
- applicable hooks;
- required validators;
- retry policy;
- delivery policy.

If any required dependency is unresolved, return a blocked result instead of freezing an incomplete packet.

## Evidence entries

Each evidence entry should preserve provenance and role metadata sufficient for later audit.

Example:

```yaml
- id: canonical-front
  authority: CANONICAL_VISUAL
  role: IDENTITY
  scope: [primary-identity]
  source: subject-pack
```

External evidence must include its explicit allowed roles. Continuity evidence must identify the accepted clean master from which it originated.

## Preserve constraints and risk guards

`preserve_constraints` are positive invariants that the operation must keep stable, such as an already accepted camera relationship, a structural region, or unaffected areas of an edit target.

`risk_guards` are explicit failure-prevention constraints, such as preventing external identity contamination, protecting untouched regions during an edit, or forbidding delivery-only overlays in a clean master.

These fields should express semantics, not backend prompt tricks.

## Retry semantics

`RETRY` reuses the same packet semantics. A retry may vary only execution details that do not alter intended meaning, such as backend randomness, a transport retry, or another provider-supported nondeterministic sample.

A retry must not silently change:

- shot geometry;
- camera intent;
- pose intent;
- composition;
- canonical evidence roles;
- external-reference roles;
- preserve constraints;
- series locks;
- validators;
- hook requirements;
- delivery policy.

If any of those must change, the operation is a `REVISE`, not a retry.

## Revision semantics

`REVISE` starts from the prior packet, applies only principal-authorized semantic changes, re-runs affected routing and evidence planning, and produces a newly frozen packet with a new revision identifier.

Unchanged fields should remain stable so revisions are attributable and reviewable.

## Packet provenance

The runtime should retain enough provenance to answer:

- which Subject Pack revision was used;
- which evidence items were selected and why;
- which external roles were authorized;
- which clean master supplied continuity;
- which hooks and validators were required;
- whether the result came from the initial attempt, a safe retry, or a revised packet.

Packet provenance is session runtime evidence. It does not write back into Subject Canon automatically.

## Clean-master and delivery boundary

Generation output begins as a construction result or clean-master candidate. Only after required validation and acceptance may it become an accepted clean master.

Delivery derivatives are created from the accepted clean master according to delivery policy. They may be resized, converted, watermarked, composited, sharpened, or otherwise prepared for delivery, but they never replace the accepted clean master in continuity or identity evidence.

## Result linkage

Every generation result must link to the packet revision that produced it. Later runtime work may classify that result as `ACCEPT`, `HARD_RESET`, `RETRY_REQUIRED`, `REFINE_ELIGIBLE`, or `BLOCKED`, but classification must not mutate the frozen packet retroactively.
