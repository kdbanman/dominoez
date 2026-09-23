"""A fat crescent moon, its horns pointing right and its bulge to the
left, with one plump five-pointed star floating in the hollow between
the horns."""

import math

from shapely.geometry import Polygon

from ..geometry import dot, union
from ..motif import Motif

MOON_C, MOON_D = (-1.5, 0.0), 20.0  # the full disc the crescent is cut from
BITE_C, BITE_D = (4.0, 1.0), 17.5  # the disc taken out of it
STAR_C, STAR_R, STAR_INNER = (5.0, 4.0), 4.0, 0.55  # centre, outer radius, inner radius as a fraction
ROUND = 0.6  # blunts the horns and the star's points


def _star(c, r, inner, n=5):
    cu, cv = c
    pts = []
    for i in range(2 * n):
        a = math.pi / 2 + math.pi * i / n
        rr = r if i % 2 == 0 else r * inner
        pts.append((cu + rr * math.cos(a), cv + rr * math.sin(a)))
    return Polygon(pts)


def draw():
    moon = dot(*MOON_C, MOON_D).difference(dot(*BITE_C, BITE_D))
    star = _star(STAR_C, STAR_R, STAR_INNER)
    sky = union(moon, star)
    return sky.buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="crescent_moon", issue=109, draw=draw)
