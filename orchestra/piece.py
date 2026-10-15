"""A piece: parts written in the note syntax, plus tempo, dynamics, keys and directions."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

from .instruments import ORCHESTRA, Instrument
from .notation import DYNAMICS, Event, Meter, midi, parse, sample


@dataclass
class Part:
    instrument: str  # key in ORCHESTRA
    music: str
    dyn: str = "1 mf"  # "1 p, 3 p, 5:3 f": ramps between points, steps where two share a position
    name: str = ""  # defaults to the instrument's name
    gain: float = 0.0  # dB on top of the instrument default
    vel: int | None = None  # base velocity override

    @property
    def inst(self) -> Instrument:
        return ORCHESTRA[self.instrument]

    @property
    def label(self) -> str:
        return self.name or self.inst.name


@dataclass
class Piece:
    title: str
    key: str  # "Eb major", or keyed by position: "1 C major, 11 E major"
    tempo: str  # "1 56, 9:4 44"
    parts: list[Part]
    time: str = "4/4"
    pickup: float = 0
    tempo_text: str = ""
    directions: str = ""  # "8:3 allargando; 10 molto espressivo"
    apex: str = ""  # position of the intended emotional peak, reported in seconds
    tail: float = 4.0  # seconds of ring-out after the last note
    segments: list[tuple[str, str, str]] = field(default_factory=list)  # (name, start, end) cut from the render
    preview: list[tuple[str, int | None]] = field(default_factory=list)  # segments to play in order; int = bars
    seams: list[tuple[str, str]] = field(default_factory=list)  # (segment, loop): segment's end must flow into loop
    meter: Meter = field(init=False)

    def __post_init__(self):
        self.meter = Meter(self.time, self.pickup)

    def events(self, part: Part) -> list[Event]:
        default_art = next(iter(part.inst.arts))
        events = parse(part.music, self.meter, default_art)
        for e in events:
            if e.art not in part.inst.arts:
                raise ValueError(f"{part.label}: no articulation {e.art!r}")
            for p in e.pitches:
                if not part.inst.lo <= midi(p) <= part.inst.hi:
                    raise ValueError(f"{part.label}: {p} out of range at {self.meter.where(e.start)}")
        return events

    def length(self) -> Fraction:
        ends = {p.label: self.events(p)[-1].end for p in self.parts}
        if len(set(ends.values())) != 1:
            raise ValueError(f"parts end at different beats: {ends}")
        return next(iter(ends.values()))

    def dynamics(self, part: Part) -> list[tuple[float, float]]:
        return self.meter.curve(part.dyn, DYNAMICS)

    def keys(self) -> list[tuple[Fraction, str, str]]:
        out = []
        for item in filter(None, (s.strip() for s in self.key.split(","))):
            words = item.split()
            pos = self.meter.at(words[0]) if len(words) == 3 else Fraction(0)
            out.append((pos, words[-2], words[-1]))
        return out

    def directions_at(self) -> list[tuple[Fraction, str]]:
        out = []
        for item in filter(None, (s.strip() for s in self.directions.split(";"))):
            pos, text = item.split(maxsplit=1)
            out.append((self.meter.at(pos), text))
        return out

    def clock(self) -> Clock:
        return Clock(self.meter.curve(self.tempo), float(self.length()) + 8)


class Clock:
    """Beats -> seconds under a piecewise-linear tempo map."""

    STEP = 1 / 48

    def __init__(self, points: list[tuple[float, float]], end: float):
        self.beats = np.arange(0, end, self.STEP)
        bpm = np.array([sample(points, b) for b in self.beats])
        self.secs = np.concatenate([[0.0], np.cumsum(60.0 / bpm[:-1] * self.STEP)])

    def __call__(self, beat: float) -> float:
        return float(np.interp(float(beat), self.beats, self.secs))
