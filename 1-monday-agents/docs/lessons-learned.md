# Lessons learned

Mistakes already made, so nobody makes them twice — including you, in six
months, having forgotten.

**One entry per mistake that cost real time.** What happened, how it surfaced,
and what changed so it cannot happen again. Append at the end.

---

## L-001 — An empty map is a projection error until proved otherwise

**What happened.** `scripts/plot_finds.py` ran without an error and produced a
blank map. Twenty minutes went into the plotting code before anybody looked at
the numbers.

**How it surfaced.** Printing the first coordinate: `-598120.0`. No latitude is
−598 120.

**What changed.** Any script that draws a map prints the range of the
coordinates it is about to plot, before it plots them.

---

<!--
  Add yours below. The "what changed" line is the one that matters —
  a lesson with no change is a complaint.
-->
