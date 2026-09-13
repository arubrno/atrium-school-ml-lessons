# Monday — Python fundamentals for CV

**Monday afternoon** · instructor: Filip Hájek

Enough Python to read, change and debug the code an AI tool writes for you, then
the three libraries behind most image work: NumPy, Matplotlib and OpenCV. The
session ends with a first computer-vision workflow, which separates the Venus of
Dolní Věstonice from its background and measures it.

## Notebooks

- [`python_intro.ipynb`](python_intro.ipynb): why learn Python when AI writes
  code, and how to turn a task into an algorithm before writing any.
- [`python_for_cv.ipynb`](python_for_cv.ipynb): the hands-on part. Code cells are
  empty, and you fill them in with the instructor: notebooks, Python basics,
  NumPy, Matplotlib, and OpenCV on the Venus photograph.
- [`python_for_cv_filled.ipynb`](python_for_cv_filled.ipynb): the same notebook
  with every cell filled in, for catching up or checking your version.

## Data

| | |
|---|---|
| Access | `public` |
| Licence | TBC: the instructor's own photograph, see [`data/CREDITS.md`](data/CREDITS.md) |
| Source | `repo` ([`data/`](data/)), see [`../datasets.yml`](../datasets.yml) |

```python
from atrium_data import get_dataset
path = get_dataset("venus")
```
