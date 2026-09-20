# Evidence Authority Model

Resolve evidence by declared authority and scope, never by recency, visual appeal or attachment order. This hierarchy governs visual evidence only; it does not override host permissions, safety requirements or instruction authority.

## Base hierarchy

```text
WRITTEN_CANON
  > CANONICAL_VISUAL
  > APPROVED_CALIBRATION
  > ROLE_SCOPED_EXTERNAL_REFERENCE
  > ACCEPTED_CONTINUITY
  > PREVIEW_ONLY
  > GENERATED_UNVERIFIED
```

Written Canon owns durable facts and invariants. Canonical visuals provide primary identity/structure evidence. Approved calibration contributes only its declared view/regions. External references contribute only authorized operation dimensions. Accepted continuity corroborates Canon and carries scoped series state. Previews carry planned or selected shot geometry. Unverified generated images supply no identity or continuity authority.

A higher-ranked item is not automatically relevant to every shot. Evidence planning still selects the minimum adequate subset subject to required assets and subject policy. Authority is scoped: a structural calibration image does not acquire authority over incidental facial or material details merely because they are visible.

## Role isolation

Apply [Image Role Resolver](image-role-resolver.md) before [External Reference Router](external-reference-router.md). Protect canonical assets, explicit edit bases, selected preview geometry and verified continuity before assigning external roles.

The external router supports baseline pose, camera, composition, lighting, wardrobe, environment, object and secondary-subject roles plus explicit generic non-identity extensions. `NON_HUMAN_SUBJECT` remains a supported narrower role; `SECONDARY_SUBJECT` is broader. Neither permits primary identity transfer. `ORIGINAL_PROMPT_REFERENCE` identifies conservative fallback provenance, whose allowed dimensions still require prompt or Subject Pack policy authorization.

Promoting an external image into primary identity authority requires a separate subject-owned Canon approval/update process. Ordinary routing cannot perform that promotion, even when the external image appears more attractive or recent than Canon.

## Conflict handling

Identify each item's authority and scope, intersect it with the frozen effective specification and preserve constraints, and retain higher-authority invariants. Lower-authority evidence may fill only allowed, non-conflicting dimensions. Unresolved conflicts block instead of producing an invented compromise.

A Subject Pack can narrow influence, require a particular profile/asset or disable optional recovery. It cannot let unverified generations replace Canon, grant an external subject the primary identity, or erase final invariants merely to pass validation.

## Generated-image chain prohibition

Only an eligible, fully validated and approved clean master may be admitted as accepted continuity. Previews, diagnostics, construction intermediates, failed generations, refine-only candidates, delivery copies and watermarked derivatives are prohibited.

Each later generation independently requires the canonical evidence selected for its own shot. Continuity supplements Canon; it never replaces Canon. An imported or newly generated image does not gain authority from its timestamp, transport availability or presence in chat history.
