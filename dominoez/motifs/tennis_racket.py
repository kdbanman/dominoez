"""A tennis racket leaning to the right: a big oval head with a fat frame
and a coarse standing grid of strings, two walls along the handle's axis
and two across it, a short throat and a fat straight handle. The racket
is drawn upright and rotated as a whole, so the strings stay square to
the handle."""

from shapely import affinity
from shapely.geometry import Point, Polygon, box

from ..geometry import stroke, union
from ..motif import Motif

HEAD_C = (0.0, 8.0)
HEAD = (8.5, 10.0)  # outer half-width and half-height of the oval
FRAME_W = 2.3
STRING_W = 1.6  # standing walls, above the island minimum
STRING_PITCH = 2.3  # walls sit this far either side of the head's centre, so the middle cells are 3 mm and the outer ones wider
STRING_ALONG = (0.1, 15.9)  # bottom and top of the two walls along the axis; they end square inside the frame
STRING_ACROSS = 6.65  # half-length of the two walls across the axis, ending square inside the frame
THROAT = [(-4.2, -1.0), (4.2, -1.0), (2.4, -4.5), (-2.4, -4.5)]  # trapezoid from the head's bottom into the handle
HANDLE = [(0.0, -3.5), (0.0, -14.0)]
HANDLE_W = 4.2
TILT = -28.0  # degrees, so the head leans right
ROUND = 0.5  # blunts the string cells' corners
CLOSE = 0.6  # smooths the throat


def _oval(rx, ry):
    return affinity.scale(Point(*HEAD_C).buffer(1.0, 96), rx, ry, origin=HEAD_C)


def draw():
    outer = _oval(*HEAD)
    cu, cv = HEAD_C
    strings = union(
        *(box(cu + s * STRING_PITCH - STRING_W / 2, STRING_ALONG[0], cu + s * STRING_PITCH + STRING_W / 2, STRING_ALONG[1]) for s in (-1, 1)),
        *(box(cu - STRING_ACROSS, cv + s * STRING_PITCH - STRING_W / 2, cu + STRING_ACROSS, cv + s * STRING_PITCH + STRING_W / 2) for s in (-1, 1)),
    )
    racket = union(outer, Polygon(THROAT), stroke(HANDLE, HANDLE_W))
    racket = racket.buffer(CLOSE, 16).buffer(-CLOSE, 16).difference(strings).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.rotate(racket, TILT, origin=(0, 0))


motif = Motif(name="tennis_racket", issue=137, draw=draw)
