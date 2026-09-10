"""A toucan head, side view, facing right. A round head with a big eye and a
beak as deep as the head that curves down to a blunt tip, like a banana. A
standing line parts the beak from the head, where the colours break on the bird."""

from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_R = 7.0
HEAD_C = (-4.5, 0.0)
EYE_D = 3.4
EYE_C = (-4.0, 2.0)
# The beak is a disc swept along a quadratic curve (start, control, end), its
# width falling from the base, inside the head, to the tip.
BEAK_PATH = ((-4.5, -0.5), (5.5, 1.0), (10.5, -4.0))
BEAK_W = 11.0
TIP_W = 3.2
# The colour break between head and beak: a standing line, above the wall minimum.
BREAK = [(1.0, 8.5), (2.0, -7.0)]
BREAK_W = 1.2
CLOSE = 3.0  # radius that fills the crease between crown and beak into one arch


def _bezier(t, p0, p1, p2):
    return tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t**2 * c for a, b, c in zip(p0, p1, p2))


def draw():
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    beak = union(
        *(Point(*_bezier(t, *BEAK_PATH)).buffer((TIP_W + (BEAK_W - TIP_W) * (1 - t) ** 0.8) / 2, 32) for t in (i / 80 for i in range(81)))
    )
    bird = union(head, beak)
    # Fill the creases where the beak meets the head.
    bird = bird.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return bird.difference(dot(*EYE_C, EYE_D)).difference(stroke(BREAK, BREAK_W, cap="flat"))


motif = Motif(name="toucan", issue=5, draw=draw)
