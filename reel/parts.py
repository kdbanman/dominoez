"""The reel's printed parts.

Each part is built in its print frame (on the bed, z up) by `<part>_print()`, and placed
in the assembly by `<part>_world()`. Nothing in any print frame overhangs more than 45
degrees except the chassis bridge's flat underside, a 28 mm bridge between the cheeks.
"""

import math

import numpy as np
from manifold3d import CrossSection, JoinType, Manifold, OpType

from .spec import *  # noqa: F403

SEG = 96

# print frame (x, y, z) -> world (x=z, y=x, z=y): a round part printed axis-up, turned to lie on the axle
AXLE = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]


# ---------------------------------------------------------------- helpers
def place(m: Manifold, rot, t) -> Manifold:
    return m.transform(np.hstack([np.asarray(rot, float), np.asarray(t, float)[:, None]]))


def yz_plate(cs: CrossSection, thickness: float, x0: float) -> Manifold:
    """An outline drawn in (y, z) extruded along +x from x0."""
    return place(cs.extrude(thickness), [[0, 0, 1], [1, 0, 0], [0, 1, 0]], [x0, 0, 0])


def x_cyl(d, x0, x1, y=0.0, z=0.0, seg=SEG) -> Manifold:
    return Manifold.cylinder(x1 - x0, d / 2, d / 2, seg).rotate([0, 90, 0]).translate([x0, y, z])


def z_cyl(d, z0, z1, seg=SEG) -> Manifold:
    return Manifold.cylinder(z1 - z0, d / 2, d / 2, seg).translate([0, 0, z0])


def polygon(n, af, phase):
    r = af / 2 / math.cos(math.pi / n)
    return [(r * math.cos(math.radians(phase + 360 / n * i)), r * math.sin(math.radians(phase + 360 / n * i)))
            for i in range(n)]


def hexagon(af):
    """Flats top and bottom."""
    return polygon(6, af, 0)


def octagon(af):
    """Flats on the axes."""
    return polygon(8, af, 22.5)


def z_prism(poly, z0, z1) -> Manifold:
    return CrossSection([poly]).extrude(z1 - z0).translate([0, 0, z0])


def teardrop(d, at=(0.0, 0.0)) -> CrossSection:
    """A round hole with a 45 degree point on top, so it prints as a vertical hole with no ceiling."""
    r = d / 2
    tip = CrossSection([[(-0.01, 0), (0.01, 0), (0, r * math.sqrt(2))]])
    return CrossSection.batch_hull([CrossSection.circle(r, 48), tip]).translate(list(at))


def on_lock_circle(deg):
    return (LOCK_R * math.cos(math.radians(deg)), LOCK_R * math.sin(math.radians(deg)))


# ---------------------------------------------------------------- wheel
def wheel_print() -> Manifold:
    """Flat flange on the bed, the groove's 45 degree flank above it, an open cup on top.

    The line goes through the anchor hole in the groove floor and is knotted inside the cup.
    """
    h1, h2 = LOWER_FLANGE, LOWER_FLANGE + FLOOR_W
    h3 = h2 + (FLANGE_R - FLOOR_R)
    k = SHELL * math.sqrt(2)  # horizontal thickness of the 45 degree shell
    prof = CrossSection([[
        (0, 0), (FLANGE_R, 0), (FLANGE_R, h1), (FLOOR_R, h1), (FLOOR_R, h2), (FLANGE_R, h3),
        (FLANGE_R, WHEEL_W), (FLANGE_R - k, WHEEL_W), (FLANGE_R - k, h3), (FLOOR_R - k, h2),
        (FLOOR_R - k, WEB), (HUB_R, WEB), (HUB_R, WHEEL_W), (0, WHEEL_W)]])
    w = Manifold.revolve(prof, SEG) - z_prism(hexagon(WHEEL_HEX_AF), -1, WHEEL_W + 1)
    for i in range(LOCK_N):
        x, y = on_lock_circle(90 + 360 / LOCK_N * i)
        w = w - Manifold.cylinder(WHEEL_W + 2, PENCIL_HOLE / 2, PENCIL_HOLE / 2, 48).translate([x, y, -1])
    anchor = Manifold.cylinder(12, ANCHOR_D / 2, ANCHOR_D / 2, 16).rotate([0, 90, 0])
    anchor = anchor.translate([FLOOR_R - k - 3, 0, h1 + FLOOR_W / 2]).rotate([0, 0, 18])
    return w - anchor


def wheel_world() -> Manifold:
    return place(wheel_print(), AXLE, [-WHEEL_W / 2, 0, 0])


# ---------------------------------------------------------------- axle tube
def _tube_z(x):
    """World x along the axle -> the tube's print z (head on the bed)."""
    return x + XO + 0.5 + TUBE_HEAD_T


