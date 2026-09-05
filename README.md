# dominoez

3D-printable toppling dominoes, each with a picture engraved on both faces. The STLs in `stl/` are ready to print, foot down.

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
uv run dominoez build           # everything: check, SVG, PNG, STL
```

A motif that breaks a printability rule fails the build with the rule and where it broke. CI rebuilds everything and fails if the committed `stl/`, `svg/`, or `png/` differ from what the code produces.

## Adding a motif

1. Add `dominoez/motifs/<name>.py` exposing `motif = Motif(name=..., issue=..., draw=...)`. `draw` returns shapely geometry in motif coordinates: u right, v up, origin at face centre, millimetres. Helpers are in `dominoez/geometry.py`.
2. Register it in `dominoez/motifs/__init__.py`.
3. `uv run dominoez render <name>` and get the PNG approved.
4. `uv run dominoez build <name>`, commit SVG, PNG, and STL together.
