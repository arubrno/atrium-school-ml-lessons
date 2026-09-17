# Satellite imagery: cropmarks in Sentinel-2

**Thursday** · instructor: Filip Hájek

Buried ditches and walls change how crops grow above them, and those differences
can be seen from space. This session uses Sentinel-2 multispectral imagery of the
Bronze Age fortification at Cornești-Iarcuri (Romania), taken on 7 April 2026, to
find its cropmark. You will:

- learn what spectral bands, spectral signatures and NDVI are;
- read georeferenced rasters with rasterio and make true- and false-colour composites;
- bring out the cropmark with local background removal and a Frangi ridge filter;
- train a Random Forest on hand-placed points, then retrain it with
  *hard negatives*, the false positives of the first model;
- turn the result into polygons and export them for GIS.

## Notebooks

- [`cropmarks.ipynb`](cropmarks.ipynb): the hands-on notebook. Code cells are
  empty, and you fill them in with the instructor.
- [`cropmarks_filled.ipynb`](cropmarks_filled.ipynb): the same notebook with
  every cell filled in, for catching up or checking your version.

Both write their results (a GeoTIFF and a zipped shapefile) to an `outputs/`
folder next to the notebook.

## Data

| | |
|---|---|
| Access | `public` |
| Licence | TBC: Copernicus Sentinel-2 data and the instructor's own annotations, see [`data/CREDITS.md`](data/CREDITS.md) |
| Source | `repo` ([`data/`](data/)), see [`../datasets.yml`](../datasets.yml) |

```python
from atrium_data import get_dataset
path = get_dataset("satellite")
```

| | |
|---|---|
| `sentinel2/` | Sentinel-2 L2A bands B2, B3, B4 and B8 (10 m), GeoTIFF |
| `training_samples/` | `cropmark.shp` and `non_cropmark.shp`, training points |
| `round2/` | `hard_negatives_all.shp`, false positives of the first model |
| `gis/` | `cropmark_cleaned_final.shp`, candidate polygons after review in GIS |
