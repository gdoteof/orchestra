# orchestra

Late-Romantic orchestral sketches written as text, engraved as scores and rendered with free orchestral samples.

```
uv run python -m orchestra pieces/withheld.py     # -> build/withheld/{mix.mp3, score.musicxml, score-N.png}
```

- `pieces/` - one module per piece, each defining `PIECE`. The note syntax is documented in `orchestra/notation.py`.
- `orchestra/` - the parser, the instrument table (`instruments.py`), rendering (one MIDI file per part and
  articulation through `sfizz_render`, then a synthetic hall) and engraving (music21 -> MusicXML -> Verovio).
- `samples/` (gitignored) - [Virtual Playing Orchestra 3](https://virtualplaying.com/virtual-playing-orchestra/):
  the wave files and both script sets unzipped into `samples/Virtual-Playing-Orchestra3/`.
- `third_party/sfizz` (gitignored) - built from source for its `sfizz_render` CLI:
  `cmake -B build -DCMAKE_BUILD_TYPE=Release -DSFIZZ_JACK=OFF -DSFIZZ_RENDER=ON -DSFIZZ_SHARED=OFF && cmake --build build --target sfizz_render`.

The build prints the apex time and a loudness per bar, to check that the arc peaks where it was planned.

## Sound

There is no synthesis. Every note is a recorded sample, played back by a sampler:

- **Sampler:** [sfizz](https://github.com/sfztools/sfizz), an open-source SFZ player, run offline through its
  `sfizz_render` CLI (built from the `develop` branch, commit `f5c6e29`). Each part and articulation becomes
  its own MIDI file, and `sfizz_render` turns it into a 48 kHz stem.
- **Samples:** [Virtual Playing Orchestra 3](https://virtualplaying.com/virtual-playing-orchestra/) by Paul
  Battersby (Performance Orchestra 3.3, wave files 3.2). It is free and built from Sonatina Symphonic Orchestra,
  VSCO 2 CE, No Budget Orchestra, University of Iowa and other free libraries. Strings, winds and brass use the
  `*-PERF` section patches, where CC1 (the mod wheel) sets the dynamic and velocity sets the attack. Timpani,
  cymbals, snare, bass drum and harp respond to note velocity.
- **Room:** no reverb plugin. `render.py` builds a synthetic hall impulse response (decorrelated noise,
  RT60 2.3 s, highs dying first) and convolves the summed stems with it.

The samples are not in this repo. Download them from the link above.

## Game cues

`orchestra/cue.py` writes a looping game cue as sections with their own bar numbers, renders them in one pass and
cuts the render into segments (`build/<name>/segments/*.wav` and `.ogg`, sample-exact, plus `manifest.json` and a
`preview.mp3` that plays them in order). The render order gives each segment the right reverb tail at its head: a
looping section is rendered twice and only the second pass is cut, and the segments that lead into the loop end
on a 30 ms crossfade into the first pass's ending, so both seams are sample-continuous.

`pieces/wager.py` is a battle-betting cycle at 144 bpm in D minor:

| segment | length | |
|---|---|---|
| `bets` | 15 bars, 25.0 s | scherzando, building over the last five bars |
| `countdown` | 3 bars, 5.0 s | "no more bets" hit, then a drum crescendo into the battle |
| `start` | 4 bars, 6.67 s | fanfare; plays once, then straight into `loop` |
| `loop` | 32 bars, 53.33 s | the battle; loops seamlessly for as long as it lasts |
| `recap` | 11 bars, 25.0 s | D major, broad, slowing to a soft close; then `bets` again |

Leave the battle at a bar line of `loop` (every 1.6667 s) if the player can, with a 20-50 ms fade, and start
`recap` at once: it opens on a tutti hit that covers the cut. Use the `.ogg` or `.wav` files for looping, not MP3,
whose encoder padding puts a gap in the loop.
