"""A classic round artist's paint brush tilted 45 degrees, bristles up and
to the right: a long slender handle that tapers gently to a rounded butt, a
short metal ferrule a little wider than the handle, and a short tuft of
bristles a little wider still that tapers to a rounded point. The whole
brush is one smooth silhouette; two thin standing lines part the ferrule
from the handle and from the bristles."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import stroke, union
from ..motif import Motif

# Drawn upright along v, bristles at the top, then tilted.
HANDLE_L = 18.0
HANDLE_W, BUTT_W = 3.8, 3.0  # width at the ferrule, tapering to the butt
FERRULE_W, FERRULE_L = 5.4, 5.0
BRISTLE_W, BRISTLE_L = 6.2, 7.5  # width at the ferrule, length to the tip
BELLY_W, BELLY_AT = 6.6, 1.6  # the tuft swells a little just past the ferrule, then tapers
TAPER = 1.8  # exponent of the tuft's taper; 2 is an ellipse, lower is pointier
TUFT_STEPS = 12  # points along one side of the taper
GAP = 1.2  # standing line between handle, ferrule and bristles, past the wall minimum
TILT = -45.0  # degrees; negative leans the bristles to the right
ROUND = 1.2  # rounds the handle butt and the bristle tip


def _taper(v_from, v_to):
    """The right edge of the tuft from its belly to its tip: a smooth ogive."""
    pts = []
    for i in range(TUFT_STEPS + 1):
        t = i / TUFT_STEPS
        pts.append((BELLY_W / 2 * (1 - t**TAPER), v_from + (v_to - v_from) * t))
    return pts


def draw():
    v0 = -(HANDLE_L + FERRULE_L + BRISTLE_L) / 2  # handle butt
    v1 = v0 + HANDLE_L  # handle meets ferrule
    v2 = v1 + FERRULE_L  # ferrule meets bristles
    v3 = v2 + BRISTLE_L  # bristle tip
    right = [
        (BUTT_W / 2, v0),
        (HANDLE_W / 2, v1),
        (FERRULE_W / 2, v1),
        (FERRULE_W / 2, v2),
        (BRISTLE_W / 2, v2),
        *_taper(v2 + BELLY_AT, v3),
    ]
    left = [(-u, v) for u, v in reversed(right[:-1])]
    brush = Polygon(right + left).buffer(-ROUND, 16).buffer(ROUND, 16)
    half = BRISTLE_W  # the lines run clear past both edges
    lines = union(*(stroke([(-half, v), (half, v)], GAP, cap="flat") for v in (v1, v2)))
    return affinity.rotate(brush.difference(lines), TILT, origin=(0, 0))


motif = Motif(name="paint_brush", issue=40, draw=draw)
