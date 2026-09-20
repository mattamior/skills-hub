# Runtime State 0.1

Runtime state is session-local coordination, not Subject Canon. A new session resolves durable subject truth and starts with fresh transient fields. The [schema](../assets/schemas/runtime-state.schema.json) describes the serializable state.

## Initial state

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

`current_subject` points to an id and resolved pack revision, not duplicated identity facts. `current_route` is the route enum; the resolver's target and reason record belongs in operation provenance. A command route locating an existing packet does not rewrite that packet's origin route.

## Ordered stages

Progress through subject resolution, route resolution, image-role resolution, external routing, evidence planning, packet freeze, execution, validation and acceptance or blocking as applicable. Prompt Mode stops at its compiled handoff and never performs canonical transport. A metadata-only plan is not an executed or accepted stage.

Shot registry entries retain unique ids, definitions, revisions, preview provenance and accepted result links. The selected shot must be unambiguous for current-shot commands. The series lock and ratio retain authorized shared values; revisions invalidate affected scope approvals, rather than silently carrying them forward.

## Gates and image bindings

Identity and preview gates use `OPEN`, `PASSED`, `BLOCKED` or `NOT_REQUIRED`, with source approval evidence and scope hash when passed. Do not infer approval from an attached image or conversational enthusiasm. Packet declarations distinguish pre-execution approval from post-validation candidate review; later approval receipts live in the execution envelope and do not mutate the frozen declaration.

`edit_target`, `edit_contract` and `preview_shot_reference` are populated only from resolved current-operation bindings. External mode is `NONE`, `ROLE_SCOPED` or `CONSERVATIVE_FALLBACK`; the per-image role map cannot be widened by later stages.

## Candidates, masters and recovery

The candidate pointer refers to the exact post-processing output currently under validation or bounded refinement. `accepted_clean_master` and continuity entries refer only to eligible fully accepted masters with byte, subject/pack, shot, packet and approval provenance. Failure of a later candidate preserves the prior accepted master.

`retry_count` counts execution retries for the active packet revision. `hard_reset_auto_retry_count` is capped at one, may remain zero under a no-auto-retry subject policy, and cannot be reset by relabeling a packet. A genuine authorized semantic revision freezes a new packet and gets new packet-local counters.

Store the latest observed report, result id and classification separately from immutable packet data. A helper report list may be wrapped in the serializable state's `validation_report` object with its packet/result/hash provenance. Old diagnostics may remain in history but never become active evidence implicitly.

## SESSION_IMPORT

Require an explicit current-session instruction naming the fields to restore and their source. Revalidate subject revision, approvals and accepted-master provenance; reacquire actual image inputs in the current host. Do not automatically hydrate gates, packets, retry allowances, tool handles, clean masters, styling or shot selections from foreign-session summaries.

The optional helper supports a conservative subset: shot registry, selected shot, series lock, ratio, accepted master and continuity entries. It requires an exact subject/pack match and starts gates/counters/packet state fresh. Import a selected shot together with its registry. Unsupported restoration requires an explicit host workflow with equivalent provenance checks, not silent helper coercion.

An imported preview or unverified result retains its prior restricted status. No runtime transition writes new facts or assets back into Subject Canon; that requires a separate subject-owned approval process.
