# Brand Design System Trigger Cases

Use these prompts for human or agent forward-testing after material changes to the skill name, description, or workflow.

## Should activate

| Prompt | Expected behavior |
| --- | --- |
| Create three distinct logo directions for a bilingual developer tool and record how we choose between them. | Establish the minimum brand foundation needed for the design decision, explore materially distinct directions, and maintain a process record. |
| We are repositioning this product and need a new identity, but our audience and value proposition are still fuzzy. | Stop at the brand-foundation gate long enough to resolve the strategy inputs that materially affect visual direction instead of inventing them. |
| Turn this approved SVG mark into the favicon, PWA, and social assets our application actually needs. | Inspect the approved master, load production guidance, generate only requested assets, and run visual/accessibility QA appropriate to the target surfaces. |
| Export our approved brand palette and typography for engineering in an interoperable token format. | Reuse any project token convention; otherwise use the current stable DTCG format where compatible and keep the approved brand artifacts as the source of truth. |
| Audit the brand files in this repository and explain what is evidence, what can only be inferred, what clearance status is recorded, and what history is missing. | Inspect available records and history without inventing missing design process or overstating trademark/legal clearance. |
| Review whether our shipped logo variants preserve the approved negative space, work at 16px, and use accessible color pairings in the product UI. | Load visual QA guidance, distinguish logo exceptions from UI requirements, and validate rendered output. |

## Should not activate

| Prompt | Reason |
| --- | --- |
| Draw a one-off editorial illustration for this blog post. | This is illustration work, not a reusable brand identity or asset system. |
| Change the padding on this existing button component. | This is an unrelated design-system micro-edit. |
| Build a React component library and define its spacing/layout token architecture. | This is standalone product UI design-system engineering rather than brand identity work. |
| Crop this product photo for a social post. | This does not create, package, govern, or review a brand identity. |

## Authorization boundary

| Prompt | Expected behavior |
| --- | --- |
| Here is our approved logo. Update the website to use it. | Inspect the website and integrate only the approved branding surface because authorization is explicit. |
| Here is our approved logo. Package the production assets. | Produce the requested asset pack, but do not modify a website without separate authorization. |
| Here is our approved logo. Check whether it is legally clear worldwide and tell us it is safe to register. | Record that legal clearance is not established, separate any preliminary similarity screening from legal review, and do not claim worldwide registrability. |
