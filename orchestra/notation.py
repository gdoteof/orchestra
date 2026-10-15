"""The compact note syntax that piece files are written in.

    E5:4.        dotted quarter          r:8        eighth rest
    E5:8t        triplet eighth          <C4 E4>:2  chord (half note)
    E5:2~ E5:8   tie                     |          bar check
    E5:4!        accent   E5:4'  staccato   E5:4_  tenuto
    A2:8*8       the same token eight times
    @trem        switch articulation for the notes that follow
    %80          base velocity for the notes that follow (lower is a softer, slower attack)

A token without a duration reuses the previous duration. Durations are counted in quarter-note
beats, so 6/8 has three beats to the bar.

Positions in a piece (dynamics, tempo, directions) are written `bar` or `bar:beat`, 1-based, with
bar 0 being the pickup bar: `9:3.5` is the "and" of beat 3 in bar 9.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

STEP = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)
ALTER = {"": 0, "#": 1, "##": 2, "x": 2, "b": -1, "bb": -2}
_PITCH = re.compile(r"([A-G])(##|#|x|bb|b)?(-?\d)$")
_TOKEN = re.compile(r"(r|<[^>]+>|[A-G](?:##|#|x|bb|b)?-?\d)(?::(\d+)(\.*)(t?))?([~!'_]*)$")

DYNAMICS = dict(ppp=20, pp=32, p=46, mp=60, mf=74, f=88, ff=104, fff=118)


def midi(name: str) -> int:
    m = _PITCH.match(name)
    if not m:
        raise ValueError(f"bad pitch {name!r}")
    step, alter, octave = m.groups()
    return 12 * (int(octave) + 1) + STEP[step] + ALTER[alter or ""]


@dataclass
class Event:
    start: Fraction
    dur: Fraction
    pitches: tuple[str, ...]  # empty for a rest
    art: str
    accent: bool = False
    staccato: bool = False
    tenuto: bool = False
    art_change: bool = False  # first event after an @switch
    vel: int | None = None  # base velocity set by a %token

    @property
    def rest(self) -> bool:
        return not self.pitches

    @property
    def end(self) -> Fraction:
        return self.start + self.dur


class Meter:
    """Converts between beats and bar positions for one time signature and pickup."""

    def __init__(self, time: str, pickup: float):
        num, den = (int(x) for x in time.split("/"))
        self.time = time
        self.bar = Fraction(num * 4, den)
        self.pickup = Fraction(pickup).limit_denominator(48)

    def bar_of(self, beat: Fraction) -> int:
        return 0 if beat < self.pickup else int((beat - self.pickup) // self.bar) + 1

    def where(self, beat: Fraction) -> str:
        b = self.bar_of(beat)
        into = beat - (self.pickup + (b - 1) * self.bar)
        return f"bar {b} beat {float(into) + 1:g}"

    def at(self, spec: str) -> Fraction:
        bar, _, beat = spec.partition(":")
        if int(bar) == 0 and not beat:
            return Fraction(0)
        pos = self.pickup + (int(bar) - 1) * self.bar + Fraction(beat or "1") - 1
        if pos < 0:
            raise ValueError(f"position {spec} is before the start")
        return pos

    def curve(self, spec: str, names: dict[str, float] | None = None) -> list[tuple[float, float]]:
        """`"1 p, 3 p, 5:3 f"` -> [(beat, value), ...]; values are names from `names` or numbers."""
        points = []
        for item in filter(None, (s.strip() for s in spec.split(","))):
            pos, value = item.split()
            v = names[value] if names and value in names else float(value)
            points.append((float(self.at(pos)), v))
        return points


def sample(points: list[tuple[float, float]], beat: float) -> float:
    """Piecewise-linear lookup; two points at one position make a step."""
    if beat <= points[0][0]:
        return points[0][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if beat < x1:
            return y0 if x1 == x0 else y0 + (y1 - y0) * (beat - x0) / (x1 - x0)
    return points[-1][1]


def _duration(base: str, dots: str, tup: str) -> Fraction:
    total = add = Fraction(4, int(base))
    for _ in dots:
        add /= 2
        total += add
    return total * Fraction(2, 3) if tup else total


def parse(text: str, meter: Meter, art: str) -> list[Event]:
    events: list[Event] = []
    pos = Fraction(0)
    dur = Fraction(1)
    tie = False
    art_change = False
    vel = None
    tokens = []
    for tok in re.findall(r"<[^>]*>\S*|\S+", text):
        m = re.fullmatch(r"(.+)\*(\d+)", tok)
        tokens += [m.group(1)] * int(m.group(2)) if m else [tok]
    for tok in tokens:
        if tok == "|":
            if pos < meter.pickup or (pos - meter.pickup) % meter.bar:
                raise ValueError(f"bar check failed at {meter.where(pos)}")
            continue
        if tok.startswith("@"):
            art, art_change = tok[1:], True
            continue
        if tok.startswith("%"):
            vel = int(tok[1:])
            continue
        m = _TOKEN.match(tok)
        if not m:
            raise ValueError(f"bad token {tok!r} at {meter.where(pos)}")
        head, base, dots, tup, marks = m.groups()
        if base:
            dur = _duration(base, dots, tup)
        if head == "r":
            pitches: tuple[str, ...] = ()
        elif head.startswith("<"):
            pitches = tuple(head[1:-1].split())
        else:
            pitches = (head,)
        for p in pitches:
            midi(p)
        if tie:
            prev = events[-1]
            if [midi(p) for p in prev.pitches] != [midi(p) for p in pitches]:
                raise ValueError(f"tie into different pitches at {meter.where(pos)}")
            prev.dur += dur
        else:
            events.append(Event(pos, dur, pitches, art, "!" in marks, "'" in marks, "_" in marks, art_change, vel))
            art_change = False
        tie = "~" in marks
        pos += dur
    if tie:
        raise ValueError("dangling tie at the end")
    return events
