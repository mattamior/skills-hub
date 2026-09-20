# Gen Mode contract

Execute one authorized logical target at a time from a resolved specification. This guide coordinates the narrower contracts; it is not a provider API adapter.

## Preflight

Resolve the Subject Pack revision and current-session specification. Read [runtime state](runtime-state.md), [route resolution](route-resolver.md), [image roles](image-role-resolver.md), [external routing](external-reference-router.md), and [evidence planning](evidence-planner.md), in that order. An explicit registered target wins over an implicit current-shot reference. The command route used to locate a retry must not rewrite the origin route inside its already-frozen packet.

Bind `output_kind` separately from route: `IDENTITY_CHECK`, `PREVIEW`, `FINAL`, `CALIBRATION`, or `DIAGNOSTIC`. A named-series-shot route can still produce a preview; the route alone does not grant final-master eligibility.

Compile the effective specification from current explicit revisions and authorized series/shot values, never from foreign-session summaries. Resolve required gates with scope, approval evidence and status. Approval for an earlier scope is not approval for revised identity, styling or shot selection. Stop at a required approval; never silently select a preview cell.

For an edit, resolve an actual unique base and an edit contract describing changes and protected scopes. Canonical originals are protected references, not ordinary edit targets. A delivery-only source may produce only another explicitly delivery-only derivative, never a clean master. For selected preview regeneration, use the selected cell only as geometry evidence; final output is a new generation with current canonical coverage.

## Select, freeze, materialize

Select the minimum adequate canonical subset, preserving all assets that a Subject Pack profile explicitly requires. Optional calibration, external and accepted continuity evidence remain separate channels and retain their scopes. Honor a subject-owned single-primary-profile policy rather than indiscriminately unioning every matching profile.

Resolve [hook requirements](hooks.md), phased validation, recovery limits, delivery policy and [transport capabilities](transport.md) before freeze. Freeze [the Generation Packet](generation-packet.md), including edit/preview bindings and the selected authority/transport variant identities. Then materialize and verify those exact bindings before calling the image backend. A metadata-only dry run may stop with a ready plan, but cannot claim transport readiness.

Honor a pack-declared session bootstrap separately from each call's selected evidence. Reuse a verified session pool; reload only a missing selected asset. Do not equate all cached assets with all generation inputs.

## Execute construction and finalization

Invoke the frozen `PRE_GENERATION` hooks, then the backend using its actual supported interface. A transport receipt must attest which image objects were consumed. Do not substitute descriptive text for a required visual reference or silently drop an input to fit a provider limit.

When a pack declares a construction stage, classify that output as `CONSTRUCTION_INTERMEDIATE`. Run the declared pre-finalization checks, including subject-owned handling of intentionally deferred regions. Final-only invariants remain mandatory at final validation. A failed base is not made acceptable by skipping a check or running a cosmetic hook over a major failure.

Invoke required `POST_GENERATION` and `PRE_VALIDATION` hooks in their frozen order. Only the finalized output enters the full [Validator Model](validator.md). Validate the exact bytes that would be accepted; any subsequent pixel change invalidates that report. `POST_VALIDATION` hooks are observational only unless a new validation cycle is explicitly required.

## Classify and stop correctly

Apply [result classification](result-model.md) and [recovery](recovery.md). The automatic hard-reset allowance is at most one for the initial sample of the frozen packet; a Subject Pack may reduce it to zero, particularly for Principal-gated calibration. No automatic retry follows `RETRY_REQUIRED`, `REFINE_ELIGIBLE` or `BLOCKED`. After the single permitted automatic fresh retry, stop automatic generation regardless of its result.

Only a fully validated eligible clean-master candidate may be promoted. `ACCEPT` on a preview or diagnostic means that limited artifact passed its own checks; it does not produce an accepted clean master. Preserve the prior accepted master when a later candidate fails. A refinement gets a new bounded edit contract and full revalidation, not an implicit chain of endless edits.

## Continuity and delivery

Admit accepted clean masters through [continuity rules](continuity.md), preserving subject/pack, shot, packet and byte provenance. A later shot independently requires Canon even when continuity is present. Calibration approval remains region-scoped and does not promote every visible feature to identity authority.

Run `PRE_DELIVERY` on a separate derivative of the accepted master. Required delivery QA can block delivery without invalidating an already accepted master. Preview decorations remain preview derivatives. Retain the pristine source and never feed watermarked or export-only copies back into ordinary identity/continuity inputs.

Report what actually happened: executed target and packet revision, observed validation result, available clean master or derivative, automatic retry count, and any blocking dependency. Obey the active image tool's own response contract; do not invent download links, calls, approvals, exact formatting guarantees or visual-test evidence.
