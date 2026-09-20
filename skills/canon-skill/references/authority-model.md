# Evidence Authority Model

Canon Skill resolves visual conflicts by authority and role, not by image recency. Every piece of evidence must have an explicit provenance class and, when externally supplied, an allowed role.

## Base authority hierarchy

The default authority order is:

```text
WRITTEN_CANON
  >
CANONICAL_VISUAL
  >
APPROVED_CALIBRATION
  >
ROLE_SCOPED_EXTERNAL_REFERENCE
  >
ACCEPTED_CONTINUITY
  >
PREVIEW_ONLY
  >
GENERATED_UNVERIFIED
```

A Subject Pack may narrow the scope of an item, but it must not invert this hierarchy in a way that lets convenience evidence overwrite canonical identity or structure.

Higher authority does not mean every higher-ranked asset must be attached to every generation. Evidence Planner still selects the minimum role-relevant subset.

## Evidence classes

`WRITTEN_CANON` is durable written subject truth. It governs named invariants, exclusions, and subject-owned constraints.

`CANONICAL_VISUAL` is the primary visual authority for identity, structure, surface, silhouette, materials, or other declared invariant regions.

`APPROVED_CALIBRATION` is validated view- or diagnostic-specific evidence. It may carry strong authority for its declared regions and view, but its scope must be explicit.

`ROLE_SCOPED_EXTERNAL_REFERENCE` is user- or task-provided evidence whose influence is restricted to authorized roles.

`ACCEPTED_CONTINUITY` is an accepted clean master admitted only to preserve series continuity. It supplements canon and never replaces canonical authority.

`PREVIEW_ONLY` is compositional or selection evidence. It may describe a planned shot or chosen preview state but does not become final identity authority.

`GENERATED_UNVERIFIED` is any generated output that has not passed the required validation and acceptance gates. It must never enter the identity chain.

## External reference roles

External evidence must be role-scoped before it can influence generation. Baseline roles include:

```text
POSE
CAMERA
COMPOSITION
LIGHTING
WARDROBE
ENVIRONMENT
OBJECT
SECONDARY_SUBJECT
ORIGINAL_PROMPT_REFERENCE
```

Additional generic roles may be introduced when they describe reusable visual functions rather than subject-specific facts.

An external image that contains another person, animal, character, product, or object must not donate identity to the canonical subject unless the Subject Pack and task explicitly authorize that identity role. In ordinary subject-preservation workflows, external identity is contamination risk.

## Image-role resolution precedence

Image Role Resolver runs before external-reference routing. The v1 precedence is:

```text
PROTECTED_CANONICAL
  >
EDIT_TARGET
  >
PREVIEW_SHOT_REFERENCE
  >
ACCEPTED_CONTINUITY
  >
EXPLICIT_EXTERNAL_ROLE
  >
ORIGINAL_PROMPT_REFERENCE
```

This prevents an uploaded edit target from being reinterpreted as a pose reference and prevents a preview cell from being treated as an implicit final-quality source.

When one image appears eligible for multiple roles, bind the highest-precedence role first, then explicitly add any additional allowed roles. Do not infer lower-priority roles from visual similarity alone.

## Conflict resolution

When evidence conflicts:

1. identify each item's authority class;
2. limit each item to its declared scope or role;
3. preserve higher-authority canonical invariants;
4. use lower-authority evidence only where it does not contradict those invariants;
5. block execution when the conflict cannot be resolved without guessing.

Do not solve conflicts by choosing the newest image, the most photorealistic image, the largest image, or the last-generated image.

## Continuity admission

Only an `ACCEPTED_CLEAN_MASTER` may become `ACCEPTED_CONTINUITY`.

The following are prohibited from continuity admission:

- previews;
- failed generations;
- `HARD_RESET` results;
- unverified history;
- delivery-only derivatives;
- watermarked derivatives;
- construction intermediates.

Continuity evidence may help preserve pose-adjacent styling, environment, camera language, wardrobe state, or other series consistency that has already been accepted. It cannot override Subject Canon.

## Generated-image chain prohibition

A sequence of accepted generations must never become a self-referential identity chain with no canonical anchor. Every generation that depends on continuity still requires the canonical evidence needed for the shot under the Subject Pack's reference profiles.
