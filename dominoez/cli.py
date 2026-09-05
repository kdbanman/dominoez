import argparse
import sys
from pathlib import Path

from .build import REPO, Unprintable, build_motif, render_motif
from .check import check
from .motifs import MOTIFS
from .slice import SlicerMissing, slice_motif, stats


def _select(names: list[str]):
    if not names:
        return list(MOTIFS.values())
    missing = [n for n in names if n not in MOTIFS]
    if missing:
        sys.exit(f"unknown motif(s): {', '.join(missing)}. Known: {', '.join(MOTIFS)}")
    return [MOTIFS[n] for n in names]


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
    args = p.parse_args(argv)

    if args.cmd == "list":
        for m in MOTIFS.values():
            print(f"{m.name}\t#{m.issue}")
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
