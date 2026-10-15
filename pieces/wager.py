"""The Wager: a looping cue for battle betting.

Play order: bets (25 s) -> countdown (5 s) -> start (4 bars) -> loop (32 bars, repeated for as long as the
battle lasts) -> recap (25 s) -> bets ... The battle loop may be left at any bar line; the recap opens
on a tutti hit that covers the cut.

One motto runs through every section, D minor, rising a fifth and stepping back down. The bets play it
staccato over a pizzicato clock, the battle declaims it in horns and then in full strings, and the recap
broadens it into D major, darkening to a minor iv for one bar before the cadence.

The render runs recap, bets, countdown, start, loop, loop: each segment then carries the reverb tail of what
precedes it in play, and the exported loop is the second pass, which starts with its own tail.
"""

from orchestra.cue import Section, join

ORDER = ["fl", "ob", "cl", "bn", "hn", "tpt", "tbn", "tba", "timp", "snare", "cym", "bd",
         "vln1", "vln2", "vla", "vc", "cb"]


def bars(*b: str) -> str:
    return " | ".join(b) + " |"


def rest(n: int) -> str:
    return "r:1 | " * n


def gallop(x: str, beats: int = 4) -> str:
    return " ".join([f"{x}:8 {x}:16 {x}:16"] * beats)


def stab(x: str) -> str:
    return f"{x}:4! r:8 {x}:8! r:4 {x}:4!"


def pizz_clock(lo: str, hi: str) -> str:
    return f"{lo}:4 {hi}:4 {lo}:4 {hi}:4"


def offbeats(chord: str, n: int = 4) -> str:
    return " ".join([f"r:8 {chord}:8"] * n)


MOTTO_MINOR = ["D{o}:4 A{o}:4. G{o}:8 F{o}:4", "E{o}:4. F{o}:8 G{o}:4 A{o}:4", "Bb{o}:4 A{o}:4. G{o}:8 F{o}:4",
               "E{o}:2 A{p}:2", "D{o}:4 A{o}:4. G{o}:8 F{o}:4", "E{o}:4. F{o}:8 G{o}:4 A{o}:4",
               "D{q}:4. C{q}:8 Bb{o}:4 A{o}:4", "G{o}:4 E{o}:4 D{o}:2"]
MOTTO_MAJOR = ["D{o}:4 A{o}:4. G{o}:8 F#{o}:4", "E{o}:4. F#{o}:8 G{o}:4 A{o}:4", "B{o}:4 A{o}:4. G{o}:8 F#{o}:4",
               "E{o}:2 A{p}:2", "D{o}:4 A{o}:4. G{o}:8 F#{o}:4", "E{o}:4. F#{o}:8 G{o}:4 A{o}:4",
               "D{q}:4. C{q}:8 Bb{o}:4 A{o}:4", "G{o}:4 E{o}:4 D{o}:2"]


def legato(b: list[str], vel: int = 62) -> list[str]:
    return [f"%{vel} {b[0]}", *b[1:]]


def motto(lines: list[str], octave: int) -> list[str]:
    """The eight bars in the octave of their first note; A{p} is the octave below, D{q} the octave above."""
    return [b.format(o=octave, p=octave - 1, q=octave + 1) for b in lines]


