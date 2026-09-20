# Contract Tools

Use [contracts.py](../scripts/contracts.py) for repeated deterministic checks, not visual judgment. The JSON Schemas use Draft 2020-12 and only bundled references; input data cannot choose a remote schema or executable hook.

## Commands

```bash
python scripts/contracts.py validate-pack subject-pack.json
python scripts/contracts.py validate-spec generation-spec.json
python scripts/contracts.py freeze packet.json
python scripts/contracts.py verify frozen-packet.json
python scripts/contracts.py compare frozen-a.json frozen-b.json
```

Paths above are relative to the installed skill directory. JSON input rejects duplicate object keys and non-finite constants. The Python dependency is jsonschema; the repository validation environment pins its version. `compare` exits 1 for unequal valid packets; dependency/contract/input errors exit 2.

The importable helpers additionally resolve normalized routes and image roles, isolate external role declarations, select minimum canonical covers, aggregate supplied validation reports, bound retry actions, initialize fresh state, and check transport/continuity records.

## Safety and limits

The helpers do not parse ambiguous natural-language intent, judge images, locate landmarks, generate/edit pixels, load arbitrary pack code, fetch assets, certify truthful receipts or grant Principal approval. These remain host/Subject Pack responsibilities.

Fixtures and mock reports are declaration-only tests. Their NO_IMAGE-label hashes and fixture-only handles must never be used as live transport or promoted to accepted continuity. Keep simulation evidence separate from real consumer acceptance.

Use [Subject Pack](subject-pack.md), [Generation Packet](generation-packet.md), [hooks](hooks.md) and [backend](generation-backend.md) alongside executable checks. A passing helper is necessary for its machine-readable contract, not sufficient for safe actual generation.
