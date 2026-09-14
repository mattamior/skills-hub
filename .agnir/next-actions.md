# Next Actions

- Let the candidate PR generate the npm dependency lock on GitHub Actions, commit that exact lockfile, switch validation to `npm ci`, and require the full repository/browser validation to pass before merging and observing production acceptance.
- Enable a lightweight GitHub ruleset for `main`: require the `Validate skills` check and block force-pushes and branch deletion without adding unnecessary approval overhead for this personal repository.
- Run an end-to-end `pet-avatar-generation` acceptance in ChatGPT using a real source pet image when a usable image is available in the active conversation: explore materially distinct styles, select one direction, refine it, and request transparent-background output. Record only evidence-backed gaps that require a skill change.
- After the pet-avatar acceptance is complete, choose the next reusable skill to add; keep gallery expansion data-driven so new catalog pages, localization coverage, installer checks, browser smoke tests, and deployment acceptance require no hand-maintained skill allowlist.
