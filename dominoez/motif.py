from collections.abc import Callable
from dataclasses import dataclass

from shapely.geometry.base import BaseGeometry


@dataclass(frozen=True)
class Motif:
    """A picture cut into both faces of a domino.

    `draw` returns the engraved region in motif coordinates (see geometry.py).
    Return an empty geometry for a blank.
    """

    name: str
    issue: int  # sub-issue under the motif backlog, #2
    draw: Callable[[], BaseGeometry]

    def geometry(self) -> BaseGeometry:
        return self.draw()
