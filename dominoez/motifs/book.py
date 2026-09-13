"""An open book, the classic flat icon: two engraved pages side by side
forming a wide V, each rising from a standing spine to a slightly higher
outer edge, top and bottom edges gently bowed like a page seen from the
front and above. Three standing text lines run out from the spine across
each page, stopping short of the page's outer edge."""

from shapely.geometry import Polygon

from ..geometry import stroke, union
from ..motif import Motif

SPINE = 1.2  # standing gap between the pages
PAGE_W = 11.4  # each page, from the spine out to its edge
PAGE_H = 14.0  # page height, the same at the spine and at the outer edge
RISE = 2.0  # how much higher the outer edge sits than the spine
BOW = 0.4  # the top and bottom edges bulge up by this much in their middle, so the outer corner stays highest
MID_V = -1.0  # v of the page's mid line at the spine
TEXT_V = [3.4, 0.0, -3.4]  # standing lines, offset from the page's mid line
TEXT_W = 1.2
TEXT_INSET = 2.6  # from the outer page edge to the end of a line
ROUND = 0.8  # rounds every page corner


def _edge(sign, v0, n=24):
    """Points along a page edge from the spine out, starting at height v0.

    The edge rises by RISE over the page and bows up by BOW in the middle: a
    quadratic curve through the spine end, a raised control point, and the
    outer end.
    """
    x0, x1 = sign * SPINE / 2, sign * (SPINE / 2 + PAGE_W)
    xm, vm = (x0 + x1) / 2, v0 + RISE / 2 + 2 * BOW
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t**2
        pts.append((a * x0 + b * xm + c * x1, a * v0 + b * vm + c * (v0 + RISE)))
    return pts


def _page(sign):
    """One page; sign is +1 for the right page, -1 for the left."""
    top = _edge(sign, MID_V + PAGE_H / 2)
    bottom = _edge(sign, MID_V - PAGE_H / 2)
    page = Polygon(bottom + top[::-1])
    page = page.buffer(-ROUND, 16).buffer(ROUND, 16)
    # Text lines follow the bow of the page, start inside the spine so they
    # join the standing face, and stop short of the outer edge.
    x_end = SPINE / 2 + PAGE_W - TEXT_INSET - TEXT_W / 2
    lines = []
    for dv in TEXT_V:
        pts = [(u, v) for u, v in _edge(sign, MID_V + dv) if abs(u) <= x_end]
        lines.append(stroke([(0, MID_V + dv), *pts], TEXT_W))
    return page.difference(union(*lines))


def draw():
    return union(_page(1), _page(-1))


motif = Motif(name="book", issue=51, draw=draw)
