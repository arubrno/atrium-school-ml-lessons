#!/usr/bin/env python3
"""Check the notebooks of this repository before they are committed or taught from.

    python3 .agents/skills/notebook-hygiene/scripts/nb_check.py [path ...]

With no arguments, checks every .ipynb tracked in the repository (ignoring
.ipynb_checkpoints). Prints one line per problem and exits non-zero if there
was any. --fix clears outputs and execution counts in place; everything else
has to be fixed by hand.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
BADGE_PREFIX = (
    "https://colab.research.google.com/github/arubrno/"
    "atrium-school-ml-lessons/blob/main/"
)
BOOTSTRAP_MARKER = "from atrium_bootstrap import setup"
GPU_MARKERS = (".cuda(", 'device="cuda"', "device='cuda'", "cuda:0")


def notebooks(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(p) for p in paths]
    return sorted(
        p
        for p in REPO_ROOT.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in p.parts and ".venv" not in p.parts
    )


def check(path: Path, fix: bool) -> list[str]:
    problems: list[str] = []
    try:
        nb = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read as a notebook: {exc}"]

    cells = nb.get("cells", [])
    code = [c for c in cells if c.get("cell_type") == "code"]
    source = "\n".join("".join(c.get("source", [])) for c in cells)

    dirty = [
        i
        for i, c in enumerate(code)
        if c.get("outputs") or c.get("execution_count") is not None
    ]
    if dirty and fix:
        for c in code:
            c["outputs"] = []
            c["execution_count"] = None
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
        print(f"{path}: cleared outputs in {len(dirty)} cell(s)")
    elif dirty:
        problems.append(
            f"{len(dirty)} code cell(s) still carry outputs or an execution count"
            " — clear them before committing (re-run with --fix)"
        )

    if not code:
        problems.append("no code cells")
    elif BOOTSTRAP_MARKER not in "".join(code[0].get("source", [])):
        problems.append(
            "the first code cell is not the ATRIUM bootstrap cell — copy it"
            " verbatim from 1-monday-intro/clip_zero_shot.ipynb"
        )

    if "get_dataset(" not in source and "demo-images" not in source:
        problems.append(
            "no get_dataset(...) call — data paths belong in datasets.yml,"
            " not in a notebook"
        )

    for marker in GPU_MARKERS:
        if marker in source:
            problems.append(f"assumes a GPU ({marker}) — everything runs on CPU")

    badges = [line for line in source.splitlines() if BADGE_PREFIX in line]
    try:
        rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        rel = None
    if badges and rel and not any(BADGE_PREFIX + rel in b for b in badges):
        problems.append(f"the Colab badge URL does not point at {rel}")
    if not badges:
        problems.append(
            "no Colab badge — add one unless this notebook uses a restricted"
            " dataset (satellite, rock-art)"
        )

    meta = nb.get("metadata", {})
    if meta.get("kernelspec", {}).get("name") != "python3":
        problems.append('metadata.kernelspec.name should be "python3"')

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument(
        "--fix", action="store_true", help="clear outputs and execution counts in place"
    )
    args = parser.parse_args()

    failed = 0
    for path in notebooks(args.paths):
        problems = check(path, args.fix)
        for problem in problems:
            print(f"{path}: {problem}")
        failed += bool(problems)

    if failed:
        print(f"\n{failed} notebook(s) need attention.")
        return 1
    print("All notebooks look fine.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
