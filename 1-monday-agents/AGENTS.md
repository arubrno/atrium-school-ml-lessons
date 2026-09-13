# Agent instructions

<!--
  This file is read at the start of every conversation, before anything else.
  It is the highest-value thing in the folder.

  Half of it is filled in. The other half is exercise C — add what you have
  already had to say to the agent twice this morning, then start a fresh
  conversation and check that it knows.
-->

Teaching folder for the **agents session**. Whoever is working here is an
archaeologist, not a programmer, and is learning what an agent does by watching
this one.

## How we work

- **Explain before changing anything.** Say what you are about to do and why,
  then do it.
- **Say what a command will do before you run it.**
- **Never touch `data/`.** It is the only thing here that cannot be regenerated.
- Do not commit. Ever. That is the human's job.

## About this material

- `data/finds.csv` — 142 archaeological finds. One row per object.
- Coordinates are **EPSG:5514** (S-JTSK / Krovak East North), in metres, and
  **negative**. They are not latitude and longitude, and a script that treats
  them as such produces an empty map.
- `datum` is a **year**, in Czech. It is not a full date.
- The file has faults in it on purpose — missing values, an impossible depth, a
  year that is clearly a typo, a site name without diacritics, one coordinate
  with the wrong sign. **Say what you found. Do not quietly repair them.**
- `scripts/` is throwaway. `data/` and `docs/` are not.
- `scripts/plot_finds.py` deliberately needs **no packages at all** — matplotlib
  if it is there, a hand-written SVG if it is not. Keep it that way. Anything
  needing torch or transformers belongs in `clip_classify.py`, which lives off
  the repository environment one level up.
- `artifacts/` is where generated pages go.

## Before you do these things, read the skill first

- making any picture or chart → `visualize`
- identifying an object in a photograph → `classify-image`

## What we have already decided

`docs/decisions.md` and `docs/lessons-learned.md` are read before proposing
anything. If something there already rules out what you are about to suggest,
say so instead of suggesting it.

## TODO — exercise C

Add five lines below. Facts about the material, or rules about how you want to
be worked with. At least one of them should be something this agent got wrong
in the last half hour.

1.
2.
3.
4.
5.
