"""An acoustic guitar lying diagonally, body at the lower left and neck
pointing up and to the right at thirty-five degrees: a figure-eight body
of two round bouts with a smooth waist, a fat neck and a slightly wider
headstock. The sound hole is a standing disc. Strings are omitted."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

# Laid out with the neck straight up, then turned
UPPER_BOUT = ((0.0, 3.2), 4.8)  # (centre, radius)
LOWER_BOUT = ((0.0, -5.0), 6.2)
WAIST = 2.0  # closing radius that smooths the waist between the bouts
NECK = [(0.0, 5.0), (0.0, 13.0)]
NECK_W = 3.2
HEAD = (4.6, 4.6, 1.4, (0.0, 14.6))  # headstock: width, height, corner radius, centre; nose to headstock is about 27 mm
SOUND_HOLE = (0.0, -2.2, 4.0)  # standing (u, v, diameter)
TILT = -55.0  # degrees counter-clockwise from neck-up, so the neck points 35 degrees above horizontal to the right
CLOSE = 1.0  # blends the neck into the body and the headstock
ROUND = 0.5
SCALE = 0.96  # shrunk a few percent so the headstock stays inside the box once turned


def draw():
    body = union(Point(*UPPER_BOUT[0]).buffer(UPPER_BOUT[1], 64), Point(*LOWER_BOUT[0]).buffer(LOWER_BOUT[1], 64))
    body = body.buffer(WAIST, 16).buffer(-WAIST, 16)
    head = affinity.translate(rounded_rect(HEAD[0], HEAD[1], HEAD[2]), *HEAD[3])
    guitar = union(body, stroke(NECK, NECK_W), head).buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    guitar = guitar.difference(dot(*SOUND_HOLE))
    return affinity.rotate(affinity.scale(guitar, SCALE, SCALE, origin=(0, 0)), TILT, origin=(0, 0))


motif = Motif(name="guitar", issue=145, draw=draw)
