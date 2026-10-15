"""uv run python -m orchestra pieces/withheld.py [--no-audio]"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from .engrave import engrave
from .render import ROOT, render


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PIECE


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pieces", nargs="+", type=Path)
    ap.add_argument("--no-audio", action="store_true")
    args = ap.parse_args()
    for path in args.pieces:
        piece = load(path)
        outdir = ROOT / "build" / path.stem
        outdir.mkdir(parents=True, exist_ok=True)
        print(f"== {piece.title}: {float(piece.length())} beats")
        for page in engrave(piece, outdir):
            print("score", page)
        if not args.no_audio:
            report = render(piece, outdir)
            print("audio", outdir / "mix.mp3", json.dumps({k: v for k, v in report.items() if k != "bars"}))
            print("  ".join(f"{b}@{t}s:{db}" for b, t, db in report["bars"]))


if __name__ == "__main__":
    main()
