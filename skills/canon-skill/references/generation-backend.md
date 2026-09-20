# Generation Backend Interface

Backend adapters are supplied by the host or Subject Project. This skill ships no credential, provider SDK, external service configuration or implicit ability to fetch private images.

## Capability preflight

Resolve generation/edit support, actual image attachment transport, relevant format/ratio limits, access to required original/approved transport bytes, validator visibility, and trusted deterministic/local hook execution. Distinguish usable input images from strings describing them.

Capability gaps are `BLOCKED`; never simulate a missing image tool or weaken required evidence. Do not transmit private assets to a different service without authorization. A pack locator is not an instruction to install code or broaden provider permissions.

## Request contract

Pass the verified frozen semantic packet plus an adapter-owned binding table. Each selected canonical/external/continuity image and edit/preview base needs a receipt: image ID, actual handle, checksum, packet digest, materialization and attachment status. Only permitted transport variants may substitute for the source bytes.

Resolve approved project sources before fallback. Backend input limits do not allow silently dropping an image, merging identities, treating a board as a final image, or executing an edit as fresh unconstrained generation. Unsupported semantics require a Principal revision or a different authorized capable adapter.

`verify_transport` checks receipt consistency, not the truth of self-reported receipts. Actual host tool results and inspectable artifacts supply evidence. Test handles and fixture hashes cannot certify production transport.

## Response and failure

Return request/attempt identity, packet digest, exact candidate image and checksum, backend/version, execution status and actual input receipts. Transport errors are dependency failures, not visual HARD_RESET classifications. Do not create a result with invented image pixels or a fake visual PASS.

Repeated network retrieval of the same completed attempt is not a new sample. A new stochastic call follows the bounded recovery contract. After an automatic recovery budget is spent, adapter internals must not hide extra generations behind a request retry.

## Native-agent execution

When an active host exposes a native image tool, map the frozen specification and actual usable references into that tool's supported invocation. Follow the tool's own schema and output conventions rather than copying provider arguments from this document. If required role isolation or image transport cannot be established on that surface, stop with the specific dependency unavailable.
