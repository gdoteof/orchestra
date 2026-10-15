"""Withheld: the cadence home is denied twice, then granted at the apex.

Eb major. Bar 5 is a deceptive cadence (V7 -> vi). Bar 8 is the false peak: V7 lurches to Cb major (bVI)
at ff. The first true V7 -> I arrives at bar 10, with the melody on an appoggiatura (F6 over Eb, resolving
a half note later). The coda's IV -> iv -> I recalls the Cb.
"""

from orchestra.piece import Part, Piece

STRINGS = "1 pp, 2 p, 4:3 p, 5 mp, 5:3 p, 6 p, 7:3 f, 8 ff, 8:3 f, 9 f, 10 fff, 10:3 ff, 11 f, 11:3 mp, 12 p, 12:4 pp"
WINDS = "8 ff, 8:3 f, 9 f, 10 fff, 10:3 ff, 11 f, 11:3 mp"

PIECE = Piece(
    title="Withheld",
    key="Eb major",
    tempo="1 54, 5 54, 6 58, 7 60, 7:4 56, 8 54, 9 54, 9:4 44, 10 48, 11 50, 12 42, 12:4 34",
    tempo_text="Adagio",
    directions="9:3 allargando; 12 morendo",
    apex="10",
    parts=[
        Part("fl", "r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | Cb6:2. Bb5:4 | Ab5:4 Cb6:4 Bb5:4 D6:4 |"
                   " F6:2 Eb6:2 | C6:2 Cb6:2 | r:1 |", dyn=WINDS, gain=-1),
        Part("ob", "r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | Cb5:2. Bb4:4 | Ab4:4 Cb5:4 Bb4:4 D5:4 |"
                   " F5:2 Eb5:2 | C5:2 Cb5:2 | r:1 |", dyn=WINDS, gain=-3),
        Part("cl", "r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | Eb4:2 D4:2 | Eb4:1 | Eb4:2 D4:2 | Eb4:1 | Eb4:1 | Eb4:1 |",
             dyn="7 p, 7:3 mf, 8 f, 9 f, 10 ff, 11 mf, 12 p, 12:4 pp", gain=-5),
        Part("bn", "r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | Cb3:2 Ab2:2 | F2:2 Bb2:2 | Eb2:1 | Ab2:1 | r:1 |",
             dyn="8 f, 9 f, 10 ff, 11 mf", gain=-4),
        Part("hn", "r:1 | r:1 | r:1 | r:1 | r:1 | <C4 Eb4>:1 | <Bb3 Eb4 G4>:2 <Bb3 D4 F4>:2 |"
                   " <Cb4 Eb4 Gb4>:2 <Cb4 Eb4 Ab4>:2 | <Cb4 Eb4 Ab4>:2 <Bb3 D4 F4 Ab4>:2 | <Bb3 Eb4 G4 Bb4>:1 |"
                   " <C4 Eb4 Ab4>:2 <Cb4 Eb4 Ab4>:2 | <Bb3 Eb4 G4>:1 |",
             dyn="6 p, 7:3 mf, 8 ff, 8:3 f, 9 f, 10 fff, 10:3 ff, 11 f, 11:3 mp, 12 p, 12:4 pp"),
        Part("timp", "r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | r:1 | r:2 Bb2:2 | @hit Eb3:4 @roll Eb3:2. | r:1 |"
                     " Eb3:1 |", dyn="9:3 p, 10 ff, 10:2 f, 10:4 p, 12 pp", gain=-3),
        Part("vln1", "r:2. Bb4:4 | G5:2 F5:4 Eb5:4 | D5:2 C5:4 Bb4:4 | Ab4:2 C5:4 Bb4:8 Ab4:8 | G4:2. C5:4 |"
                     " Ab5:2 G5:4 F5:4 | G5:4 Ab5:4 Bb5:2 | Cb6:2. Bb5:4 | Ab5:4 Cb6:4 Bb5:4 D6:4 | F6:2 Eb6:2 |"
                     " C6:2 Cb6:2 | Bb5:1 |",
             dyn="1 p, 2 mp, 2:3 mp, 3 p, 4:3 mp, 5 mp, 5:3 p, 6 mp, 7:3 f, 8 ff, 8:3 f, 9 f, 10 fff, 10:3 ff,"
                 " 11 f, 11:3 mp, 12 p, 12:4 pp", gain=4),
        Part("vln2", "G4:1 | Bb4:2. C5:4 | Bb4:2 Ab4:2 | F4:1 | Eb4:1 | Ab4:2 G4:4 F4:4 | G4:4 Ab4:4 Bb4:2 |"
                     " Cb5:2. Bb4:4 | Ab4:4 Cb5:4 Bb4:4 D5:4 | F5:2 Eb5:2 | C5:2 Cb5:2 | Bb4:1 |", dyn=STRINGS, gain=1),
        Part("vla", "Eb4:1 | G4:2 F4:4 G4:4 | G4:2 Eb4:2 | C4:2 D4:2 | C4:1 | <C4 Eb4>:1 |"
                    " <Bb3 Eb4>:2 <Ab3 D4>:2 | <Gb3 Eb4>:2 <Ab3 Eb4>:2 | <Ab3 Eb4>:2 <Ab3 D4>:2 | <G3 Eb4>:1 |"
                    " <Ab3 C4>:2 <Ab3 Cb4>:2 | <G3 Bb3>:1 |", dyn=STRINGS, gain=-3),
        Part("vc", "Eb3:1 | Eb3:2 D3:4 C3:4 | G2:2 Ab2:2~ | Ab2:2 Bb2:2 | C3:1 | Ab2:2 A2:2 | Bb2:1 |"
                   " Cb3:2 Ab2:2 | F2:2 Bb2:2 | Eb2:1 | Ab2:1 | Eb3:1 |", dyn=STRINGS),
        Part("cb", "Eb2:1 | Eb2:2 D2:4 C2:4 | G1:2 Ab1:2~ | Ab1:2 Bb1:2 | C2:1 | Ab1:2 A1:2 | Bb1:1 |"
                   " Cb2:2 Ab1:2 | F1:2 Bb1:2 | Eb1:1 | Ab1:1 | Eb2:1 |", dyn=STRINGS, gain=-3),
    ],
)
