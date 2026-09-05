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

**Blank**:
A domino with no motif. The reference body, printed first to check that the shape stands and prints cleanly.
