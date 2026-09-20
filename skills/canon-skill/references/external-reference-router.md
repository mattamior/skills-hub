# External Reference Router

External Reference Router converts resolved external image roles into explicit allowed influence, denied influence, and contamination guards.

It runs only after Image Role Resolver. It must not reclassify edit targets, previews, continuity images, or protected canonical assets.

## External-reference modes

Runtime State uses one of three v1 modes:

- `NONE` — no external-reference evidence is active.
- `ROLE_SCOPED` — every active external reference has an explicit allowed role map.
- `CONSERVATIVE_FALLBACK` — one or more `ORIGINAL_PROMPT_REFERENCE` images remain and are restricted to prompt-explicit non-canonical influence.

If any explicit role mapping exists, preserve it exactly. Do not widen an explicit map because another image uses fallback mode.

## Baseline roles

The v1 external roles are:

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

These roles describe reusable visual functions. They do not grant authority over the canonical primary subject's identity or structure.

## Routing record

For each external reference, produce:

```yaml
image_id: external-01
authority: ROLE_SCOPED_EXTERNAL_REFERENCE
roles: [POSE, CAMERA]
allowed_influence:
  - primary_subject.pose
  - camera.view
denied_influence:
  - primary_subject.identity
  - primary_subject.structural_invariants
risk_guards:
  - NO_EXTERNAL_IDENTITY_TRANSFER
  - PRESERVE_CANONICAL_STRUCTURE
source: explicit_role_map
```

Use generic paths or invariant-group identifiers supplied by the compiled spec. Do not invent human-specific body parts or subject features in the router.

## Role isolation

Map each role to only the operation dimensions it authorizes.

- `POSE` may influence articulated pose or subject orientation but not identity geometry.
- `CAMERA` may influence view, lens language, perspective, or camera position.
- `COMPOSITION` may influence framing and spatial arrangement.
- `LIGHTING` may influence direction, intensity relationships, contrast, and illumination character.
- `WARDROBE` may influence wearable items only when the Subject Pack or effective spec allows wardrobe variation.
- `ENVIRONMENT` may influence background, setting, and scene context.
- `OBJECT` may introduce or define a requested prop or object without donating primary-subject identity.
- `SECONDARY_SUBJECT` may define an explicitly requested additional subject while remaining isolated from the canonical primary subject.
- `ORIGINAL_PROMPT_REFERENCE` is limited to non-canonical properties explicitly requested by the prompt.

If a role conflicts with a series lock, edit preserve constraint, or Subject Pack invariant, the higher-authority constraint wins.

## External identity contamination

External references must not donate primary-subject identity by default.

When an external image contains a person, animal, character, product, robot, or other potentially identity-bearing subject, add `NO_EXTERNAL_IDENTITY_TRANSFER` unless the external subject is explicitly routed as `SECONDARY_SUBJECT`.

`SECONDARY_SUBJECT` authorizes that additional subject to appear; it still does not authorize it to overwrite or blend with the canonical primary subject.

If the principal intends an external image to become authoritative primary-subject identity evidence, that is a Subject Pack update or another explicit subject-owned process, not ordinary external-reference routing.

## Edit operations

For edits, route external references around the `EDIT_TARGET` and its `edit_contract`.

Example:

```yaml
edit_contract:
  change: [background]
  preserve: [primary_subject]
external_reference:
  roles: [ENVIRONMENT]
```

The router allows the external environment to guide the replacement background while explicitly denying changes to protected subject regions.

Do not infer pose or composition transfer from an environment reference unless those roles were separately authorized.

## Explicit role versus fallback

An explicit role map always wins over `ORIGINAL_PROMPT_REFERENCE` fallback for the same image.

If the prompt says "use image 2 only for lighting," the router records `LIGHTING` and removes any broad fallback influence. "Only" is a hard scope limiter.

If no role is explicit, fallback may use only prompt-explicit non-canonical properties. If the prompt merely says "use this reference" and safe influence cannot be determined, stop with `SPEC_UNRESOLVED`.

## Output to Evidence Planner

External Reference Router outputs `external_evidence` candidates plus risk guards. Evidence Planner does not upgrade their authority.

External evidence may satisfy camera, pose, composition, lighting, wardrobe, environment, object, or secondary-subject requirements. It must not satisfy missing canonical identity or structural coverage.