# ---------------------------------------------------------------- recap: D major, broad, 11 bars
RECAP_STRINGS = "1 ff, 1:3 mf, 2 f, 7 f, 8 ff, 8:4 ff, 9 f, 9:3 mf, 10 mp, 11 p, 11:4 pp"
RECAP_BRASS = "1 ff, 1:3 mp, 2 mf, 7 mf, 8 f, 8:4 f, 9 mf, 10 p, 11 pp"
RECAP_INNER = "1 ff, 1:3 mp, 2 mf, 7 mf, 8 f, 8:4 f, 9 mf, 9:3 mp, 10 p, 11 p, 11:4 pp"
recap = Section(
    # the ritardando is tuned so that the recap lasts exactly 25 s, the game's recap phase
    bars=11, key="D major", tempo="1 114, 9 114, 9:3 100, 10 95, 11 85, 11:4 71.78", directions="1 Maestoso",
    music={
        "fl": bars("%90 D6:1!", *legato(motto(MOTTO_MAJOR, 5)), "%60 B5:2 Bb5:2", "A5:1"),
        "ob": bars("%90 A5:1!", *legato(motto(MOTTO_MAJOR, 5)), "%60 B5:2 Bb5:2", "A5:1"),
        "cl": bars("%90 A4:1!", *legato(motto(MOTTO_MAJOR, 4)), "%60 D4:1", "D4:1"),
        "bn": bars("%90 D3:1!", "%60 D3:1", "C#3:1", "B2:1", "A2:1", "D3:1", "A2:1", "Bb2:1", "A2:2 D3:2", "G2:1",
                   "D3:1"),
        "hn": bars("%95 <D4 F#4 A4 D5>:1!", "%60 <F#4 A4 D5>:1", "<E4 G4 A4>:1", "<D4 G4 B4>:1", "<C#4 E4 A4>:1",
                   "<D4 F#4 A4>:1", "<C#4 E4 G4>:1", "<D4 G4 Bb4>:1", "<C#4 E4 G4>:2 <D4 F#4 A4>:2",
                   "<D4 G4 B4>:2 <D4 G4 Bb4>:2", "<D4 F#4 A4>:1"),
        "tpt": bars("%95 <D4 A4 D5>:1!", *["%65 " + b if i == 0 else b for i, b in enumerate(motto(MOTTO_MAJOR, 4))],
                    "r:1", "r:1"),
        "tbn": bars("%95 <D3 A3 F#4>:1!", "%60 <D3 A3>:1", "<C#3 G3>:1", "<B2 G3>:1", "<A2 E3>:1", "<D3 A3>:1",
                    "<A2 G3>:1", "<Bb2 G3>:1", "<A2 G3>:2 <D3 A3>:2", "<G2 D3>:1", "<D3 A3>:1"),
        "tba": bars("%95 D2:1!", "%60 D2:1", "C#2:1", "B1:1", "A1:1", "D2:1", "A1:1", "Bb1:1", "A1:2 D2:2", "G1:1",
                    "D2:1"),
        "timp": bars("@hit D3:4! @roll D3:2.", "r:1", "r:1", "r:1", "@hit A2:4! r:2.", "r:1", "@roll A2:1",
                     "@hit G2:4! r:2.", "A2:4! r:4 D3:4! r:4", "r:1", "@roll D3:1"),
        "cym": bars("F#4:1", *["r:1"] * 6, "C#4:1", "r:1", "r:1", "r:1"),
        "bd": bars("D2:1", *["r:1"] * 10),
        "vln1": bars("@trem %90 <A5 D6>:1!", *["@arco %60 " + b if i == 0 else b
                                                for i, b in enumerate(motto(MOTTO_MAJOR, 5))], "B5:2 Bb5:2", "A5:1"),
        "vln2": bars("@trem %90 <F#4 D5>:1!", *["@arco %60 " + b if i == 0 else b
                                                 for i, b in enumerate(motto(MOTTO_MAJOR, 4))],
                     "<D4 B4>:2 <D4 Bb4>:2", "<D4 A4>:1"),
        "vla": bars("@trem %90 <A3 F#4>:1!", "@arco %55 <A3 F#4>:1", "<A3 E4>:1", "<G3 D4>:1", "<A3 E4>:1",
                    "<F#3 D4>:1", "<A3 E4>:1", "<G3 D4>:1", "<A3 E4>:2 <A3 F#4>:2", "<G3 D4>:1", "<F#3 D4>:1"),
        "vc": bars("@trem %90 D3:1!", *["@arco %60 " + b if i == 0 else b for i, b in enumerate(motto(MOTTO_MAJOR, 3))],
                   "G2:1", "D3:1"),
        "cb": bars("@trem %90 D2:1!", "@arco %60 D2:1", "C#2:1", "B1:1", "A1:1", "D2:1", "A1:1", "Bb1:1", "A1:2 D2:2",
                   "G1:1", "D2:1"),
    },
    dyn={**{k: RECAP_STRINGS for k in ("fl", "ob", "cl", "vln1", "vln2", "vc")},
         **{k: RECAP_INNER for k in ("bn", "vla", "cb")},
         **{k: RECAP_BRASS for k in ("hn", "tbn", "tba")},
         "tpt": "1 ff, 1:3 mp, 2 mf, 7 mf, 8 ff, 8:4 ff, 9 mf",
         "timp": "1 ff, 1:2 mf, 1:4 p, 4:4 p, 5 f, 6 f, 7 mp, 8 ff, 9 f, 10 f, 11 p, 11:4 pp", "cym": "1 ff, 8 f",
         "bd": "1 ff"},
)

