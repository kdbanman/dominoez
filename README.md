# dominoez

3D-printable toppling dominoes, each with a picture engraved on both faces. They are sliced for one printer and filament (Creality CR-10 Smart Pro, 0.4 mm nozzle, PLA): the blank's gcode is committed in `gcode/`, every motif's gcode is an artifact named after it on the latest CI run. The STLs in `stl/` are for anyone else, foot down.

- `CONTEXT.md`: vocabulary.
- `GUIDELINES.md`: dimensions, print limits, how to draw a motif.
- `docs/adr/`: decisions that are hard to reverse.
- Motif backlog: issue #2.

## Building

Needs [uv](https://docs.astral.sh/uv/).

```
uv sync
uv run pytest
uv run dominoez list            # registered motifs and their issue numbers
uv run dominoez render heart    # SVG and PNG only, for approval
uv run dominoez build           # check, SVG, PNG, STL
uv run dominoez slice           # STL to gcode, needs prusa-slicer on the path
```

Slicing uses `slicer/profile.ini`, a PrusaSlicer profile lifted from a print that came out well. Install PrusaSlicer (`apt install prusa-slicer` on Ubuntu) or set `PRUSA_SLICER` to the binary. `build` does not need it.

A motif that breaks a printability rule fails the build with the rule and where it broke. CI rebuilds and reslices everything, fails if the committed `stl/`, `svg/`, `png/`, or `gcode/blank.gcode` differ from what the code produces, and uploads each motif's gcode as an artifact named `<motif>.gcode`.

## Adding a motif

1. Add `dominoez/motifs/<name>.py` exposing `motif = Motif(name=..., issue=..., draw=...)`. `draw` returns shapely geometry in motif coordinates: u right, v up, origin at face centre, millimetres. Helpers are in `dominoez/geometry.py`.
2. Register it in `dominoez/motifs/__init__.py`.
3. `uv run dominoez render <name>` and get the PNG approved.
4. `uv run dominoez build <name>`, commit SVG, PNG, and STL together. CI slices it; download the run's `<name>.gcode` artifact.
