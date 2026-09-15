"""A bunny's face, front on. A round head with two tall ears standing up
from the crown, each with a standing inner-ear slot; eyes, a nose and a
split-lip mouth left standing."""

from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_R = 7.5
HEAD_C = (0.0, -2.0)
EAR = [(3.0, 3.0), (4.5, 12.5)]  # right ear, base to tip; the left is mirrored
EAR_W = 4.6
INNER_EAR = [(3.6, 5.5), (4.5, 10.5)]  # standing
INNER_EAR_W = 1.8
EYES = [(-3.0, -0.5), (3.0, -0.5)]
EYE_D = 2.6
NOSE = [(-2.1, -2.8), (2.1, -2.8), (0.0, -5.0)]
MOUTH = [[(0.0, -4.4), (0.0, -5.8)], [(-2.6, -5.4), (-1.3, -6.5), (0.0, -5.8), (1.3, -6.5), (2.6, -5.4)]]
FEATURE_W = 1.8  # standing strokes, wide enough to survive rounding below
ROUND = 0.8  # every standing tip rounds to this, past half the island minimum
CLOSE = 0.8  # fills the crease where each ear leaves the head


def _mirror(points):
    return [(-u, v) for u, v in points]


def draw():
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    ears = [stroke(EAR, EAR_W), stroke(_mirror(EAR), EAR_W)]
    bunny = union(head, *ears).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    features = union(
        stroke(INNER_EAR, INNER_EAR_W),
        stroke(_mirror(INNER_EAR), INNER_EAR_W),
        *(dot(u, v, EYE_D) for u, v in EYES),
        Polygon(NOSE),
        *(stroke(m, FEATURE_W) for m in MOUTH),
    ).buffer(-ROUND, 16).buffer(ROUND, 16)
    return bunny.difference(features)


motif = Motif(name="bunny_face", issue=39, draw=draw)