# ---------------------------------------------------------------- bets: 15 bars at 144 = 25 s
DM, A7, GM, A = "<F3 A3>", "<E3 G3>", "<G3 Bb3>", "<E3 C#4>"
bets = Section(
    bars=15, key="D minor", tempo="1 144", directions="1 Scherzando; 11 poco a poco cresc.",
    music={
        "cl": bars("r:1", "r:1", "%62 D4:4' A4:4. G4:8 F4:4'", "E4:4. F4:8 G4:4' A4:4'", "Bb4:4' A4:4. G4:8 F4:4'",
                   "E4:2 A3:2", "r:1", "r:1", "r:1", "r:1", "D4:4' A4:4. G4:8 F4:4'", "r:1", "A4:1", "Bb4:1", "A4:1"),
        "fl": bars(*["r:1"] * 6, "%62 D5:4' A5:4. G5:8 F5:4'", "E5:4. F5:8 G5:4' A5:4'", "D6:4. C6:8 Bb5:4 A5:4",
                   "G5:4' E5:4' D5:2", "r:1", "r:1", "A5:4' E6:4. D6:8 C#6:4'", "Bb5:4' F6:4. Eb6:8 D6:4'",
                   "%75 A5:8 Bb5 C#6 D6 E6 F6 G6 G#6"),
        "ob": bars(*["r:1"] * 6, "%62 D4:4' A4:4. G4:8 F4:4'", "E4:4. F4:8 G4:4' A4:4'", "D5:4. C5:8 Bb4:4 A4:4",
                   "G4:4' E4:4' D4:2", "r:1", "F4:4' C5:4. Bb4:8 A4:4'", "A4:4' E5:4. D5:8 C#5:4'",
                   "Bb4:4' F5:4. Eb5:8 D5:4'", "%75 A4:8 Bb4 C#5 D5 E5 F5 G5 G#5"),
        "hn": bars(*["r:1"] * 12, "%55 <C#4 E4>:1", "<D4 G4>:1", "<C#4 E4 G4>:1"),
        "timp": bars(*["r:1"] * 14, "@hit A2:4! A2:4! A2:4! A2:4!"),
        "snare": bars(*["r:1"] * 13, "F#3:8*8", "F#3:16*16"),
        "vln1": bars(*["r:1"] * 12, "@arco %66 A4:4' E5:4. D5:8 C#5:4'", "Bb4:4' F5:4. Eb5:8 D5:4'",
                     "%78 A4:8 Bb4 C#5 D5 E5 F5 G5 G#5"),
        "vln2": bars("r:1", "r:1", "@pizz %70 r:4 <A4 D5>:4 r:4 <A4 D5>:4", "r:4 <G4 C#5>:4 r:4 <G4 C#5>:4",
                     "r:4 <G4 Bb4>:4 r:4 <G4 Bb4>:4", "r:4 <E4 C#5>:4 r:4 <E4 C#5>:4", "r:4 <A4 D5>:4 r:4 <A4 D5>:4",
                     "r:4 <G4 C5>:4 r:4 <G4 Bb4>:4", "r:4 <F4 Bb4>:4 r:4 <G4 Bb4>:4", "r:4 <E4 G4>:4 r:4 <F4 A4>:4",
                     "@arco %66 D4:4' A4:4. G4:8 F4:4'", "F4:4' C5:4. Bb4:8 A4:4'", "@trem %70 <A4 C#5>:1",
                     "<G4 Bb4>:1", "<E4 G4>:1"),
        "vla": bars("@pizz %70 " + offbeats(DM), offbeats(DM), offbeats(DM), offbeats(A7), offbeats(GM), offbeats(A),
                    offbeats(DM), offbeats("<E3 Bb3>"), offbeats("<F3 Bb3>", 2) + " " + offbeats(GM, 2),
                    offbeats(A7, 2) + " " + offbeats(DM, 2), "@trem %70 <F3 A3>:1", "<F3 C4>:1", "<E3 C#4>:1",
                    "<G3 Bb3>:1", "<C#4 G4>:1"),
        "vc": bars(*["r:1"] * 10, "@stacc %75 D3:8*8", "D3:8*8", "D3:8*8", "G2:8*8", "A2:8*8"),
        "cb": bars("@pizz %70 " + pizz_clock("D2", "A1"), pizz_clock("D2", "A1"), pizz_clock("D2", "A1"),
                   pizz_clock("A1", "E2"), pizz_clock("G1", "D2"), pizz_clock("A1", "E2"), pizz_clock("D2", "A1"),
                   pizz_clock("C2", "G1"), "Bb1:4 F2:4 G1:4 D2:4", "A1:4 E2:4 D2:4 A1:4",
                   "@stacc %75 D2:8*8", "D2:8*8", "D2:8*8", "G1:8*8", "A1:8*8"),
    },
    dyn={"cl": "3 f, 6 f, 7 mp, 11 f, 15 ff", "fl": "7 f, 10 f, 13 f, 15 ff", "ob": "7 f, 10 f, 12 f, 15 ff",
         "hn": "13 mp, 15 f", "timp": "15 mf, 15:4 ff", "snare": "14 mp, 15 f", "vln1": "13 f, 15 ff",
         "vln2": "1 mp, 10 mp, 11 f, 15 ff", "vla": "1 mp, 10 mp, 11 mp, 15 f", "vc": "11 mp, 15 f",
         "cb": "1 mp, 10 mp, 11 mp, 15 f"},
)

