"""Ask CLIP which of your labels best fits a photograph.

The same model, and the same pinned weights, as Monday morning's notebook —
so an answer here and an answer there are the same answer.

    python scripts/clip_classify.py --image photo.jpg \
        --labels "a bronze brooch,a ceramic sherd,a stone tool"

Prints a table for a human and one line of JSON for a program. Runs on CPU.
"""

import argparse
import json
import sys

MODEL_ID = "openai/clip-vit-base-patch32"
# Safetensors conversion of the same weights — see 1-monday-intro for why.
WEIGHTS = "c237dc49a33fc61debc9276459120b7eac67e7ef"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--image", required=True, help="path to the photograph")
    ap.add_argument("--labels", required=True,
                    help="comma-separated candidate labels")
    ap.add_argument("--json", action="store_true", help="print only the JSON line")
    args = ap.parse_args()

    labels = [s.strip() for s in args.labels.split(",") if s.strip()]
    if len(labels) < 2:
        sys.exit("give at least two labels — CLIP compares them against each other")

    try:
        import torch
        from PIL import Image
        from transformers import CLIPModel, CLIPProcessor
    except ImportError as exc:
        sys.exit(
            f"missing package: {exc.name}\n"
            "\nThis script needs the project environment. From the repository root:\n"
            "    python -m venv .venv\n"
            "    .venv/bin/pip install -r requirements.txt\n"
            "\nthen run it with that interpreter:\n"
            "    ../.venv/bin/python scripts/clip_classify.py --image ... --labels ...\n"
            "\nplot_finds.py needs none of this and runs with any Python."
        )

    try:
        image = Image.open(args.image).convert("RGB")
    except OSError as exc:
        sys.exit(f"cannot open the image: {exc}")

    model = CLIPModel.from_pretrained(
        MODEL_ID, revision=WEIGHTS, use_safetensors=True).eval()
    processor = CLIPProcessor.from_pretrained(MODEL_ID)

    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        probs = model(**inputs).logits_per_image.softmax(dim=1)[0].tolist()

    ranked = sorted(zip(labels, probs), key=lambda p: -p[1])
    payload = {
        "image": args.image,
        "labels": labels,
        "scores": {lab: round(p, 4) for lab, p in ranked},
        "best": ranked[0][0],
        "margin": round(ranked[0][1] - ranked[1][1], 4),
    }

    if not args.json:
        width = max(len(lab) for lab in labels)
        for lab, p in ranked:
            bar = "█" * round(p * 30)
            print(f"  {lab:<{width}}  {p:6.1%}  {bar}")
        print()
        print("  These add up to 100% across YOUR labels and nothing else.")
        print("  There is no “none of the above”, and rewording a label")
        print("  changes the answer. Read the margin, not just the winner.")
        print()

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
