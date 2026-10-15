"""The Climb: five bars over a held A, and the minor tune comes out in major.

D minor, 4/4. Cellos sing the tune (A-D-E-F) under a high string halo. From bar 5 the basses and a
timpani roll hold the dominant A while the tune's head climbs a step each bar, over i64, V7b9, III6, iv
and V7b9 again, with the inner strings throbbing in eighths. Bar 10 lets go of the pedal onto D major:
the F the tune has always ended on becomes F#, at the top of the orchestra.
"""

from orchestra.piece import Part, Piece

BUILD = "1 pp, 5 pp, 9 f, 9:4 ff, 10 fff, 11 ff, 12 f, 13 mf, 13:4 p"
ARRIVAL = "8 mf, 9 f, 9:4 ff, 10 fff, 11 ff, 12 f, 13 mf, 13:4 p"
WARM = "5 pp, 9 mf, 10 f, 11 f, 12 mf, 13 mf, 13:4 p"
TUNE_MAJOR = "D6:4. E6:8 F#6:2 | G6:4. F#6:8 E6:4 A6:4 | F#6:4. E6:8 D6:4 C#6:4 | D6:1 |"
TUNE_MAJOR_8VB = "D5:4. E5:8 F#5:2 | G5:4. F#5:8 E5:4 A5:4 | F#5:4. E5:8 D5:4 C#5:4 | D5:1 |"

PIECE = Piece(
    title="The Climb",
    key="D minor, 10 D major",
    tempo="1 58, 4 56, 4:3 50, 5 58, 8 66, 9 64, 9:4 48, 10 50, 11 50, 12 46, 12:4 40, 13 40, 13:4 32",
    tempo_text="Lento",
    directions="5 poco a poco cresc.; 9:3 allargando; 10 Grandioso",
    apex="10",
    parts=[
        Part("fl", "r:1 | " * 7 + "D5:4 G5:4. A5:8 Bb5:4 | E5:4 A5:4. Bb5:8 C#6:4 | " + TUNE_MAJOR, dyn=ARRIVAL, gain=-2),
        Part("ob", "r:1 | " * 8 + "E5:4 A5:4. Bb5:8 C#6:4 | " + TUNE_MAJOR_8VB, dyn=ARRIVAL, gain=-4),
        Part("cl", "r:1 | " * 9 + "A4:1 | B4:2 A4:2 | A4:2. G4:4 | F#4:1 |",
             dyn="10 f, 11 f, 12 mf, 13 mf, 13:4 p", gain=-5),
        Part("bn", "r:1 | " * 4 + "A2:1 | A2:1 | A2:1 | A2:1 | A2:1 | D3:1 | G2:2 A2:2 | A2:1 | D2:1 |",
             dyn=WARM, gain=-4),
        Part("hn", "r:1 | " * 5 + "<C#4 E4 G4>:1 | <C4 F4>:1 | <Bb3 D4 G4>:1 | <C#4 E4 G4 Bb4>:1 |"
                   " <D4 F#4 A4 D5>:1 | <D4 G4 B4>:2 <C#4 E4 G4 A4>:2 | <D4 F#4 A4>:2. <C#4 E4 G4>:4 |"
                   " <D4 F#4 A4 D5>:1 |", dyn="6 pp, 9 f, 9:4 ff, 10 fff, 11 ff, 12 f, 13 mf, 13:4 p", gain=-3),
        Part("tbn", "r:1 | " * 9 + "<D3 F#3 A3>:1 | <D3 G3 B3>:2 <C#3 E3 A3>:2 | <D3 F#3 A3>:2. <C#3 E3 G3>:4 |"
                    " <D3 F#3 A3>:1 |", dyn="10 f, 11 f, 12 mf, 13 mf, 13:4 p", gain=-6),
        Part("timp", "r:1 | " * 4 + "A2:1~ | A2:1~ | A2:1~ | A2:1~ | A2:1 | @hit D3:4! @roll D3:2. | r:1 | r:1 | D3:1 |",
             dyn="5 pp, 9:4 ff, 10 ff, 10:2 mf, 10:4 p, 13 p, 13:4 pp"),
        Part("vln1", "F5:1 | G5:1 | F5:2. G5:4 | F5:2 r:2 | A4:4 D5:4. E5:8 F5:4 | Bb4:4 E5:4. F5:8 G5:4 |"
                     " C5:4 F5:4. G5:8 A5:4 | D5:4 G5:4. A5:8 Bb5:4 | E5:4 A5:4. Bb5:8 C#6:4 | " + TUNE_MAJOR,
             dyn="1 pp, 4:3 pp, 5 p, 9 f, 9:4 ff, 10 fff, 11 ff, 12 f, 13 mf, 13:4 p", gain=4),
        Part("vln2", "<A4 D5>:1 | <Bb4 D5>:2 <A4 C#5>:2 | <A4 D5>:2. <A4 C#5>:4 | <A4 D5>:2 r:2 |"
                     " F4:8*8 | G4:8*8 | F4:8*8 | G4:8*8 | G4:8*8 | " + TUNE_MAJOR_8VB, dyn=BUILD, vel=68),
        Part("vla", "r:1 | r:1 | r:1 | r:1 | D4:8*8 | C#4:8*8 | C4:8*8 | D4:8*8 | C#4:8*8 |"
                    " <A3 F#4>:1 | <B3 G4>:2 <C#4 G4>:2 | <A3 F#4>:2. <A3 G4>:4 | <A3 F#4>:1 |", dyn=BUILD, vel=68, gain=-2),
        Part("vc", "A3:4 D4:4. E4:8 F4:4 | G4:4. F4:8 E4:4 A4:4 | F4:4. E4:8 D4:4 C#4:4 | D4:2 r:2 |"
                   " A2:8*8 | A2:8*8 | A2:8*8 | A2:8*8 | A2:8*8 | D3:1 | G2:2 A2:2 | A2:1 | D2:1 |",
             dyn="1 mp, 2:3 mf, 3:3 mp, 4 p, 5 pp, 9 f, 9:4 ff, 10 fff, 11 ff, 12 f, 13 mf, 13:4 p", gain=2),
        Part("cb", "D2:1 | G1:2 A1:2 | D2:2. A1:4 | D2:2 A1:2 | A1:1 | A1:1 | A1:1 | A1:1 | A1:1 | D2:1 |"
                   " G1:2 A1:2 | A1:1 | D1:1 |", dyn="1 p, 5 pp, 9 f, 9:4 ff, 10 fff, 11 ff, 12 f, 13 mf, 13:4 p", gain=-3),
    ],
)
