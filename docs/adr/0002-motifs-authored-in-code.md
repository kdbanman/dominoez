# Motifs are authored in code, SVG is a build output

A motif's source of truth is a Python function returning shapely geometry. The SVG and PNG in the repo are rendered from it for review, never edited by hand.

The alternative was hand-authored SVG files parsed into geometry. We rejected it because a 0.4 mm nozzle needs every stroke and gap to clear a minimum width, and those limits are only enforceable when strokes are parameters (a centerline buffered by half a stroke width) rather than drawn paths. Code also makes families of motifs cheap: a pipped domino or a Game of Life pattern is a loop, not a drawing.