# ---------------------------------------------------------------- countdown: 3 bars = 5 s, on the dominant
HUSH = "1 ff, 1:2 p, 3:4 ff"
countdown = Section(
    bars=3, tempo="1 144", directions="1 no more bets",
    music={
        "fl": bars("%95 A5:4! r:4 r:2", "r:1", "r:2 %85 D5:16 E5 F5 G5 A5 Bb5 C6 C#6"),
        "ob": bars("%95 E5:4! r:4 r:2", "r:1", "r:1"),
        "cl": bars("%95 A4:4! r:4 r:2", "r:1", "r:2 %85 D4:16 E4 F4 G4 A4 Bb4 C5 C#5"),
        "bn": bars("%95 A2:4! r:4 r:2", "%60 A2:1", "A2:1"),
        "hn": bars("%95 <A3 E4 A4 C#5>:4! r:4 r:2", "%60 <A3 E4>:1", "<A3 E4 G4>:1"),
        "tpt": bars("%95 <E4 A4 C#5>:4! r:4 r:2", "r:1", "%90 " + " ".join(["A4:8t! A4:8t A4:8t"] * 4)),
        "tbn": bars("%95 <A2 E3 C#4>:4! r:4 r:2", "r:1", "%70 <A2 E3 G3>:1"),
        "tba": bars("%95 A1:4! r:4 r:2", "r:1", "%70 A1:1"),
        "timp": bars("@hit %100 A2:4! @roll A2:2.~", "A2:1~", "A2:1"),
        "snare": bars("r:1", "F#3:16*16", "F#3:16*16"),
        "cym": bars("C#4:4 r:4 r:2", "r:1", "r:1"),
        "bd": bars("D2:4 r:4 r:2", "r:1", "r:1"),
        "vln1": bars("@stacc %100 <E5 A5>:4! r:4 r:2", "@trem %70 <D5 F5>:1",
                     "<C#5 E5>:2 @arco %85 D5:16 E5 F5 G5 A5 Bb5 C6 C#6"),
        "vln2": bars("@stacc %100 <A4 C#5>:4! r:4 r:2", "@trem %70 <A4 D5>:1", "<A4 C#5>:2 <G4 C#5>:2"),
        "vla": bars("@stacc %100 <A3 E4>:4! @trem %70 A3:2.", "<A3 D4>:1", "<A3 C#4>:2 <G3 C#4>:2"),
        "vc": bars("@stacc %100 A2:4! @trem %70 A2:2.", "A2:1", "A2:1"),
        "cb": bars("@stacc %100 A1:4! @trem %70 A1:2.", "A1:1", "A1:1"),
    },
    dyn={**{k: HUSH for k in ("bn", "hn", "tbn", "tba", "timp", "vln1", "vln2", "vla", "vc", "cb", "fl", "cl")},
         "ob": "1 ff", "tpt": "1 ff, 3 mf, 3:4 ff", "snare": "2 pp, 3:4 ff", "cym": "1 f", "bd": "1 ff"},
)


# ---------------------------------------------------------------- the last bar of the loop, which also ends the start
def turnaround() -> dict[str, str]:
    return {
        "fl": "%95 E6:4! r:4 %85 F5:16 G5 A5 Bb5 C6 C#6 D6 E6", "ob": "%95 A5:4! r:4 r:2",
        "cl": "%95 E5:4! r:4 %85 D4:16 E4 F4 G4 A4 Bb4 C5 C#5", "bn": "@stacc %95 A2:4! r:4 r:2",
        "hn": "%95 <C#4 E4 G4 A4>:4! r:4 r:2", "tpt": "%95 <E4 A4 C#5>:4! r:4 r:2",
        "tbn": "%95 <A2 E3 G3>:4! r:4 r:2", "tba": "%95 A1:4! r:4 r:2",
        "timp": "@hit %100 A2:4! r:4 A2:8 A2:8 A2:8 A2:8", "snare": "F#3:4! r:4 F#3:16*8", "bd": "D2:4 r:4 r:2",
        "cym": "r:1",
        "vln1": "@arco %95 <E5 A5>:4! r:4 %85 F4:16 G4 A4 Bb4 C5 C#5 D5 E5",
        "vln2": "@arco %95 <G4 C#5>:4! r:4 %85 D4:16 E4 F4 G4 A4 Bb4 C5 C#5",
        "vla": "@stacc %95 <E4 A4>:4! r:4 r:2", "vc": "@stacc %90 A2:4! r:4 A2:8*4", "cb": "@stacc %90 A1:4! r:4 A1:8*4",
    }


def with_turnaround(music: dict[str, str]) -> dict[str, str]:
    end = turnaround()
    return {k: (music.get(k, "") + " " + end[k]).strip() + " |" for k in end}


# ---------------------------------------------------------------- start: 4 bars, fanfare over the gallop
STABS = {  # instrument -> (Bb, Gm, A) voicings for the syncopated bar
    "fl": ("D6", "D6", "C#6"), "ob": ("Bb5", "Bb5", "A5"), "cl": ("F5", "G5", "E5"), "bn": ("Bb2", "G2", "A2"),
    "hn": ("<D4 F4 Bb4>", "<D4 G4 Bb4>", "<C#4 E4 A4>"), "tpt": ("<F4 Bb4 D5>", "<G4 Bb4 D5>", "<E4 A4 C#5>"),
    "tbn": ("<Bb2 F3>", "<G2 D3>", "<A2 E3>"), "tba": ("Bb1", "G1", "A1"), "timp": ("D3", "D3", "A2"),
    "snare": ("F#3", "F#3", "F#3"), "bd": ("D2", "D2", "D2"), "cym": ("C#4", None, None),
    "vln1": ("<F5 Bb5>", "<G5 Bb5>", "<E5 A5>"), "vln2": ("<Bb4 D5>", "<Bb4 D5>", "<A4 C#5>"),
    "vla": ("<D4 F4>", "<D4 G4>", "<C#4 E4>"), "vc": ("Bb2", "G2", "A2"), "cb": ("Bb1", "G1", "A1"),
}


