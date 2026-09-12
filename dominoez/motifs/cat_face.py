"""A cat's face, front on. A round head with pointed ears and three whiskers
a side; eyes, nose and mouth left standing."""

from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_R = 9.0
HEAD_C = (0.0, -1.0)
EAR = [(-9.5, 1.5), (-2.5, 6.5), (-7.5, 12.0)]  # left ear, base to tip; the right is mirrored
WHISKERS = [((8.0, 0.5), (13.0, 1.8)), ((8.6, -2.5), (13.2, -2.5)), ((8.0, -5.5), (13.0, -6.8))]  # right side
WHISKER_W = 1.5
EYES = [(-3.6, 1.8), (3.6, 1.8)]
EYE_D = 2.8
NOSE = [(-2.6, -1.0), (2.6, -1.0), (0.0, -4.2)]
MOUTH = [[(0.0, -3.6), (0.0, -5.2)], [(-3.0, -5.0), (-1.5, -6.2), (0.0, -5.2), (1.5, -6.2), (3.0, -5.0)]]
FEATURE_W = 1.8  # standing strokes, wide enough to survive rounding below
ROUND = 0.8  # every standing tip rounds to this, past half the island minimum
CLOSE = 0.6  # rounds the standing wedges between whiskers


def _mirror(points):
    return [(-u, v) for u, v in points]


def draw():
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    ears = [Polygon(EAR).buffer(-ROUND, 8).buffer(ROUND, 8), Polygon(_mirror(EAR)).buffer(-ROUND, 8).buffer(ROUND, 8)]
    whiskers = [stroke(list(w), WHISKER_W) for w in WHISKERS] + [stroke(_mirror(w), WHISKER_W) for w in WHISKERS]
    cat = union(head, *ears, *whiskers).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    features = union(
        *(dot(u, v, EYE_D) for u, v in EYES),
        Polygon(NOSE),
        *(stroke(m, FEATURE_W) for m in MOUTH),
    ).buffer(-ROUND, 16).buffer(ROUND, 16)
    return cat.difference(features)


motif = Motif(name="cat_face", issue=10, draw=draw)
