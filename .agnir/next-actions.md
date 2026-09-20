# Next Actions

- Update the GitHub repository About/homepage URL from the legacy `https://skills-hub.hkooii.com` value to `https://skills-hub.lapplax.com/` when a repository-metadata write capability is available.
- Enable a lightweight GitHub ruleset for `main`: require the `Validate skills` check and block force-pushes and branch deletion without adding unnecessary approval overhead for this personal repository. The currently connected GitHub capability cannot mutate repository rulesets.
- Clean up stale remote topic branches after confirming any intentionally retained history and when branch-ref deletion is available. This includes historical deployment branches and temporary structured-localization branches created during hardening.
- Run an end-to-end `pet-avatar-generation` acceptance in ChatGPT when a usable real source pet image is present in the active conversation: explore materially distinct styles, select one direction, refine it, and request transparent-background output. Record only evidence-backed gaps that require a skill change.
- Review the stacked `canon-skill` Day 1-3 draft changes after validation. Then implement Day 4 Prompt/Gen interface hardening: explicit Prompt Mode and Gen Mode contracts, Generation Packet freeze handoff, hook lifecycle semantics, generation transport abstraction, and anonymous Human/Pet/Virtual end-to-end dry-run cases.
