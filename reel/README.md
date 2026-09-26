# Reel

A lockable reel for fishing line that hangs from a 1/2" hole in a 3/4" plywood shelf and holds up to 10 lb. Eight printed parts, PLA, no glue, no supports. It lives on this branch for now and shares the domino repo's tooling, not its code.

```
uv run reel build     # reel/stl/<part>.stl, each part as it sits on the bed
uv run reel render    # reel/png/, the review renders
uv run reel plate     # reel/plate/test_fit and full, .stl and, with prusa-slicer, .gcode
uv run pytest tests/test_reel.py
```

Every dimension is in `reel/spec.py`. The parts are built in `reel/parts.py`.

## How it works

- The **wheel** (Ø100) winds 50 lb braid in a groove whose floor is Ø70. A 10 lb load holds with 1.56 N·m: 31 N on the 50 mm crank, or 31 N at the rim if you turn it by hand. 3 m of braid builds up about 1 mm in the groove, so the groove's depth is there for leverage and grip, not for storage. The line goes through a hole in the groove floor and is knotted inside the open cup.
- The **lock pin** goes through both cheeks and one of ten holes in the wheel's web, so the wheel locks every 36°. The curved window beside the axle shows the two wheel holes left and right of the axle. When they are centred in it, the pin will go in. The lock and hinge holes are 8.4 mm, so a round pencil crayon stands in for a lost pin.
- The **axle tube** slides through the head-side cheek, the wheel and the far cheek, and its slotted lip snaps past the far cheek. Its hex middle drives the wheel. Its hex bore takes the **crank**, which pulls out.
- The **hanger shaft** is an octagon that nearly fills the 1/2" hole and turns freely in it. A **cross pin** above the plywood holds it up. Its flat tongue hangs the chassis from the **hinge pin**, so the reel can both turn and lean toward the pull. Loaded straight down, it leans 30°, which puts the line right under the hinge pin. Whichever way it's pulled, the shaft is never bent. The chassis's bridge is round about the hinge pin, which sits 18 mm below the plywood, so the reel can lean about 65° either way without touching the board.
- The shaft sits 7 mm off the wheel's centre plane, right over the groove, so the line pulls in the hinge's plane.

## Printing

| Part | On the bed |
| --- | --- |
| chassis | upright on its two feet, each with a 4 mm flare outside. The horizontal holes have pointed tops. The bridge's underside spans 28 mm between the cheeks. |
| wheel | flat flange down, cup open on top. The groove's upper flank is 45°. |
| axle tube | head down |
| hanger shaft | on its side, so its layers run the length of the pull |
| crank, pins | flat |

Both plates slice with the domino profile plus a 4 mm brim. Without the brim, PrusaSlicer warns of low bed adhesion: the chassis stands 111 tall. The full plate also gets 4 perimeters and 30% gyroid infill, since it carries the load. CI uploads the gcode as `reel-test_fit.gcode` and `reel-full.gcode`.

| Plate | What's on it | Time | PLA |
| --- | --- | --- | --- |
| test_fit | a cheek strip with both tube holes and three pin holes; a ladder bar with three wheel hexes, three pin holes and three cross-pin holes; a short axle tube; the hanger shaft; the hinge and cross pins; three crank-hex stubs; a nominal 1/2" hole. `reel/fit_map.html` says what goes into what. | 4h 49m | 41 g |
| full | all eight parts | 17h 25m | 167 g |

The only slicer warning left on the full plate is "long bridging extrusions", which is the bridge's 28 mm underside.

Assembly: shaft's tongue into the slot and hinge pin through → wheel between the cheeks → axle tube through from the head side until the lip clicks → tie the line through the anchor hole → shaft up through the shelf, cross pin through above.

## Fits

The first test fit, at 0.3 across a hex's flats and 0.6 on a round fit, was too tight: the hexes would not go in at all, and every round fit took too much force. The printer's extrusion and elephant's foot are calibrated, so the blame went to sharp corners ringing, plus too little clearance. Round two:

| Fit | Sizes | Clearance |
| --- | --- | --- |
| hexes (tube in wheel, crank in tube) | corners filleted 1.5 male, 1.0 female | 0.8 across flats |
| tube bearings in the cheeks | Ø24 in Ø24.9, Ø20 in Ø20.9 | 0.9 on diameter |
| lock and hinge pins | Ø7.6 in Ø8.6 | 1.0 on diameter |
| cross pin | Ø6.1 in Ø6.9 | 0.8 on diameter |
| tongue in its slot | 11.4 in 12.6 | 1.2 |
| shaft in the 1/2" hole | octagon 11.4 across flats, corners filleted 1.5, in Ø12.7 | |
| snaps (tube lip, pin tips) | overlap the hole's edge by 0.15 each side | |

The test-fit plate carries ladders for the hexes and pin holes: 1, 2 or 3 notches mark 0.2 tighter than these, these, and 0.2 looser.
