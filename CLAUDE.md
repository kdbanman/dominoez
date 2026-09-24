# Working in this repo

- When a plate or motif gcode has been built in CI, attach the gcode file in chat and link the run's build page, where the artifact is listed. A direct artifact link on its own does not open from chat.
- Never use scheduled tasks or timed check-ins to monitor a PR. Subscribing to its webhook events is sufficient.
- Motifs are reviewed in batches through a review doc built with `.claude/skills/review-doc/`, never as PNGs pasted into chat one at a time. Nothing from a batch is committed until its review doc has no redo left.
- Well-known shapes (sprites, glyphs, emoji, icons, flags) are traced from the real asset, never drawn from memory. The drawing brief for every batch says so and points at "Tracing sources" in `GUIDELINES.md`.
