# Python mesh stack instead of OpenSCAD or a CAD kernel

Dominoes are convex slabs with pockets cut into two faces, so a real CAD kernel buys nothing. We build them in Python with shapely for 2D geometry, trimesh plus manifold3d for extrusion and booleans, and cairosvg for review renders. Managed with uv.

## Considered options

- OpenSCAD: no raster preview of the motif, slow booleans in the 2021 apt build, and text or path work is clumsy.
- build123d or CadQuery: true fillets and chamfers, but a heavy OCCT install for a shape whose fillets we can get exactly by extruding rounded rectangles and hull-sweeping a profile.
- JS with manifold-3d: works, but the 2D tooling is weaker than shapely and nothing is gained.

## Consequences

Rounded edges are built from 2D offsets and convex hulls, not fillet operations. Anyone wanting a non-convex body later will have to add a different construction.
