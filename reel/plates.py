"""Two print plates for the reel.

test_fit: every fit in the reel before committing to the full print. The small real parts
(hanger shaft, two pins) plus stubs and coupons standing in for the rest, each printed
in the same orientation as the part it stands in for, so its holes come out the same way.
Sliced with the plain profile: it tests sizes, not strength.

full: all eight parts on one bed.
"""

from pathlib import Path

import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold, OpType

from . import parts as P
from .spec import (BEAR_CLEAR, BEAR_HEAD, BEAR_SNAP, BOARD_HOLE, CHEEK_T, CRANK_HEX_AF, CROSS_HOLE, PENCIL_HOLE,
                   WHEEL_HEX_AF)

GAP = 8.0          # between parts on the bed
BED_USE = 270.0    # the 290 bed less a 10 mm margin each side

# The full plate carries 10 lb; the domino profile's 3 walls and 10% grid are for dominoes.
STRONG = {"perimeters": "4", "fill_density": "30%", "fill_pattern": "gyroid"}


# Size ladders: three of a fit side by side, marked by 1, 2 or 3 notches.
# One notch is 0.2 tighter than the design, two is the design, three is 0.2 looser.
LADDER = (-0.2, 0.0, 0.2)


def notches(n, at, pitch=3.0, r=1.0) -> CrossSection:
    """n half-round notches centred on `at` along an edge that runs in the first axis."""
    x0 = at[0] - pitch * (n - 1) / 2
    return CrossSection.compose([CrossSection.circle(r, 16).translate([x0 + pitch * i, at[1]]) for i in range(n)])


def cheek_coupon() -> Manifold:
    """A strip of cheek standing upright like the chassis on a small foot: both axle-tube
    bearing holes, and a ladder of three lock/hinge pin holes. Tests the tube's bearings and
    snap lip, and a pin or pencil crayon through a cheek."""
    w, h, zc = 96.0, 35.0, 15.0  # tall enough for the big hole and its pointed top
    x0 = -w / 2
    plate = CrossSection.square((w, h)).translate([x0, 0])
    plate = plate - P.teardrop(BEAR_HEAD + BEAR_CLEAR, (x0 + 16, zc)) - P.teardrop(BEAR_SNAP + BEAR_CLEAR, (x0 + 44, zc))
    for i, extra in enumerate(LADDER):
        x = x0 + 64 + 12 * i
        plate = plate - P.teardrop(PENCIL_HOLE + extra, (x, zc)) - notches(i + 1, (x, h))
    slab = P.yz_plate(plate, CHEEK_T, -CHEEK_T / 2)
    foot = Manifold.cube([CHEEK_T + 8, w, 1.0]).translate([-CHEEK_T / 2 - 4, x0, 0])
    return slab + foot


def ladder_bar() -> Manifold:
    """Printed flat like the wheel and the lying shaft, so its holes are vertical like theirs:
    three of the wheel's hex bore, three lock/hinge pin holes, three cross-pin holes."""
    col, w, h = 30.0, 90.0, 46.0
    bar = CrossSection.square((w, h)).translate([-w / 2, 0])
    for i, extra in enumerate(LADDER):
        x = -w / 2 + col / 2 + col * i
        bar = bar - P.hex_hole(WHEEL_HEX_AF + extra).translate([x, 30]) - notches(i + 1, (x, h))
        bar = bar - CrossSection.circle((PENCIL_HOLE + extra) / 2, 48).translate([x - 7, 8])
        bar = bar - CrossSection.circle((CROSS_HOLE + extra) / 2, 48).translate([x + 7, 8])
    return bar.extrude(3)


def crank_stub(i) -> Manifold:
    """14 mm of the crank's hex rod on a notched tab, lying flat like the crank. Stub i is
    LADDER[i] thinner, since it is the male side."""
    af = CRANK_HEX_AF - LADDER[i]
    rod = P.hexagon(af).extrude(14).transform(np.array([[0, 0, 1, 4], [1, 0, 0, 0], [0, 1, 0, af / 2]], float))
    tab = CrossSection.square((4, 18)).translate([0, -9]) - notches(i + 1, (0, 0), pitch=4.0).rotate(90)
    tab = P.place(tab.extrude(af), [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 0, 0])
    return rod + tab


