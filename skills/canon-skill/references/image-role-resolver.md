# Image Role Resolver

Image Role Resolver assigns the operational role of every usable image before any external-reference routing or canonical evidence selection.

Roles answer "what is this image allowed to be in this operation?" Authority answers "how strongly may its evidence control the result?" Keep those concepts separate.

## Precedence

Resolve primary image roles in this order:

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

A lower-precedence interpretation must never silently replace a higher-precedence role.

## Role definitions

`PROTECTED_CANONICAL` applies to assets registered by the resolved Subject Pack as canonical or approved calibration evidence. They remain subject-owned evidence even when the same asset was attached directly to the prompt.

`EDIT_TARGET` applies when the operation explicitly edits image pixels or a runtime edit contract names the image as the target. The target is the source state to preserve except where the edit contract authorizes change.

`PREVIEW_SHOT_REFERENCE` applies to preview material linked by provenance to a shot definition. It may communicate pose, camera, composition, staging, or other planned shot properties, but it is not automatically an edit target, a final master, or canonical identity evidence.

`ACCEPTED_CONTINUITY` applies only to an accepted clean master admitted under the continuity rules. It retains its clean-master provenance and may supplement canon for series consistency.

`EXPLICIT_EXTERNAL_ROLE` applies when the principal explicitly authorizes one or more external-reference roles.

`ORIGINAL_PROMPT_REFERENCE` is the conservative fallback for an image supplied with the task that has no higher-precedence provenance and no explicit role map.

## Inputs

For each image, consider:

```yaml
image_id:
origin:
subject_pack_asset_id:
clean_master_provenance:
preview_provenance:
explicit_external_roles:
edit_target_signal:
prompt_attachment:
```

Also consider `selected_shot`, `edit_target`, `edit_contract`, and `preview_shot_reference` from Runtime State.

Do not classify from visual similarity alone when provenance or explicit task semantics are available.

## Output contract

Produce one binding per image:

```yaml
image_id: image-02
primary_role: EDIT_TARGET
authority: ACCEPTED_CONTINUITY
provenance:
  clean_master_id: master-B3-r2
secondary_roles: []
allowed_influence:
  - source_pixels
denied_influence:
  - canonical_identity_override
notes:
  - continuity provenance retained even though edit-target role wins
```

`authority` may describe the image's evidence class even when its current operational role is different. For example, an accepted clean master can become the edit target while retaining `ACCEPTED_CONTINUITY` provenance.

## Edit target rules

An explicit edit instruction has operational priority over reference use.

For "replace the background in this image," bind that image as `EDIT_TARGET`. Do not infer POSE, CAMERA, or COMPOSITION reference roles merely because those properties are visible.

Additional external roles for an edit target require explicit authorization and must not weaken the edit contract's preserve constraints.

Delivery derivatives may not become edit targets for canon-preserving work when the accepted clean master is available. If only a delivery derivative is supplied and fidelity depends on the clean master, block with `EDIT_TARGET_UNAVAILABLE`.

## Preview rules

When a request names an existing shot and includes that shot's preview, bind the preview as `PREVIEW_SHOT_REFERENCE`.

"Generate B3" means generate from B3's frozen or revised shot definition, using the preview only as approved preview evidence. It does not mean "upscale this preview cell."

If the principal explicitly asks to edit the preview pixels themselves, `EDIT_TARGET` takes precedence, while preview provenance remains recorded.

## Continuity rules

Only images already admitted as accepted continuity may receive `ACCEPTED_CONTINUITY`.

A generated image with no acceptance provenance is `GENERATED_UNVERIFIED` evidence and is not eligible for this role even if it visually matches the current series.

When an accepted continuity image is explicitly edited, `EDIT_TARGET` becomes its operational role, but continuity authority still cannot replace canonical identity or structure.

## Explicit external roles

Baseline explicit roles are:

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

Explicit role assignment controls external influence only after higher-precedence operational roles are protected.

An explicit external role cannot demote a canonical asset, convert a preview into a final master, or promote unverified generation history into continuity.

## Fallback rules

`ORIGINAL_PROMPT_REFERENCE` is deliberately weak. It may support only non-canonical attributes that are clearly requested by the prompt and must not override primary-subject identity or structural invariants.

If fallback influence cannot be separated safely from canonical identity or structure, leave it unresolved for External Reference Router to block rather than broadening its authority.
