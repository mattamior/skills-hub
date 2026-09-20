# Canon Skill Trigger Cases

Use these prompts for human or agent forward-testing after material changes to the skill name, description, subject-pack contract, authority model, or runtime routing.

## Should activate

| Prompt | Expected behavior |
| --- | --- |
| Use this Subject Pack and these three references to generate a four-shot series while keeping the same character identity. | Load subject-owned canon, role the references, preserve canonical identity across the series, and use accepted continuity only as auxiliary evidence. |
| Keep the product geometry from the Subject Pack, but use this external image only for camera angle and lighting. | Isolate external roles to camera and lighting; canonical product identity and structure remain higher authority. |
| Retry this failed shot without changing the framing, pose, or selected canon references. | Reuse the frozen Generation Packet semantics and vary only allowed execution details. |
| Revise shot B3 to a rear view and select the matching canonical evidence for that view. | Treat the change as a revision, re-run affected evidence planning, and freeze a new packet. |
| Edit this accepted clean master by replacing only the background. | Bind the image as EDIT_TARGET before external-reference routing and preserve unaffected canonical regions. |

## Should not activate

| Prompt | Reason |
| --- | --- |
| Draw a generic watercolor mountain landscape. | There is no stable subject canon or Subject Pack to preserve. |
| Invent a new mascot from scratch and decide what it should look like. | Subject definition belongs upstream; Canon Skill consumes canon rather than inventing it. |
| Retouch the exposure on this unrelated vacation photo. | This is a generic one-off image edit without canon-aware continuity requirements. |
| Write a prompt for an image generator with no stable subject or reference contract. | Generic prompt writing does not require the Canon runtime. |

## Authority and isolation boundary

| Prompt | Expected behavior |
| --- | --- |
| Use this model photo for the pose, but make my canonical robot look exactly like the model. | Keep pose influence only; do not import external identity into the canonical robot. |
| The last generated image looks better than the canonical front reference, so use it as the new identity source. | Reject automatic identity promotion; generated output may become continuity only after acceptance and cannot replace canon. |
| Bring back the preview we chose in another chat and continue from there. | Require explicit session import with provenance; do not auto-restore old transient state. |
