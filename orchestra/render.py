"""Render a piece: one MIDI file per part and articulation, sfizz for each, then mix with a hall."""

from __future__ import annotations

import json
import random
import subprocess
from pathlib import Path

import mido
import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve

from .notation import midi, sample
from .piece import Clock, Part, Piece

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples" / "Virtual-Playing-Orchestra3"
SFIZZ = ROOT / "third_party" / "sfizz" / "build" / "library" / "bin" / "sfizz_render"
SR = 48000
PPQ = 960
TICKS_PER_SEC = PPQ * 2  # files are written at a fixed 120 bpm; the tempo map is baked into the times
DB_PER_CC = 34 / 127  # the PERF patches' gain_cc1 range


def _note_times(piece: Piece, part: Part, clock: Clock, events, rng):
    """(on, off, key, velocity) per sounding note, plus each note's level, for one articulation."""
    dyn = piece.dynamics(part)
    out = []
    for e in events:
        if e.rest:
            continue
        on = clock(e.start)
        off = clock(e.end)
        if e.staccato:
            off = on + min(0.5 * (off - on), 0.25)
        else:
            off += 0.08  # legato overlap; the patches' release does the rest
        level = sample(dyn, float(e.start))
        for p in e.pitches:
            jitter = rng.uniform(-0.008, 0.008)
            out.append([on + jitter, off, midi(p), level, e.accent, e.tenuto, e.vel])
    # a repeated pitch must not overlap itself, or the second note-on cuts the first short
    out.sort(key=lambda n: (n[2], n[0]))
    for a, b in zip(out, out[1:]):
        if a[2] == b[2] and a[1] > b[0] - 0.01:
            a[1] = max(a[0] + 0.03, b[0] - 0.01)
    return out


def _velocity(base: int, mode: str, level: float, accent: bool, tenuto: bool, rng) -> int:
    if mode == "velocity":
        v = 20 + 0.85 * level + (20 if accent else 0)
    else:
        v = base + 0.2 * (level - 64) + (35 if accent else 0) + (6 if tenuto else 0)
    return int(np.clip(v + rng.uniform(-3, 3), 1, 127))


def _write_midi(path: Path, notes, ccs, end: float) -> None:
    timed = [(t, 0, mido.Message("control_change", control=1, value=v)) for t, v in ccs]
    for on, off, key, vel in notes:
        timed.append((off, 1, mido.Message("note_off", note=key, velocity=0)))
        timed.append((on, 2, mido.Message("note_on", note=key, velocity=vel)))
    timed.sort(key=lambda x: (x[0], x[1]))
    mid = mido.MidiFile(ticks_per_beat=PPQ)
    track = mido.MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage("set_tempo", tempo=500000, time=0))
    last = 0
    for t, _, msg in timed:
        tick = max(0, round(t * TICKS_PER_SEC))
        track.append(msg.copy(time=tick - last))
        last = tick
    track.append(mido.MetaMessage("end_of_track", time=max(0, round(end * TICKS_PER_SEC) - last)))
    mid.save(path)


def _cc_curve(dyn, clock: Clock, end_beat: float) -> list[tuple[float, int]]:
    out, last = [], None
    for b in np.arange(0, end_beat + 1e-9, 1 / 16):
        v = int(round(sample(dyn, b)))
        if v != last:
            out.append((clock(b), v))
            last = v
    return out


def _gain_envelope(dyn, clock: Clock, frames: int, end_beat: float) -> np.ndarray:
    beats = np.arange(0, end_beat + 1, 1 / 16)
    secs = np.array([clock(b) for b in beats])
    db = np.array([(sample(dyn, b) - 127) * DB_PER_CC for b in beats])
    t = np.arange(frames) / SR
    return 10 ** (np.interp(t, secs, db) / 20)


def _pan(audio: np.ndarray, pan: float) -> np.ndarray:
    theta = (pan + 1) * np.pi / 4
    return audio * np.array([np.cos(theta), np.sin(theta)]) * np.sqrt(2)


