"""A cassette tape, tilted a little: a rounded rectangle with a standing
label across its upper half, two cut reel holes in the label, and a
standing trapezoid notch at the bottom edge for the head window."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import dot, rounded_rect, union
from ..motif import Motif

BODY_W, BODY_H, BODY_ROUND = 24.0, 15.5, 1.8
LABEL_W, LABEL_H, LABEL_ROUND, LABEL_V = 20.0, 8.0, 1.2, 1.6  # standing label, centred this far above the middle
REELS = [(-5.0, LABEL_V), (5.0, LABEL_V)]  # cut holes in the label
REEL_D = 4.4
WINDOW = [(-5.5, -BODY_H / 2 - 1.0), (5.5, -BODY_H / 2 - 1.0), (4.0, -5.0), (-4.0, -5.0)]  # standing notch up from the bottom edge
TILT = 12.0  # degrees counter-clockwise


def draw():
    body = rounded_rect(BODY_W, BODY_H, BODY_ROUND)
    label = affinity.translate(rounded_rect(LABEL_W, LABEL_H, LABEL_ROUND), 0, LABEL_V)
    tape = body.difference(union(label, Polygon(WINDOW)))
    tape = union(tape, *(dot(u, v, REEL_D) for u, v in REELS))
    return affinity.rotate(tape, TILT, origin=(0, 0))


motif = Motif(name="cassette_tape", issue=149, draw=draw)