def syncopated(inst: str) -> str:
    x, y, z = STABS[inst]
    if y is None:
        return f"{x}:4 r:2."
    return f"{x}:4! r:8 {y}:8! r:4 {z}:4!"


start_music = {
    "fl": bars("%95 D6:4! r:4 r:2", "r:1", "%95 " + syncopated("fl")),
    "ob": bars("%95 A5:4! r:4 r:2", "r:1", "%95 " + syncopated("ob")),
    "cl": bars("%95 F5:4! r:4 r:2", "r:1", "%95 " + syncopated("cl")),
    "bn": bars("@stacc %80 D3:8*8", "A2:8*8", "%95 " + syncopated("bn")),
    "hn": bars("%90 <D4 A4>:4! r:4 <D4 A4>:4! r:4", "A4:4! E4:8. E4:16 A4:4! C#5:4!", "%95 " + syncopated("hn")),
    "tpt": bars("%90 D5:4! A4:8. A4:16 D5:4! F5:4!", "r:1", "%95 " + syncopated("tpt")),
    "tbn": bars("%90 <D3 A3>:4! r:4 <D3 A3>:4! r:4", "<A2 E3>:4! r:4 <A2 E3>:4! r:4", "%95 " + syncopated("tbn")),
    "tba": bars("%90 D2:4! r:4 D2:4! r:4", "A1:4! r:4 A1:4! r:4", "%95 " + syncopated("tba")),
    "timp": bars("@hit %100 D3:4! r:4 D3:4! r:4", "A2:4! r:4 A2:4! r:4", syncopated("timp")),
    "snare": bars("r:1", "F#3:8 F#3:16 F#3:16 " * 4, syncopated("snare")),
    "cym": bars("F#4:1", "r:1", syncopated("cym")),
    "bd": bars("D2:2 D2:2", "r:1", syncopated("bd")),
    "vln1": bars("@stacc %80 D6:8! F5:16 F5:16 " + gallop("F5", 3), gallop("E5"), "%95 " + syncopated("vln1")),
    "vln2": bars("@stacc %80 " + gallop("A4"), gallop("G4"), "%95 " + syncopated("vln2")),
    "vla": bars("@stacc %80 " + gallop("D4"), gallop("C#4"), "%95 " + syncopated("vla")),
    "vc": bars("@stacc %80 D3:8*8", "A2:8*8", "%95 " + syncopated("vc")),
    "cb": bars("@stacc %80 D2:8*8", "A1:8*8", "%95 " + syncopated("cb")),
}
start = Section(
    bars=4, tempo="1 144", directions="1 Allegro con fuoco", music=with_turnaround(start_music),
    dyn={k: "1 ff" for k in ORDER} | {"vln1": "1 ff, 1:2 f, 3 ff", "vln2": "1 ff, 1:2 f, 3 ff",
                                      "vla": "1 ff, 1:2 f, 3 ff", "snare": "2 mf, 3 ff"},
)

# ---------------------------------------------------------------- loop: 32 bars, motto / song / motto / stabs
A_HARM = [("F5", "A4", "D4"), ("E5", "G4", "C#4"), ("F5", "Bb4", "D4"), ("E5", "A4", "C#4"), ("F5", "A4", "D4"),
          ("E5", "Bb4", "C4")]
A_BASS = ["D3", "A2", "G2", "A2", "D3", "C3"]


def a_gallop(voice: int) -> list[str]:
    split = [("F5", "F5"), ("D5", "D5"), ("Bb3", "Bb3")], [("E5", "F5"), ("C#5", "D5"), ("A3", "A3")]
    return ([gallop(h[voice]) for h in A_HARM]
            + [gallop(split[0][voice][0], 2) + " " + gallop(split[0][voice][1], 2),
               gallop(split[1][voice][0], 2) + " " + gallop(split[1][voice][1], 2)])


def a_bass(octave_down: bool) -> list[str]:
    def o(n: str) -> str:
        return n[:-1] + str(int(n[-1]) - 1) if octave_down else n
    return [f"{o(n)}:8*8" for n in A_BASS] + [f"{o('Bb2')}:8*4 {o('G2')}:8*4", f"{o('A2')}:8*4 {o('D3')}:8*4"]


B_SONG = ["A{o}:2. C{q}:4", "Bb{o}:4. A{o}:8 G{o}:2", "A{o}:2. F{o}:4", "G{o}:2 E{o}:2", "Bb{o}:2. D{q}:4",
          "C{q}:4. Bb{o}:8 A{o}:2", "Bb{o}:2 G{o}:2", "A{o}:1"]
