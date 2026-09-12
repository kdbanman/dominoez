"""Many dominoes on one print bed.

A plate is a set of built dominoes laid out standing on the bed, foot down,
and written as one STL so the slicer prints them together, layer by layer.
Dominoes stand in rows across the bed with their faces along x, spaced so the
skirt, travel moves, and a wobbling nozzle clear every tower.
"""

import re
from pathlib import Path

import trimesh

from .build import REPO
from .motif import Motif
from .slice import PROFILE
from .spec import BODY

GAP = 10.0  # standing material to standing material, between neighbours
MARGIN = 10.0  # from the bed edge to the nearest domino, past the 3 mm skirt


def bed(profile: Path = PROFILE) -> tuple[float, float, float, float]:
    """The bed rectangle (xmin, ymin, xmax, ymax) from the profile's bed_shape."""
    text = profile.read_text()
    match = re.search(r"^bed_shape = (.+)$", text, re.MULTILINE)
    if match is None:
        raise ValueError(f"{profile} has no bed_shape")
    corners = [tuple(float(c) for c in p.split("x")) for p in match.group(1).split(",")]
    xs = [x for x, _ in corners]
    ys = [y for _, y in corners]
    return min(xs), min(ys), max(xs), max(ys)


def capacity(profile: Path = PROFILE) -> tuple[int, int]:
    """How many dominoes fit across (columns) and up (rows) the bed."""
    xmin, ymin, xmax, ymax = bed(profile)
    cols = int((xmax - xmin - 2 * MARGIN + GAP) // (BODY.width + GAP))
    rows = int((ymax - ymin - 2 * MARGIN + GAP) // (BODY.thickness + GAP))
    return cols, rows


def layout(count: int, profile: Path = PROFILE) -> list[tuple[float, float]]:
    """Bed coordinates of each domino's centre, filling rows from the front, the whole block centred."""
    cols, rows = capacity(profile)
    if count > cols * rows:
        raise ValueError(f"{count} dominoes do not fit: the bed holds {cols} x {rows} = {cols * rows}")
    if count == 0:
        return []
    used_cols = min(count, cols)
    used_rows = -(-count // cols)
    xmin, ymin, xmax, ymax = bed(profile)
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    x0 = cx - ((used_cols - 1) * (BODY.width + GAP)) / 2
    y0 = cy - ((used_rows - 1) * (BODY.thickness + GAP)) / 2
    return [
        (x0 + (i % cols) * (BODY.width + GAP), y0 + (i // cols) * (BODY.thickness + GAP))
        for i in range(count)
    ]


def plate(motifs: list[Motif], name: str, out: Path = REPO) -> Path:
    """Write `out/plate/<name>.stl` holding one built domino per entry in `motifs`, in layout order."""
    meshes = []
    for motif, (x, y) in zip(motifs, layout(len(motifs))):
        stl = out / "stl" / f"{motif.name}.stl"
        if not stl.exists():
            raise FileNotFoundError(f"{stl} is missing. Run `dominoez build {motif.name}` first.")
        mesh = trimesh.load(stl, file_type="stl", process=False)
        mesh.apply_translation([x, y, 0.0])
        meshes.append(mesh)
    (out / "plate").mkdir(parents=True, exist_ok=True)
    path = out / "plate" / f"{name}.stl"
    trimesh.util.concatenate(meshes).export(path, file_type="stl")
    return path
