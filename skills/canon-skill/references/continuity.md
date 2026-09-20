# Clean Master and Continuity

Continuity exists to preserve accepted series state without creating a generated-image-only identity chain.

The core invariant is:

```text
continuity evidence supplements Canon;
it never replaces Canon.
```

## Provenance classes

Every generated or edited visual result belongs to one provenance class:

```text
CONSTRUCTION_INTERMEDIATE
CLEAN_MASTER_CANDIDATE
ACCEPTED_CLEAN_MASTER
DELIVERY_DERIVATIVE
```

### Construction intermediate

A construction intermediate is any temporary compositing, masking, generation, edit, repair, or processing artifact not yet presented to the full required validation path.

It cannot enter continuity or delivery as the authoritative master.

### Clean master candidate

A clean master candidate is the exact post-generation/postprocess result submitted for validation.

`HARD_RESET`, `RETRY_REQUIRED`, and `BLOCKED` candidates are rejected.

A `REFINE_ELIGIBLE` candidate remains a candidate and may be used only as an explicit local-refinement edit target under the recovery contract.

### Accepted clean master

An accepted clean master is the exact candidate that received `ACCEPT`.

Its provenance record should include:

```yaml
clean_master_id:
result_id:
subject_id:
subject_pack_revision:
packet_revision:
attempt_index:
shot_id:
shot_revision:
source_operation:
canonical_evidence_ids: []
external_evidence_ids: []
continuity_evidence_ids: []
hook_execution_record:
validation_report:
accepted_at_runtime_stage: ACCEPTED
```

The accepted master is immutable as provenance. A later edit produces a new candidate and, if accepted, a new clean master identifier.

Acceptance does not rewrite Subject Canon.

### Delivery derivative

A delivery derivative is created from an accepted clean master for export or presentation.

Examples include:

- resize or crop for delivery;
- file-format conversion;
- watermark or delivery mark;
- sharpening;
- color-space conversion;
- compositing onto a delivery background;
- packaging-specific decoration.

A delivery derivative must retain a link to its source clean master but must never replace that master in continuity, identity, edit-target preference, or validation provenance.

## Continuity admission

Only an `ACCEPTED_CLEAN_MASTER` may be admitted as `ACCEPTED_CONTINUITY`.

Admission also requires:

- verified clean-master provenance;
- the same canonical primary subject or an explicitly compatible subject scope;
- relevance to a future series/shot property;
- no unresolved hard-reset or validation status;
- the original clean master, not a delivery derivative.

Admission is not required for every accepted master. Prefer no continuity evidence when canonical evidence and the effective specification are already sufficient.

## Continuity scope

Continuity may carry accepted state such as:

- environment state;
- wardrobe state;
- prop/object state;
- camera language;
- lighting continuity;
- staging or relative placement;
- other non-canonical series state;
- canonical appearance only as corroborating auxiliary evidence.

Continuity may not redefine canonical identity, structural invariants, or written canon.

When continuity conflicts with higher-authority canon, Canon wins and the conflict is recorded.

## Prohibited continuity inputs

Never admit:

- previews;
- failed generations;
- `HARD_RESET` results;
- `RETRY_REQUIRED` results;
- `REFINE_ELIGIBLE` candidates;
- unverified generated history;
- construction intermediates;
- delivery-only derivatives;
- watermarked derivatives;
- results with unverified provenance.

An apparently successful image with no acceptance record remains `GENERATED_UNVERIFIED`.

## No generated-image-only identity chain

Every generation that uses continuity still requires the canonical evidence required by Evidence Planner.

Do not perform:

```text
Canon -> accepted generation A -> accepted generation B -> accepted generation C
```

while progressively dropping Canon and treating the previous generated image as the sole identity source.

The valid pattern is:

```text
Canon + optional accepted continuity A -> result B
Canon + optional accepted continuity B -> result C
```

where each shot independently satisfies required canonical coverage.

## Replacing clean masters

When a shot revision produces a new accepted clean master:

1. retain old provenance for audit;
2. update the active shot pointer to the new accepted master;
3. re-evaluate whether the older master remains a useful continuity auxiliary;
4. do not silently treat the newer image as stronger canonical authority.

Superseded clean masters may remain in history, but only explicitly admitted, relevant masters should remain active continuity auxiliaries.

## Continuity record

A runtime continuity entry should preserve:

```yaml
continuity_id:
source_clean_master_id:
source_shot_id:
source_shot_revision:
packet_revision:
subject_id:
admitted_roles: []
admission_reason:
provenance_verified: true
```

`admitted_roles` should state the continuity dimensions being carried. It is not a license to override canonical identity.

Runtime continuity remains session-local unless explicitly imported with verified provenance.