B_BASS = ["F2", "G2", "A2", "C3", "Bb2", "A2", "G2", "A2"]
B_HORNS = ["<A3 C4 F4>", "<G3 Bb3 D4>", "<A3 C4 F4>", "<G3 Bb3 E4>", "<G3 Bb3 D4>", "<A3 C4 F4>", "<G3 Bb3 D4>",
           "<A3 C#4 E4>"]
B_VIOLAS = ["<C4 F4>", "<D4 G4>", "<C4 F4>", "<Bb3 E4>", "<D4 G4>", "<C4 F4>", "<D4 G4>", "<C#4 E4>"]
A2_HORNS = ["<D4 F4 A4>:2! <D4 F4 A4>:2", "<C#4 E4 G4>:2! <C#4 E4 G4>:2", "<D4 F4 Bb4>:2! <D4 F4 Bb4>:2",
            "<C#4 E4 A4>:2! <C#4 E4 A4>:2", "<D4 F4 A4>:2! <D4 F4 A4>:2", "<C4 E4 Bb4>:2! <C4 E4 Bb4>:2",
            "<D4 F4 Bb4>:2! <D4 G4 Bb4>:2!", "<C#4 E4 G4>:2! <D4 F4 A4>:2!"]
A2_TROMBONES = ["<D3 A3>:2! <D3 A3>:2", "<A2 E3>:2! <A2 E3>:2", "<G2 D3>:2! <G2 D3>:2", "<A2 E3>:2! <A2 E3>:2",
                "<D3 A3>:2! <D3 A3>:2", "<C3 G3>:2! <C3 G3>:2", "<Bb2 F3>:2! <G2 D3>:2!", "<A2 E3>:2! <D3 A3>:2!"]
TUBA = ["D2:1", "A1:1", "G1:1", "A1:1", "D2:1", "C2:1", "Bb1:2 G1:2", "A1:2 D2:2"]
TIMP_A = ["D3", "A2", "G2", "A2", "D3", "C3"]
FEUD = [  # Dm, C, Bb, A: the stab chords of bars 25-28
    {"vln1": "<F5 A5>", "vln2": "<A4 D5>", "vla": "<D4 F4>", "vc": "D3", "cb": "D2", "bn": "D3", "tba": "D2",
     "hn": "<D4 F4 A4>", "tpt": "<F4 A4 D5>", "tbn": "<D3 A3>", "ob": "A5", "cl": "D5", "timp": "D3"},
    {"vln1": "<E5 G5>", "vln2": "<G4 C5>", "vla": "<C4 E4>", "vc": "C3", "cb": "C2", "bn": "C3", "tba": "C2",
     "hn": "<C4 E4 G4>", "tpt": "<E4 G4 C5>", "tbn": "<C3 G3>", "ob": "G5", "cl": "C5", "timp": "C3"},
    {"vln1": "<D5 F5>", "vln2": "<F4 Bb4>", "vla": "<Bb3 D4>", "vc": "Bb2", "cb": "Bb1", "bn": "Bb2", "tba": "Bb1",
     "hn": "<Bb3 D4 F4>", "tpt": "<D4 F4 Bb4>", "tbn": "<Bb2 F3>", "ob": "F5", "cl": "Bb4", "timp": "Bb2"},
    {"vln1": "<C#5 E5>", "vln2": "<E4 A4>", "vla": "<A3 C#4>", "vc": "A2", "cb": "A1", "bn": "A2", "tba": "A1",
     "hn": "<A3 C#4 E4>", "tpt": "<C#4 E4 A4>", "tbn": "<A2 E3>", "ob": "E5", "cl": "C#5", "timp": "A2"},
]
FEUD_FLUTE = ["D6:4! r:8 D6:8! A5:16 Bb5 C6 C#6 D6:4!", "C6:4! r:8 C6:8! G5:16 A5 Bb5 B5 C6:4!",
              "Bb5:4! r:8 Bb5:8! E5:16 F5 G5 A5 Bb5:4!", "E6:4! r:8 E6:8! A5:16 B5 C#6 D6 E6:4!"]


def feud(inst: str) -> list[str]:
    return [stab(chord[inst]) for chord in FEUD]


