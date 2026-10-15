"""The orchestra: Virtual Playing Orchestra 3 patches, seating and default levels.

Each articulation names its SFZ patch, how dynamics reach it, and optionally a gain in dB:
  cc1       the mod wheel (the PERF patches: CC1 is volume, velocity is attack speed)
  velocity  note velocity (struck and plucked instruments)
  gain      a gain envelope applied to the rendered audio (looped rolls)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    name: str
    abbr: str
    clef: str  # treble, alto, bass, bass8vb
    arts: dict[str, tuple]  # articulation -> (patch, dynamics mode[, gain dB])
    lo: int  # playable range, MIDI
    hi: int
    vel: int = 52  # base velocity: lower is a softer, slower attack
    pan: float = 0.0  # -1 left .. 1 right
    gain: float = 0.0  # dB


def _strings(prefix: str) -> dict[str, tuple[str, str]]:
    return {
        "arco": (f"Strings/{prefix}-SEC-PERF.sfz", "cc1"),
        "trem": (f"Strings/{prefix}-SEC-PERF-tremolo.sfz", "cc1"),
        "pizz": (f"Strings/{prefix}-SEC-PERF-pizzicato.sfz", "cc1"),
        "stacc": (f"Strings/{prefix}-SEC-PERF-staccato.sfz", "cc1"),
    }


def _winds(path: str) -> dict[str, tuple[str, str]]:
    return {"ord": (f"{path}.sfz", "cc1"), "stacc": (f"{path}-staccato.sfz", "cc1")}


ORCHESTRA = {
    "fl": Instrument("Flute", "Fl.", "treble", _winds("Woodwinds/flute-SEC-PERF"), 60, 98, pan=-0.1),
    "ob": Instrument("Oboe", "Ob.", "treble", _winds("Woodwinds/oboe-SEC-PERF"), 58, 93, pan=0.1),
    "cl": Instrument("Clarinet", "Cl.", "treble", _winds("Woodwinds/clarinet-SEC-PERF"), 50, 94, pan=-0.15),
    "cl_solo": Instrument("Clarinet", "Cl.", "treble", _winds("Woodwinds/clarinet-SOLO-PERF"), 50, 94, pan=-0.15),
    "bn": Instrument("Bassoon", "Bn.", "bass", _winds("Woodwinds/bassoon-SEC-PERF"), 34, 75, pan=0.15),
    "hn": Instrument("Horns", "Hn.", "treble", _winds("Brass/french-horn-SEC-PERF"), 35, 77, pan=-0.3, gain=-6),
    "tpt": Instrument("Trumpets", "Tpt.", "treble", _winds("Brass/trumpet-SEC-PERF"), 54, 84, pan=0.2),
    "tbn": Instrument("Trombones", "Tbn.", "bass", _winds("Brass/trombone-SEC-PERF"), 40, 77, pan=0.35),
    "tba": Instrument("Tuba", "Tba.", "bass", _winds("Brass/tuba-SOLO-PERF"), 26, 62, pan=0.4),
    "timp": Instrument(
        "Timpani", "Timp.", "bass",
        {"roll": ("Percussion/timpani-roll.sfz", "gain", -8), "hit": ("Percussion/timpani-hit.sfz", "velocity")},
        36, 60, vel=90, pan=0.1, gain=-8,
    ),
    # percussion "pitches" are the patch's keys: crash F#4, piatti C#4; snare F#3, roll E3; bass drum D2
    "cym": Instrument("Cymbals", "Cym.", "perc", {"ord": ("Percussion/cymbals.sfz", "velocity")}, 60, 70, pan=0.2,
                      gain=-6),
    "snare": Instrument("Snare Drum", "S.D.", "perc", {"ord": ("Percussion/snare.sfz", "velocity")}, 48, 55, pan=0.15,
                        gain=-8),
    "bd": Instrument("Bass Drum", "B.D.", "perc", {"ord": ("Percussion/bassdrum.sfz", "velocity")}, 36, 38, pan=0.1,
                     gain=-4),
    "harp": Instrument("Harp", "Hp.", "treble", {"ord": ("Strings/harp-sustain.sfz", "velocity")}, 23, 104, pan=-0.35,
                       gain=-14),
    "vln1": Instrument("Violins I", "Vln. I", "treble", _strings("1st-violin"), 55, 105, pan=-0.45),
    "vln2": Instrument("Violins II", "Vln. II", "treble", _strings("2nd-violin"), 55, 105, pan=-0.2),
    "vla": Instrument("Violas", "Vla.", "alto", _strings("viola"), 48, 93, pan=0.15),
    "vc": Instrument("Cellos", "Vc.", "bass", _strings("cello"), 36, 81, pan=0.35),
    "cb": Instrument("Basses", "Cb.", "bass8vb", _strings("bass"), 24, 67, pan=0.5),
}
