"""uv run tenting build    the cradles' and test-fit trays' STLs in tenting/stl/
uv run tenting render   the review renders in tenting/png/
uv run tenting slice    tenting/stl/ to tenting/gcode/, needs prusa-slicer on the path
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


def slice_all(stl_dir: Path, out: Path):
    from dominoez.slice import slice_stl, stats

    for name in PRINTED:
        gcode = out / f"{name}.gcode"
        slice_stl(stl_dir / f"{name}.stl", gcode)
        print(gcode.relative_to(ROOT.parent))
        for key, value in stats(gcode).items():
            print(f"  {key}: {value}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="tenting")
    ap.add_argument("command", choices=["build", "render", "slice"])
    args = ap.parse_args(argv)
    if args.command == "build":
        for p in write_stls(ROOT / "stl"):
            print(p.relative_to(ROOT.parent))
    elif args.command == "render":
        from .views import render_all
        render_all(ROOT / "png")
    else:
        slice_all(ROOT / "stl", ROOT / "gcode")
