"""A flying saucer: a wide flat lens of a hull with three standing lights
along its rim, a round dome on top, and a fat beam fanning out below,
narrow at the hull and wide at the ground, parted from the hull by a
standing gap."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, union
from ..motif import Motif

HULL_C, HULL_W, HULL_H = (0.0, 3.0), 24.0, 6.6  # lens of a hull
DOME = (0.0, 5.0, 11.0)  # (u, v, diameter); the lower half hides in the hull
LIGHTS = [(-6.8, 3.0, 2.3), (0.0, 2.5, 2.3), (6.8, 3.0, 2.3)]  # standing (u, v, diameter)
BEAM_TOP, BEAM_BOTTOM = 5.0, 16.0  # width at the hull and at the far end
BEAM_V0, BEAM_V1 = -1.5, -12.5  # top and bottom of the beam
ROUND = 0.6  # blunts the beam corners and the hull rim


def _ellipse(c, w, h):
    return affinity.scale(Point(c).buffer(1.0, 96), w / 2, h / 2, origin=c)


def draw():
    hull = _ellipse(HULL_C, HULL_W, HULL_H)
    dome = dot(*DOME)
    saucer = union(hull, dome).buffer(-ROUND, 16).buffer(ROUND, 16)
    saucer = saucer.difference(union(*(dot(u, v, d) for u, v, d in LIGHTS)))
    beam = Polygon([(-BEAM_TOP / 2, BEAM_V0), (BEAM_TOP / 2, BEAM_V0), (BEAM_BOTTOM / 2, BEAM_V1), (-BEAM_BOTTOM / 2, BEAM_V1)])
    beam = beam.buffer(-ROUND, 16).buffer(ROUND, 16)
    return union(saucer, beam)


motif = Motif(name="ufo", issue=110, draw=draw)
