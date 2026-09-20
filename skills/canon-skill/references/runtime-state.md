# Runtime State v1

Use [runtime-state.schema.json](../schemas/runtime-state.schema.json) for serialized state. `contracts.new_state()` creates an independent empty namespace; there is no implicit previous-session argument.

## Fields

Track current_subject, current_route, current_stage; series_lock and target_ratio; identity_gate and preview_gate; shot_registry, selected_shot and current_revision; image_operation_role; edit_target and edit_contract; preview_shot_reference; external_reference_mode and external_reference_role_map; accepted_clean_master and continuity_auxiliaries; generation_packet, retry_count and hard_reset_auto_retry_count; validation_report, last_result_classification, last_result_id and candidate_clean_master; session_import.

Subject fields point to current durable pack/revision, never duplicate subject facts as new universal anatomy keys. Null/empty defaults do not mean gates are satisfied. Gate statuses are OPEN, PASSED, BLOCKED or NOT_REQUIRED, with scope and approval evidence recorded by the host.

## Transitions

Resolve subject -> route -> image roles -> external scopes -> evidence -> freeze -> execute -> validate -> classify. Only eligible accepted final output changes the accepted-master pointer. Preview/diagnostic success and delivery-only edits do not.

A retry increments attempt/retry history while preserving packet digest. A Principal semantic revision creates a new frozen revision and resets its packet-local automatic budget; internal relabeling or transport repair must not reset it. Ordinary retry dispatch may use CURRENT_SHOT_OPERATION without changing the original packet route.

Keep per-attempt results and hook/validation hashes. Rejecting an attempt clears its active candidate without erasing a previously accepted master. Never overwrite accepted source pixels in place. Preserve prior provenance when a new accepted revision supersedes a master.

## SESSION_IMPORT

Begin a new session empty, except re-resolved durable Canon. Explicit import records source session, exact requested fields, source pack/revisions, actual available image objects and verified provenance. Do not automatically restore the entire previous namespace.

Validate imported gates against the same approved scope. Reconcile stale subject revisions. Importing an image does not upgrade its authority. Restoring an active packet requires its retry budget and result history too; never reset a consumed automatic allowance by importing only the packet. Missing required provenance blocks the dependent operation.

Runtime state never writes Subject Canon or Agnir subject facts automatically. Durable subject updates use a separate, explicitly authorized subject-owned process.
