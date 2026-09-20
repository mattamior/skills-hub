# Generation Packet

[Generation Packet schema](../schemas/generation-packet.schema.json) defines the v1 execution snapshot. [Generation Spec](../schemas/generation-spec.schema.json) is a separate Prompt Mode artifact and is never an already executable packet.

## Freeze

Freeze subject ID and pack revision; route, operation and output kind; effective spec, series lock and shot; written authority and canonical/external/continuity evidence; image roles, edit target and preview binding; preserve constraints, risk guards, hooks/versions, validators, required gates, retry and delivery policies. Include a construction policy only when the pack declares one.

Resolve semantic uncertainty first. Host preflight must separately verify actual images, trusted handlers and approvals; a schema-valid handler name is not a loaded implementation. Bind asset content hashes or approved transport variants before dispatch.

`contracts.py freeze` produces `{format, digest, payload}` using versioned canon-json-v1 serialization: UTF-8, sorted object keys, ordered arrays, finite JSON numbers. It is not an RFC 8785 claim or a cross-language signature standard. Byte fingerprints detect changes; they do not prove truthful validation or attachment receipts.

## RETRY

Reuse the same frozen payload and digest. Only approved transport handles/request IDs and stochastic sampling may vary. Adapter receipts must still identify the same authorized content/transport variants. Do not change camera, pose, scene, ratio, evidence membership/order/roles, edit base, preview selection, Canon, validators, hook requirements or delivery rules.

The runtime's CURRENT_SHOT_OPERATION dispatch label does not rewrite the packet's original route. Failed output is never an input to its fresh retry. No transport failure authorizes dropping required evidence or switching to text-only generation.

## REVISE

Start from the previous packet, apply only Principal-authorized field changes, re-resolve affected roles/evidence/gates and freeze a new shot/packet revision. A changed digest alone does not establish authorization. Preserve all untouched constraints.

The helper accepts exact existing object paths and requires a distinct revision ID; array surgery and unspecified changes are deliberately not inferred. New authorized work may assemble a new complete packet. Do not manufacture no-op revisions merely to reset the automatic retry budget.

## Provenance

Link every attempt, hook result, validation report, candidate and delivery derivative to the producing packet digest and exact image content. Validate again after any pixel mutation. A result classification never mutates its historical packet. Session import preserves these records but does not turn them into Subject Canon.
