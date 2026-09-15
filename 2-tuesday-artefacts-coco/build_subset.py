"""Build the artefacts-coco training dataset: a 10-class subset of the AMČR-PAS COCO export.

Run from the repository root:  python3 2-tuesday-artefacts-coco/build_subset.py [--out DIR]

Reads the AMČR-PAS COCO export and its photographs from the FiftyOne copy of the dataset
(FIFTYONE_ROOT, default ~/Documents/fiftyone), and writes to --out (default temp/):

  artefacts-coco/                  the dataset folder, as participants will see it
    images/                        the photographs, 640 px on the long side
    annotations.json               COCO boxes and polygons, rescaled to the copies
    credits.csv                    each photograph's AMČR record and DOI
    README.md                      what is in it, and the licence
  artefacts-coco.zip               that folder, zipped, for upload
  artefacts-coco-contact-sheet.jpg six photographs per class with their polygons, to check by eye

It also rewrites 2-tuesday-artefacts-coco/credits.csv (committed). The photographs are
CC BY-NC 4.0 and are never committed; datasets.yml points at the uploaded zip.

The selection is deterministic (fixed seed, fixed zip timestamps), so rebuilding gives
the same zip and the same sha256.
"""

import argparse
import csv
import hashlib
import json
import os
import random
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None

FIFTYONE = Path(os.environ.get("FIFTYONE_ROOT", Path.home() / "Documents/fiftyone"))
COCO = FIFTYONE / "datasets/amcr-pas/amcr-pas_v0.filtered.json"
HERE = Path(__file__).resolve().parent
EXERCISE = HERE.parent / "2-tuesday-artefacts/credits.csv"
NAME = "artefacts-coco"

# The ten largest classes by number of photographs, leaving out the catch-alls
# (adornment, metal sheet, amorphous fragment/object, exceptional object), which say
# more about the recorder than about the object. potsherd has more boxes than buckle
# but only 109 photographs, too few for the per-class target.
CLASSES = [
    "fibula", "coin", "arrow/arrowhead", "mount", "pendant",
    "clothing pin", "circle/ring", "bracelet", "sickle", "buckle",
]
PER_CLASS = 150   # photographs showing each class
LONG_EDGE = 640   # the usual detector input size; smaller photographs are left out
SEED = 2026
ROSARY = "M202400071N00083F01"  # the live-demo photograph of the annotation session
ZIP_DATE = (2026, 9, 15, 0, 0, 0)


def record_id(stem):
    """M202400071N00083F01 -> M-202400071-N00083 (the AMČR record; F01 is the file)."""
    m = re.fullmatch(r"([A-Z])(\d{9})(N\d{5})F\d{2}", stem)
    return f"{m[1]}-{m[2]}-{m[3]}" if m else ""


def exercise_stems():
    """The hands-on photographs, kept out so nobody trains on what they annotated."""
    with EXERCISE.open() as f:
        return {Path(r["filename"]).stem.split("_", 1)[1] for r in csv.DictReader(f)} | {ROSARY}


def select(coco, cat_ids):
    """Pick about PER_CLASS photographs per class, one photograph per record first."""
    anns = defaultdict(list)
    for a in coco["annotations"]:
        anns[a["image_id"]].append(a)
    skip = exercise_stems()
    wanted = set(cat_ids.values())
    eligible = [
        i for i in coco["images"]
        if anns[i["id"]]
        and {a["category_id"] for a in anns[i["id"]]} <= wanted   # no unlabelled objects
        and max(i["width"], i["height"]) >= LONG_EDGE
        and Path(i["file_name"]).stem not in skip
    ]
    rng = random.Random(SEED)
    rng.shuffle(eligible)
    # Records often hold two or three views of one find (F01, F02...). Take the first
    # view of every record before any second view, so the classes show many finds.
    seen = Counter()
    rank = {}
    for i in eligible:
        r = record_id(Path(i["file_name"]).stem) or i["file_name"]
        rank[i["id"]] = seen[r]
        seen[r] += 1
    eligible.sort(key=lambda i: rank[i["id"]])

    chosen = {}
    # Smallest classes first, so photographs with two classes count towards the rare one.
    by_size = Counter(a["category_id"] for i in eligible for a in anns[i["id"]])
    for cid in sorted(wanted, key=lambda c: by_size[c]):
        have = sum(any(a["category_id"] == cid for a in anns[k]) for k in chosen)
        for i in eligible:
            if have >= PER_CLASS:
                break
            if i["id"] not in chosen and any(a["category_id"] == cid for a in anns[i["id"]]):
                chosen[i["id"]] = i
                have += 1
    return sorted(chosen.values(), key=lambda i: Path(i["file_name"]).stem), anns


