---
name: add-dataset
description: Add, move or document a dataset in datasets.yml for the training school - choosing the right source kind (repo, url, hub, zenodo), licence and access fields, and wiring it to get_dataset(). Use when a new dataset arrives, a dataset moves or is archived to Zenodo, a download URL or checksum needs filling in, or a notebook needs data it cannot yet reach.
---

# Add or move a dataset

`datasets.yml` is the single source of truth for where data lives. Notebooks say
`get_dataset("<name>")` and never a path, so moving a dataset edits that file and
nothing else. Read it before editing — the comments at the top define the
vocabulary.

## Decide the source kind

| `kind` | When | Needs |
| --- | --- | --- |
| `repo` | Small, public, redistributable — a folder committed here | `path` relative to the repository root |
| `url` | A `.zip` / `.tar.gz` fetched once and cached | `url`, and `sha256` once the file is final |
| `hub` | Already on the school JupyterHub, put there by the organisers | `path` under `~/_atrium-data/` |
| `zenodo` | Archived with a DOI — the preferred end state | the DOI |

Rules of thumb:

- Anything above a few megabytes is not `repo`, however tempting.
- Anything not redistributable is `hub` plus `access: restricted` plus a `note`
  telling the participant what to do when the folder is missing.
- After the school, `url` entries should become `zenodo` entries.

## The entry

Every dataset needs all of these keys. Unknown values are `TBC`, never omitted —
a missing licence is a question for the instructor, not a detail to be silently
dropped.

```yaml
<key>:                      # lower case, hyphens, matches get_dataset("<key>")
  title: Human-readable description of the images
  day: Wednesday
  instructor: Name or TBC
  licence: CC BY-NC 4.0     # or TBC; per-image credits go in a CREDITS.md
  access: public            # public | restricted
  source:
    kind: url
    url: "https://..."
    sha256: null            # TODO until the file is final
```

For `access: restricted`, add a `note:` that says where the data is and whom to
ask. It is shown to the participant when the data cannot be found.

## After editing

1. Check the file parses and the entry resolves:

   ```bash
   python3 -c "import yaml; d = yaml.safe_load(open('datasets.yml')); print(d['<key>'])"
   python3 -c "from atrium_data import get_dataset; print(get_dataset('<key>'))"
   ```

   For a `hub` dataset off the hub, and for a `url` dataset that is not yet
   published, `get_dataset` is expected to fail — check it fails with a sentence
   a participant can act on, not a traceback.

2. If the dataset is committed (`kind: repo`), add a `CREDITS.md` beside the
   images recording the source and licence of each one, as
   `1-monday-intro/demo-images/CREDITS.md` does.

3. Mention the dataset in that day's `README.md`.

4. Never commit the data of a `url`, `hub` or `zenodo` dataset, not even "just
   a few examples to test with".
