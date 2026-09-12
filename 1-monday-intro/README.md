# Monday — Kick-off & Python for CV

**Monday** · instructor: Petr Pajdla

What computer vision is, the family of tasks it covers, discriminative vs.
generative models, and a first working model before lunch.

The [slides](https://arup-cas.github.io/atrium-school-ml/materials/intro.html)
are on the school website.

## Notebooks

- [`clip_zero_shot.ipynb`](clip_zero_shot.ipynb) — zero-shot classification with
  CLIP. Classifying artefact photographs with no training and no annotation, and
  three ways it misleads you: the probabilities are over *your* label list,
  rewording a label changes the answer, and there is no "none of the above".
- [`clip_zero_shot_v2.ipynb`](clip_zero_shot_v2.ipynb) — the same notebook with
  the code spelled out step by step and commented line by line, plus an optional
  look inside the model. For beginners who want to follow every line.

## Data

| | |
|---|---|
| Access | `public` |
| Licence | CC BY-NC 4.0 — AMČR find photographs, see [`demo-images/CREDITS.md`](demo-images/CREDITS.md) |
| Source | `repo` — [`demo-images/`](demo-images/), see [`../datasets.yml`](../datasets.yml) |

```python
from atrium_data import get_dataset
path = get_dataset("demo")
```

To try your own photographs, use section 8 of the notebook — keep them in your
own folder rather than adding them to `demo-images/`, which on the school
JupyterHub everybody shares.