def tube_stub() -> Manifold:
    """The axle tube cut short, head down like the real one: head, the head-side bearing,
    8 mm of the drive hex, the snap-side bearing and its slotted lip, and the crank's socket.
    Each piece meets its coupon: the bearings and lip in the cheek strip, the hex in the bar."""
    t = P.z_cyl(P.TUBE_HEAD_D, 0, P.TUBE_HEAD_T)
    z = P.TUBE_HEAD_T
    t = t + P.z_cyl(BEAR_HEAD, z, z + CHEEK_T + 1)
    z += CHEEK_T + 1
    t = t + P.z_prism(P.hexagon(P.TUBE_HEX_AF), z, z + 8)
    z += 8
    t = t + P.z_cyl(BEAR_SNAP, z, z + CHEEK_T + 0.5)
    z += CHEEK_T + 0.5
    t = t + P.snap_lip(z)
    t = t - P.z_prism(P.hex_hole(P.BORE_HEX_AF), -1, z + 5)
    for ang in (0, 90):
        t = t - Manifold.cube([40, 2.0, 16], center=True).rotate([0, 0, ang]).translate([0, 0, z + 2])
    return t


def shelf_coupon() -> Manifold:
    """A nominal 1/2" hole in a plate, to try the shaft in before the real shelf's hole."""
    r = BOARD_HOLE / 2
    return Manifold.cube([22, 22, 3]).translate([-11, -11, 0]) - Manifold.cylinder(5, r, r, 64).translate([0, 0, -1])


TEST_FIT = {
    "cheek": cheek_coupon,
    "ladder_bar": ladder_bar,
    "tube_stub": tube_stub,
    "hanger_shaft": P.PRINTED["hanger_shaft"],
    "hinge_pin": P.PRINTED["hinge_pin"],
    "cross_pin": P.PRINTED["cross_pin"],
    "crank_stub_1": lambda: crank_stub(0),
    "crank_stub_2": lambda: crank_stub(1),
    "crank_stub_3": lambda: crank_stub(2),
    "shelf_hole": shelf_coupon,
}

FULL = dict(P.PRINTED)


def on_bed(m: Manifold) -> Manifold:
    b = m.bounding_box()
    return m.translate([-b[0], -b[1], -b[2]])


def arrange(pieces: dict[str, Manifold], width: float = BED_USE) -> dict[str, Manifold]:
    """Shelf packing: deepest first, left to right, rows upward, GAP apart.
    Pieces longer in y than x are turned a quarter so rows stay shallow."""
    placed = {}
    items = []
    for name, m in pieces.items():
        m = on_bed(m)
        b = m.bounding_box()
        if b[4] - b[1] > b[3] - b[0]:
            m = on_bed(m.rotate([0, 0, 90]))
        items.append((name, m))
    items.sort(key=lambda it: -(it[1].bounding_box()[4]))
    x = y = row_h = 0.0
    for name, m in items:
        b = m.bounding_box()
        w, d = b[3], b[4]
        if x > 0 and x + w > width:
            x, y, row_h = 0.0, y + row_h + GAP, 0.0
        placed[name] = m.translate([x, y, 0])
        x += w + GAP
        row_h = max(row_h, d)
    b = Manifold.batch_boolean(list(placed.values()), OpType.Add).bounding_box()
    if b[3] > width or b[4] > width:
        raise ValueError(f"plate is {b[3]:.0f} x {b[4]:.0f} mm; the bed allows {width:.0f}")
    return placed


def write_plate(name: str, builders: dict, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    placed = arrange({n: f() for n, f in builders.items()})
    meshes = []
    for m in placed.values():
        mm = m.to_mesh()
        meshes.append(trimesh.Trimesh(np.asarray(mm.vert_properties)[:, :3], np.asarray(mm.tri_verts), process=False))
    path = out / f"{name}.stl"
    trimesh.util.concatenate(meshes).export(path, file_type="stl")
    return path


COLOUR = {"cheek": "chassis", "ladder_bar": "wheel", "tube_stub": "axle_tube", "shelf_hole": "board",
          "crank_stub_1": "crank", "crank_stub_2": "crank", "crank_stub_3": "crank"}


def placed_views(name: str) -> list[tuple[str, str, Manifold]]:
    """(piece, render colour, placed solid) for every piece on a plate."""
    builders = TEST_FIT if name == "test_fit" else FULL
    return [(n, COLOUR.get(n, n), m) for n, m in arrange({n: f() for n, f in builders.items()}).items()]


PLATES = {"test_fit": (TEST_FIT, {}), "full": (FULL, STRONG)}  # name: (parts, slicer overrides)