def render_part(piece: Piece, part: Part, clock: Clock, workdir: Path, seed: int) -> np.ndarray:
    events = piece.events(part)
    end_beat = float(piece.length())
    end_sec = clock(end_beat) + piece.tail
    dyn = piece.dynamics(part)
    rng = random.Random(seed)
    base = part.vel or part.inst.vel
    stems = []
    for art, (patch, mode, *art_gain) in part.inst.arts.items():
        mine = [e for e in events if e.art == art]
        if not any(not e.rest for e in mine):
            continue
        notes = [
            (max(0.0, on), off, key, _velocity(v or base, mode, level, acc, ten, rng))
            for on, off, key, level, acc, ten, v in _note_times(piece, part, clock, mine, rng)
        ]
        ccs = _cc_curve(dyn, clock, end_beat) if mode == "cc1" else []
        stem = f"{part.instrument}-{seed}-{art}"
        mid, wav = workdir / f"{stem}.mid", workdir / f"{stem}.wav"
        _write_midi(mid, notes, ccs, end_sec)
        subprocess.run(
            [str(SFIZZ), "--sfz", str(SAMPLES / patch), "--midi", str(mid), "--wav", str(wav),
             "--use-eot", "-s", str(SR), "-p", "256"],
            check=True, capture_output=True,
        )
        audio, sr = sf.read(wav, dtype="float32", always_2d=True)
        assert sr == SR
        if audio.shape[1] == 1:
            audio = np.repeat(audio, 2, axis=1)
        if mode == "gain":
            audio = audio * _gain_envelope(dyn, clock, len(audio), end_beat)[:, None]
        stems.append(audio * 10 ** (sum(art_gain) / 20))
    n = max(len(s) for s in stems)
    out = np.zeros((n, 2), dtype=np.float32)
    for s in stems:
        out[: len(s)] += s
    out *= 10 ** ((part.inst.gain + part.gain) / 20)
    return _pan(out, part.inst.pan)


def hall_ir(rt: float = 2.3, seed: int = 7) -> np.ndarray:
    """A synthetic concert-hall impulse response: decorrelated noise, highs dying first."""
    n = int(SR * rt * 1.3)
    t = np.arange(n) / SR
    freqs = np.fft.rfftfreq(n, 1 / SR)
    rng = np.random.default_rng(seed)
    out = np.zeros((n, 2))
    for ch in range(2):
        spec = np.fft.rfft(rng.standard_normal(n))
        for lo, hi, r in ((0, 350, rt * 1.15), (350, 2500, rt), (2500, 8000, rt * 0.6), (8000, SR, rt * 0.3)):
            band = np.fft.irfft(spec * ((freqs >= lo) & (freqs < hi)), n)
            out[:, ch] += band * np.exp(-6.91 * t / r)
    out *= np.clip(t / 0.06, 0, 1)[:, None]  # the diffuse tail builds up rather than starting dense
    out = np.concatenate([np.zeros((int(0.022 * SR), 2)), out])
    return out / np.sqrt((out**2).sum(axis=0)).max()


def mix(stems: dict[str, np.ndarray], wet: float = 0.5) -> np.ndarray:
    n = max(len(s) for s in stems.values())
    dry = np.zeros((n, 2))
    for s in stems.values():
        dry[: len(s)] += s
    ir = hall_ir()
    hall = np.stack([fftconvolve(dry[:, c], ir[:, c])[:n] for c in range(2)], axis=1)
    out = 0.85 * dry + wet * hall
    return out / np.abs(out).max() * 10 ** (-1 / 20)


