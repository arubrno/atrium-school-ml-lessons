---
name: notebook-hygiene
description: Check and clean the training-school notebooks before committing or teaching - clear outputs, verify the ATRIUM bootstrap cell, the Colab badge, CPU-only code and dataset access through get_dataset. Use before a commit that touches an .ipynb, when a notebook is about to be taught, or when asked to tidy, review or clear a notebook.
---

# Notebook hygiene

Notebooks in this repository are read by ~25 participants on three different
platforms, and updated in place during the week. The rules below are what keeps
a `git pull` on the school JupyterHub from ruining a session.

## Run the check

```bash
python3 .agents/skills/notebook-hygiene/scripts/nb_check.py            # all notebooks
python3 .agents/skills/notebook-hygiene/scripts/nb_check.py <path>     # one notebook
python3 .agents/skills/notebook-hygiene/scripts/nb_check.py --fix      # clear outputs in place
```

It reports, and `--fix` clears, only the first of these; the rest are fixed by
hand:

| Check | Why |
| --- | --- |
| No outputs, no `execution_count` | A committed output makes every participant's `git pull` a JSON merge conflict, and bloats the repository with base64 images. |
| First code cell is the ATRIUM bootstrap cell | It is identical in every notebook by design: on Colab nothing of this repository exists when it runs. |
| Data reached through `get_dataset("<name>")` | `datasets.yml` is the only place a path may live. |
| No CUDA-only code | Everything this week runs on CPU; the hub has no GPU. |
| Colab badge points at the notebook's real path | A wrong badge opens the wrong file, or a 404, in front of the room. |
| `kernelspec.name` is `python3` | Colab and the hub both expect it. |

## After the check passes

1. **Run the notebook top to bottom** in a fresh kernel. A notebook that only
   works when cells are run out of order will be run out of order by someone.
2. **Clear the outputs again** (`--fix`, or *Kernel → Restart and clear output*)
   and only then commit.
3. Keep an eye on the runtime: no cell should take more than a minute or two on
   a CPU laptop. If one does, cache the result or shrink the input, and say in
   the markdown above it how long it takes.
4. If the notebook loads a Hugging Face model, check the weights are pinned to a
   revision and loaded with `use_safetensors=True` — the hub image ships torch
   2.4.1, which cannot load `pytorch_model.bin`.

## What not to do

- Do not edit a notebook another instructor is teaching from this week without
  asking. Copy it instead.
- Do not "modernise" the bootstrap cell. General fixes go into
  `atrium_bootstrap.py`, where they reach every notebook at once.
- Do not add a dependency to make a notebook shorter. Every package added to
  `requirements.txt` is another install on the shared hub and another minute of
  the session spent watching pip.
