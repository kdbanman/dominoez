"""The review renders: the assembly unloaded and loaded, sections, and each part as printed."""

import math
from pathlib import Path

from manifold3d import Manifold

from . import parts as P
from .plates import placed_views
from .render import render, save
from .spec import (BOARD_HOLE, BOARD_T, BOARD_Z, CRANK, CROSS_Z, FLANGE_R, FLOOR_R, GROOVE_X, LINE_N,
                   LOADED_TILT, LOCK_R, PIVOT_DROP, PIVOT_Z, TONGUE_R, WHEEL_W, XI, XO)

SWINGS = ("chassis", "wheel", "axle_tube", "lock_pin", "hinge_pin", "crank")


def board() -> Manifold:
    b = Manifold.cube([140, 170, BOARD_T]).translate([-70, -85, BOARD_Z])
    return b - Manifold.cylinder(BOARD_T + 2, BOARD_HOLE / 2, BOARD_HOLE / 2, 48).translate([GROOVE_X, 0, BOARD_Z - 1])


def line(y, z_top, bottom=-110.0):
    ln = Manifold.cylinder(z_top - bottom, 0.6, 0.6, 12).translate([GROOVE_X, y, bottom])
    load = Manifold.cube([16, 16, 16], center=True).translate([GROOVE_X, y, bottom - 8])
    return [("line", ln), ("load", load)]


def assembly(tilt=0.0, with_board=True, with_crank=True, with_line=True):
    """tilt: degrees the reel swings on the hinge pin. At LOADED_TILT the line, leaving
    the wheel on the -y side, hangs straight under the pin."""
    parts = [("chassis", P.chassis_world()), ("wheel", P.wheel_world()), ("axle_tube", P.tube_world()),
             ("hanger_shaft", P.shaft_world()),
             ("lock_pin", P.pin_world("lock_pin", -XO - 0.5, 0, LOCK_R)),
             ("hinge_pin", P.pin_world("hinge_pin", -XO - 0.5, 0, PIVOT_Z)),
             ("cross_pin", P.pin_world("cross_pin", GROOVE_X - P.SHAFT_AF / 2 - 0.5, 0, CROSS_Z, roll=0))]
    if with_crank:
        parts.append(("crank", P.crank_world()))
    if tilt:
        parts = [(n, m.translate([0, 0, -PIVOT_Z]).rotate([tilt, 0, 0]).translate([0, 0, PIVOT_Z]) if n in SWINGS else m)
                 for n, m in parts]
    if with_line:
        t = math.radians(tilt)
        ay, az = PIVOT_Z * math.sin(t), PIVOT_Z - PIVOT_Z * math.cos(t)  # where the axle went
        parts += line(ay - FLOOR_R if tilt else FLOOR_R, az)
    if with_board:
        parts.append(("board", board()))
    return parts


def exploded():
    shift = {"chassis": (0, 0, 0), "wheel": (0, 0, -100), "axle_tube": (-80, 0, -100), "hanger_shaft": (0, 0, 50),
             "lock_pin": (-75, 0, 0), "hinge_pin": (-75, 0, 10), "cross_pin": (60, 0, 50), "crank": (95, 0, -100)}
    return [(n, m.translate(list(shift[n]))) for n, m in assembly(with_board=False, with_line=False)]


def bed_layout():
    """Every part as printed, spread out."""
    spots = {"chassis": (0, 0), "wheel": (150, 0), "axle_tube": (250, 0), "hanger_shaft": (0, 110),
             "lock_pin": (70, 110), "hinge_pin": (95, 110), "cross_pin": (120, 110), "crank": (190, 110)}
    out = []
    for name, build in P.PRINTED.items():
        m = build()
        if name in P.PINS or name == "crank":
            m = m.rotate([0, 0, 90])
        b = m.bounding_box()
        x, y = spots[name]
        out.append((name, m.translate([x - (b[0] + b[3]) / 2, y - (b[1] + b[4]) / 2, -b[2]])))
    return out