def tube_print() -> Manifold:
    """Head on the bed. A round bearing in each cheek, a hex between them that drives the
    wheel, a slotted lip that snaps past the far cheek, and a hex socket for the crank."""
    z = _tube_z
    t = z_cyl(TUBE_HEAD_D, 0, TUBE_HEAD_T)
    t = t + z_cyl(BEAR_HEAD, z(-XO - 0.5), z(-WHEEL_W / 2))
    t = t + z_prism(hexagon(TUBE_HEX_AF), z(-WHEEL_W / 2), z(WHEEL_W / 2))
    t = t + z_cyl(BEAR_SNAP, z(WHEEL_W / 2), z(XO + 0.5))
    # lip: a 0.8 mm ledge that catches the cheek, then a lead-in taper
    r = BEAR_SNAP / 2
    t = t + Manifold.cylinder(2.0, r + 0.8, r - 0.3, SEG).translate([0, 0, z(XO + 0.5)])
    t = t - z_prism(hexagon(BORE_HEX_AF), -1, z(XO + 5))
    for ang in (0, 90):
        t = t - Manifold.cube([40, 2.0, 16], center=True).rotate([0, 0, ang]).translate([0, 0, z(XO + 2.5)])
    return t


def tube_world() -> Manifold:
    return place(tube_print(), AXLE, [-_tube_z(0), 0, 0])


# ---------------------------------------------------------------- chassis
def cheek_outline() -> CrossSection:
    """A cheek in (y, z): flat foot, sides narrowing to the round top about the hinge pin."""
    return CrossSection.batch_hull([
        CrossSection.circle(BRIDGE_R, SEG).translate([0, PIVOT_Z]),
        CrossSection.square((2 * BRIDGE_R, 1)).translate([-BRIDGE_R, PIVOT_Z - BRIDGE_FLAT]),
        CrossSection.square((2 * FOOT_HALF, 1)).translate([-FOOT_HALF, FOOT_Z]),
    ])


def window() -> CrossSection:
    """Curved slot on the circle of lock holes, beside the axle."""
    a0, a1 = WINDOW
    rw = WINDOW_W / 2
    ts = np.linspace(a0, a1, 32)
    band = [((LOCK_R + rw) * math.cos(math.radians(t)), (LOCK_R + rw) * math.sin(math.radians(t))) for t in ts] + \
           [((LOCK_R - rw) * math.cos(math.radians(t)), (LOCK_R - rw) * math.sin(math.radians(t))) for t in ts[::-1]]
    return CrossSection([band]) + teardrop(WINDOW_W, on_lock_circle(a0)) + teardrop(WINDOW_W, on_lock_circle(a1))


def tongue_silhouette(reach) -> CrossSection:
    """The shaft's outline in (y, z) from the round end of its tongue up to reach above the pin."""
    return CrossSection.batch_hull([
        CrossSection.circle(TONGUE_R, 64).translate([0, PIVOT_Z]),
        CrossSection.square((SHAFT_AF, 1)).translate([-SHAFT_AF / 2, PIVOT_Z + reach - 1]),
    ])


def tongue_slot() -> CrossSection:
    """Everywhere the shaft goes as the reel swings SWING degrees either way, plus clearance."""
    body = tongue_silhouette(45).offset(SLOT_CLEAR / 2, JoinType.Round)
    sweep = [body.translate([0, -PIVOT_Z]).rotate(a).translate([0, PIVOT_Z]) for a in np.arange(-SWING, SWING + 0.1, 2.5)]
    return CrossSection.batch_boolean(sweep, OpType.Add)


def chassis_world() -> Manifold:
    """Two A-shaped cheeks joined by the round bridge at the top. Prints upright on the feet."""
    common = teardrop(PENCIL_HOLE, on_lock_circle(90)) + teardrop(PENCIL_HOLE, (0, PIVOT_Z)) + window()
    left = yz_plate(cheek_outline() - teardrop(BEAR_HEAD + BEAR_CLEAR) - common, CHEEK_T, -XO)
    right = yz_plate(cheek_outline() - teardrop(BEAR_SNAP + BEAR_CLEAR) - common, CHEEK_T, XI)
    bridge_cs = CrossSection.circle(BRIDGE_R, SEG).translate([0, PIVOT_Z]) + \
        CrossSection.square((2 * BRIDGE_R, BRIDGE_FLAT)).translate([-BRIDGE_R, PIVOT_Z - BRIDGE_FLAT])
    bridge = yz_plate(bridge_cs - teardrop(PENCIL_HOLE, (0, PIVOT_Z)), 2 * XI, -XI)
    w = SHAFT_AF + SLOT_CLEAR
    return left + right + bridge - yz_plate(tongue_slot(), w, GROOVE_X - w / 2)


def chassis_print() -> Manifold:
    return chassis_world().translate([0, 0, -FOOT_Z])


