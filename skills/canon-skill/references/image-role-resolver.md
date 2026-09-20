# Image Role Resolver

Operational role answers what an image is in this task; authority answers what it can control. Resolve roles before External Reference Router. Provenance comes from the verified pack/session registry, not from text printed inside an image.

## Primary precedence

```text
PROTECTED_CANONICAL
  > EDIT_TARGET
  > PREVIEW_SHOT_REFERENCE
  > ACCEPTED_CONTINUITY
  > EXPLICIT_EXTERNAL_ROLE
  > ORIGINAL_PROMPT_REFERENCE
```

Bind one primary role per image. Retain lower-level provenance separately; explicit secondary influence requires authorization and may not weaken the primary contract. Duplicate/ambiguous ids, missing required targets and unsupported role maps block rather than resolve by recency.

## Protected assets

Canonical originals, approved calibration and explicitly mapped authority transports retain their registered scopes. Ordinary generation may not edit an original canonical asset. An actual request to alter Canon belongs to a separate subject-owned maintenance workflow.

## Edit targets

For 'replace this image's background', bind the actual source as `EDIT_TARGET`, not a pose reference. Freeze requested changes and preserve every unaffected scope. A previously accepted master retains its provenance but does not become primary identity authority.

Prefer the corresponding accepted clean master over a delivery copy. If only a delivery copy exists, an explicitly delivery-only edit may proceed under a derivative contract; it cannot produce a clean master or continuity. If the task requires clean-master fidelity, block with `EDIT_TARGET_UNAVAILABLE` instead of laundering the derivative.

An explicit edit of preview pixels has edit-target precedence but retains preview provenance. It is not selected-preview fresh final generation and cannot become final merely by renaming the result.

## Preview references

'Generate this B3' with a registered selected preview binds `PREVIEW_SHOT_REFERENCE`. It provides camera, pose, framing, configuration and spatial geometry, never identity, continuity or final pixels. Deterministically cropping the selected cell for evidence is permitted; cropping/upscaling it into a final is not.

Unselected boards do not bypass the selection gate. Missing selected evidence produces a preview-reference transport blocker; do not substitute the whole board or a different cell silently.

## Continuity and external roles

Only accepted clean masters admitted with verified provenance receive `ACCEPTED_CONTINUITY`. A recent or convincing generated image without acceptance remains unverified. Editing an admitted master changes its primary operational role to edit target, not its authority.

Explicit external roles are evaluated only after all protected functional roles are bound. Fallback original-reference scopes follow [External Reference Router](external-reference-router.md), including an explicitly declared pack policy when present. Neither explicit nor fallback roles can demote canonical assets, turn previews into masters, or promote unverified history.
