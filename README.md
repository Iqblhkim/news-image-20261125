[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Iqblhkim/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Iqblhkim/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World in One Day — Wednesday 25 November 2026

A program that draws a one-page newspaper front page summing up the
world's news of Wednesday 25 November 2026: 36 stories across 6 regions,
every one dated to that day.

## What the page shows

- A navy top strip stating the premise: 36 stories, 6 regions, all dated
  Wednesday 25 November 2026.
- The masthead date in a thin serif face, a red rule, and a three-part
  red subhead (Kyiv hit again, Zelenskyy on the stalled Patriots, the
  Houthi strike on Riyadh's tallest tower).
- A row of six big numbers: Venezuela's $237.5bn public debt, the
  700,000 Russian troops killed in the war, the 74,746 Gaza death toll,
  the 266m people facing acute food insecurity, the 48 Patriot
  interceptors awaiting US sign-off, and the 11 wounded in Riyadh.
- A coloured region bar (Europe 8, Middle East 5, Americas 12,
  Asia-Pacific 9, Africa 1, World 1).
- Three lead stories with drawn scenes: Russian drones over Kyiv and
  Odesa, the Patriot interceptor standoff in Washington, and the Houthi
  drone strike on Riyadh's tallest tower.
- Twelve illustrated tiles (New Delhi, Benghazi, Washington, New York,
  the Gulf of Hormuz, Brussels, Mumbai, London, Tehran, Kabul), each
  with its own small drawn scene.
- A world map with numbered pins for the stories, an "Also on Wednesday"
  list of the remaining 21 stories, a DATE CHECK box explaining which
  well-known events were left out because they happened on earlier days,
  and a sources footer.

## How it is built

Pure Python 3.13 standard library — no Pillow, no numpy, no fonts, no
network, no clock, no randomness. Everything is drawn by hand:

- Every letter comes from a vector stroke alphabet defined in the
  program (an 8-unit em, cap top to baseline, with descenders). Text is
  rendered as thick round-ended strokes at any size; the masthead uses
  a thinner refined face with small serif ticks on the stems.
- Every picture — skylines, drones, a missile launcher, a tower, a medal,
  a monitor, a cargo ship, a ballot box, a warning triangle — is drawn
  from rectangles, discs and polygons.
- Every tile scene is positioned with fractions of its own 40-pixel
  band only, and a clipping rectangle is set while a scene draws, so no
  illustration can ever escape its band and cover a headline or kicker.
- A built-in layout checker verifies that every text block fits its box
  with at least 4 pixels to spare, that no scene pixel leaves its band,
  and that nothing leaves the 1024×1024 canvas. It prints its issue
  count and the program exits non-zero unless the count is 0.
- The PNG is encoded by hand (zlib + struct). Two runs produce a
  byte-identical file.

## How to run it

```sh
MAKEFUN_OUTPUT_DIR=<directory> python3 main.py
```

It creates the directory if needed and writes `<directory>/entry.png`
(1024×1024, under 1 MiB). It prints the layout checker's verdict first;
if the checker finds any issue the program stops without writing a file.
