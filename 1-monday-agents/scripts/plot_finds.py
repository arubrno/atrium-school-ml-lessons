"""Plot every find in data/finds.csv on a map.

Run it:  python scripts/plot_finds.py

It writes map.png next to itself. At the moment the map comes out empty,
and working out why is the first exercise of the session.
"""

import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
FINDS = HERE.parent / "data" / "finds.csv"
OUT = HERE.parent / "map.png"


def load(path):
    """Read the finds. Rows without coordinates are skipped."""
    lon, lat, datum = [], [], []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not row["x_jtsk"] or not row["y_jtsk"]:
                continue
            lon.append(float(row["x_jtsk"]))
            lat.append(float(row["y_jtsk"]))
            datum.append(int(row["datum"]))
    return lon, lat, datum


def main():
    lon, lat, datum = load(FINDS)
    print(f"{len(lon)} finds with coordinates")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(lon, lat, c=datum, cmap="viridis", s=28, edgecolor="white", linewidth=.4)

    # the whole world, so nothing can fall off the edge
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.set_title("Finds by year")
    ax.grid(alpha=.25)

    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
