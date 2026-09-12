"""A bold slab-serif capital I, hand-built from strokes in the style of the
letter G: a thick vertical stem with a short serif bar across each end, so
it reads as a capital I and not a lowercase l."""

from ..geometry import stroke, union
from ..motif import Motif

STROKE = 4.5  # width of every stroke, matching the G
HEIGHT = 21.5  # overall, serif to serif, matching the G's outer diameter
SERIF_W = 11.0  # end to end


def draw():
    half = HEIGHT / 2 - STROKE / 2  # centreline of each serif bar
    stem = stroke([(0.0, -half), (0.0, half)], STROKE, cap="flat")
    serifs = [stroke([(-SERIF_W / 2, v), (SERIF_W / 2, v)], STROKE, cap="flat") for v in (-half, half)]
    return union(stem, *serifs)


motif = Motif(name="letter_i", issue=30, draw=draw)
