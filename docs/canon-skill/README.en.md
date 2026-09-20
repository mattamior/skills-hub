# Canon Skill development and acceptance

[简体中文](README.zh.md)

## Delivered core

Canon Skill is an experimental agent-instruction runtime with deterministic contract helpers, not a bundled image model or visual identity detector. Its caller owns the Subject Pack and generation backend.

Day 1–4 cover the subject-agnostic contract, evidence authority, six routes, role isolation, minimum evidence selection, transient state, frozen packets, three validator layers, five result classes, bounded retry, provenance, Prompt/Gen handoff, staged hooks and transport abstraction. JSON Schemas and executable anonymous Human/Pet/Virtual declaration tests accompany the instructions.

Run `python -m unittest discover -s tests/canon-skill -v` with jsonschema and PyYAML. Existing Markdown scenario tables remain manual forward-test cases; gallery/installer CI is not a runtime or visual acceptance test. The additional Canon workflow runs actual unit tests and pinned upstream skill-creator validation.

## Consumer migration

Extract legacy behavior into GENERIC, SUBJECT_SPECIFIC and INFRASTRUCTURE categories without changing production routing. Build the Subject Pack in its own project, pin Canon Skill by immutable revision, and preserve source metadata with a drift check. Compare independently normalized legacy and pack-driven execution plans; do not count two calls to the same mapper as independent regression.

Test anchor IDs and order, conditional supports, external roles, edit/preview behavior, gates, retry, continuity, calibration, canonical-detail finalization and delivery provenance. Contradictory legacy rules must remain explicit cutover blockers rather than silently changing the generic contract.

Cut over only after semantic regression, actual image transport, trusted hook execution and required live acceptance evidence pass. Keep a reversible legacy entry point. Existing approved Canon/calibration assets must not be regenerated just to exercise a migration.

## Release gates

v0.1.0 requires the generic contract to serve three subject classes and all runtime/interface models to be defined and validated. A source candidate is not automatically a published release.

v0.2.0 additionally requires a real consumer Subject Pack, complete legacy-versus-Canon regression, preserved generation semantics, verified calibration mapping and subject-owned detail hooks. A declaration-only shadow test does not prove production image parity or authorize cutover.

v1.0.0 additionally requires at least two distinct real Subject Projects with successful actual consumption. Anonymous fixtures do not count. No synthetic PASS, self-declared attachment receipt, or unexecuted visual checklist may satisfy these gates.

## Boundaries retained

No concrete consumer facts, reference filenames or calibration numbering enter the reusable implementation. Required image/validator/hook/gate failures stay BLOCKED. Construction prechecks never become full acceptance, calibration can forbid automatic retry, and delivery derivatives never feed identity or continuity.
