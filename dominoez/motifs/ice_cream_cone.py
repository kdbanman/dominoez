"""An ice cream cone as one solid silhouette: one big round scoop, wider
than the cone's mouth, sitting in a wide plain cone, with one thin standing
smile line along the cone's top edge where the scoop meets it."""

import math

from shapely.geometry import Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

SCOOP = (0.0, 5.0, 22.0)  # (u, v, diameter); its bottom sinks 6 mm into the cone's mouth
CONE = [(-8.5, 0.0), (8.5, 0.0), (0.0, -16.0)]  # triangle, mouth up
SMILE = ((-10.5, 0.0), (10.5, 0.0))  # ends of the standing arc along the cone's top edge, run out past the scoop's sides
SMILE_BOW = 2.0  # the arc's middle sits this far above its ends
SMILE_W = 1.2  # standing
ROUND = 0.4  # blunts the tip and the corners
STEPS = 24


def _smile():
    (u0, v0), (u1, v1) = SMILE
    points = [(u0 + (u1 - u0) * t, v0 + (v1 - v0) * t + SMILE_BOW * math.sin(math.pi * t)) for t in (i / STEPS for i in range(STEPS + 1))]
    return stroke(points, SMILE_W)


def draw():
    cone = union(dot(*SCOOP), Polygon(CONE))
    return cone.difference(_smile()).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="ice_cream_cone", issue=114, draw=draw)
