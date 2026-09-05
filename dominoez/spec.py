"""Every dimension in one place. Millimetres. See GUIDELINES.md."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Body:
    height: float = 72.0  # foot to crown
    width: float = 36.0
    thickness: float = 12.0
    edge_radius: float = 2.5  # vertical edges
    crown_radius: float = 2.5
    foot_chamfer: float = 0.5


@dataclass(frozen=True)
class Engraving:
    depth: float = 1.5
    margin: float = 4.0  # from every face edge to the motif box


@dataclass(frozen=True)
class Texture:
    """Relief on every pocket floor: a hexagonal lattice of smooth bumps, like a
    layer of close-packed spheres. Three cosines at 60 degrees to each other.

    Bumps (shallowest points) sit `spacing` mm apart along a row. Rows are
    squeezed together by `row_squash` (1.0 is a regular hexagonal lattice;
    smaller stretches each bump sideways so the field reads as woven threads).
    Depth spans Engraving.depth +/- amplitude. The floor is sampled on a grid
    of `step` mm.
    """

    amplitude: float = 0.33
    spacing: float = 3.0
    row_squash: float = 0.6
    step: float = 0.3


@dataclass(frozen=True)
class Limits:
    """Printability minimums for a 0.4 mm nozzle. The build fails when a motif breaks one."""

    channel: float = 1.0  # narrowest engraved cut
    wall: float = 1.0  # narrowest standing material between cuts
    island: float = 1.5  # narrowest standing material surrounded by cut
    residual_area: float = 0.2  # mm^2 of lost material that counts as a violation


BODY = Body()
ENGRAVING = Engraving()
TEXTURE = Texture()
LIMITS = Limits()


def motif_box_size() -> tuple[float, float]:
    """Width and height of the motif box."""
    return (
        BODY.width - 2 * ENGRAVING.margin,
        BODY.height - 2 * ENGRAVING.margin,
    )
