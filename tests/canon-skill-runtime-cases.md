# Canon Skill Runtime Conflict Cases

Use these cases to forward-test the Day 2 runtime contracts. Each case assumes a valid Subject Pack is already resolved unless the case states otherwise.

## Route resolution

| Case | Expected result |
| --- | --- |
| `shot_registry` contains B3; request: "Generate B3." | Route = `EXISTING_SERIES_SHOT`, shot = B3. A B3 preview attachment does not change the route to preview editing. |
| B3 is selected; request: "Retry this shot." | Route = `CURRENT_SHOT_OPERATION`; reuse the current frozen packet semantics when retry is otherwise allowed. |
| Request: "Make a preview board for these four planned shots." | Route = `PREVIEW_ONLY` with series context retained in runtime state. |
| Request: "Create four final shots with one shared ratio." | Route = `SERIES`; compile the ratio into the series lock. |
| Request: "Run the declared rear diagnostic calibration." | Route = `CALIBRATION` only when the Subject Pack enables and declares that calibration capability. |
| No selected shot; request: "Retry this." | `BLOCKED / SPEC_UNRESOLVED`; do not infer the target from the newest image. |

## EDIT_TARGET versus reference

| Case | Expected result |
| --- | --- |
| User attaches an accepted clean master and says "replace only the background." | Primary image role = `EDIT_TARGET`; retain accepted provenance, protect subject scopes in the edit contract, and do not infer pose/camera roles. |
| User attaches the same image and explicitly says "edit the background and also preserve this exact composition." | Primary role remains `EDIT_TARGET`; composition preservation belongs in the edit contract rather than downgrading the image to an external reference. |
| User supplies only a watermarked delivery derivative while an accepted clean master is required for fidelity. | `BLOCKED / EDIT_TARGET_UNAVAILABLE`; the derivative does not become the clean master. |

## Preview versus final

| Case | Expected result |
| --- | --- |
| B3 exists with a preview cell; request: "Generate B3 final." | Preview image role = `PREVIEW_SHOT_REFERENCE`; final generation uses B3's shot definition plus canonical evidence. Do not upscale or treat preview pixels as the final source. |
| User says "paint over this preview itself." | The preview becomes `EDIT_TARGET` because explicit pixel editing outranks preview-reference use; preview provenance remains recorded. |
| A preview visually resembles the subject more than the canonical reference. | Canonical evidence remains higher authority; preview does not become identity evidence. |

## Canonical versus external identity

| Case | Expected result |
| --- | --- |
| Canonical robot + external human reference explicitly assigned `POSE`. | External plan allows pose only and adds `NO_EXTERNAL_IDENTITY_TRANSFER`; robot identity and structure come from Canon. |
| Canonical pet + external animal reference assigned `LIGHTING`. | Lighting may transfer; face geometry, coat pattern, body structure, and other canonical groups cannot transfer. |
| User says "use this external person as the primary identity reference" without changing the Subject Pack. | Do not route external primary identity; require a subject-owned canon update process or block the incompatible request. |

## Continuity versus Canon

| Case | Expected result |
| --- | --- |
| Accepted shot A1 is relevant to B1's environment continuity and canonical evidence is available. | Include A1 only as `continuity_evidence`; canonical evidence remains present. |
| Accepted shot A1 is available but the canonical identity asset required by B1 is missing. | `BLOCKED / CANONICAL_EVIDENCE_UNAVAILABLE`; continuity cannot replace Canon. |
| Latest generated shot looks correct but has not passed acceptance. | It remains `GENERATED_UNVERIFIED` and cannot enter `continuity_auxiliaries`. |

## Explicit role versus default role

| Case | Expected result |
| --- | --- |
| User says "use image 2 only for lighting." | Image 2 = `EXPLICIT_EXTERNAL_ROLE` with `LIGHTING`; no `ORIGINAL_PROMPT_REFERENCE` fallback influence remains for that image. |
| User says only "use this reference," and the prompt provides no safe non-canonical dimension. | `BLOCKED / SPEC_UNRESOLVED`; do not grant broad reference authority. |
| User attaches an image with no explicit role but says "match the camera angle shown here." | Router may preserve the prompt-explicit camera scope under conservative fallback; identity and structure remain denied. |

## Minimum evidence selection

| Case | Expected result |
| --- | --- |
| Human fixture, frontal close-up. | Select the front identity evidence needed by the matched close-up profile; do not attach unrelated full-body/rear evidence. |
| Pet fixture, full-body shot. | Select the full-body reference covering identity, coat, body, and tail groups according to the fixture profile. |
| Virtual fixture, rear shot. | Select matching rear canonical evidence; diagnostic-only calibration may be used for validation but not generation when marked ineligible. |
| External pose reference covers the desired pose but canonical identity coverage is missing. | External pose does not satisfy canonical coverage; block. |

## Session isolation

| Case | Expected result |
| --- | --- |
| A new session begins after a prior session accepted B3. | Do not auto-restore B3 selection, clean master, edit target, gates, packet, or continuity state. Resolve durable Subject Canon only. |
| Principal explicitly imports prior B3 state with verified provenance. | Restore only requested fields under `SESSION_IMPORT`; imported images retain their prior authority and do not become Canon. |
