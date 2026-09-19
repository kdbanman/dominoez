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

**Plate**:
Many dominoes laid out standing on one print bed and sliced as a single print.
_Avoid_: Batch, tray, build plate, multi-print

**Round**:
A numbered backlog of motifs with one parent issue, one issue per category, and one issue per motif.
_Avoid_: Backlog, milestone, phase

**Batch**:
The motifs from a few categories of a round that are drawn together and reviewed together, up to fifty. One branch, one review doc, one PR.
_Avoid_: Sprint, chunk, wave

**Review doc**:
The single page that shows every render in a batch at the SVG stage, where each motif is approved by default and can be marked redo or drop with a note. The page copies its own state to the clipboard for pasting into chat.
_Avoid_: Contact sheet, gallery, review artifact, approval page

**Profile**:
The one set of PrusaSlicer settings every domino is sliced with, for the one printer and filament we target. Captured from a print that came out well, never tuned by hand.
_Avoid_: Slicer settings, print settings, config
