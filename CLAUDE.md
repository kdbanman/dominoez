# Working in this repo

- When a plate's gcode has been built in CI, attach the gcode file in chat and link the run's build page, where the artifact is listed. A direct artifact link on its own does not open from chat.
- Dominoes print as plates of 10 to 20, one file each in `plates/`, tracked as sub-issues of the print tracker issue. A batch's PR adds its plate files; its sub-issues are opened when the PR merges; a printed plate's file is deleted and its sub-issue closed. No per-motif gcode.
- Never use scheduled tasks or timed check-ins to monitor a PR. Subscribing to its webhook events is sufficient.
- Motifs are reviewed in batches through a review doc built with `.claude/skills/review-doc/`, never as PNGs pasted into chat one at a time. Nothing from a batch is committed until its review doc has no redo left.
- Well-known shapes (sprites, glyphs, emoji, icons, flags) are traced from the real asset, never drawn from memory. The drawing brief for every batch says so and points at "Tracing sources" in `GUIDELINES.md`.
