# Runtime State v1

Runtime State is session-local execution state. It coordinates routing, image roles, evidence planning, generation packets, gates, and continuity without becoming Subject Canon.

A new session starts with fresh runtime state and resolves durable Subject Canon again. No transient field is automatically restored from an earlier chat or run.

## Minimum state

```yaml
current_subject: null
current_route: null
current_stage: null

series_lock: {}
target_ratio: null

identity_gate:
  status: OPEN
preview_gate:
  status: OPEN

shot_registry: {}
selected_shot: null
current_revision: null

image_operation_role: null

edit_target: null
edit_contract: null

preview_shot_reference: null

external_reference_mode: NONE
external_reference_role_map: {}

accepted_clean_master: null
continuity_auxiliaries: []

generation_packet: null
retry_count: 0
hard_reset_auto_retry_count: 0

validation_report: null
last_result_classification: null
last_result_id: null
candidate_clean_master: null

session_import: null
```

Subject Packs may expose additional durable capabilities, but subject-specific facts must not be copied into Runtime State as new generic schema fields.

## Stage progression

Use these generic stages when useful:

```text
SUBJECT_RESOLVED
ROUTE_RESOLVED
IMAGE_ROLES_RESOLVED
EXTERNAL_REFERENCES_ROUTED
EVIDENCE_PLANNED
PACKET_FROZEN
EXECUTING
VALIDATING
ACCEPTED
BLOCKED
```

A preview-only or diagnostic operation may stop before `ACCEPTED`, but it must not skip ordering constraints among the stages it does use.

Moving backward because semantics changed is a revision, not a retry.

## Subject and route

`current_subject` records the resolved Subject Pack identifier and revision for this session. It points to durable canon; it does not duplicate canon facts.

`current_route` stores Route Resolver output. A route may change only through a semantic revision before a new Generation Packet is frozen.

## Series and shot state

`series_lock` contains accepted series-wide constraints such as target aspect ratio, shared visual conditions, or canon-bearing requirements compiled at the generic spec level.

`target_ratio` is an explicit runtime convenience field when aspect ratio is separately needed by the backend or validator.

`shot_registry` maps stable shot identifiers to shot definitions, preview provenance, revision history, and accepted result links.

`selected_shot` enables `CURRENT_SHOT_OPERATION`. It must be unambiguous before commands such as "retry this shot" can use it.

`current_revision` identifies the semantic shot or packet revision currently being operated on. A `REVISE` creates a new revision; `RETRY` does not.

## Gates

`identity_gate` and `preview_gate` are explicit gate records, not booleans inferred from conversation tone.

Recommended statuses are:

```text
OPEN
PASSED
BLOCKED
NOT_REQUIRED
```

A route may declare a gate requirement. Generation must not bypass a required gate merely because the needed image is attached.

## Image operation state

`image_operation_role` records whether the current image operation is generation, edit, preview-reference use, calibration, validation-only work, or another generic operation supported by the route contract.

`edit_target` identifies the image whose pixels are being modified. It is populated only after Image Role Resolver binds an `EDIT_TARGET`.

`edit_contract` declares changed and preserved scopes. Unaffected scopes remain protected across generation, validation, refinement, and delivery.

`preview_shot_reference` identifies preview evidence associated with the selected shot. It is not an edit target unless the principal explicitly requests pixel editing.

## External references

`external_reference_mode` is `NONE`, `ROLE_SCOPED`, or `CONSERVATIVE_FALLBACK`.

`external_reference_role_map` stores resolved role scopes by image identifier. Once External Reference Router has run, later stages must not broaden this map silently.

## Clean master and continuity

`accepted_clean_master` points only to the latest accepted clean master for the active shot when one exists.

`continuity_auxiliaries` contains only accepted clean masters admitted for series continuity. Every entry retains source shot, revision, packet, and acceptance provenance.

The following must never be stored in `continuity_auxiliaries`:

- preview images;
- failed or hard-reset results;
- unverified generations;
- construction intermediates;
- delivery derivatives.

Replacing an accepted clean master does not rewrite Subject Canon.

## Generation Packet and retries

`generation_packet` is null until evidence planning, hooks, validators, retry policy, and delivery policy are ready to freeze.

After `PACKET_FROZEN`, the packet is immutable. A safe retry reuses it and increments `retry_count`.

`retry_count` is packet-revision local. It resets when `REVISE` freezes a new packet.

`hard_reset_auto_retry_count` is also packet-revision local and is capped at 1. It records whether the one automatic fresh retry for a `HARD_RESET` has already been consumed.

`validation_report`, `last_result_classification`, and `last_result_id` retain the latest attempt's validation provenance. `candidate_clean_master` points only to the exact post-generation candidate currently under validation or bounded refinement; it is cleared or superseded when the attempt is rejected or a new result is produced.

Runtime diagnostics may retain older packet/result links for provenance, but only the active frozen packet is used for execution.

## Session isolation

The following are transient by default and are not automatically restored in a new session:

- current route and stage;
- series lock;
- gates;
- shot registry and selected shot;
- current revision;
- edit target and contract;
- preview reference;
- external-reference mode and role map;
- accepted clean master pointer;
- continuity auxiliaries;
- active Generation Packet;
- retry count and hard-reset automatic-retry count;
- validation report, last result classification, and candidate clean-master pointer.

Durable Subject Canon remains in the Subject Project/Subject Pack, not in this state.

## SESSION_IMPORT

Cross-session recovery requires explicit `SESSION_IMPORT`.

An import record should state:

```yaml
session_import:
  source_session: opaque-session-id
  imported_fields:
    - shot_registry
    - selected_shot
    - accepted_clean_master
  provenance_verified: true
```

Import only fields that the principal or authorized workflow explicitly requests.

Imported clean masters and continuity entries must preserve acceptance provenance. Imported preview or generated images do not gain authority because they crossed a session boundary.

If provenance cannot be verified, keep the item unverified or block the dependent operation rather than promoting it.

## No canon writeback

Runtime State never mutates Subject Canon automatically.

A Subject Project may define a separate, explicit process to approve new canonical facts or assets. That process occurs outside normal Canon Skill runtime state transitions and must preserve the Subject Pack's ownership boundary.
