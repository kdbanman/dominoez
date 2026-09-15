"""A cat walking in side profile, facing right: a wedge of a head with two
pointed ears and a short muzzle on a short neck, a long level back over a
deep chest, four legs (the far pair a step behind and a little shorter),
and a thin tail that rises from the rump in an S-curve and curls over
above the back. A solid silhouette traced from a classic cat icon; only
the eye is left standing."""

from shapely.geometry import Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

# One closed outline, clockwise from the nose: up the forehead, over the crown
# and down the nape, along the back to the rump, down the near hind leg to its
# paw, along the belly, down the near front leg to its paw, then up the chest
# and throat to the chin. The ears sit on the crown.
BODY = [
    (12.8, 3.0), (12.4, 3.8), (11.6, 4.6), (10.6, 5.2), (9.8, 5.5), (7.8, 5.7), (6.4, 5.5),  # nose, forehead, crown
    (5.0, 4.9), (4.7, 4.5), (4.6, 3.8), (4.4, 3.2), (4.0, 2.7), (3.4, 2.5),  # back of head and nape
    (2.6, 2.5), (-1.1, 2.3), (-4.8, 2.0), (-7.9, 1.9), (-9.1, 1.1), (-9.5, -0.2), (-9.3, -1.1),  # back and rump
    (-9.1, -2.7), (-8.6, -4.2), (-8.1, -6.1), (-7.2, -8.6), (-6.8, -10.0), (-6.6, -10.8), (-3.8, -10.8), (-3.9, -10.3), (-4.6, -9.7),  # hind leg and paw
    (-4.7, -7.3), (-4.2, -5.5), (-3.6, -4.7), (-2.4, -4.7), (0.1, -4.5), (2.0, -4.3), (2.6, -4.2),  # belly
    (3.1, -5.0), (3.3, -7.3), (3.2, -10.0), (3.3, -10.8), (6.8, -10.8), (6.5, -10.2), (5.9, -9.4), (5.9, -7.3), (6.4, -4.5),  # front leg and paw
    (7.3, -2.4), (8.1, -1.1), (8.8, 0.4), (9.4, 0.9), (10.2, 1.1), (11.0, 1.3), (11.8, 1.7), (12.4, 2.3),  # chest, throat and chin
]
EARS = [[(10.4, 5.0), (9.3, 9.4), (7.8, 5.6)], [(6.4, 5.6), (5.2, 9.2), (4.7, 4.5)]]  # near ear leaning forward, far ear leaning back: base, tip, base
FAR_LEGS = [[(3.5, -5.2), (1.7, -5.2), (1.8, -9.6), (3.5, -9.6)], [(-7.0, -5.6), (-9.4, -5.6), (-8.0, -9.6), (-6.6, -9.6)]]  # a step behind the near legs and a little shorter
TAIL = [(-8.4, -0.4), (-10.2, 1.2), (-11.0, 3.2), (-11.6, 5.2), (-11.6, 7.2), (-11.0, 8.9), (-9.9, 10.2), (-8.6, 10.7), (-7.2, 10.2)]  # from inside the rump, rising in an S and curling over the back
TAIL_W = 2.3
EYE = (9.6, 3.4, 2.0)  # standing (u, v, diameter)
CLOSE = 0.9  # blends the creases where the far legs and tail meet the body
EAR_CLOSE = 0.5  # blends the ear bases into the crown without filling the notch between the ears
ROUND = 0.55  # finally blunts the ear tips, nose and paw corners past half the channel minimum


def _spline(points, steps=8):
    """Points along a Catmull-Rom spline through `points`, so a stroke through them has no facets."""
    pts = [points[0], *points, points[-1]]
    out = []
    for p0, p1, p2, p3 in zip(pts, pts[1:], pts[2:], pts[3:]):
        for s in range(steps):
            t = s / steps
            out.append(
                tuple(
                    0.5 * (2 * b + (c - a) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (3 * b - a - 3 * c + d) * t * t * t)
                    for a, b, c, d in zip(p0, p1, p2, p3)
                )
            )
    return [*out, points[-1]]


def draw():
    cat = union(Polygon(BODY), *(Polygon(leg) for leg in FAR_LEGS), stroke(_spline(TAIL), TAIL_W))
    cat = cat.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    cat = union(cat, *(Polygon(ear) for ear in EARS))
    cat = cat.buffer(EAR_CLOSE, 16).buffer(-EAR_CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return cat.difference(dot(*EYE))


motif = Motif(name="kitty", issue=47, draw=draw)
