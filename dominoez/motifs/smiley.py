"""A smiley: one cut disc with two standing dots for eyes and a single
standing arc for the smile. Nothing else."""

import math

from shapely.geometry import LineString, Point

from ..geometry import dot, union
from ..motif import Motif

FACE_D = 25.0  # mm diameter of the disc
EYE_D = 3.0  # mm diameter of each standing eye
EYES = [(-4.4, 3.6), (4.4, 3.6)]  # (u, v) of each eye
SMILE_C = (0.0, 1.0)  # centre of the circle the smile is an arc of
SMILE_R = 7.2  # mm radius of that circle
SMILE_ARC = (215.0, 325.0)  # degrees, the arc below the centre from left to right
SMILE_W = 2.5  # mm width of the standing smile


def _smile():
    a0, a1 = SMILE_ARC
    pts = [
        (SMILE_C[0] + SMILE_R * math.cos(math.radians(a)), SMILE_C[1] + SMILE_R * math.sin(math.radians(a)))
        for a in [a0 + (a1 - a0) * i / 48 for i in range(49)]
    ]
    return LineString(pts).buffer(SMILE_W / 2, 16)


def draw():
    face = Point(0, 0).buffer(FACE_D / 2, 96)
    features = union(*(dot(u, v, EYE_D) for u, v in EYES), _smile())
    return face.difference(features)


motif = Motif(name="smiley", issue=159, draw=draw)
