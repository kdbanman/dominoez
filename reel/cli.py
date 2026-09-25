"""uv run reel build     every printed part's STL in reel/stl/
uv run reel render    the review renders in reel/png/
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
    ap.add_argument("command", choices=["build", "render"])
    args = ap.parse_args(argv)
    if args.command == "build":
        for p in write_stls(ROOT / "stl"):
            print(p.relative_to(ROOT.parent))
    else:
        from .views import render_all
        render_all(ROOT / "png")
