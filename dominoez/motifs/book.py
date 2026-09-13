"""An open book seen from the front. Two engraved pages rise from a standing
spine, each page's top edge sweeping up toward the middle, with three
standing text lines running out from the spine across each page. A band of
engraved cover shows below the pages, parted from them by a standing wall,
dipping to a point under the spine."""

from shapely.geometry import Polygon, box

from ..geometry import stroke, union
from ..motif import Motif

PAGE_W = 9.5  # each page, from the spine out to its edge
SPINE_W = 1.4  # standing wall between the pages
BOTTOM_IN, BOTTOM_OUT = -6.0, -4.5  # page bottom at the spine and at the outer edge
TOP_OUT, TOP_IN = 4.5, 7.5  # page top at the outer edge and at the spine
BOW = -0.8  # the top edge sags by this much in its middle, so it sweeps up into the spine
TEXT_V = [2.8, 0.0, -2.8]  # standing lines, from the top down
TEXT_W = 1.6
TEXT_LEN = 6.0
COVER_OUT = 2.8  # how far the cover reaches below the pages
COVER_SIDE = 1.2  # how far the cover reaches past the pages' outer edges
COVER_TOP = -3.5  # the cover only shows below this height
WALL = 1.0  # standing gap between pages and cover
SMOOTH = 1.2  # rounds the cover's inner edge under the spine
ROUND = 0.7  # softens every page and cover corner


def _page(sign):
    """One page; sign is +1 for the right page, -1 for the left."""
    s = sign
    x0 = s * SPINE_W / 2
    x1 = s * (SPINE_W / 2 + PAGE_W)
    mid = (x0 + x1) / 2
    # Top edge: a gentle curve from the outer corner up into the spine.
    top = [(x1, TOP_OUT), (mid, (TOP_OUT + TOP_IN) / 2 + BOW), (x0, TOP_IN)]
    page = Polygon([(x0, BOTTOM_IN), (x1, BOTTOM_OUT), *top])
    page = page.buffer(-ROUND, 8).buffer(ROUND, 8)
    lines = [stroke([(0, v), (x0 + s * TEXT_LEN, v)], TEXT_W, cap="flat") for v in TEXT_V]
    return page.difference(union(*lines))


def draw():
    pages = union(_page(1), _page(-1))
    inner = pages.buffer(WALL, 8).buffer(SMOOTH, 8).buffer(-SMOOTH, 8)
    cover = pages.buffer(COVER_OUT, 8).difference(inner)
    reach = SPINE_W / 2 + PAGE_W + COVER_SIDE
    cover = cover.intersection(box(-reach, -20, reach, COVER_TOP))
    cover = cover.buffer(-ROUND, 8).buffer(ROUND, 8)
    return union(pages, cover)


motif = Motif(name="book", issue=51, draw=draw)
