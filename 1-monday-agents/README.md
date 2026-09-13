# Monday — Coding with agents

**Monday afternoon** · 90 minutes · practical

What an agent actually is, how to steer one, and how to leave a record that
outlives the conversation. Nobody writes code. You write **instructions**, and
find out where they go wrong.

## Open this folder in Zed

**File → Open Folder → `1-monday-agents`**

Open **this folder**, not the whole repository. Everything the agent reads —
the instructions, the skills, the data — is scoped to the folder you open, so
opening the right one is the first thing that matters.

Then open the agent panel and leave it on **ask before acting** for the whole
session.

## What is here

```
AGENTS.md              read at the start of every conversation. Half written —
                       finishing it is exercise C
.agents/skills/        procedures the agent reads only when they apply
  visualize/           make a self-contained HTML page in artifacts/
  classify-image/      ask this morning's CLIP model what is in a photograph
data/finds.csv         142 finds, one row per object. Faults on purpose
data/sites.csv         the eight sites and where they are
scripts/plot_finds.py  draws a map. The map comes out empty
scripts/clip_classify.py   the command behind the classify-image skill
docs/decisions.md      why things are the way they are
docs/lessons-learned.md    mistakes already made
artifacts/             where visualize writes
```

## The data

142 find records from eight Moravian sites. It is **invented**, and it is
invented carefully: the coordinates are in the projection Czech excavations
actually use, the column names are the ones you meet in a real archive, and
there are faults in it of the kind that cost people afternoons.

| | |
| --- | --- |
| `datum` | a **year**, in Czech. Not a full date |
| `x_jtsk`, `y_jtsk` | **EPSG:5514**, metres, negative. Not latitude and longitude |
| the faults | a missing weight, a missing coordinate, `2105` for `2015`, `Bronze` for `bronze`, `Boritov` for `Bořitov`, a depth of −20, one coordinate with the sign flipped |

Nobody is told where the faults are. Noticing them is part of the point.

## The four exercises

| | | |
| --- | --- | --- |
| **A** | 6 min | Run a task and **count the turns of the loop** |
| **B** | 4 min | **Refuse** an edit, and read what it does next |
| **C** | 6 min | Finish **AGENTS.md**, then open a fresh conversation and test it |
| **D** | 4 min | Use a skill, read the one that did it, **write your own** |

## Running the scripts

The session's environment is the repository's — see
[`../README.md`](../README.md). Everything here runs on CPU.

```bash
python scripts/plot_finds.py
python scripts/clip_classify.py --image <photo> --labels "a,b,c"
```

`clip_classify.py` uses the **same model and the same pinned weights** as
[`../1-monday-intro/clip_zero_shot.ipynb`](../1-monday-intro/clip_zero_shot.ipynb),
so an answer here and an answer this morning are the same answer. The first run
downloads about 600 MB; do it before the session, not during it.

## Slides

The deck for this session is separate. It expects this folder to be open in
Zed, and it refers to these files by name.
