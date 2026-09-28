"""uv run reel build     every printed part's STL in reel/stl/
uv run reel render    the review renders in reel/png/
uv run reel plate     the test_fit and full plates in reel/plate/, sliced when prusa-slicer is on the path
"""

import argparse
from pathlib import Path

import numpy as np
import trimesh

from .parts import PRINTED

ROOT = Path(__file__).parent


def write_stls(out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for name, build in PRINTED.items():
        m = build().to_mesh()
        mesh = trimesh.Trimesh(np.asarray(m.vert_properties)[:, :3], np.asarray(m.tri_verts), process=False)
        path = out / f"{name}.stl"
        mesh.export(path, file_type="stl")
        written.append(path)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(prog="reel")
    ap.add_argument("command", choices=["build", "render", "plate"])
    args = ap.parse_args(argv)
    if args.command == "build":
        for p in write_stls(ROOT / "stl"):
            print(p.relative_to(ROOT.parent))
    elif args.command == "render":
        from .views import render_all
        render_all(ROOT / "png")
    else:
        plate_all(ROOT / "plate")


def plate_all(out: Path):
    from dominoez.slice import SlicerMissing, slice_stl, slicer_binary, stats

    from .plates import PLATES, write_plate
    try:
        slicer_binary()
        can_slice = True
    except SlicerMissing as e:
        print(f"not slicing: {e}")
        can_slice = False
    for name, (builders, overrides) in PLATES.items():
        stl = write_plate(name, builders, out)
        print(stl.relative_to(ROOT.parent))
        if can_slice:
            gcode = stl.with_suffix(".gcode")
            slice_stl(stl, gcode, overrides=overrides)
            print(gcode.relative_to(ROOT.parent))
            for key, value in stats(gcode).items():
                print(f"  {key}: {value}")
