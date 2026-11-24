# THE WORLD — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/didinska21/world-news-tuesday-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/didinska21/world-news-tuesday-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124)

One day, one page: the whole of Tuesday 24 November 2026 drawn as a
single newspaper front page — **44 date-checked stories across 8
regions**, with six illustrated lead stories and 38 briefs. Every
story on the page happened, or was first reported, on that Tuesday
(UTC); nothing is carried over from any other day.

The leads: Asia's chip rally (Tokyo +4.5%), the dawn quake in Nepal,
the overnight strike on Zaporizhzhia, Seoul's air alert over a
Russian jet, the Himalayan flood, and America's Thanksgiving getaway.

## How it runs

- `entry.png` is the deliverable: a 1024×1024 front page drawn
  entirely in code (no photographs, no AI image generation).
- `main.ts` is the entry point. Run it with Node 22+:

  ```
  node main.ts
  ```

  It copies `entry.png` to `/output/entry.png`, byte for byte, using
  only the Node standard library.
- `draw_frontpage.py` is the generator that produced `entry.png`
  (Python 3 + Pillow). It is kept in the repo so the page can be
  reproduced exactly:

  ```
  python3 draw_frontpage.py
  ```

## Layout of the page

- Masthead with the day, the story count and the region count.
- A UTC timeline strip: the day around the world.
- Six lead panels, each with its own drawn scene, a region chip, a
  headline and a two-line summary.
- "More of the Day": 38 briefs in three columns, each tagged with
  its region code, plus a region key with per-region story counts.
