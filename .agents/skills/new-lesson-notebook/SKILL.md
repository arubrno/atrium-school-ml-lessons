---
name: new-lesson-notebook
description: Scaffold a new lesson notebook for the ATRIUM training school, with the standard ATRIUM bootstrap cell, Colab badge, header and section structure. Use when asked to create a new notebook, add an exercise notebook to a day's folder, or start a session's material from scratch.
---

# New lesson notebook

Creates a notebook that runs unchanged in Google Colab, on the school
JupyterHub and on a local machine, and that looks like the ones already in the
repository.

## Before writing anything

Ask, or work out from the request:

1. **Which day's folder?** One of `1-monday-intro/`, `1-monday-python/`, `2-tuesday-artefacts/`,
   `3-wednesday-use-wear/`, `4-thursday-satellite/`, `4-thursday-rock-art/`,
   `5-friday-coins/`.
2. **File name** — lower case, underscores, descriptive of the method, not of
   the day (`clip_zero_shot.ipynb`, not `monday_2.ipynb`).
3. **Which dataset**, by its key in `datasets.yml`. If it is not there yet, add
   it first — see the `add-dataset` skill.
4. **Which packages** the bootstrap must ensure, e.g. `setup("torch", "transformers")`.
   Only what the notebook actually imports.

Restricted datasets (`satellite`, `rock-art`) are on the school JupyterHub only.
A notebook built on one of them must not carry a Colab badge, and must say so
in its header.

## Structure

Read `1-monday-intro/clip_zero_shot.ipynb` and follow it. Cell order:

1. **Markdown — header.** Title, then the school line, the day and session, the
   Colab badge, what the notebook does in three or four numbered points, and
   the *make your own copy* warning for Colab and the hub.
2. **Markdown — "## 1. Setup".** What the next cell does, plus the collapsible
   `<details>` blocks for Colab and the hub.
3. **Code — the ATRIUM bootstrap cell.** Copy it verbatim from
   `1-monday-intro/clip_zero_shot.ipynb`; change only the argument list of
   `setup(...)`. Do not rewrite, shorten or "improve" it — it is identical in
   every notebook on purpose, and anything general belongs in
   `atrium_bootstrap.py` instead.
4. **Code — imports and model loading.** Pin model weights by revision when
   loading from Hugging Face, with a comment saying why (the hub image has
   torch 2.4.1, so `use_safetensors=True` and a pinned revision are required).
5. **Numbered sections**, each a markdown cell followed by one or two short code
   cells.
6. **A closing "Try it yourself" section** with two or three open-ended tasks.

The Colab badge URL, with the real path of the new file:

```
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arubrno/atrium-school-ml-lessons/blob/main/<folder>/<file>.ipynb)
```

## Writing style

British English, second person, plain words. Explain the archaeology and what
the method does to it; do not teach Python syntax. A markdown cell before every
code cell. Keep cells short enough to read on a projector and fast enough to run
on a CPU laptop — a minute or two at most.

## Notebook JSON

Write the file with `nbformat` 4 / `nbformat_minor` 4 and this metadata, which
is what the existing notebooks carry:

```json
"metadata": {
  "kernelspec": {"display_name": "Python 3", "name": "python3"},
  "language_info": {"name": "python"}
}
```

Every code cell must have `"outputs": []` and `"execution_count": null`.

## Finish

- Add the notebook to the day's `README.md`.
- Run `.agents/skills/notebook-hygiene/scripts/nb_check.py <path>` and fix what
  it reports.
- Tell the user to run it top to bottom before it is taught from, and to clear
  the outputs again afterwards.
