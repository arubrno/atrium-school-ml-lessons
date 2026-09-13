"""Plot every find in data/finds.csv on a map.

    python scripts/plot_finds.py

Writes map.png if matplotlib is available, and map.svg if it is not — so it
runs whether or not you have the project environment activated.

At the moment the map comes out empty, and working out why is the first
exercise of the session.
"""

import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FINDS = HERE.parent / "data" / "finds.csv"

# The whole world, so that nothing can fall off the edge.
XMIN, XMAX = -180, 180
YMIN, YMAX = -90, 90


def load(path):
    """Read the finds. Rows without coordinates are skipped, and counted."""
    lon, lat, datum = [], [], []
    skipped = 0
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not row["x_jtsk"] or not row["y_jtsk"]:
                skipped += 1
                continue
            lon.append(float(row["x_jtsk"]))
            lat.append(float(row["y_jtsk"]))
            datum.append(int(row["datum"]))
    return lon, lat, datum, skipped


def draw_png(lon, lat, datum, out):
    """The nice version. Needs matplotlib."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(lon, lat, c=datum, cmap="viridis", s=28,
               edgecolor="white", linewidth=.4)
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.set_title("Finds by year")
    ax.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(out, dpi=150)


def draw_svg(lon, lat, datum, out):
    """The plain version, in case matplotlib is not installed.

    Same axes, same result — an SVG is just text, so this needs nothing at
    all beyond Python itself.
    """
    W, H, PAD = 1000, 700, 60

    def px(x):
        return PAD + (x - XMIN) / (XMAX - XMIN) * (W - 2 * PAD)

    def py(y):
        return H - PAD - (y - YMIN) / (YMAX - YMIN) * (H - 2 * PAD)

    lo, hi = min(datum), max(datum)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="white"/>',
        f'<rect x="{PAD}" y="{PAD}" width="{W - 2 * PAD}" height="{H - 2 * PAD}" '
        f'fill="none" stroke="#ccc"/>',
        f'<text x="{PAD}" y="{PAD - 22}" font-family="sans-serif" font-size="20">'
        f'Finds by year</text>',
        f'<text x="{W / 2}" y="{H - 18}" font-family="sans-serif" font-size="14" '
        f'text-anchor="middle" fill="#666">longitude</text>',
    ]
    for x, y, d in zip(lon, lat, datum):
        shade = int(40 + 180 * (d - lo) / max(1, hi - lo))
        parts.append(
            f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="5" '
            f'fill="rgb({shade},{200 - shade // 2},120)" stroke="white"/>'
        )
    parts.append("</svg>")
    out.write_text("\n".join(parts), encoding="utf-8")


def main():
    lon, lat, datum, skipped = load(FINDS)
    print(f"{len(lon)} finds with coordinates, {skipped} without")

    try:
        out = HERE.parent / "map.png"
        draw_png(lon, lat, datum, out)
    except ImportError:
        out = HERE.parent / "map.svg"
        print("matplotlib is not installed — writing an SVG instead")
        draw_svg(lon, lat, datum, out)

    print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
