# Artefact photographs

**Tuesday** · instructor: TBC

Classification and detection of artefact types from photographs.

## Hands-on: annotate in CVAT

Everything the annotation exercise needs is in this folder. Clone or pull the
repository and you are ready — no Python needed for this part.

| | |
|---|---|
| `images/` | ten photographs of metal-detector finds from AMČR-PAS, numbered `01`–`10` |
| `labels.json` | the label set for CVAT: twelve artefact classes with their questions, and a tag for the whole photo |
| `credits.csv` | where each photograph comes from: its file name and the DOI of its AMČR record |

Everyone annotates the same ten photographs, each in their own CVAT project.

### Set up your project (about 5 minutes)

1. Open **CVAT** at the address on the board and **Create an account**.
2. **Projects → + → Create a new project**. Give it a name, open the **Raw** tab,
   replace everything in it with the contents of `labels.json`, then **Done** and
   **Submit & Open**. The Raw tab must contain only `labels.json` — one `[` at the
   start, one `]` at the end.
3. In the project: **+ → Create a new task**. Give it a name, add all ten files from
   `images/` under **Select files**, then **Submit & Open**.
4. Click the **job** in the task. That opens the first photograph.

### Annotate (16 minutes)

For every artefact in a photograph:

1. Outline it — with **SAM 2** (AI Tools → Interactors), a polygon or a box, your
   choice — and give it a **class**.
2. In the objects list, answer its two questions:
   - **fragment** — is it a piece of an object, not a whole one?
   - **damage** — none, minor or major?

Then, once for the whole photograph: **Setup tag → photo**, and answer **scale** —
is there a scale bar in the frame?

Every question starts at `?`, which means *not answered yet*. `unknown` means you
looked and cannot tell. Not sure what something is? Annotate it anyway and write why
in **note**. Save with **Ctrl+S** before moving to the next photograph.

Do not compare with your neighbour. We will talk about what you decided, and why.

### The classes

fibula · clothing pin · buckle · spur · mount · pendant · coin · token · circle/ring ·
finger ring · amorphous fragment/object · other / not sure

The question keys and values follow the ArchaeoTag image-tagging schema.

### Credits

The photographs come from [AMČR-PAS](https://amcr-info.aiscr.cz), the portal of the
Archaeological Information System of the Czech Republic, and are published under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). The copies here are
downscaled to 1600 px on the long side. `credits.csv` gives the record DOI for each:
`04_M202101534N00375F02.jpg` is photograph `F02` of record
[M-202101534-N00375](https://doi.org/10.71928/M-202101534-N00375).

## Data

| | |
|---|---|
| Access | `public` |
| Licence | TBC |
| Source | `repo` (see [`../datasets.yml`](../datasets.yml)) |

Get it from a notebook — never by hand, and never by committing it here:

```python
from atrium_data import get_dataset
path = get_dataset("artefacts")
```

If the dataset moves, gains a DOI, or changes size, edit its entry in
`../datasets.yml`. No notebook needs to change.

To train a model, use the larger annotated dataset in
[`../2-tuesday-artefacts-coco/`](../2-tuesday-artefacts-coco/): 1500 AMČR-PAS
photographs in ten classes, in COCO format (`get_dataset("artefacts-coco")`).

## Notebooks

_To be added._
