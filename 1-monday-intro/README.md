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

## Data

| | |
|---|---|
| Access | `public` |
| Licence | CC BY-SA 4.0 |
| Source | `repo` — [`demo-images/`](demo-images/), see [`../datasets.yml`](../datasets.yml) |

```python
from atrium_data import get_dataset
path = get_dataset("demo")
```

Add your own photographs to `demo-images/` and they appear in the notebook.
