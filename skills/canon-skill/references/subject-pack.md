# Subject Pack Contract

A Subject Pack is the subject-owned input contract consumed by Canon Skill. It defines durable canonical truth, the evidence that supports that truth, and optional subject-specific validation, hooks, and delivery behavior.

Canon Skill must be able to consume Subject Packs for humans, animals, virtual characters, products, robots, or other stable visual subjects without changing its core schema.

## Required top-level shape

A v1 Subject Pack uses this minimum shape:

```yaml
subject:
  id: example-subject
  type: arbitrary-subject-class

canon:
  written_authority: []
  invariant_groups: []

references:
  inventory: []
  profiles: []
  bootstrap_policy: {}

calibration:
  enabled: false
  profiles: []

validators:
  identity: []
  structure: []
  local_quality: []

postprocess:
  hooks: []

delivery:
  policies: []
```

Fields may be extended by future compatible versions, but subject-specific concepts must not become required generic keys.

## Subject identity

`subject.id` is a stable project-scoped identifier. `subject.type` is descriptive routing metadata, not a hard-coded switch inside Canon Skill.

Canon Skill must not branch on values such as `human`, `pet`, or `robot` to discover mandatory body parts. Subject-specific behavior is declared through invariant groups, reference profiles, validators, and hooks.

## Canon

`canon.written_authority` contains durable written facts or references to authoritative written sources. Each entry should identify its provenance and scope so runtime conflicts can be resolved without relying on recency.

`canon.invariant_groups` describes features that must remain stable across generation. A group should use generic concepts such as:

```yaml
- id: primary-identity
  class: identity
  regions: [head, upper-body]
  constraints:
    - preserve distinguishing geometry
    - preserve canonical surface pattern
```

Recommended `class` values include `identity`, `structure`, `surface`, `silhouette`, `material`, and `symbol`, but packs may define additional classes when needed.

Do not require generic keys such as `face`, `hair`, `beauty_mark`, `coat`, or `human_anatomy`. Those are subject-owned semantics if a pack needs them.

## Reference inventory

`references.inventory` registers durable visual evidence. Each record should include enough metadata to determine authority, view, visible regions, generation eligibility, and provenance.

Example:

```yaml
- id: canonical-front
  asset: asset://subject/canonical-front
  authority: CANONICAL_VISUAL
  views: [front]
  visible_regions: [primary-identity, torso-structure]
  generation_eligible: true
  diagnostic_only: false
```

`asset` may be a repository path, project asset identifier, or another transportable locator understood by the active Subject Project. Canon Skill treats it as opaque until a generation backend adapter resolves transport.

## Reference profiles

`references.profiles` lets the Subject Pack describe minimum role-relevant evidence sets without forcing Canon Skill to send every canonical reference into every shot.

Example:

```yaml
- id: front-closeup
  match:
    views: [front, three-quarter-front]
    framing: [close-up, bust]
  require:
    invariant_groups: [primary-identity]
  prefer_assets: [canonical-front]
```

Evidence Planner selects the smallest profile-supported evidence set that covers the shot's required invariant groups and view constraints. If no profile satisfies required canon, generation is blocked rather than silently weakening evidence.

`references.bootstrap_policy` defines whether and how a subject may begin work when normal evidence is incomplete. Bootstrap policy never elevates generated images above the authority model.

## Calibration

Calibration is optional and generic:

```yaml
calibration:
  enabled: true
  profiles:
    - id: side-diagnostic
      purpose: verify side geometry
      visible_regions: [profile-structure]
      authority_assets: [calibration-side]
      generation_eligible: false
      diagnostic_only: true
```

Canon Skill understands approved calibration authority, matching-view calibration, generation eligibility, and diagnostic-only evidence. It does not interpret subject-specific calibration numbering or feature names.

## Validators

Validator declarations may reference generic runtime validators or subject-provided implementations.

```yaml
validators:
  identity:
    - id: stable-identity
      required_for: [FINAL]
  structure:
    - id: primary-geometry
      required_for: [FINAL]
  local_quality:
    - id: surface-integrity
      required_for: [FINAL]
```

Subject-provided validators may inspect subject-specific regions or semantics, but they report through the generic validation/result model.

## Hooks

Hooks provide deterministic subject-specific processing without teaching Canon Skill the feature itself.

```yaml
postprocess:
  hooks:
    - id: canonical-detail-finalize
      stage: POST_GENERATION
      required_for: [FINAL]
```

Supported lifecycle stages are expected to include `PRE_GENERATION`, `POST_GENERATION`, `PRE_VALIDATION`, `POST_VALIDATION`, and `PRE_DELIVERY`. Canon Skill invokes declared hooks; the Subject Pack owns their behavior.

## Delivery policies

`delivery.policies` declares subject-specific output requirements such as mandatory finalization hooks, permitted derivative types, or export constraints. Delivery policy cannot promote a derivative into canonical or continuity authority.

## Capability variability

A valid pack may omit calibration, custom hooks, custom validators, or specialized delivery rules. Runtime code must feature-detect declared capabilities instead of assuming every Subject Pack implements the same workflow.

The anonymous fixtures demonstrate the same contract across three subject classes:

- [human fixture](fixtures/human.yaml)
- [pet fixture](fixtures/pet.yaml)
- [virtual-character fixture](fixtures/virtual-character.yaml)

If a requirement cannot be expressed naturally across these classes without adding a subject-specific generic field, revise the contract before extending runtime implementation.