def render_all(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    parts = assembly()
    loaded = assembly(tilt=LOADED_TILT)
    th = LOADED_TILT
    torque = LINE_N * FLOOR_R / 1000

    save(out, "01_hanging", render(parts, 215, 25, "Hanging, unloaded (plywood see-through)"))
    save(out, "02_crank_side", render(parts, 35, 20, "Crank side: the crank's hex sits in the axle tube"))
    save(out, "03_loaded", render(loaded, 215, 20, f"Loaded straight down: the reel swings {th:.0f}° on the hinge pin"))
    save(out, "04_front", render(parts, 180, 0, "Front, looking along the axle, unloaded", size=(1100, 900), annotate=[
        ("dim", (0, -FLANGE_R, -FLANGE_R - 8), (0, FLANGE_R, -FLANGE_R - 8), "flange Ø100", (0, 28)),
        ("dim", (0, 75, 0), (0, 75, BOARD_Z), f"axle to plywood {BOARD_Z:.0f}", (0, 0)),
        ("dim", (0, -30, PIVOT_Z), (0, -30, BOARD_Z), f"hinge pin {PIVOT_DROP:.0f} below", (0, 0)),
        ("label", (0, 0, LOCK_R + 4), "lock pin", (190, -60)),
        ("label", (0, -LOCK_R, 0), "window: two wheel holes\ncentred here means\nthe lock pin will go in", (220, 60)),
        ("label", (0, 0, PIVOT_Z + 4), "hinge pin", (-160, -60)),
        ("label", (0, 0, CROSS_Z), "cross pin above the plywood", (100, -30)),
        ("label", (0, FLOOR_R, -80), "line, 50 lb braid", (-60, 0)),
    ]))
    save(out, "05_front_loaded", render(loaded, 180, 0, f"Front, loaded straight down: leans {th:.0f}°, line under the hinge pin",
                                        size=(1100, 900), annotate=[
        ("label", (0, 0, PIVOT_Z), "the bridge is round about the pin,\nso it never touches the plywood", (-120, -110))]))
    save(out, "06_side", render(parts, 90, 0, "Side, looking along the wheel's edge", size=(900, 900), annotate=[
        ("dim", (-XO, 0, -FLANGE_R - 6), (XO, 0, -FLANGE_R - 6), f"{2 * XO:.0f} across the cheeks", (0, 26)),
        ("label", (GROOVE_X, 0, PIVOT_Z + TONGUE_R + 3), "tongue in a slot;\nthe shaft turns in its hole", (150, -40)),
        ("label", (XO + 30, 0, -CRANK * 0.7), f"{CRANK:.0f} mm crank, pulls out", (-60, 70)),
    ]))
    save(out, "07_top", render(parts, 180, 89.5, "Top (plywood see-through)", size=(900, 700)))
    save(out, "08_exploded", render(exploded(), 215, 22, "Exploded: 8 printed parts", size=(1000, 900)))
    section = [(n, m) for n, m in assembly(with_crank=False, with_line=False)]
    save(out, "09_section", render(section, 90.001, 0.001,
         f"Section through the axle. 10 lb holds with {torque:.2f} N·m, {torque / CRANK * 1000:.0f} N on the crank",
         size=(900, 1000), cut=((1e-6, -1, 0), 0.0), annotate=[
             ("label", (GROOVE_X, 0, -FLOOR_R), f"groove floor Ø{2 * FLOOR_R:.0f}, {FLANGE_R - FLOOR_R:.0f} deep", (-60, 70)),
             ("label", (XI - 3, 0, -32), "open cup: the line's\nknot sits in here", (80, 40)),
             ("label", (GROOVE_X, 0, PIVOT_Z), "hinge pin through\nthe tongue", (-150, -20)),
             ("dim", (-WHEEL_W / 2, 0, -FLANGE_R - 6), (WHEEL_W / 2, 0, -FLANGE_R - 6), f"wheel {WHEEL_W:.0f} wide", (0, 30))]))
    save(out, "10_hinge", render([(n, m) for n, m in section if n in ("chassis", "hanger_shaft", "hinge_pin", "cross_pin", "board")],
                                 230, 30, "The hinge: tongue on a pin in the round bridge", size=(900, 800),
                                 cut=((0, -1, 0), -1.0)))
    save(out, "11_bed", render(bed_layout(), 200, 45, "As printed: every part on the bed, no supports", size=(1100, 800)))
    save(out, "12_chassis_print", render([("chassis", P.chassis_print())], 210, 25,
                                         "Chassis printed upright on its feet; holes get pointed tops", size=(900, 700)))
    save(out, "13_wheel_print", render([("wheel", P.wheel_print())], 200, 40,
                                       "Wheel as printed: open cup up, lock holes through the 5 mm web", size=(900, 700)))
    save(out, "14_wheel_under", render([("wheel", P.wheel_print())], 200, -35,
                                       "Wheel from underneath: the flat flange on the bed", size=(900, 700), light=(0.3, -0.4, -0.8)))
    pins = [("lock_pin", P.pin_print("lock_pin")),
            ("hinge_pin", P.pin_print("hinge_pin").translate([0, 24, 0])),
            ("cross_pin", P.pin_print("cross_pin").translate([0, 48, 0]))]
    save(out, "15_pins", render(pins, 240, 40, "Pins: lock (7.8, plain), hinge (7.8, snap tip), cross (6.2, snap tip)", size=(900, 600)))
    save(out, "16_tube_crank", render([("axle_tube", P.tube_print()),
                                       ("crank", P.crank_print().translate([40, -40, 0]))], 220, 35,
                                      "Axle tube (head down) and crank (flat), as printed", size=(900, 700)))
    save(out, "17_test_fit_plate", render(placed_views("test_fit"), 200, 50,
                                          "Test-fit plate: stubs and coupons for every fit", size=(1100, 650)))
    save(out, "18_full_plate", render(placed_views("full"), 200, 50, "Full plate: all eight parts", size=(1100, 800)))
