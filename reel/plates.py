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
from .spec import (BEAR_CLEAR, BEAR_HEAD, BEAR_SNAP, BOARD_HOLE, CHEEK_T, CRANK_HEX_AF, PENCIL_HOLE, PIVOT_Z,
                   WHEEL_HEX_AF)

GAP = 12.0         # between parts on the bed, room for a 4 mm brim each side
BED_USE = 270.0    # the 290 bed less a 10 mm margin each side

# The full plate carries 10 lb; the domino profile's 3 walls and 10% grid are for dominoes.
STRONG = {"perimeters": "4", "fill_density": "30%", "fill_pattern": "gyroid"}
# Without it PrusaSlicer warns of low bed adhesion: the chassis stands 111 tall on its feet,
# the shaft lies on a 4.7 wide flat.
BRIM = {"brim_width": "4"}


def cheek_coupon() -> Manifold:
    """A strip of cheek with both axle-tube holes and a pin hole, standing upright like the
    chassis on a small foot. Tests the tube's bearings and snap lip, and a pin through a cheek."""
    holes = [(BEAR_HEAD + BEAR_CLEAR, -19.0), (BEAR_SNAP + BEAR_CLEAR, 8.5), (PENCIL_HOLE, 26.0)]
    w, h, zc = 66.0, 35.0, 15.0  # tall enough for the 24.6 hole and its pointed top
    plate = CrossSection.square((w, h)).translate([-33.0, 0])
    for d, y in holes:
        plate = plate - P.teardrop(d, (y, zc))
    slab = P.yz_plate(plate, CHEEK_T, -CHEEK_T / 2)
    foot = Manifold.cube([CHEEK_T + 8, w, 1.0]).translate([-CHEEK_T / 2 - 4, -33.0, 0])
    return slab + foot


def hub_coupon() -> Manifold:
    """The wheel's hex bore in a thin ring, plus one lock hole in a tab, printed flat like the
    wheel: the tube's hex in the wheel, and a pin or pencil crayon in a wheel hole."""
    ring = Manifold.cylinder(4, 15.5, 15.5, P.SEG) - P.z_prism(P.hexagon(WHEEL_HEX_AF), -1, 5)
    tab = Manifold.cube([16, 16, 4]).translate([14, -8, 0]) - \
        Manifold.cylinder(6, PENCIL_HOLE / 2, PENCIL_HOLE / 2, 48).translate([23, 0, -1])
    return ring + tab


def crank_stub() -> Manifold:
    """20 mm of the crank's hex rod on a small tab, lying flat like the crank."""
    af = CRANK_HEX_AF
    rod = CrossSection([P.hexagon(af)]).extrude(20).transform(
        np.array([[0, 0, 1, 4], [1, 0, 0, 0], [0, 1, 0, af / 2]], float))
    return rod + Manifold.cube([4, 18, af]).translate([0, -9, 0])


def tube_stub() -> Manifold:
    """The axle tube cut short, head down like the real one: head, the head-side bearing,
    8 mm of the drive hex, the snap-side bearing and its slotted lip, and the crank's socket.
    Each piece meets its coupon: the bearings and lip in the cheek strip, the hex in the hub."""
    t = P.z_cyl(P.TUBE_HEAD_D, 0, P.TUBE_HEAD_T)
    z = P.TUBE_HEAD_T
    t = t + P.z_cyl(BEAR_HEAD, z, z + CHEEK_T + 1)
    z += CHEEK_T + 1
    t = t + P.z_prism(P.hexagon(P.TUBE_HEX_AF), z, z + 8)
    z += 8
    t = t + P.z_cyl(BEAR_SNAP, z, z + CHEEK_T + 0.5)
    z += CHEEK_T + 0.5
    r = BEAR_SNAP / 2
    t = t + Manifold.cylinder(2.0, r + 0.8, r - 0.3, P.SEG).translate([0, 0, z])
    t = t - P.z_prism(P.hexagon(P.BORE_HEX_AF), -1, z + 5)
    for ang in (0, 90):
        t = t - Manifold.cube([40, 2.0, 16], center=True).rotate([0, 0, ang]).translate([0, 0, z + 2])
    return t


def shelf_coupon() -> Manifold:
    """A nominal 1/2" hole in a plate, to try the shaft in before the real shelf's hole."""
    r = BOARD_HOLE / 2
    return Manifold.cube([22, 22, 3]).translate([-11, -11, 0]) - Manifold.cylinder(5, r, r, 64).translate([0, 0, -1])


TEST_FIT = {
    "cheek": cheek_coupon,
    "hub": hub_coupon,
    "tube_stub": tube_stub,
    "hanger_shaft": P.PRINTED["hanger_shaft"],
    "hinge_pin": P.PRINTED["hinge_pin"],
    "cross_pin": P.PRINTED["cross_pin"],
    "crank_stub": crank_stub,
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


def placed_views(name: str) -> list[tuple[str, Manifold]]:
    builders = TEST_FIT if name == "test_fit" else FULL
    colour = {"cheek": "chassis", "hub": "wheel", "tube_stub": "axle_tube", "crank_stub": "crank", "shelf_hole": "board"}
    return [(colour.get(n, n), m) for n, m in arrange({n: f() for n, f in builders.items()}).items()]


PLATES = {"test_fit": (TEST_FIT, BRIM), "full": (FULL, {**STRONG, **BRIM})}  # name: (parts, slicer overrides)
