"""The Turn: a tune in C major builds toward C, and comes back in E major instead.

3/4. A clarinet sings the tune over harp; the violins take it up; bars 9-10 sit on G7 and promise C.
After a breath, the unison pickup B (the leading tone of C, and the fifth of E) lands on E major, a
chromatic mediant away, and the whole orchestra plays the tune with its opening leap widened to a sixth.
"""

from orchestra.piece import Part, Piece

R8 = "r:2. | " * 8
R6 = "r:2. | " * 6
STRINGS = "1 p, 4:3 p, 8 mp, 9 mp, 10 f, 10:2 ff, 11 ff, 12 fff, 13 ff, 14:3 f, 15 f, 16:3 pp"
TUTTI = "9 mp, 10 f, 10:2 ff, 11 ff, 12 fff, 13 ff, 14:3 f, 15 f, 16:3 pp"
TUNE_E = "E5:4. F#5:8 G#5:4 | E6:2 D#6:8 C#6:8 | B5:4. A5:8 G#5:4 | F#5:2 D#5:4 | E5:2.~ | E5:2. |"
TUNE_E_8VB = "E4:4. F#4:8 G#4:4 | E5:2 D#5:8 C#5:8 | B4:4. A4:8 G#4:4 | F#4:2 D#4:4 | E4:2.~ | E4:2. |"
TUNE_E_15MB = "E3:4. F#3:8 G#3:4 | E4:2 D#4:8 C#4:8 | B3:4. A3:8 G#3:4 | F#3:2 D#3:4 | E3:2.~ | E3:2. |"

PIECE = Piece(
    title="The Turn",
    key="0 C major, 11 E major",
    time="3/4",
    pickup=1,
    tempo="0 66, 8 66, 9 70, 10 64, 10:3 50, 11 58, 12 54, 13 52, 14:3 44, 15 42, 16:3 36",
    tempo_text="Andante",
    directions="10:3 (breath); 11 Maestoso; 14:3 allargando",
    apex="12",
    parts=[
        Part("fl", "r:4 | " + R8 + "A5:4 B5:4 C6:4 | D6:2 r:4 | " + TUNE_E, dyn=TUTTI, gain=-2),
        Part("ob", "r:4 | " + R8 + "r:2. | r:2. | " + TUNE_E_8VB, dyn=TUTTI, gain=-5),
        Part("cl_solo", "G4:4 | C5:4. D5:8 E5:4 | G5:2 F5:4 | E5:4. D5:8 C5:4 | D5:2 r:4 | " + R6 + TUNE_E_8VB,
             name="Clarinet", dyn="0 mp, 1:3 mf, 2:3 mp, 4 p, 11 mf, 12 f, 14 mf, 15 mf, 16:3 pp", gain=3),
        Part("bn", "r:4 | " + R8 + "r:2. | r:2. | " + TUNE_E_15MB, dyn=TUTTI, gain=-3),
        Part("hn", "r:4 | " + R8 + "<D4 F4>:2 <C4 F4>:4 | <B3 D4 F4>:2 r:4 | <B3 E4 G#4 B4>:2. | <A3 C#4 E4 A4>:2. |"
                   " <B3 E4 G#4 B4>:2. | <A3 C#4 E4 F#4>:2 <A3 B3 D#4 F#4>:4 | <B3 E4 G#4 B4>:2.~ | <B3 E4 G#4 B4>:2. |",
             dyn=TUTTI, gain=-3),
        Part("tbn", "r:4 | " + R8 + "r:2. | r:2. | <E3 G#3 B3>:2. | <E3 A3 C#4>:2. | <E3 G#3 B3>:2. |"
                    " <C#3 E3 A3>:2 <D#3 F#3 B3>:4 | <E3 G#3 B3>:2.~ | <E3 G#3 B3>:2. |",
             dyn="11 f, 12 ff, 13 f, 15 f, 16:3 pp", gain=-6),
        Part("tba", "r:4 | " + R8 + "r:2. | r:2. | E2:2. | A1:2. | B1:2. | A1:2 B1:4 | E2:2.~ | E2:2. |",
             dyn="11 f, 12 ff, 13 f, 15 f, 16:3 pp", gain=-6),
        Part("timp", "r:4 | " + R8 + "G2:2. | G2:2 r:4 | @hit E2:4! @roll E2:2 | r:2. | r:2. | r:2 B2:4 |"
                     " @hit E2:4 @roll E2:2~ | E2:2. |",
             dyn="9 p, 10:2 ff, 11 ff, 11:2 f, 11:3 p, 14:3 mp, 15 f, 15:2 mf, 16:3 pp"),
        Part("harp", "r:4 | C3:8 G3 C4 E4 G4 E4 | F2:8 C3 F3 A3 C4 A3 | A2:8 E3 A3 C4 F#2 C3 | G2:8 D3 G3 B3 D4 B3 |"
                     " C3:8 G3 C4 E4 G4 E4 | F2:8 C3 F3 A3 E3 C4 | A2:8 E3 A3 C4 F#3 C4 | G2:8 D3 G3 B3 D4 G4 |"
                     " " + R6 + "E2:8 B2 E3 G#3 B3 E4 | G#4:2. |",
             dyn="1 mp, 8 mp, 15 mf, 16 mp", gain=-2),
        Part("vln1", "r:4 | r:2. | r:2. | r:2. | r:2 G4:4 | C5:4. D5:8 E5:4 | A5:2 G5:4 | C6:4. B5:8 A5:4 | G5:2. |"
                     " A5:4 B5:4 C6:4 | D6:2 r:8 B4:8 | " + TUNE_E,
             dyn="4:3 mp, 6 mp, 7 mf, 8 mp, 9 mp, 10 f, 10:2 ff, 11 ff, 12 fff, 13 ff, 14:3 f, 15 f, 16:3 pp", gain=4),
        Part("vln2", "r:4 | E4:2. | F4:2. | E4:2 D4:4 | D4:2. | E4:2. | F4:2 G4:4 | E4:2 D4:4 | D4:2. |"
                     " @trem <D4 F4>:2 <C4 F4>:4 | <D4 F4>:2 r:8 @arco B3:8 | " + TUNE_E_8VB, dyn=STRINGS, gain=1),
        Part("vla", "r:4 | G3:2. | A3:2. | A3:2. | B3:2. | C4:2. | C4:2. | C4:2. | B3:2. |"
                    " @trem <G3 B3>:2 <A3 C4>:4 | <G3 B3>:2 r:8 @arco B3:8 | <G#3 B3>:2. | <A3 C#4>:2. | <G#3 B3>:2. |"
                    " <A3 C#4>:2 <A3 B3>:4 | <G#3 B3>:2.~ | <G#3 B3>:2. |", dyn=STRINGS, gain=-3),
        Part("vc", "r:4 | C3:2. | F2:2. | A2:2 F#2:4 | G2:2. | C3:2. | F2:2 E2:4 | A2:2 F#2:4 | G2:2. | G2:2. |"
                   " G2:2 r:8 B2:8 | " + TUNE_E_15MB, dyn=STRINGS, gain=1),
        Part("cb", "r:4 | @pizz C2:4 r:2 | F1:4 r:2 | A1:4 r:4 F#1:4 | G1:4 r:2 | C2:4 r:2 | F1:4 r:4 E1:4 |"
                   " A1:4 r:4 F#1:4 | G1:4 r:2 | @arco G1:2. | G1:2 r:4 | E1:2. | A1:2. | B1:2. | A1:2 B1:4 |"
                   " E1:2.~ | E1:2. |", dyn=STRINGS, gain=-3),
    ],
)
