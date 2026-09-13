# Decision log

Why things are the way they are. **One entry per real choice between real
alternatives** — deciding to do the job properly is not a decision and does not
belong here.

Append at the end. Never rewrite an entry: a decision that is overturned keeps
its text, has its status changed, and points at the one that replaced it.

---

## D-001 — Coordinates stay in EPSG:5514

**Status:** accepted

**Context.** The finds were recorded in S-JTSK, which is what every Czech
excavation uses and what the site archive expects back. Plotting them needs
latitude and longitude, and converting is one line of code.

**Decision.** The stored data stays in EPSG:5514. Anything that needs lat/lon
converts on the way out and never writes the result back.

**Consequences.** Every script that draws a map has to convert first. A script
that forgets produces an empty map rather than a wrong one, which is the
failure we prefer.

---

## D-002 — Faults in the data are recorded, not repaired

**Status:** accepted

**Context.** `finds.csv` contains a handful of errors — a missing weight, an
impossible depth, a year that is obviously a typo, one coordinate with the
wrong sign.

**Decision.** They stay. Anything that reads the file reports what it found and
excludes those rows explicitly, with a count.

**Consequences.** Every output has to say how many rows it dropped. That is
deliberate: a chart that silently loses seventeen rows is a chart that lies.

---

<!--
  Add yours below in the same shape. Four headings, a few lines each:
  Context (what was true), Decision (what we chose), Consequences (what follows).
-->
