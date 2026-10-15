"""Engrave a piece: MusicXML through music21, page images through Verovio."""

from __future__ import annotations

import re
from pathlib import Path

import cairosvg
import verovio
from music21 import (articulations, chord, clef, dynamics, expressions, instrument, key, metadata, meter,
                     note, stream)

from .notation import DYNAMICS, sample
from .piece import Piece

CLEFS = {"treble": clef.TrebleClef, "alto": clef.AltoClef, "bass": clef.BassClef, "bass8vb": clef.Bass8vbClef,
         "perc": clef.PercussionClef}
PERC = {"bd": ("F", 4, "normal"), "snare": ("C", 5, "normal"), "cym": ("A", 5, "x")}  # staff position, notehead
ART_TEXT = {"trem": "trem.", "pizz": "pizz.", "arco": "arco", "ord": "ord.", "stacc": "", "roll": "roll", "hit": ""}


def _m21_pitch(name: str) -> str:
    m = re.match(r"([A-G])(##|#|x|bb|b)?(-?\d)$", name)
    step, alter, octave = m.groups()
    return step + {"": "", "#": "#", "##": "##", "x": "##", "b": "-", "bb": "--"}[alter or ""] + octave


def _dynamic_marks(piece: Piece, part, p: stream.Part, notes: list, pad: float) -> None:
    pts = [(x + pad, v) for x, v in piece.dynamics(part)]
    names = {v: k for k, v in DYNAMICS.items()}

    def notes_between(a, b):
        return [n for n in notes if a <= n.offset < b]

    prev = None
    for i, (x, v) in enumerate(pts):
        if v != prev and v in names:
            p.insert(x, dynamics.Dynamic(names[v]))
        if i and pts[i - 1][1] != v and pts[i - 1][0] != x:
            span = notes_between(pts[i - 1][0], x)
            if len(span) > 1:
                wedge = dynamics.Crescendo if v > pts[i - 1][1] else dynamics.Diminuendo
                p.insert(0, wedge(span[0], span[-1]))
        prev = v


def to_score(piece: Piece) -> stream.Score:
    score = stream.Score()
    score.metadata = metadata.Metadata(title=piece.title, composer="Claude")
    pad = (piece.meter.bar - piece.meter.pickup) % piece.meter.bar  # pickup notes sit at the end of bar 0
    for i, part in enumerate(piece.parts):
        p = stream.Part()
        inst = instrument.Instrument()
        inst.partName, inst.partAbbreviation = part.label, part.inst.abbr
        p.insert(0, inst)
        p.insert(0, CLEFS[part.inst.clef]())
        p.insert(0, meter.TimeSignature(piece.time))
        perc = part.inst.clef == "perc"
        for pos, tonic, mode in piece.keys():
            # an unpitched staff needs its own empty signature, or Verovio gives it the score's key
            sig = key.KeySignature(0) if perc else key.Key(tonic.replace("b", "-") if len(tonic) > 1 else tonic, mode)
            p.insert(float(pos + pad), sig)
        if i == 0:
            first_bpm = piece.meter.curve(piece.tempo)[0][1]
            mark = expressions.TextExpression(f"{piece.tempo_text} ({first_bpm:g} bpm)".strip())
            mark.style.fontWeight, mark.placement = "bold", "above"
            p.insert(0, mark)
            for pos, text in piece.directions_at():
                d = expressions.TextExpression(text)
                d.style.fontStyle, d.placement = "italic", "above"
                p.insert(float(pos + pad), d)
        notes = []
        for e in piece.events(part):
            if e.rest:
                n = note.Rest(quarterLength=e.dur)
            elif perc:
                n = note.Unpitched(quarterLength=e.dur)
                n.displayStep, n.displayOctave, n.notehead = PERC.get(part.instrument, ("B", 4, "normal"))
            elif len(e.pitches) == 1:
                n = note.Note(_m21_pitch(e.pitches[0]), quarterLength=e.dur)
            else:
                n = chord.Chord([_m21_pitch(x) for x in e.pitches], quarterLength=e.dur)
            if e.accent:
                n.articulations.append(articulations.Accent())
            if e.staccato or e.art == "stacc":
                n.articulations.append(articulations.Staccato())
            if e.tenuto:
                n.articulations.append(articulations.Tenuto())
            if e.art == "trem" and not e.rest:
                n.expressions.append(expressions.Tremolo(numberOfMarks=3))
            if e.art == "roll" and not e.rest:
                n.expressions.append(expressions.Tremolo(numberOfMarks=3))
            if e.art_change and ART_TEXT.get(e.art):
                p.insert(float(e.start + pad), expressions.TextExpression(ART_TEXT[e.art]))
            p.insert(float(e.start + pad), n)
            if not e.rest:
                notes.append(n)
        if pad:
            p.insert(0, note.Rest(quarterLength=pad))
        _dynamic_marks(piece, part, p, notes, float(pad))
        p.makeMeasures(inPlace=True)
        p.makeTies(inPlace=True)
        if pad:
            m0 = p.getElementsByClass(stream.Measure).first()
            for r in list(m0.getElementsByClass(note.Rest)):
                if r.offset < pad:
                    m0.remove(r)
            m0.paddingLeft = float(pad)
            for m in p.getElementsByClass(stream.Measure):
                m.number -= 1
        score.insert(0, p)
    return score


def _unpitched_keys(tk: verovio.toolkit, perc: set[int]) -> None:
    """Verovio turns a key change in every pitched part into a score-wide one, which puts sharps and flats on the
    percussion staves; rewrite each such change as per-staff changes for the pitched staves only."""
    mei = tk.getMEI()
    staves = sorted({int(n) for n in re.findall(r'<staffDef[^>]*\bn="(\d+)"', mei)})

    def per_staff(m: re.Match) -> str:
        defs = "".join(f'<staffDef n="{n}">{m.group(1)}</staffDef>' for n in staves if n not in perc)
        return f"<scoreDef><staffGrp>{defs}</staffGrp></scoreDef>"

    mei, count = re.subn(r'<scoreDef xml:id="[^"]+">\s*(<keySig[^>]*/>)\s*</scoreDef>', per_staff, mei)
    if count:
        tk.loadData(mei)


def engrave(piece: Piece, outdir: Path) -> list[Path]:
    xml = outdir / "score.musicxml"
    to_score(piece).write("musicxml", fp=xml)
    tk = verovio.toolkit()
    tk.setOptions({"pageWidth": 2600, "pageHeight": 3600, "scale": 38, "adjustPageHeight": True,
                   "footer": "none", "breaks": "auto", "condense": "none"})
    tk.loadFile(str(xml))
    perc = {i + 1 for i, part in enumerate(piece.parts) if part.inst.clef == "perc"}
    if perc:
        _unpitched_keys(tk, perc)
    pages = []
    for n in range(1, tk.getPageCount() + 1):
        png = outdir / f"score-{n}.png"
        cairosvg.svg2png(bytestring=tk.renderToSVG(n).encode(), write_to=str(png), background_color="white",
                         output_width=1800)
        pages.append(png)
    return pages
