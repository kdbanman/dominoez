# Slice in the repo with the PrusaSlicer command line

Every domino goes to the same printer with the same filament, so slicing is part of the build, not a manual step on a desktop. `dominoez slice` runs `prusa-slicer --export-gcode` on each STL with the one profile in `slicer/profile.ini`. CI installs PrusaSlicer from apt, slices everything, and uploads the gcode as a build artifact. Only the blank's gcode is committed, and CI fails if it changes: it is the canary for slicer or profile drift.

The profile is the config block PrusaSlicer writes at the end of every gcode file, lifted from a blank that printed well. That block holds printer, print, and filament settings together, and any PrusaSlicer version reads it back with `--load`. The known-good print is the source of truth, and its gcode is kept unchanged in `slicer/reference/`. To change a setting, change it in PrusaSlicer, print, and paste the new block in.

## Considered options

- A Python slicer. Nothing mature exists. The few that do (mandoline and friends) lack perimeters, infill, and printer-specific gcode, so we would be writing a slicer.
- CuraEngine. A real headless engine, but its settings model is its own and cannot load the PrusaSlicer profile that already prints well.
- Kiri:Moto. JavaScript with a command line, same profile problem.
- Slicing by hand on a desktop and committing the result. Works until a motif is rebuilt and nobody reslices it.

## Consequences

- The slicer version in CI is whatever apt on Ubuntu 24.04 ships, 2.7.2 today, while the profile came from 2.9.2. Newer keys are ignored. On the blank the two versions agree on filament mass to the hundredth of a gram and on print time to within seconds; toolpaths differ in detail. If parity ever matters, pin a specific build instead of apt.
- Gcode is deterministic for a fixed slicer version, profile, and STL once the timestamp on the first line is removed. `dominoez slice` removes it. A slicer upgrade in CI will change the committed blank gcode, which is the point.
- Gcode files are 1.5 to 2 MB each, so motif gcode lives in CI artifacts rather than the repo. Artifacts expire (90 days by default), and a fresh run regenerates them.
- Anyone running `dominoez slice` locally needs `prusa-slicer` on their path, or `PRUSA_SLICER` pointing at it. `build` does not need it.