# ---------------------------------------------------------------- hanger shaft
def shaft_world() -> Manifold:
    """Octagon stem through the 1/2" hole, flat tongue on the hinge pin below, a hole for
    the cross pin above the plywood. It turns freely in the hole, so with the hinge the
    reel can face and lean toward any pull."""
    stem_z0 = PIVOT_Z + TONGUE_R
    top = CROSS_Z + SHAFT_TOP
    stem = z_prism(octagon(SHAFT_AF), stem_z0, top).translate([GROOVE_X, 0, 0])
    tongue_cs = tongue_silhouette(TONGUE_R) - CrossSection.circle(PENCIL_HOLE / 2, 48).translate([0, PIVOT_Z])
    tongue = yz_plate(tongue_cs, SHAFT_AF, GROOVE_X - SHAFT_AF / 2)
    return stem + tongue - x_cyl(CROSS_HOLE, GROOVE_X - 10, GROOVE_X + 10, 0, CROSS_Z, 48)


def shaft_print() -> Manifold:
    """On its side, a flat of the octagon and the tongue's face on the bed, so its layers
    run the length of the pull."""
    m = shaft_world().rotate([0, 90, 0])
    b = m.bounding_box()
    return m.translate([-b[0], -b[1], -b[2]])


# ---------------------------------------------------------------- pins
PINS = {  # name: (diameter, length, snap tip)
    "lock_pin": (PENCIL_PIN, LOCK_PIN_L, False),    # slides in and out, like the pencil crayon it stands in for
    "hinge_pin": (PENCIL_PIN, HINGE_PIN_L, True),
    "cross_pin": (CROSS_PIN, CROSS_PIN_L, True),
}


def pin_print(name) -> Manifold:
    """Along +x from a flat head tab, everything on one bed plane. A snap tip is split,
    with a bump each side that squeezes through the last hole and springs back."""
    d, length, snap = PINS[name]
    z0 = d / 2 - PIN_FLAT
    tl, tw = PIN_TAB
    body = x_cyl(d, tl, tl + length, 0, z0, 48) ^ Manifold.cube([length + 10, 20, 20]).translate([0, -10, 0])
    out = body + Manifold.cube([tl, tw, 2 * z0]).translate([0, -tw / 2, 0])
    if snap:
        tip = tl + length
        bump = Manifold.hull(Manifold.cube([0.1, d + 1.0, 2 * z0], center=True).translate([tip - 4, 0, z0]) +
                             Manifold.cube([0.1, d - 0.4, 2 * z0], center=True).translate([tip - 0.05, 0, z0]))
        bump = bump ^ x_cyl(d + 1.0, tip - 5, tip, 0, z0, 48)
        out = out + bump
        out = out - Manifold.cube([12, 1.2, 20], center=True).translate([tip - 4, 0, 5])
    return out


def pin_world(name, x_tab_face, y, z, roll=90.0) -> Manifold:
    """The tab's inner face at x_tab_face, the pin running +x; roll 90 stands the tab upright."""
    d, _, _ = PINS[name]
    m = pin_print(name).translate([0, 0, -(d / 2 - PIN_FLAT)]).rotate([roll, 0, 0])
    return m.translate([x_tab_face - PIN_TAB[0], y, z])


# ---------------------------------------------------------------- crank
CRANK_ROD = XO + 6 + WHEEL_W / 2 - 2


def crank_print() -> Manifold:
    """Z-shaped and flat: hex rod, arm, knob, all on one bed plane."""
    af = CRANK_HEX_AF
    along_x = np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, af / 2]], float)
    rod = CrossSection([hexagon(af)]).extrude(CRANK_ROD).transform(along_x)
    arm = Manifold.cube([CRANK_ARM_T, CRANK + 18, af]).translate([CRANK_ROD, -9, 0])
    knob = CrossSection([octagon(af)]).extrude(KNOB_L).transform(along_x).translate([CRANK_ROD + CRANK_ARM_T, CRANK, 0])
    return rod + arm + knob


def crank_world(angle_deg=-120.0) -> Manifold:
    """angle_deg is a multiple of 60 so the rod's hex lines up with the tube's socket."""
    a = math.radians(angle_deg)
    rot = [[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]]
    return place(crank_print().translate([0, 0, -CRANK_HEX_AF / 2]), rot, [-WHEEL_W / 2 + 2, 0, 0])


# ---------------------------------------------------------------- the lot
PRINTED = {
    "chassis": chassis_print,
    "wheel": wheel_print,
    "axle_tube": tube_print,
    "hanger_shaft": shaft_print,
    "lock_pin": lambda: pin_print("lock_pin"),
    "hinge_pin": lambda: pin_print("hinge_pin"),
    "cross_pin": lambda: pin_print("cross_pin"),
    "crank": crank_print,
}
