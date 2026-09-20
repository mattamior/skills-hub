# Begin a Canon task

Resolve the requested deliverable before loading images. A request for a prompt is not authorization to generate; a request to develop this skill is repository work, not a subject-generation task.

## Discover and bind

Find an explicitly supplied Subject Pack or the active Subject Project's declared pack locator. Do not scan unrelated projects, select a person from memory, or invent a default subject. Resolve one subject id and immutable pack revision; conflicting or missing locators block with `SUBJECT_PACK_UNAVAILABLE` or `SPEC_UNRESOLVED`.

Load written authority and capability metadata only as needed. A pack may consist of an entry manifest plus source-owned metadata normalized by its consumer adapter. The resolved manifest must satisfy [the Subject Pack contract](subject-pack.md) and [schema](../assets/schemas/subject-pack.schema.json). A source pointer alone is not proof that image bytes are usable.

Initialize [fresh runtime state](runtime-state.md). Prior-session shot selections, gates, images, styling and packets remain quarantined unless the current Principal explicitly requests a scoped `SESSION_IMPORT`. Re-resolve assets and approvals against current Canon; do not import old tool handles or automatic-retry permissions.

## Select exactly one active mode

For analysis, reference transcription, shot planning or copy-ready specifications, use [Prompt Mode](prompt-mode.md). It reads written Canon and compiler policy, not canonical image inventories, generation reference profiles or image transports.

For actual images, edits, identity checks, preview boards, selected final shots, or explicit retries, use [Gen Mode](gen-mode.md). It discovers and materializes only the evidence required at the current authorized stage.

For a mixed request, finish the Prompt handoff first, then transition explicitly into Gen Mode. No canonical image bootstrap occurs during the Prompt portion. An instruction to continue a series does not waive a still-required identity approval or choose a preview cell on the Principal's behalf.

## Capability failure

Use the active host's real capabilities, not presumed tool names or invented identifiers. Missing image generation, deterministic processing, required validators, source transport or approval produces a specific blocked dependency. Never report an image as generated or accepted when only a specification, script, schema check or simulated run exists.