def downscale(src, dst, size):
    im = ImageOps.exif_transpose(Image.open(src))
    if im.size != size:
        return None  # the annotations were drawn on a different orientation; skip it
    s = LONG_EDGE / max(im.size)
    im = im.convert("RGB").resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im.save(dst, quality=88, optimize=True)
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=Path("temp"))
    args = ap.parse_args()

    coco = json.loads(COCO.read_text())
    by_name = {c["name"]: c["id"] for c in coco["categories"]}
    cat_ids = {name: by_name[name] for name in CLASSES}
    new_id = {old: n for n, old in enumerate(cat_ids.values(), 1)}

    picked, anns = select(coco, cat_ids)
    root = args.out / NAME
    (root / "images").mkdir(parents=True, exist_ok=True)
    for old in (root / "images").glob("*.jpg"):
        old.unlink()

    images, annotations, credits, sheet = [], [], [], defaultdict(list)
    for img in picked:
        stem = Path(img["file_name"]).stem
        name = f"{stem}.jpg"
        im = downscale(FIFTYONE / img["file_name"], root / "images" / name, (img["width"], img["height"]))
        if im is None:
            print(f"  skipped {stem}: image size does not match its annotations")
            continue
        sx, sy = im.width / img["width"], im.height / img["height"]
        rid = record_id(stem)
        doi = f"https://doi.org/10.71928/{rid}" if rid else ""
        iid = len(images) + 1
        images.append({"id": iid, "file_name": name, "width": im.width, "height": im.height,
                       "license": 1, "record": rid, "doi": doi})
        own = anns[img["id"]]
        for a in own:
            x, y, w, h = a["bbox"]
            annotations.append({
                "id": len(annotations) + 1, "image_id": iid,
                "category_id": new_id[a["category_id"]],
                "bbox": [round(x * sx, 2), round(y * sy, 2), round(w * sx, 2), round(h * sy, 2)],
                "segmentation": [[round(v * (sx if k % 2 == 0 else sy), 2) for k, v in enumerate(poly)]
                                 for poly in a["segmentation"]],
                "area": round(a["area"] * sx * sy, 2),
                "iscrowd": 0,
                # occluded is left out: it was CVAT's unticked default, false on every box.
                "attributes": {"recognizable": a["attributes"]["recognizable"] == "true"},
            })
        classes = sorted({CLASSES[new_id[a["category_id"]] - 1] for a in own})
        credits.append({"file_name": name, "classes": "; ".join(classes), "record": rid, "doi": doi})
        for c in classes:
            sheet[c].append((im, annotations[-len(own):]))

    categories = [{"id": n, "name": c, "supercategory": "artefact"} for n, c in enumerate(CLASSES, 1)]
    (root / "annotations.json").write_text(json.dumps({
        "info": {
            "description": "AMČR-PAS metal-detector finds: a 10-class subset for the ATRIUM "
                           "Training School, Brno 2026. Photographs downscaled to 640 px.",
            "version": "1.0", "year": 2026, "date_created": "2026-09-15",
            "contributor": "AMČR-PAS (Archaeological Information System of the Czech Republic)",
            "url": "https://amcr-info.aiscr.cz",
        },
        "licenses": [{"id": 1, "name": "CC BY-NC 4.0",
                      "url": "https://creativecommons.org/licenses/by-nc/4.0/"}],
        "images": images,
        "categories": categories,
        "annotations": annotations,
    }, ensure_ascii=False), encoding="utf-8")

    for dst in (root / "credits.csv", HERE / "credits.csv"):
        with dst.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=credits[0].keys())
            w.writeheader()
            w.writerows(credits)

    counts = [(c["name"], sum(1 for r in credits if c["name"] in r["classes"].split("; ")),
               sum(1 for a in annotations if a["category_id"] == c["id"])) for c in categories]
    (root / "README.md").write_text(readme(counts, len(images), len(annotations)), encoding="utf-8")

    zpath = args.out / f"{NAME}.zip"
    with zipfile.ZipFile(zpath, "w") as z:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(f"{NAME}/{p.relative_to(root).as_posix()}", ZIP_DATE)
                # JPEGs are compressed already; deflating them again only costs time.
                info.compress_type = zipfile.ZIP_STORED if p.suffix == ".jpg" else zipfile.ZIP_DEFLATED
                z.writestr(info, p.read_bytes())

    contact_sheet(sheet, args.out / f"{NAME}-contact-sheet.jpg")

    print(f"{'class':<18}{'photos':>8}{'boxes':>8}")
    for name, n_img, n_ann in counts:
        print(f"{name:<18}{n_img:>8}{n_ann:>8}")
    print(f"{'total':<18}{len(images):>8}{len(annotations):>8}")
    print(f"\n{zpath}  {zpath.stat().st_size / 1e6:.1f} MB")
    print(f"sha256: {hashlib.sha256(zpath.read_bytes()).hexdigest()}")


