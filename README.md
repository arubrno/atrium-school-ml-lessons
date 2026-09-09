# Computer Vision in Archaeology — lessons and exercises

Notebooks and case-study exercises for the **ATRIUM Training School, Brno,
14–18 September 2026**.

Slides, programme, practical information and the setup guide live on the school
website: <https://arup-cas.github.io/atrium-school-ml/>.

## The week

| | | |
|---|---|---|
| [`1-monday-intro/`](1-monday-intro/) | Kick-off & Python for CV | zero-shot classification with CLIP |
| [`2-tuesday-artefacts/`](2-tuesday-artefacts/) | Artefact photographs | datasets, licensing, annotation |
| [`3-wednesday-use-wear/`](3-wednesday-use-wear/) | Microscopic use-wear | pre-processing, augmentation, OpenCV |
| [`4-thursday-satellite/`](4-thursday-satellite/) | Satellite imagery | object detection on remote-sensing data |
| [`4-thursday-rock-art/`](4-thursday-rock-art/) | Rock art | to be confirmed |
| [`5-friday-coins/`](5-friday-coins/) | Coins | combining methods, vision-language models |

Each folder has a README with the case study, and the notebooks for that day.

## Running the notebooks

Every notebook opens with the same setup cell. It works out where it is running,
fetches this repository if it has to, installs only what is missing, and points
the model and dataset caches somewhere sensible. **Nothing needs editing to move
between platforms.**

**Google Colab** — nothing to install. Click the *Open in Colab* badge in a
notebook's first cell and run it. Colab wipes its disk when the runtime is
recycled; to keep the model weights between sessions, change the last line of
the setup cell to `setup("torch", "transformers", drive=True)` and approve the
Google Drive prompt.

**School JupyterHub** — you get a URL on the first morning that drops you
straight into JupyterLab, with the server running and this repository already
in place. Open the day's folder and double-click the notebook.

**Your own machine** —

```bash
git clone --depth 1 https://github.com/arubrno/atrium-school-ml-lessons.git
cd atrium-school-ml-lessons
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple
```

That `--index-url` matters: a plain `pip install torch` pulls the CUDA runtime
(~2.5 GB) even on a laptop with no NVIDIA card. Everything this week runs on CPU.

## Datasets

Data is **not** in this repository — some of it is several gigabytes, and some is
not redistributable. Every notebook gets its data the same way:

```python
from atrium_data import get_dataset
path = get_dataset("coins")
```

Where each dataset actually lives — in this repository, mounted on the hub, or
downloaded once and cached — is recorded in [`datasets.yml`](datasets.yml), and
nowhere else. Moving a dataset edits that file and no notebook.

The satellite and rock-art datasets are restricted and are mounted on the school
JupyterHub only; those two case studies do not run in Colab.

## What is where

```
atrium_bootstrap.py   platform detection, package install, cache locations
atrium_data.py        get_dataset()
datasets.yml          where every dataset lives — the only file that changes
                      when one moves
requirements.txt      the notebook environment
```

## Working on a notebook

Copy it before you edit it (`cp clip_zero_shot.ipynb my-clip.ipynb`). We push
updates during the week, and `git pull` onto a notebook you have changed produces
a merge conflict in raw JSON that nobody enjoys resolving.

## Licence

MIT for the code, see [LICENSE](LICENSE). Datasets carry their own licences,
recorded per dataset in `datasets.yml`.
