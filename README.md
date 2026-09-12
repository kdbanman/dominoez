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
uv run dominoez plate           # every plate in plates/, as plate/<name>.stl (+ gcode with prusa-slicer)
uv run dominoez plate heart x4 bicycle x2 --name party   # an ad hoc plate
```

Slicing uses `slicer/profile.ini`, a PrusaSlicer profile lifted from a print that came out well. Install PrusaSlicer (`apt install prusa-slicer` on Ubuntu) or set `PRUSA_SLICER` to the binary. `build` does not need it.

`plate` lays built dominoes out standing on one bed and writes `plate/<name>.stl`, then slices it to `plate/<name>.gcode` when prusa-slicer is on the path. Each motif name may be followed by a count like `x4`, and `*` means one of every motif. With no names it makes every plate described in `plates/`, one file per plate listing the same tokens. The bed holds 6 by 12. Plate outputs are not committed.

For a one-off plate without a slicer at hand, run the `plate` workflow by hand from the Actions tab with the same tokens (say `toilet cat_face dog_face train`) and download `plate-<name>.gcode` from that run. Plates in `plates/` are sliced on every CI run instead and uploaded the same way, `plate-all.gcode` today.

A motif that breaks a printability rule fails the build with the rule and where it broke. CI rebuilds and reslices everything, fails if the committed `stl/`, `svg/`, `png/`, or `gcode/blank.gcode` differ from what the code produces, and uploads each motif's gcode as an artifact named `<motif>.gcode`.

## Adding a motif

1. Add `dominoez/motifs/<name>.py` exposing `motif = Motif(name=..., issue=..., draw=...)`. `draw` returns shapely geometry in motif coordinates: u right, v up, millimetres, drawn centred on the origin. The build moves it so its centre of mass sits in the middle of the top half of the face (see `GUIDELINES.md`, "Motif placement"). Helpers are in `dominoez/geometry.py`.
2. Register it in `dominoez/motifs/__init__.py`.
3. `uv run dominoez render <name>` and get the PNG approved.
4. `uv run dominoez build <name>`, commit SVG, PNG, and STL together. CI slices it; download the run's `<name>.gcode` artifact.
