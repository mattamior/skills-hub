# Canon mode, hook and transport checkpoint

Day 4 now has explicit begin/Prompt/Gen guides, five-stage hooks and generation transport abstraction. Architecture routing links the new guides, pending the final thin-entry/localization reconciliation. Policies distinguish output kind from route, accepted previews from clean masters, declared construction checks from final acceptance, source hashes from approved transport payload hashes, and host evidence from simulated receipts.

The first committed implementation CI run (35500556914) passed repository and upstream skill validators but failed before pack tests because the compressed Subject Pack JSON Schema was missing a closing brace. This revision replaces that schema with structurally explicit JSON. No test was removed or relaxed. Full committed-fixture regression and gallery checks must rerun before acceptance.

Consumer integration remains separate from the public skill. No private subject facts, assets or production cutover are introduced by this checkpoint.
