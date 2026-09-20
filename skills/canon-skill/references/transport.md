# Generation transport abstraction

Authority, storage location and usable backend image inputs are different properties. Canon Skill requires the active host to prove transport, not merely name an asset.

## Host adapter contract

The adapter exposes capability discovery, authorized asset materialization, generation/edit submission, result retrieval, and delivery processing. It may be a conversational tool adapter or an application integration. Use actual supported tool parameters; never fabricate callable endpoints from this abstract contract.

A capability record describes accepted input forms, supported reference roles, maximum image count, edit/mask support, ratio/dimension handling, deterministic processing, result-byte access, inspection ability and failure semantics. Reject an unsupported requirement with `BACKEND_CAPABILITY_UNAVAILABLE`; do not silently change the packet.

## Authority identity versus transport variants

An asset binding has a stable authority id and source revision/hash. A Subject Pack may separately authorize transport variants, each with a locator, expected payload hash, permitted purpose and approval provenance. A cleaned or compact runtime derivative is not automatically independent canonical authority.

Freeze the chosen variant and its expected payload hash before submission. Keep the canonical source identity/hash in provenance. Compare received bytes against the selected variant hash, not accidentally against a different original's hash. Unlisted variants, overview boards, delivery derivatives and arbitrary generated substitutes are not allowed recovery transports.

The normalized packet's evidence `sha256` refers to the selected transport payload; source-authority identity remains in its provenance record. The Subject Project owns and verifies that mapping. Changing to a semantically different variant requires replanning/revision, not a hidden retry change.

## Materialization and receipts

Every required canonical, external, continuity, edit-target or preview input must be an actually usable image/attachment/file object in the current execution surface. A filename, repository path, opaque id, prior-chat description or inaccessible link does not satisfy this condition.

A host receipt records authority id, chosen payload hash, actual usable handle, originating source, permitted roles, current execution scope, and which call consumed it. Handles and credentials remain transient. Durable evidence should contain safe ids and checksums, not API keys, private signed URLs or authorization headers.

A host may bootstrap a pack-declared session pool once, then pass only the selected subset for each shot. Prompt Mode never bootstraps that pool. When a retained asset already exists, attempt the authorized retrieval path before asking for a duplicate upload.

## Failure and retries

Missing inputs block with the applicable canonical/external/edit/preview transport code. An unknown backend job status must be resolved using its job/idempotency contract before resubmission; do not generate duplicate paid samples merely because result retrieval timed out.

A transport retry reuses the same payload binding and intent. A hard-reset image retry reuses the frozen packet and never adds the failed output as evidence. Alternative storage of the same approved payload is a transport repair; an unapproved substitute is not.

Provider safety limits and system instructions remain in force. Canon authority is a visual-evidence ordering, not an instruction hierarchy that can override host safety or permissions.

## Dry runs and helper boundary

Metadata planning can succeed before images materialize; generation may not. Simulated adapters must mark receipts, candidate records and results as `simulation: true`. Never mix them with live inputs, report synthetic PASS outcomes as visual acceptance, or claim a fixture has become a real adopted Subject Project.

[contract_runtime.py](../scripts/contract_runtime.py) checks immutable JSON semantics, declared role capability and supplied receipts. The host remains responsible for honest byte acquisition, actual image consumption, visual inspection and secure authorization. Validate the [packet schema](../assets/schemas/generation-packet.schema.json) before helper calls; the helpers do not replace a schema validator or a real generation backend.
