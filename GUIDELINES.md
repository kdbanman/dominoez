# Guidelines

Everything here follows from one fact: a domino prints standing on its foot, on a single-colour printer with a 0.4 mm nozzle. Vocabulary is in `CONTEXT.md`. Why we chose the tools is in `docs/adr/`.

The printer is a Creality CR-10 Smart Pro and the filament is PLA. Both are fixed, so slicing is part of the build: `slicer/profile.ini` holds the PrusaSlicer settings (0.20 mm layers, 3 perimeters, 10% grid infill, a skirt, no supports). Only the blank's gcode is committed, as a check that the slicer output has not drifted; every motif's gcode is an artifact named `<motif>.gcode` on the latest CI run. Change the profile only by printing the change first, then pasting the config block from that gcode over the file.

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

## Motif placement

| Part | Value |
| --- | --- |
| Across | centered |
| Crown gap (crown to the top of the motif) | 6 mm |

Motifs sit high on the face, hung from a line 6 mm below the crown, so a row of standing dominoes reads as a row of pictures at eye level. A motif is drawn centred on the origin and the build moves it into place, so the placement can change without touching any motif. The crown gap must be at least the margin or the motif crosses the motif box.

## Engraving

1.5 mm deep on average, straight walls, identical motif on both faces. Each face's copy is oriented so a viewer standing in front of that face reads it correctly.

Every pocket floor carries the same texture: a lattice of smooth bumps, like a layer of close-packed spheres squeezed vertically until it reads as woven threads. Bumps sit 3 mm apart along a row, rows are 1.56 mm apart (a regular hexagonal lattice compressed to 0.6), and each row is offset half a bump from the next. Bump tops are the shallowest points at 1.17 mm, the gaps between three bumps are the deepest at 1.83 mm, so the relief is plus or minus 0.33 mm about 1.5 mm and the solid core is never thinner than 8.3 mm. The lattice is centred on the face with a bump top at the centre. The texture is there so a recess catches light differently from the flat face on a single-colour print. It applies to every motif with no switch, including the field of a field-cut grid motif.

The relief is three cosines with wave vectors 60 degrees apart, so bumps are round and the transitions are smooth. Vertical is the layer direction, so the row squash sets how far each layer's perimeter shifts from the one below: at 0.6 the wall is at most 46 degrees from vertical and the shift is 0.21 mm per 0.2 mm layer, about half a nozzle width. Squashing further steepens that quickly. Along a row the bump spacing is nozzle-limited; under about 2 mm it turns to noise.

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
- Standing shapes may meet corner to corner (a hole in the cut touching its edge at one point). The build parts the two rings by a hair before extruding the pocket, so the mesh closes and the print is unchanged.

## Grid motifs

Two styles, chosen per motif.

**Live cells cut.** Each live cell is an engraved square. Adjacent live cells are separated by a wall of the minimum wall width. Used for the Game of Life glider and R-pentomino, where the pattern is a few cells on an empty field.

**Field cut, live cells standing.** The whole bounding grid is engraved and live cells stay at face level. Adjacent live cells merge into one island. Used for the Minecraft creeper face, where the eyes and mouth are the picture and the field is background.

Cell size comes from dividing the motif box width by the grid width. A creeper at 8 cells across gives 3.5 mm cells, above the island minimum.

## Review flow

1. Write the motif as a Python function returning shapely geometry.
2. Build renders `svg/<name>.svg` and `png/<name>.png` showing the whole face at true scale: face outline, foot chamfer line, the motif box as a faint dashed rectangle, the motif in black.
3. The PNG goes into chat for approval.
4. On approval, build `stl/<name>.stl`. Commit SVG, PNG, and STL together in a PR that closes the motif's sub-issue under #2. CI slices it and publishes the gcode as an artifact.

CI rebuilds everything and fails if any committed output differs from what the code produces.
