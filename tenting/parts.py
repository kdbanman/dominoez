"""The cradle and its flat test-fit tray, each built for the left half and mirrored for the right.

Both are built in plate coordinates first: pocket floor at z = 0, the plate's outline as
in spec.OUTLINE. The cradle is then tilted about a line along y through the pocket's
outermost pinky point, so the thumb side rises, lifted FLOOR off the desk, given a solid
wedge straight down to the desk, and cut off at the desk.
"""

import math

import numpy as np
from manifold3d import CrossSection, JoinType, Manifold, OpType

from .spec import (
    DECK,
    DESK_FOOT_D,
    DESK_FOOT_DEPTH,
    DESK_FOOT_MARGIN,
    DESK_FOOT_SKIN,
    FEET,
    FLOOR,
    LIP,
    NOTCHES,
    OUTLINE,
    SLOP,
    TILT,
    WALL,
)

TOP = FEET + LIP  # lip top above the pocket floor
BIG = 1000.0


def outline() -> CrossSection:
    return CrossSection([OUTLINE])


def pocket() -> CrossSection:
    return outline().offset(SLOP, JoinType.Round, circular_segments=32)


def rim() -> CrossSection:
    return outline().offset(SLOP + WALL, JoinType.Round, circular_segments=64)


def notches() -> CrossSection:
    return CrossSection.batch_boolean(
        [CrossSection.square((x1 - x0, y1 - y0)).translate([x0, y0]) for x0, y0, x1, y1 in NOTCHES.values()],
        OpType.Add)


def tray(floor: float) -> Manifold:
    """Pocket and lip on a floor `floor` thick, the floor's top at z = 0."""
    body = rim().extrude(TOP + floor).translate([0, 0, -floor])
    return body - pocket().extrude(TOP + 1) - notches().extrude(TOP + 1)


def pivot_x() -> float:
    return pocket().bounds()[0]


def tilt(m: Manifold) -> Manifold:
    """Plate coordinates to desk coordinates: turn TILT about the pivot line, floor FLOOR up."""
    t = math.radians(TILT)
    rot = np.array([[math.cos(t), 0, -math.sin(t), 0], [0, 1, 0, 0], [math.sin(t), 0, math.cos(t), 0]])
    return m.translate([-pivot_x(), 0, 0]).transform(rot).translate([0, 0, FLOOR])


def plate_transform() -> np.ndarray:
    """4x4 placing the plate (bottom face at z = 0, plate coordinates) on its feet in the cradle."""
    t = math.radians(TILT)
    rot = np.array([[math.cos(t), 0, -math.sin(t)], [0, 1, 0], [math.sin(t), 0, math.cos(t)]])
    out = np.eye(4)
    out[:3, :3] = rot
    out[:3, 3] = rot @ np.array([-pivot_x(), 0, FEET]) + [0, 0, FLOOR]
    return out


def desk_cut(m: Manifold) -> Manifold:
    return m ^ Manifold.cube([BIG, BIG, BIG]).translate([-BIG / 2, -BIG / 2, 0])


def wedge() -> Manifold:
    """Everything straight below the tilted tray's underside, down to the desk."""
    shadow = tilt(rim().extrude(0.01)).project()
    below = tilt(Manifold.cube([BIG, BIG, BIG]).translate([-BIG / 2, -BIG / 2, -BIG - DECK + 0.01]))
    return shadow.extrude(BIG / 2) ^ below


def desk_feet(body: Manifold) -> list[tuple[float, float]]:
    """Centres of the four desk-foot pockets: the corners of the base, as far out as the
    pocket and its margin allow, and far enough from the pivot edge for the wedge to hold one."""
    base = body.slice(0.1)
    inset = base.offset(-(DESK_FOOT_D / 2 + DESK_FOOT_MARGIN), JoinType.Round, circular_segments=32)
    x0 = base.bounds()[0]
    inset = inset ^ CrossSection.square((BIG, BIG)).translate([x0 + DESK_FOOT_SKIN, -BIG / 2])
    pts = np.vstack([np.asarray(p) for p in inset.to_polygons()])
    keys = (pts[:, 0] + pts[:, 1], pts[:, 0] - pts[:, 1], -(pts[:, 0] - pts[:, 1]), -(pts[:, 0] + pts[:, 1]))
    return [tuple(pts[np.argmin(k)]) for k in keys]


def cradle_left() -> Manifold:
    body = desk_cut(tilt(tray(DECK)) + wedge())
    r = DESK_FOOT_D / 2
    for x, y in desk_feet(body):
        body = body - Manifold.cylinder(2 * DESK_FOOT_DEPTH, r, r, 64).translate([x, y, -DESK_FOOT_DEPTH])
    return body


def test_fit_left() -> Manifold:
    """The cradle's pocket, lip and notches on a flat FLOOR-thick floor, to try the fit cheaply."""
    return tray(FLOOR).translate([0, 0, FLOOR])


def right(m: Manifold) -> Manifold:
    return m.mirror([1, 0, 0])


def on_bed(m: Manifold) -> Manifold:
    b = m.bounding_box()
    return m.translate([-b[0], -b[1], -b[2]])


PRINTED = {
    "cradle_left": lambda: on_bed(cradle_left()),
    "cradle_right": lambda: on_bed(right(cradle_left())),
    "test_fit_left": lambda: on_bed(test_fit_left()),
    "test_fit_right": lambda: on_bed(right(test_fit_left())),
}
