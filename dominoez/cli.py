import argparse
import re
import sys
from pathlib import Path

from .build import REPO, Unprintable, build_motif, render_motif
from .check import check
from .motifs import MOTIFS
from .plate import capacity, plate
from .slice import SlicerMissing, slice_motif, slice_stl, stats

_COUNT = re.compile(r"^(?:x(\d+)|(\d+)x)$")


def _select(names: list[str]):
    if not names:
        return list(MOTIFS.values())
    missing = [n for n in names if n not in MOTIFS]
    if missing:
        sys.exit(f"unknown motif(s): {', '.join(missing)}. Known: {', '.join(MOTIFS)}")
    return [MOTIFS[n] for n in names]


def _select_counted(tokens: list[str]):
    """Motifs for a plate: names, each optionally followed by a count like `x4` or `4x`.

    No tokens means one of every registered motif.
    """
    if not tokens:
        return list(MOTIFS.values())
    chosen = []
    for token in tokens:
        count = _COUNT.match(token)
        if count:
            if not chosen:
                sys.exit(f"count {token!r} must follow a motif name")
            chosen.extend([chosen[-1]] * (int(count.group(1) or count.group(2)) - 1))
        else:
            chosen.extend(_select([token]))
    return chosen


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="dominoez")
    sub = p.add_subparsers(dest="cmd", required=True)
    for cmd, doc in (
        ("build", "check, render SVG and PNG, and export STL"),
        ("render", "check and render SVG and PNG only (for approval)"),
        ("check", "run printability checks and report"),
        ("slice", "slice built STLs to gcode with PrusaSlicer"),
    ):
        sp = sub.add_parser(cmd, help=doc)
        sp.add_argument("names", nargs="*")
        sp.add_argument("--out", type=Path, default=REPO, help="output root (default: repo root)")
    sub.add_parser("list", help="list registered motifs")
    sp = sub.add_parser("plate", help="lay built dominoes out on one bed as plate/<name>.stl, and slice it if PrusaSlicer is on the path")
    sp.add_argument("names", nargs="*", help="motif names, each optionally followed by a count like x4 (default: one of everything)")
    sp.add_argument("--name", default="plate", help="output name (default: plate)")
    sp.add_argument("--out", type=Path, default=REPO, help="output root (default: repo root)")
    args = p.parse_args(argv)

    if args.cmd == "list":
        for m in MOTIFS.values():
            print(f"{m.name}\t#{m.issue}")
        return

    if args.cmd == "plate":
        motifs = _select_counted(args.names)
        cols, rows = capacity()
        try:
            stl = plate(motifs, args.name, args.out)
        except (ValueError, FileNotFoundError) as e:
            sys.exit(str(e))
        print(f"{args.name}: {len(motifs)} dominoes on a bed of {cols} x {rows}, {stl}")
        gcode = stl.with_suffix(".gcode")
        try:
            slice_stl(stl, gcode)
        except SlicerMissing as e:
            print(f"{args.name}: STL only, {e}")
            return
        summary = stats(gcode)
        print(
            f"{args.name}: slice ok, {summary.get('filament used [g]', '?')} g, "
            f"{summary.get('estimated printing time (normal mode)', '?')}, {gcode}"
        )
        return

    failed = False
    for motif in _select(args.names):
        if args.cmd == "slice":
            try:
                gcode = slice_motif(motif, args.out)
            except (SlicerMissing, FileNotFoundError) as e:
                sys.exit(str(e))
            summary = stats(gcode)
            print(
                f"{motif.name}: slice ok, {summary.get('filament used [g]', '?')} g, "
                f"{summary.get('estimated printing time (normal mode)', '?')}"
            )
            continue
        if args.cmd == "check":
            problems = check(motif.geometry())
            status = "ok" if not problems else "FAIL"
            print(f"{motif.name}: {status}")
            for v in problems:
                print(f"  - {v}")
            failed |= bool(problems)
            continue
        try:
            (build_motif if args.cmd == "build" else render_motif)(motif, args.out)
            print(f"{motif.name}: {args.cmd} ok")
        except Unprintable as e:
            print(e, file=sys.stderr)
            failed = True
    if failed:
        sys.exit(1)
