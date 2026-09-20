# External Reference Router

Run only after Image Role Resolver. Do not reclassify protected canonical assets, edit targets, selected previews or admitted continuity images as ordinary external references.

## Modes and scopes

Use `NONE` when there are no qualifying external references, `ROLE_SCOPED` when all active references have explicit scopes, and `CONSERVATIVE_FALLBACK` when an original-prompt reference uses approved fallback dimensions. An explicit mapping always replaces fallback for that same image; it is never widened by another image's default mode.

Baseline roles are `POSE`, `CAMERA`, `COMPOSITION`, `LIGHTING`, `WARDROBE`, `ENVIRONMENT`, `OBJECT`, `SECONDARY_SUBJECT` and `NON_HUMAN_SUBJECT`. Supported generic extensions are `TEXTURE`, `TEMPORARY_STYLING`, `EXPRESSION` and `GAZE`. `ORIGINAL_PROMPT_REFERENCE` identifies fallback provenance; it is not unlimited identity authority.

Pose controls configuration, not identity geometry. Camera controls view/perspective; composition controls spatial arrangement. Wardrobe and temporary styling apply only to allowed variables. Texture controls capture/render treatment, not new canonical surface facts. Expression/gaze apply only where meaningful for the subject. An object or secondary-subject role never merges that subject's identity into the primary subject.

## Fallback policy

Absent explicit roles, use only non-identity dimensions authorized by the current prompt or a declared Subject Pack original-reference policy, and only where consistent with the effective spec. Without either authorization, 'use this reference' is unresolved and must block. A consumer may preserve a known original-photography-reference workflow through such a declared policy; Canon Skill does not invent a broad fallback on its own.

Record the policy source, resolved roles, allowed influence, denied influence and contamination guards. If multiple original references are present, choose the relevant subset for the current target; do not average incompatible poses or send every image into every shot.

## Authority and preservation

External references cannot replace canonical identity or structural evidence. Add `NO_EXTERNAL_IDENTITY_TRANSFER` for the primary subject even when an additional secondary subject is authorized. A request to make an external image primary identity is a subject-owned Canon update, not ordinary external routing.

The effective spec, edit preserve scopes and series locks constrain reference use. A background reference for an edit does not implicitly change pose or composition. A preview cell provides selected shot geometry only. Role-scoped evidence helps execute the specification; it cannot rewrite it.

## Output

```yaml
image_id: external-01
authority: ROLE_SCOPED_EXTERNAL_REFERENCE
roles: [POSE, CAMERA]
allowed_influence: [configuration, camera]
denied_influence: [primary_identity, structural_invariants]
risk_guards: [NO_EXTERNAL_IDENTITY_TRANSFER]
source: explicit_role_map
```

Carry these bindings into the packet's separate external channel. Required visual external evidence must actually be materialized for the backend. Missing transport blocks; successful use never promotes an external image to Canon or accepted continuity.