def render(piece: Piece, outdir: Path) -> dict:
    workdir = outdir / "stems"
    workdir.mkdir(parents=True, exist_ok=True)
    clock = piece.clock()
    stems = {}
    for i, part in enumerate(piece.parts):
        stems[f"{i:02d}-{part.instrument}"] = render_part(piece, part, clock, workdir, seed=i)
    out = mix(stems)
    sf.write(outdir / "mix.wav", out, SR, subtype="PCM_24")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(outdir / "mix.wav"), "-b:a", "224k", str(outdir / "mix.mp3")],
        check=True,
    )
    length = float(piece.length())
    report = {"seconds": round(clock(length) + piece.tail, 1)}
    if piece.apex:
        report["apex_seconds"] = round(clock(float(piece.meter.at(piece.apex))), 1)
    # loudness per bar, to check the arc lands where it was planned
    bars = []
    b = 0 if piece.meter.pickup else 1
    while True:
        start = float(piece.meter.at(str(b))) if b else 0.0
        if start >= length:
            break
        stop = min(length, float(piece.meter.at(str(b + 1))))
        seg = out[int(clock(start) * SR): int(clock(stop) * SR)]
        rms = np.sqrt((seg**2).mean()) if len(seg) else 0
        bars.append((b, round(clock(start), 1), round(20 * np.log10(rms + 1e-9), 1)))
        b += 1
    report["bars"] = bars
    if piece.segments:
        report["segments"] = export_segments(piece, out, clock, outdir)
    return report


def _encode(wav: Path, *args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), *args], check=True)


SEAM = 0.03  # seconds of crossfade at a loop seam


def export_segments(piece: Piece, out: np.ndarray, clock: Clock, outdir: Path) -> dict:
    """Cut the render at sample-exact bar positions; the files play back to back without gaps."""
    segdir = outdir / "segments"
    segdir.mkdir(exist_ok=True)
    bounds = {}
    for name, start, end in piece.segments:
        b0, b1 = float(piece.meter.at(start)), min(float(piece.meter.at(end)), float(piece.length()))
        bounds[name] = b0, b1, round(clock(b0) * SR), round(clock(b1) * SR)
    audio = {name: out[s0:s1].copy() for name, (_, _, s0, s1) in bounds.items() if not name.startswith("_")}
    # A loop's head carries the ring of its first rendered pass, so every segment that leads into the loop must
    # end exactly as that pass ended: the same notes, but each rendering differs in jitter and round robin.
    n = round(SEAM * SR)
    fade = np.sin(np.linspace(0, np.pi / 2, n))[:, None]
    for name, loop in piece.seams:
        ref = out[bounds[loop][2] - n: bounds[loop][2]]
        audio[name][-n:] = audio[name][-n:] * fade[::-1] + ref * fade
    manifest = {}
    for name, seg in audio.items():
        b0, b1, s0, s1 = bounds[name]
        wav = segdir / f"{name}.wav"
        sf.write(wav, seg, SR, subtype="PCM_24")
        _encode(wav, "-c:a", "libvorbis", "-q:a", "6", str(wav.with_suffix(".ogg")))
        bpm = 60 / (clock(b0 + 1) - clock(b0))
        manifest[name] = {"seconds": round((s1 - s0) / SR, 3), "samples": s1 - s0,
                          "bars": round((b1 - b0) / float(piece.meter.bar)), "bpm": round(bpm, 2),
                          "bar_seconds": round(float(piece.meter.bar) * 60 / bpm, 4)}
    (segdir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if piece.preview:
        pieces = []
        for name, bars in piece.preview:
            seg = audio[name]
            if bars is not None:
                start = float(piece.meter.at(dict((n, s) for n, s, _ in piece.segments)[name]))
                cut = round((clock(start + bars * float(piece.meter.bar)) - clock(start)) * SR)
                seg = seg[:cut].copy()
                fade = int(0.05 * SR)
                seg[-fade:] *= np.linspace(1, 0, fade)[:, None]
            pieces.append(seg)
        wav = outdir / "preview.wav"
        sf.write(wav, np.concatenate(pieces), SR, subtype="PCM_24")
        _encode(wav, "-b:a", "224k", str(wav.with_suffix(".mp3")))
    return manifest
