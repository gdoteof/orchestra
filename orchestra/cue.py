"""Game cues: sections written with their own bar numbers, joined into one render and cut into segments.

Rendering a cue in one pass gives every cut the right reverb tail at its head: order the render so that each
segment follows what precedes it in play, and render a looping section twice so that its second pass (the one
that is cut out) starts with its own tail. The cut pass and whatever leads into the first pass then end on a short
crossfade into the first pass's ending, which is what the loop's head continues.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .notation import Meter, parse
from .piece import Part, Piece


@dataclass
class Section:
    bars: int
    tempo: str  # positions are local to the section
    music: dict[str, str]  # instrument -> notes; instruments left out rest
    dyn: dict[str, str] = field(default_factory=dict)  # instrument -> dynamics; default "1 mf"
    key: str = ""  # "D minor", in force from the section's first bar
    directions: str = ""


def _shift(spec: str, offset: int, sep: str = ",") -> list[tuple[str, str]]:
    items = []
    for item in filter(None, (s.strip() for s in spec.split(sep))):
        pos, value = item.split(maxsplit=1)
        bar, colon, beat = pos.partition(":")
        items.append((f"{int(bar) + offset}{colon}{beat}", value))
    return items


def _stepped(per_section: list[tuple[int, list[tuple[str, str]]]]) -> str:
    """Join per-section curves so that each section starts on its own value instead of ramping into it."""
    out: list[tuple[str, str]] = []
    for offset, items in per_section:
        if out:
            out.append((str(offset + 1), out[-1][1]))
        out.append((str(offset + 1), items[0][1]))
        out += items
    return ", ".join(f"{p} {v}" for p, v in out)


def join(title: str, render: list[tuple[str, Section]], order: list[str], time: str = "4/4",
         gains: dict[str, float] | None = None, preview: list[tuple[str, int | None]] | None = None,
         tail: float = 4.0) -> Piece:
    """`render` lists (segment name, section) in render order; a section may appear twice under two names."""
    meter = Meter(time, 0)
    offsets, total = [], 0
    for name, sec in render:
        for inst, text in sec.music.items():
            try:
                events = parse(text, meter, "x")
            except ValueError as err:
                raise ValueError(f"{name}/{inst}: {err}") from None
            if events[-1].end != sec.bars * meter.bar:
                raise ValueError(f"{name}/{inst}: {float(events[-1].end)} beats, expected {sec.bars} bars")
        offsets.append(total)
        total += sec.bars

    parts = []
    for inst in order:
        if not any(inst in sec.music for _, sec in render):
            continue
        music, curves = [], []
        for (name, sec), off in zip(render, offsets):
            text = sec.music.get(inst)
            if text is None:
                music.append("r:1 | " * sec.bars)
                continue
            music.append(text.strip().rstrip("|") + " |")
            curves.append((off, _shift(sec.dyn.get(inst, "1 mf"), off)))
        parts.append(Part(inst, " ".join(music), dyn=_stepped(curves), gain=(gains or {}).get(inst, 0)))

    tempo = _stepped([(off, _shift(sec.tempo, off)) for (_, sec), off in zip(render, offsets)])
    keys = ", ".join(f"{off + 1} {sec.key}" for (_, sec), off in zip(render, offsets) if sec.key)
    directions = "; ".join(f"{p} {t}" for (_, sec), off in zip(render, offsets)
                           for p, t in _shift(sec.directions, off, ";"))
    segments = [(name, str(off + 1), str(off + sec.bars + 1)) for (name, sec), off in zip(render, offsets)]
    seams = []
    for i, ((first, a), (name, b)) in enumerate(zip(render, render[1:])):
        if first.startswith("_") and a is b:
            seams.append((name, name))
            if i:
                seams.append((render[i - 1][0], name))
    return Piece(title=title, key=keys, tempo=tempo, parts=parts, time=time, directions=directions,
                 segments=segments, preview=preview or [], tail=tail, seams=seams)
