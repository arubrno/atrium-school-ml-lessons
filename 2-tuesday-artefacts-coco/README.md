# Artefacts: a training dataset in COCO format

**Tuesday** · instructor: TBC

A real annotated dataset to train and test on: 1500 photographs of metal-detector
finds from [AMČR-PAS](https://amcr-info.aiscr.cz), with the outline of every object
drawn by the people who recorded it. It is a subset of the full AMČR-PAS export
(9 702 photographs, 207 classes): the ten largest classes, 150 photographs each.

| class | photographs | objects |
|---|---|---|
| fibula | 150 | 160 |
| coin | 150 | 185 |
| arrow/arrowhead | 150 | 165 |
| mount | 150 | 174 |
| pendant | 150 | 172 |
| clothing pin | 150 | 161 |
| circle/ring | 150 | 150 |
| bracelet | 150 | 167 |
| sickle | 150 | 163 |
| buckle | 150 | 170 |
| **total** | **1500** | **1667** |

More objects than photographs: a photograph often shows one find twice, front and
back side by side, and each view has its own box.

## Get it

From a notebook, never by hand:

```python
from atrium_data import get_dataset
path = get_dataset("artefacts-coco")
```

The folder you get back holds:

| | |
|---|---|
| `images/` | the photographs, 640 px on the long side (about 58 MB) |
| `annotations.json` | COCO format: a box (`bbox`) and an outline (`segmentation`, polygons) for every object; `attributes.recognizable` is `false` where the recorder could not tell what the object was |
| `credits.csv` | the AMČR record and DOI of every photograph |
| `README.md` | the same summary |

### If the download fails

`get_dataset` downloads the zip (58 MB) from CESNET FileSender. If that keeps failing,
get it by hand:

1. Open <https://filesender.cesnet.cz/?s=download&token=0f541c2c-598b-4b6c-8000-fac724e0bfd4>
   and click **Download**. You get `artefacts-coco.zip`.
2. In a notebook, after the setup cell, find where datasets are kept:

   ```python
   from atrium_data import cache_dir
   print(cache_dir())
   ```

3. Unzip `artefacts-coco.zip` into that folder, so that you end up with
   `<that folder>/artefacts-coco/images/`. Watch out: *Extract All* on Windows adds a
   second `artefacts-coco` folder, one level too deep.
4. Run `get_dataset("artefacts-coco")` again. It now finds the folder and does not
   download anything.

There are no ready-made train/validation splits. Make your own, and keep the photos
of one AMČR record (the `record` field of each image) on the same side of the split.

## How it was chosen

- **Classes**: the ten with the most photographs, leaving out the catch-alls
  (*adornment*, *metal sheet*, *amorphous fragment/object*, *exceptional object*).
  They say more about the recorder than about the object.
- **Photographs**: only those where every recorded object belongs to one of the ten
  classes. A photograph with an unlabelled object would teach a model that the object
  is background.
- **Spread**: one photograph per AMČR record first, so the 150 per class show about
  150 different finds (1487 records in all).
- **Left out**: photographs smaller than 640 px, and the ten photographs of the
  annotation exercise in [`../2-tuesday-artefacts/`](../2-tuesday-artefacts/), so
  nobody trains on what they annotated.
- The `occluded` attribute of the original export is dropped. It was CVAT's
  unticked default and is `false` on every box.

## Credits

The photographs and annotations come from AMČR-PAS, the portal of the Archaeological
Information System of the Czech Republic, and are published under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). [`credits.csv`](credits.csv)
gives the record DOI for each: `M202400098N00219F01.jpg` is photograph `F01` of record
[M-202400098-N00219](https://doi.org/10.71928/M-202400098-N00219).

## Data

| | |
|---|---|
| Access | `public` |
| Licence | CC BY-NC 4.0 |
| Source | `url` (see [`../datasets.yml`](../datasets.yml)) |

## Rebuilding (organisers)

```bash
python3 2-tuesday-artefacts-coco/build_subset.py --out temp
```

It reads the AMČR-PAS COCO export and its photographs from the FiftyOne copy
(`$FIFTYONE_ROOT`, default `~/Documents/fiftyone`), and writes `temp/artefacts-coco/`,
`temp/artefacts-coco.zip`, a contact sheet for checking the outlines by eye, and this
folder's `credits.csv`. The build is deterministic: the same inputs give the same zip,
with the sha256 recorded in `datasets.yml`.

The zip is on CESNET FileSender. `url` in `datasets.yml` is the direct
`download.php?token=…&files_ids=…` link, which needs no click. The share link above
is the fallback. FileSender transfers expire: if the zip moves, change `url`, the
`note` in `datasets.yml` and the share link above. After the school it belongs on
Zenodo.
