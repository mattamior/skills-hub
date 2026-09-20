# Architecture Boundary

Canon Skill is a subject-agnostic runtime contract for stable visual generation. It knows how to respect canon, but it does not own the facts that define any particular subject.

## Dependency direction

The dependency direction is one-way:

```text
Canon Skill
    ↑
Subject Project / Subject Pack
```

A Subject Project may depend on Canon Skill. Canon Skill must not depend on a specific Subject Project, subject name, reference filename, calibration numbering scheme, facial feature, coat marking, emblem, or other subject-owned fact.

Generation backends are separate execution dependencies. Backend adapters may translate a frozen Generation Packet into provider-specific requests, but backend limitations must not redefine Subject Canon.

## Ownership split

Canon Skill owns runtime semantics:

- authority ordering and conflict resolution;
- image-role resolution and external-reference isolation;
- evidence planning from Subject Pack profiles;
- Prompt Mode and Gen Mode boundaries;
- Generation Packet freeze, retry, and revision semantics;
- generic validation stages and result classifications;
- continuity admission rules;
- hook lifecycle invocation;
- clean-master provenance and delivery boundaries;
- session-local runtime behavior.

The Subject Pack owns subject truth and subject-specific capabilities:

- written canonical facts and invariant groups;
- canonical reference inventory and reference profiles;
- approved calibration evidence;
- subject-specific identity or structure validators;
- deterministic postprocess hooks;
- delivery policies that are specific to the subject;
- feature semantics such as markings, emblems, decals, geometry, or other named canonical details.

The generation backend owns transport and provider execution:

- request serialization;
- supported image/reference attachment mechanisms;
- backend-specific randomness or seed controls;
- edit-mask or image-edit transport;
- provider result retrieval;
- backend capability reporting.

## Prompt Mode and Gen Mode

Prompt Mode compiles intent. It may analyze user-provided references, assign roles, build an effective generation spec, manage shot definitions, apply series locks, and perform prompt QA. It must not load generation-only canonical assets, run image generation or editing, or mutate accepted clean-master continuity.

Gen Mode executes a frozen intent. It loads the Subject Pack, selects and transports evidence, invokes generation or editing, runs hooks and validators, classifies results, applies allowed recovery, updates continuity after acceptance, and produces delivery derivatives.

The two modes share the same canon and authority model. Gen Mode may not silently redesign a Prompt Mode specification.

## Session isolation

Runtime state is session-local and transient by default. A new session inherits durable Subject Canon only.

The following do not automatically cross sessions:

- shot registry and selected shot;
- preview selection and preview gates;
- identity or operation gates;
- edit targets and edit contracts;
- temporary styling;
- generated images;
- clean masters;
- continuity auxiliaries created during the prior session;
- frozen Generation Packets and retry counters.

Cross-session restoration requires explicit `SESSION_IMPORT` semantics. Imported state must retain provenance and must not be promoted into Subject Canon merely because it was imported.

## Clean-master boundary

Keep four provenance classes distinct:

1. `CONSTRUCTION_INTERMEDIATE`
2. `CLEAN_MASTER_CANDIDATE`
3. `ACCEPTED_CLEAN_MASTER`
4. `DELIVERY_DERIVATIVE`

Only `ACCEPTED_CLEAN_MASTER` is eligible to become continuity auxiliary evidence. Delivery-only transformations such as watermarking, resizing, sharpening, format conversion, compositing, or export decoration must not flow back into identity or continuity authority.

## Extension rule

When a new requirement appears, first ask whether it describes:

- how any subject's canon should be respected;
- a fact or feature of one subject;
- a provider-specific transport capability.

Only the first category belongs in Canon Skill. If a generic extension is needed, express it as a role, invariant group, profile, validator interface, hook stage, policy, or other subject-agnostic contract rather than adding a named subject exception.
