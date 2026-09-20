# Canon runtime contract implementation checkpoint

Parent: ac528766004f81e6c905d0b5d3622c7da37086d3 (Day 3 topic branch). The new candidate is not yet authoritative main or a production deployment.

Implemented separate Prompt/Gen contracts, staged hooks, backend capability/receipt abstraction, eight Draft 2020-12 schemas, deterministic Python contract helpers and executable declaration regression. Corrected earlier broad wording: prior Markdown forward-test tables were not executable runtime tests, and prior gallery CI was not visual acceptance.

Local command: `python -m unittest discover -s tests/canon-skill -v`.
Observed: 75 tests passed on Python 3.13.5, jsonschema 4.26.0 and PyYAML 6.0.3. CI pins Python 3.12.14, jsonschema 4.25.1 and PyYAML 6.0.3 for independent reproduction.

Scope: three anonymous pack classes, schemas/cross-references, routes/image roles, explicit external isolation and namespaced extensions, mandatory primary evidence and conditional support, packet freeze/tamper/retry/revision, all five classifications, one automatic recovery bound, provenance rejection, fresh-session isolation and receipt consistency. Anonymous end-to-end runs use supplied mock reports and test-only assets; none establish a live accepted clean master.

Limitations: no actual generator/attachment transport, visual identity inspection, deterministic feature finalization on a real image, real consumer cutover or second real Subject Project acceptance has been observed in this checkpoint. Required capabilities and Principal gates remain required. Private consumer facts are not copied into the generic implementation.

Full remote repository/gallery/installer/browser and new Canon workflow results must be inspected on the resulting immutable commit before reporting CI success.
