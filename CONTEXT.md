# Dominoez

A generator for 3D-printable toppling dominoes, each carrying a picture cut into both of its large sides. This file is the glossary. Dimensions, tolerances, and tooling live in `GUIDELINES.md` and the ADRs, not here.

## Language

**Domino**:
A standing toppling domino. A tall thin slab that prints upright on its narrow long edge.
_Avoid_: Tile, game piece, brick

**Face**:
Either of the two large vertical sides of a domino. Both faces carry the same motif, each oriented to read correctly from its own side.
_Avoid_: Front, back, side

**Foot**:
The narrow edge a domino stands on. It is the surface on the print bed.
_Avoid_: Base, bottom

**Crown**:
The narrow edge opposite the foot.
_Avoid_: Top, head

**Motif**:
The 2D picture cut into a face. Authored as code, exported to SVG for review, cut into the domino for printing.
_Avoid_: Design, icon, glyph, graphic, image

**Engraved**:
Cut into the face. The only relief style motifs use.
_Avoid_: Inset, recessed, debossed, embossed, raised

**Floor texture**:
The shallow relief on every pocket floor, a vertically compressed lattice of smooth bumps that reads as woven threads, so a recess reads against the flat face. One texture for the whole set.
_Avoid_: Pattern, surface finish, bump map, weave

**Blank**:
A domino with no motif. The reference body, printed first to check that the shape stands and prints cleanly.

**Motif box**:
The rectangle on a face inside which a motif must stay. It is the face minus a fixed margin.
_Avoid_: Safe area, canvas, bounds

**Grid motif**:
A motif defined as a grid of cells that are either live or dead, rendered in one of two styles (live cells cut, or field cut with live cells standing).
_Avoid_: Pixel art, bitmap
