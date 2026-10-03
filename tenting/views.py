"""Review renders of the cradle, through the reel's flat-shaded SVG renderer."""

from pathlib import Path

from manifold3d import JoinType, Manifold, OpType

from reel.render import COL, render, save

from . import parts as P
from .spec import FEET, FLOOR, TILT

COL.update({"cradle": "#d9822b", "plate": "#4a505a", "feet": "#1c1c1c"})

# The keyboard's rubber feet, for the renders only: 8 mm bumpers in the plate's recesses.
KEYBOARD_FEET = [(-112, 70), (-112, 24), (-106, -4), (-59, -4), (-7, 3), (-1, 71)]


def plate() -> Manifold:
    """A stand-in for the bottom plate: its outline, a 2 mm floor and a 6.4 mm rim."""
    o = P.outline()
    rim = (o - o.offset(-1.6, JoinType.Miter)).extrude(6.4)
    return o.extrude(2.0) + rim


def feet() -> Manifold:
    return Manifold.batch_boolean([Manifold.cylinder(FEET, 4, 4, 32).translate([x, y, -FEET]) for x, y in KEYBOARD_FEET],
                                  OpType.Add)


def seated() -> list[tuple[str, Manifold]]:
    """The left half on its cradle. Cut into small triangles, so the renderer's painter's
    order holds where the plate sits close over the pocket floor."""
    t = P.plate_transform()[:3]
    parts = [("cradle", P.cradle_left()), ("plate", plate().transform(t)), ("feet", feet().transform(t))]
    return [(n, m.refine_to_length(4.0)) for n, m in parts]


def render_all(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    cradle = [("cradle", P.cradle_left())]
    save(out, "01_seated", render(seated(), 235, 30, f"Left half on the cradle, tented {TILT:.0f}°", size=(1000, 800)))
    save(out, "02_empty", render(cradle, 235, 50, "The pocket: notches for the XIAO's USB-C, TRRS + USB-C, power switch",
                                 size=(1000, 800)))
    save(out, "03_thumb_side", render(cradle, 15, 15, "Thumb side: the wedge drops straight to the desk", size=(1000, 800)))
    save(out, "04_under", render(cradle, 235, -40, "Underneath: four 13 mm pockets for desk feet", size=(1000, 800),
                                 light=(0.3, -0.4, -0.8)))
    save(out, "05_section", render(seated(), 270, 0.001, "Section through the middle, looking from the front",
                                   size=(1100, 800), cut=((0, 1, 0), 40.0)))
    tray = [("cradle", P.test_fit_left()), ("plate", plate().translate([0, 0, FLOOR + FEET]))]
    save(out, "06_test_fit", render([(n, m.refine_to_length(4.0)) for n, m in tray], 235, 35, f"Test-fit tray: the same pocket and lip on a {FLOOR} mm floor", size=(1000, 800)))
