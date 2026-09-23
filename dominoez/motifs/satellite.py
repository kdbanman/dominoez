"""The classic satellite icon, banked as it orbits: a square body in the
middle, two long rectangular solar panels on short struts to left and
right, each crossed by one standing line, and on top a dish drawn as a
fat quarter-circle on a short stem, parted from the body by a standing
gap, with a stub feed poking out of its face."""

from shapely import affinity
from shapely.geometry import Point, box

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

BODY = 6.0  # square body side
PANEL_W, PANEL_H = 8.6, 4.6  # each solar panel
STRUT_LEN, STRUT_W = 1.4, 2.0  # from body to panel
PANEL_SPLIT = 1.3  # standing line across each panel's middle
DISH_CORNER, DISH_R = (-3.0, 4.4), 5.6  # the quarter-circle's right-angle corner and radius; it floats above the body on a stem
DISH_GAP = 1.4  # standing gap between the dish and the body, either side of the stem
STEM = [(-1.0, 2.0), (-1.0, 5.0)]
STEM_W = 2.2
FEED = [(0.8, 6.8), (3.6, 9.6)]  # stub poking out of the dish's curved face
FEED_W = 2.4
TILT = 20.0  # degrees; the satellite banks as it passes
ROUND = 0.55
CLOSE = 0.8


def draw():
    body = rounded_rect(BODY, BODY, 0.8)
    half = BODY / 2
    panels, splits = [], []
    for sign in (-1, 1):
        u0 = sign * (half + STRUT_LEN)
        strut = stroke([(sign * (half - 1.0), 0.0), (u0, 0.0)], STRUT_W)
        panel = affinity.translate(rounded_rect(PANEL_W, PANEL_H, 0.5), u0 + sign * PANEL_W / 2, 0.0)
        panels.append(union(strut, panel))
        splits.append(affinity.translate(rounded_rect(PANEL_SPLIT, PANEL_H + 2.0, 0.0), u0 + sign * PANEL_W / 2, 0.0))
    cu, cv = DISH_CORNER
    dish = Point(cu, cv).buffer(DISH_R, 96).intersection(box(cu, cv, cu + DISH_R, cv + DISH_R))
    dish = union(dish, stroke(FEED, FEED_W))
    craft = union(body, *panels).buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    craft = craft.difference(dish.buffer(DISH_GAP, 16))
    sat = union(craft, dish.buffer(-ROUND, 16).buffer(ROUND, 16), stroke(STEM, STEM_W))
    sat = sat.difference(union(*splits))
    return affinity.rotate(sat, TILT, origin=(0.0, 0.0))


motif = Motif(name="satellite", issue=112, draw=draw)
