# Agent instructions

Teaching material for the ATRIUM Training School *Computer Vision in Archaeology*
(Brno, 14–18 September 2026). Participants are archaeologists, not programmers,
and most of them meet Python for the first time during the week. Everything here
is read by them, runs in front of them, or breaks in front of them.

Read `README.md` first — it is the ground truth for how the repository is meant
to be used.

## What this repository is

```
atrium_bootstrap.py   platform detection, package install, cache locations
atrium_data.py        get_dataset()
datasets.yml          where every dataset lives — the only file that changes
                      when one moves
requirements.txt      the notebook environment
<n>-<day>-<topic>/    one folder per session: README.md + notebooks
```

## The other half of the school

The programme, the case-study descriptions, the practical information and the
participants' setup guide are **not** here. They live in <https://arup-cas.github.io/atrium-school-ml/>):

```
[programme](https://arup-cas.github.io/atrium-school-ml/programme.html)    the day-by-day programme — the authority on what is taught when
[setup](https://arup-cas.github.io/atrium-school-ml/setup.html)    the setup instructions participants actually follow
[info](https://arup-cas.github.io/atrium-school-ml/about.html)         venue, meals, practicalities
```

Read those when you need to know what a session is meant to cover. Keep a
notebook and the session it belongs to in step — if a change here makes
`programme` or `setup` wrong, say so.


## Hard rules

- **Never commit dataset files.** Data is fetched by `get_dataset("<name>")` and
  recorded in `datasets.yml`. The only exceptions already in the repository are
  `1-monday-intro/demo-images/` and `1-monday-python/data/` (public, small,
  credited in their `CREDITS.md`).
- **Never commit notebook outputs.** Every `.ipynb` in `main` has empty
  `outputs` and no `execution_count`. Clear them before staging.
- **Everything runs on CPU.** No CUDA-only code, no `.cuda()`, no assumption
  that a GPU exists. `torch` is installed from the CPU wheel index.
- **Do not touch the version pins without saying why.** `transformers` is held
  below 5 because the school JupyterHub image ships torch 2.4.1, and
  `openai/clip-vit-base-patch32` is pinned to a safetensors revision for the
  same reason.
- **Restricted datasets** (`satellite`, `rock-art`) exist only on the school
  JupyterHub. Code that uses them must fail with a readable message elsewhere,
  never with a traceback.

## The bootstrap cell

The first code cell of every notebook is identical, by design: on Colab the
repository does not exist yet when that cell runs, so it cannot import anything
from here before it has cloned. Copy it **verbatim** from
`1-monday-intro/clip_zero_shot.ipynb` into any new notebook.

Anything that could live in `atrium_bootstrap.py` belongs there instead — a fix
in that module reaches every notebook at once, a fix in the cell has to be
copied into all of them.

## Writing for the room

- Plain words, second person. Explain the archaeology more than the
  Python syntax.
- A markdown cell before every code cell says what the next cell does and why in notebooks.
- Keep cells short enough to read; no cell that takes more than
  a minute or two on a CPU laptop.
- Each day's folder has a `README.md` with the case study; keep it in step with
  the notebooks in that folder.
- Notebook headers carry an *Open in Colab* badge whose URL must match the
  notebook's real path in the repository.

## Datasets

`datasets.yml` is the single source of truth for where data lives. Moving a
dataset edits that file and nothing else. Each entry needs `title`, `day`,
`instructor`, `licence`, `access` and a `source` of kind `repo`, `url`, `hub`
or `zenodo`. Notebooks say `get_dataset("<name>")` and never a path.

## Working in this repository

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple
python -c "import atrium_bootstrap, atrium_data"   # smoke test
```

There is no test suite and no linter configured. Verify a change by running the
affected notebook top to bottom, then clearing its outputs again.

## Ask before you act

- adding a dependency to `requirements.txt`
- changing the bootstrap cell, `atrium_bootstrap.py`, or the cache locations
- rewriting a notebook someone else is teaching from this week
- anything that touches `git push`, tags or branches

Commit messages: one line, imperative, lower case, no scope prefix — match
`git log`.
