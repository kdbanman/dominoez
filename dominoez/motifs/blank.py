"""The blank domino: no motif. Print this first."""

from shapely.geometry import Polygon

from ..motif import Motif

motif = Motif(name="blank", issue=3, draw=lambda: Polygon())
