# Slice in the repo with the PrusaSlicer command line

Every domino goes to the same printer with the same filament, so slicing is part of the build, not a manual step on a desktop. `dominoez slice` runs `prusa-slicer --export-gcode` on each STL with the one profile in `slicer/profile.ini`, and the gcode is committed next to the STL. CI installs PrusaSlicer from apt, slices everything, and fails if the committed gcode differs.

The profile is the config block PrusaSlicer writes at the end of every gcode file, lifted from a blank that printed well. That block holds printer, print, and filament settings together, and any PrusaSlicer version reads it back with `--load`. The known-good print is the source of truth. To change a setting, change it in PrusaSlicer, print, and paste the new block in.

## Considered options

- A Python slicer. Nothing mature exists. The few that do (mandoline and friends) lack perimeters, infill, and printer-specific gcode, so we would be writing a slicer.
- CuraEngine. A real headless engine, but its settings model is its own and cannot load the PrusaSlicer profile that already prints well.
- Kiri:Moto. JavaScript with a command line, same profile problem.
- Slicing by hand on a desktop and committing the result. Works until a motif is rebuilt and nobody reslices it.

## Consequences

- The slicer version in CI is whatever apt on Ubuntu 24.04 ships, 2.7.2 today, while the profile came from 2.9.2. Newer keys are ignored. On the blank the two versions agree on filament mass to the hundredth of a gram and on print time to within seconds; toolpaths differ in detail. If parity ever matters, pin a specific build instead of apt.
- Gcode is deterministic for a fixed slicer version, profile, and STL once the timestamp on the first line is removed. `dominoez slice` removes it. A slicer upgrade in CI will change every committed gcode file at once, which is the point.
- Each gcode file is about 1.5 MB. Fine for tens of motifs, worth revisiting for hundreds.
- Anyone running `dominoez slice` locally needs `prusa-slicer` on their path, or `PRUSA_SLICER` pointing at it. `build` does not need it.
