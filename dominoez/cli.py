import argparse
import sys
from pathlib import Path

from .build import REPO, Unprintable, build_motif, render_motif
from .check import check
from .motifs import MOTIFS
from .plate import PLATES, capacity, plate, read, saved, select
from .slice import SlicerMissing, slice_motif, slice_stl, stats


def _select(names: list[str]):
    if not names:
        return list(MOTIFS.values())
    missing = [n for n in names if n not in MOTIFS]
    if missing:
        sys.exit(f"unknown motif(s): {', '.join(missing)}. Known: {', '.join(MOTIFS)}")
    return [MOTIFS[n] for n in names]


def _plates(args) -> list[tuple[str, list]]:
    """(name, motifs) for each plate to make: the tokens given, or every file in plates/."""
    if args.names:
        return [(args.name, select(args.names))]
    files = saved()
    if not files:
        raise ValueError(f"no plate files in {PLATES}")
    return [(name, read(path)) for name, path in files.items()]


def _plate(name: str, motifs: list, out: Path) -> None:
    cols, rows = capacity()
    stl = plate(motifs, name, out)
    print(f"{name}: {len(motifs)} dominoes on a bed of {cols} x {rows}, {stl}")
    gcode = stl.with_suffix(".gcode")
    try:
        slice_stl(stl, gcode)
    except SlicerMissing as e:
        print(f"{name}: STL only, {e}")
        return
    summary = stats(gcode)
    print(
        f"{name}: slice ok, {summary.get('filament used [g]', '?')} g, "
        f"{summary.get('estimated printing time (normal mode)', '?')}, {gcode}"
    )


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
    sp.add_argument("names", nargs="*", help="motif names, each optionally followed by a count like x4, or * for one of everything (default: every file in plates/)")
    sp.add_argument("--name", default="plate", help="output name when motifs are given (default: plate)")
    sp.add_argument("--out", type=Path, default=REPO, help="output root (default: repo root)")
    args = p.parse_args(argv)

    if args.cmd == "list":
        for m in MOTIFS.values():
            print(f"{m.name}\t#{m.issue}")
        return

    if args.cmd == "plate":
        try:
            for name, motifs in _plates(args):
                _plate(name, motifs, args.out)
        except (ValueError, FileNotFoundError) as e:
            sys.exit(str(e))
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
