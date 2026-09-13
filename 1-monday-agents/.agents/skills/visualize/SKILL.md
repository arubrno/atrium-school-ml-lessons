---
name: visualize
description: Build a self-contained HTML page in artifacts/ that shows something visually - a chart of a CSV column, a map, a comparison, a diagram, or an explanation of how something works. Use whenever the user asks to see, show, plot, chart, draw, visualise or "give me a picture of" anything, and whenever a table of numbers would be easier to understand as a picture.
---

# Make a visual artefact

One HTML file, in `artifacts/`, that opens in a browser and needs nothing else.

## Rules

- **One file.** Everything inline — styles, scripts, data, any SVG. No build
  step, no separate assets.
- **No internet.** No CDN, no web fonts, no external images. The room is on
  conference wifi and half of it will not load. Write the chart yourself in SVG
  or canvas, or lay it out with CSS.
- **Embed the data.** Copy the numbers into the file as a JavaScript array or a
  `<script type="application/json">` block. A page that reads a CSV at runtime
  is broken the moment it is moved or emailed.
- **Name it for what it shows:** `artifacts/finds-per-year.html`, not
  `artifacts/chart.html`.
- **Say the path when you are done**, so the user can open it.

## What a good one has

| | |
| --- | --- |
| A title | what this shows, in plain words |
| The point, in a sentence | directly under the title, before the picture |
| Units and a scale | on the axes, not in a caption |
| The source | which file, which column, how many rows |
| What was left out | rows dropped for missing values, and how many |

That last row matters more than it looks. A chart that silently drops
seventeen rows is a chart that lies. Put the count on the page.

## Choosing a form

- **Comparing a few things** — bars, sorted, longest at the top.
- **Change over time** — a line, with the years actually labelled.
- **Where things are** — a scatter in the data's own coordinates. Do not
  pretend to be a map unless you have a real basemap, which you do not.
- **How something works** — boxes and arrows in SVG, not a paragraph.
- **Two versions of the same thing** — side by side, same scale, always.

## Stop and ask

Do not guess your way past any of these:

- the user has not said **which column or which file** to show
- the data has **more than one plausible reading** — for example a column of
  years that also contains an obvious typo
- the numbers are **in units you cannot identify**
- making the picture would mean **dropping more than a tenth of the rows**

Say what is ambiguous and ask. A confident chart of the wrong column is worse
than no chart.
