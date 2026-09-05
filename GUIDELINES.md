# Guidelines

Everything here follows from one fact: a domino prints standing on its foot, on a single-colour printer with a 0.4 mm nozzle. Vocabulary is in `CONTEXT.md`. Why we chose the tools is in `docs/adr/`.

The printer is a Creality CR-10 Smart Pro and the filament is PLA. Both are fixed, so slicing is part of the build: `slicer/profile.ini` holds the PrusaSlicer settings (0.20 mm layers, 3 perimeters, 10% grid infill, a skirt, no supports) and `gcode/` holds the result. Change the profile only by printing the change first, then pasting the config block from that gcode over the file.

## Body

| Part | Value |
| --- | --- |
| Height (foot to crown) | 72 mm |
| Width | 36 mm |
| Thickness | 12 mm |
| Vertical edge radius | 2.5 mm |
| Crown radius | 2.5 mm |
| Foot chamfer | 0.5 mm |

The body is convex. Vertical edges come from extruding a rounded rectangle. The crown comes from a convex hull over that rectangle shrunk along a quarter-circle profile. The foot chamfer is the same trick with a straight profile. No fillet operations anywhere.

Thickness is 12 mm rather than the usual 8 mm so the foot is wide enough to stand through some elephant's foot. The chamfer is there so the first layer's squish does not widen the footprint past the face.

## Print orientation and what it costs

Foot on the bed, faces vertical. Consequences:

- Layer lines run horizontally across each face. Horizontal detail is limited by the nozzle (0.4 mm), vertical detail by layer height (assume 0.2 mm).
- Every engraved pocket has a ceiling. On a vertical face that ceiling is a 1.5 mm cantilever with nothing beneath it. Tuned printers handle 1.5 mm; do not go deeper. Straight pocket walls for now. Revisit only if the heart's top edge prints badly.
- Both faces are equal. There is no front.

## Motif box

| Part | Value |
| --- | --- |
| Margin from every edge | 4 mm |
| Box | 28 mm wide, 64 mm tall |
| Placement | centered on the face, both axes |

The margin must exceed the 2.5 mm edge radius. Anything closer sits on the curve and the pocket floor breaks through the round.

## Engraving

1.5 mm deep, straight walls, identical motif on both faces. Each face's copy is oriented so a viewer standing in front of that face reads it correctly. Cutting 1.5 mm from each face leaves a 9 mm solid core.

## Printability rules

The build checks these and fails when a motif breaks one. Do not loosen them to get a motif through. Change the motif.

| Rule | Minimum |
| --- | --- |
| Engraved channel width (a stroke that is cut) | 1.0 mm |
| Wall left standing between two cuts | 1.0 mm |
| Island (standing material surrounded by cut on all sides) | 1.5 mm |
| Motif entirely inside the motif box | required |

The check erodes the engraved region by half the minimum channel width and confirms nothing vanishes, then does the same to the standing region. A feature that disappears under erosion is a feature the nozzle cannot make.

## Drawing motifs

- Draw for arm's length. The face is 36 mm wide. If the shape does not read at 36 mm on screen, it will not read in plastic.
- Fewer, fatter shapes. Strokes of 2 to 3 mm read best. 1 mm is the floor, not the target.
- Silhouettes beat outlines. A filled duck is a duck. An outlined duck is a wire.
- Strokes are centerlines buffered by half a width, so width is a parameter. Never draw a stroke as two parallel edges.
- No detail inside detail. An eye is a dot or nothing.
- Curves are fine. Sharp inside corners on standing material are fine. Sharp inside corners on the pocket floor round to the nozzle radius anyway.

## Grid motifs

Two styles, chosen per motif.

**Live cells cut.** Each live cell is an engraved square. Adjacent live cells are separated by a wall of the minimum wall width. Used for the Game of Life glider and R-pentomino, where the pattern is a few cells on an empty field.

**Field cut, live cells standing.** The whole bounding grid is engraved and live cells stay at face level. Adjacent live cells merge into one island. Used for the Minecraft creeper face, where the eyes and mouth are the picture and the field is background.

Cell size comes from dividing the motif box width by the grid width. A creeper at 8 cells across gives 3.5 mm cells, above the island minimum.

## Review flow

1. Write the motif as a Python function returning shapely geometry.
2. Build renders `svg/<name>.svg` and `png/<name>.png` showing the whole face at true scale: face outline, foot chamfer line, the motif box as a faint dashed rectangle, the motif in black.
3. The PNG goes into chat for approval.
4. On approval, build `stl/<name>.stl` and slice `gcode/<name>.gcode`. Commit SVG, PNG, STL, and gcode together in a PR that closes the motif's sub-issue under #2.

CI rebuilds everything and fails if any committed output differs from what the code produces.
