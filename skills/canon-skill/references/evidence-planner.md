# Evidence Planner

Select the minimum adequate canonical evidence for the current authorized operation, not the entire Subject Pack. This is Gen Mode work; Prompt Mode does not select canonical generation assets.

## Resolve requirements

Consume the resolved subject revision, route/operation, effective spec, series lock, selected shot, edit contract, image-role bindings and already-scoped external plan. The host identifies all visible or edit-risk-adjacent invariant groups from the subject-owned contract, including those protected by an edit. Do not infer human anatomy or use an external image to replace a required Canon group.

Match profiles using shot `view`, `framing` and `operation`. Combine compatible requirements only when policy allows it. Under `runtime.defaults.profile_selection: EXPLICIT_SINGLE`, require exactly one explicit `shot.reference_profile`; do not union competing primary profiles. Profile `require.assets` and explicitly resolved shot `required_asset_ids` are hard constraints. `prefer_assets` are preferences, not substitutes for mandatory evidence.

## Filter candidates

Use subject-owned inventory items with resolved provenance, supported authority, `generation_eligible: true` and `diagnostic_only: false`. Honor strict-view restrictions and matching-view calibration scope. A calibration asset requires an enabled approved profile eligible for generation; diagnostic boards may be retained for validation only.

The canonical channel must retain canonical visual anchoring appropriate to the subject. Approved calibration can supplement that evidence within its declared scope, never replace it with a generated-image-only chain. A structural calibration view does not acquire identity authority over incidental regions.

## Minimize without weakening

Choose the smallest subset covering all required invariant groups and all mandatory asset ids. For equal-size valid subsets, prefer exact view, declared preferred assets, higher authority, narrower unrelated coverage, then stable id ordering. Do not optimize away an explicitly required anchor, silently drop an invariant, or pick a conflicting profile merely to reduce image count.

The optional Python helper performs bounded exact cover for at most 24 relevant candidates. For a larger inventory, an authorized host must first scope the relevant candidate pool or provide an equivalent planner; the helper blocks rather than perform an unbounded search or silently use a non-equivalent greedy subset. This implementation bound does not limit how many assets a Subject Project may own.

## Keep evidence channels separate

Canonical, external and continuity evidence remain separate packet arrays with authority, purpose and provenance. External references satisfy only authorized operation dimensions. Continuity contains only verified accepted clean masters relevant to the same subject and compatible current Canon revision. Neither channel can fill missing canonical identity or structure coverage.

Keep the actual edit target and selected preview reference separate as operational inputs. The edit base does not become Canon merely because it depicts the subject. Preview pixels provide selected shot geometry, not final pixels or identity. Required transported image objects must still be materialized by the host.

## Planning result

Record required groups, matched profiles, selected asset ids, coverage per group, mandatory-asset satisfaction, excluded diagnostic assets, reasons for selections and unresolved dependencies. A source/transport payload mapping preserves both authority provenance and the approved transport variant hash.

Any uncovered required Canon group yields `CANONICAL_EVIDENCE_UNAVAILABLE`. Unknown groups/profiles or conflicting requirements yield `SPEC_UNRESOLVED`. Do not escape those blockers by promoting continuity, external references, previews or unverified outputs. Only an authorized revision can change the task or source policy and replan.
