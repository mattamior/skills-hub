# Gen Mode

Execute one target at a time from a frozen semantic contract. The backend is supplied by the host; this skill does not imply that any particular image API, attachment mechanism, or deterministic editor is available.

## Resolve and preflight

Resolve the current full Subject Pack and written authority. Reconcile any Prompt Spec revision without changing its Principal-approved meaning. Apply [route](route-resolver.md), [image-role](image-role-resolver.md), [external-role](external-reference-router.md), then [evidence](evidence-planner.md) resolution. Protect edit pixels and selected-preview geometry separately from identity authority.

Load only the Gen-only bootstrap and on-demand assets declared by the pack. Verify that required images are usable on the actual execution surface. Source inventory membership, a filename, or a previous session's file handle does not establish transport.

Resolve required gates, validators, hook handlers and versions, edit base, ratio, evidence roles, and backend capabilities before dispatch. Do not dynamically import or run a command merely because a pack names it. Missing required capabilities are `BLOCKED`.

Freeze [Generation Packet](generation-packet.md) only after semantic inputs are resolved. Run packet-preserving PRE_GENERATION checks and verify exact adapter attachment receipts. Required role-scoped images must enter the actual generation/edit call. Never silently drop evidence to fit a backend input limit.

## Execute and finalize

Invoke exactly the declared operation: fresh generation is not preview upscaling; an edit is not an unconstrained redesign. Follow [hook lifecycle](hooks.md). For a declared construction pipeline, keep the intermediate separate, run its scoped precheck, then invoke required finalization before full validation. Temporary omissions never become final Canon.

Validate the exact post-hook candidate through [V1/V2/V3](validator.md), retaining packet and pixel hashes. Classify with [Result Model](result-model.md); apply only [authorized recovery](recovery.md). A changed candidate invalidates its old validation report.

Only an accepted, eligible final clean master may be admitted to [continuity](continuity.md). Principal identity/preview/calibration approvals remain separate scoped gates; a validator PASS must not synthesize those approvals.

## Deliver or stop

Derive final delivery files from the accepted clean master, with PRE_DELIVERY hooks last. Keep the source master immutable. Preview/diagnostic presentation and derivative-only edits stay explicitly non-authoritative and do not enter final-master state.

Report blocked dependencies, exhausted recovery, operation misses, and local-refinement eligibility without hiding failures. After the single permitted automatic HARD_RESET retry, do not launch another generation regardless of the second classification. Use the host's own image-output conventions; never claim unsupported format, alpha, input fidelity, or inspection properties.