def readme(counts, n_images, n_anns):
    rows = "\n".join(f"| {n} | {i} | {a} |" for n, i, a in counts)
    return f"""# artefacts-coco

Photographs of metal-detector finds from [AMČR-PAS](https://amcr-info.aiscr.cz), the
portal of the Archaeological Information System of the Czech Republic, with the object
outlines drawn by the people who recorded them. A 10-class subset prepared for the
ATRIUM Training School *Computer Vision in Archaeology*, Brno, September 2026.

- `images/`: {n_images} photographs, downscaled to 640 px on the long side
- `annotations.json`: COCO format, {n_anns} objects, each with a box (`bbox`) and an
  outline (`segmentation`, polygons). `attributes.recognizable` is `false` where the
  recorder could not tell what the object was.
- `credits.csv`: the AMČR record and DOI of every photograph

| class | photographs | objects |
|---|---|---|
{rows}

A photograph can hold several objects. Often they are one find seen twice, front and
back side by side, and each view has its own box. Only photographs in which every
recorded object belongs to one of the ten classes are included, so no object in a
photograph is left without a label. There are no train/validation splits: make your own.

## Licence

The photographs and annotations are published under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Credit the AMČR record
of each photograph you show: `credits.csv` gives its DOI, e.g.
`https://doi.org/10.71928/M-202400098-N00219`. Not for commercial use.
"""


def contact_sheet(sheet, dst, per=6, tw=200):
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    img = Image.new("RGB", (130 + per * tw, len(CLASSES) * tw), "white")
    d = ImageDraw.Draw(img)
    for r, c in enumerate(CLASSES):
        d.text((6, r * tw + tw // 2), c, fill="black", font=font)
        for k, (im, anns) in enumerate(sheet[c][:per]):
            t = tw / max(im.size)
            x, y = 130 + k * tw, r * tw
            img.paste(im.resize((round(im.width * t), round(im.height * t))), (x, y))
            for a in anns:
                for poly in a["segmentation"]:
                    d.polygon([(x + poly[j] * t, y + poly[j + 1] * t) for j in range(0, len(poly), 2)],
                              outline=(220, 38, 38))
                bx, by, bw, bh = a["bbox"]
                d.rectangle([x + bx * t, y + by * t, x + (bx + bw) * t, y + (by + bh) * t],
                            outline=(37, 99, 235))
    img.save(dst, quality=85)


if __name__ == "__main__":
    main()