loop_music = {
    "fl": bars(*["r:1"] * 4, "@stacc %70 " + gallop("F6"), gallop("E6"), gallop("F6"), gallop("E6", 2) + " " + gallop("F6", 2),
               "@ord %70 " + B_SONG[0].format(o=5, q=6), *[b.format(o=5, q=6) for b in B_SONG[1:]],
               "%80 " + motto(MOTTO_MINOR, 5)[0], *motto(MOTTO_MINOR, 5)[1:], "%95 " + FEUD_FLUTE[0], *FEUD_FLUTE[1:],
               "r:1", "r:1", "%85 A5:4! E6:4. D6:8 C#6:4"),
    "ob": bars(*["r:1"] * 8, "%70 " + B_SONG[0].format(o=4, q=5), *[b.format(o=4, q=5) for b in B_SONG[1:]],
               "%80 " + motto(MOTTO_MINOR, 5)[0], *motto(MOTTO_MINOR, 5)[1:], "%95 " + feud("ob")[0], *feud("ob")[1:],
               "r:1", "r:1", "%85 A5:4! E6:4. D6:8 C#6:4"),
    "cl": bars(*["r:1"] * 8, "%70 " + B_SONG[0].format(o=4, q=5), *[b.format(o=4, q=5) for b in B_SONG[1:]],
               "%80 " + motto(MOTTO_MINOR, 4)[0], *motto(MOTTO_MINOR, 4)[1:], "%95 " + feud("cl")[0], *feud("cl")[1:],
               "r:1", "r:1", "r:1"),
    "bn": bars("@stacc %75 " + a_bass(False)[0], *a_bass(False)[1:], *[f"{n}:8*8" for n in B_BASS],
               *a_bass(False), "%95 " + feud("bn")[0], *feud("bn")[1:], "%75 A2:8*8", "A2:8*8", "A2:8*8"),
    "hn": bars("@ord %70 " + motto(MOTTO_MINOR, 4)[0], *motto(MOTTO_MINOR, 4)[1:],
               "@stacc %70 " + gallop(B_HORNS[0]), *[gallop(h) for h in B_HORNS[1:]],
               "@ord %80 " + A2_HORNS[0], *A2_HORNS[1:], "%95 " + feud("hn")[0], *feud("hn")[1:],
               "%75 A3:4! E4:4. D4:8 C#4:4", "<C#4 E4 G4>:1", "<C#4 E4 G4 A4>:1"),
    "tpt": bars(*["r:1"] * 16, "%80 " + motto(MOTTO_MINOR, 4)[0], *motto(MOTTO_MINOR, 4)[1:],
                "%95 " + feud("tpt")[0], *feud("tpt")[1:], "r:1", "%85 A4:4! E5:4. D5:8 C#5:4", "<E4 G4 C#5>:1"),
    "tbn": bars("%70 " + motto(MOTTO_MINOR, 3)[0], *motto(MOTTO_MINOR, 3)[1:], *["r:1"] * 8,
                "%80 " + A2_TROMBONES[0], *A2_TROMBONES[1:], "%95 " + feud("tbn")[0], *feud("tbn")[1:],
                "%70 <A2 E3>:1", "<A2 E3 G3>:1", "<A2 E3 G3>:1"),
    "tba": bars("%70 " + TUBA[0], *TUBA[1:], *["r:1"] * 8, *TUBA, "%95 " + feud("tba")[0], *feud("tba")[1:],
                "%70 A1:1", "A1:1", "A1:1"),
    "timp": bars("@hit %90 " + f"{TIMP_A[0]}:4! r:4 {TIMP_A[0]}:4 r:4",
                 *[f"{n}:4! r:4 {n}:4 r:4" for n in TIMP_A[1:]], "Bb2:4! r:4 G2:4! r:4", "A2:4! r:4 D3:4! r:4",
                 *[f"{n}:4! r:2." for n in B_BASS[:-1]], "@roll A2:1",
                 "@hit " + f"{TIMP_A[0]}:4! r:4 {TIMP_A[0]}:4 r:4", *[f"{n}:4! r:4 {n}:4 r:4" for n in TIMP_A[1:]],
                 "Bb2:4! r:4 G2:4! r:4", "A2:4! r:4 D3:4! r:4", *feud("timp"), "@roll A2:1~", "A2:1~", "A2:1"),
    "snare": bars(*["r:1"] * 16, *[("F#3:8 F#3:16 F#3:16 " * 4).strip()] * 8,
                  *["F#3:4! r:8 F#3:8! F#3:16 F#3 F#3 F#3 F#3:4!"] * 4, "r:1", "F#3:16*16", "F#3:16*16"),
    "cym": bars("F#4:1", *["r:1"] * 15, "F#4:1", "r:1", "r:1", "r:1", "C#4:1", "r:1", "r:1", "r:1",
                "C#4:4 r:2.", "r:1", "C#4:4 r:2.", "r:1", "r:1", "r:1", "r:1"),
    "bd": bars("D2:1", *["r:1"] * 15, "D2:1", "r:1", "r:1", "r:1", "D2:1", "r:1", "r:1", "r:1",
               *["D2:4 r:8 D2:8 r:4 D2:4"] * 4, "r:1", "r:1", "r:1"),
    "vln1": bars("@stacc %75 " + a_gallop(0)[0], *a_gallop(0)[1:],
                 "@arco %70 " + B_SONG[0].format(o=5, q=6), *[b.format(o=5, q=6) for b in B_SONG[1:]],
                 "%80 " + motto(MOTTO_MINOR, 5)[0], *motto(MOTTO_MINOR, 5)[1:],
                 "@stacc %95 " + feud("vln1")[0], *feud("vln1")[1:],
                 "@trem %70 <A4 E5>:1", "<A4 G5>:1", "@arco %85 A5:4! E6:4. D6:8 C#6:4"),
    "vln2": bars("@stacc %75 " + a_gallop(1)[0], *a_gallop(1)[1:],
                 "@arco %70 " + B_SONG[0].format(o=4, q=5), *[b.format(o=4, q=5) for b in B_SONG[1:]],
                 "%80 " + motto(MOTTO_MINOR, 4)[0], *motto(MOTTO_MINOR, 4)[1:],
                 "@stacc %95 " + feud("vln2")[0], *feud("vln2")[1:],
                 "@trem %70 <E4 G4>:1", "<E4 G4>:1", "<G4 C#5>:1"),
    "vla": bars("@stacc %75 " + a_gallop(2)[0], *a_gallop(2)[1:],
                "@trem %65 " + B_VIOLAS[0] + ":1", *[v + ":1" for v in B_VIOLAS[1:]],
                "@stacc %75 " + a_gallop(2)[0], *a_gallop(2)[1:],
                "%95 " + feud("vla")[0], *feud("vla")[1:], "@trem %70 <C#4 E4>:1", "<C#4 E4>:1", "<C#4 E4>:1"),
    "vc": bars("@stacc %75 " + a_bass(False)[0], *a_bass(False)[1:], *[f"{n}:8*8" for n in B_BASS],
               *a_bass(False), "%95 " + feud("vc")[0], *feud("vc")[1:], "%75 A2:8*8", "A2:8*8", "A2:8*8"),
    "cb": bars("@stacc %75 " + a_bass(True)[0], *a_bass(True)[1:],
               *[f"{n[:-1]}{int(n[-1]) - 1}:8*8" for n in B_BASS], *a_bass(True),
               "%95 " + feud("cb")[0], *feud("cb")[1:], "%75 A1:8*8", "A1:8*8", "A1:8*8"),
}
loop = Section(
    bars=32, tempo="1 144", music=with_turnaround(loop_music),
    dyn={"vln1": "1 mf, 9 mf, 9 f, 13 ff, 15 ff, 16 f, 17 fff, 24:4 fff, 25 ff, 28:4 ff, 29 p, 31 f, 31:4 ff, 32 ff",
         "vln2": "1 mf, 9 mf, 9 f, 13 ff, 15 ff, 16 f, 17 fff, 24:4 fff, 25 ff, 28:4 ff, 29 p, 31 f, 31:4 ff, 32 ff",
         "vla": "1 mf, 16 mf, 17 f, 24:4 f, 25 ff, 28:4 ff, 29 p, 31 f, 31:4 ff, 32 ff",
         "vc": "1 f, 9 f, 9 mf, 16 mf, 17 ff, 28:4 ff, 29 p, 31:4 ff, 32 ff",
         "cb": "1 f, 9 f, 9 mf, 16 mf, 17 ff, 28:4 ff, 29 p, 31:4 ff, 32 ff",
         "bn": "1 f, 9 f, 9 mf, 16 mf, 17 ff, 28:4 ff, 29 p, 31:4 ff, 32 ff",
         "hn": "1 fff, 9 fff, 9 mf, 16 mf, 17 f, 24:4 f, 25 ff, 28:4 ff, 29 f, 31 f, 31:4 ff, 32 ff",
         "tbn": "1 f, 24:4 f, 25 ff, 28:4 ff, 29 mf, 31:4 ff, 32 ff",
         "tba": "1 f, 24:4 f, 25 ff, 28:4 ff, 29 mf, 31:4 ff, 32 ff",
         "tpt": "17 ff, 28:4 ff, 29 f, 31:4 ff, 32 ff",
         "fl": "5 mf, 9 mf, 9 f, 13 ff, 15 ff, 16 f, 17 ff, 32 ff", "ob": "9 f, 13 ff, 15 ff, 16 f, 17 ff, 32 ff",
         "cl": "9 f, 13 ff, 15 ff, 16 f, 17 ff, 32 ff",
         "timp": "1 mf, 16 mf, 16 mp, 16:4 f, 17 ff, 28:4 ff, 29 mp, 31:4 ff, 32 ff",
         "snare": "17 mf, 24:4 mf, 25 f, 28:4 f, 30 p, 31:4 ff, 32 ff", "cym": "1 f, 16:4 f, 17 ff, 24:4 ff, 25 f",
         "bd": "1 f, 16:4 f, 17 ff, 24:4 ff, 25 f, 31:4 f, 32 ff"},
)

PIECE = join(
    "The Wager",
    [("recap", recap), ("bets", bets), ("countdown", countdown), ("start", start), ("_loop1", loop), ("loop", loop)],
    ORDER,
    gains={"vln1": 3, "vln2": 1, "vla": -2, "cb": -2, "bn": -3, "fl": -2, "ob": -3, "cl": -3, "tbn": -5, "tba": -6,
           "tpt": -3, "hn": -1},
    preview=[("bets", None), ("countdown", None), ("start", None), ("loop", None), ("loop", 6), ("recap", None)],
)
