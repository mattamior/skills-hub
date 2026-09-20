# Architecture Boundary

Canon Skill owns how a subject's Canon is respected. Subject Projects own subject truth. A consumer depends on this skill; the skill never imports a particular consumer repository, calibration scheme, face, marking, product geometry or filename.

## Entry and mode routing

Start with [begin](begin.md), then use [Prompt Mode](prompt-mode.md) to compile intent or [Gen Mode](gen-mode.md) to execute it. Both share the [authority model](authority-model.md); only Gen Mode plans and transports canonical generation assets.

## Ownership

Canon Skill owns generic routes, image-role precedence, reference isolation, evidence coverage, packet freeze/revision, validation outcomes, recovery limits, hook lifecycle and continuity boundaries. Subject Packs own written facts, invariant groups, reference profiles, calibration scopes, subject validators, deterministic feature logic, defaults, gates and delivery policies.

Backends own supported image transport, edit/mask submission, result retrieval and capability reporting. A provider limitation is a blocked capability, not permission to redefine the Subject Pack.

## State and provenance

All [runtime state](runtime-state.md) is session-local by default. Only durable Subject Canon crosses sessions automatically. Explicit import restores only authorized fields with provenance; it never restores stale handles, infers approvals, or promotes generated history.

Keep `CONSTRUCTION_INTERMEDIATE`, `CLEAN_MASTER_CANDIDATE`, `ACCEPTED_CLEAN_MASTER` and `DELIVERY_DERIVATIVE` distinct. Preview and diagnostic acceptance has limited output scope and cannot mint clean-master provenance. Only eligible, fully validated masters may enter [continuity](continuity.md).

## Generic extension points

Use [Subject Pack policies](subject-pack.md), [hook stages](hooks.md), and [transport capabilities](transport.md), not named-subject conditionals. A pack may narrow automatic retries to zero, require a single primary profile or mandatory evidence, defer declared construction invariants until finalization, and define a delivery-only mark. None of those policies may weaken final Canon, admit a failed output to continuity, or widen the automatic retry cap beyond one.

## Executable support

The standard-library [contract helpers](../scripts/contract_runtime.py) provide deterministic building blocks. [Schemas](../assets/schemas/subject-pack.schema.json) define portable data shapes. Agent instructions remain the runtime orchestration contract: these helpers do not implement visual perception, any real subject's hooks, an image model or an authorized asset store. Tests with simulated bytes are contract tests, not evidence of actual visual fidelity.
