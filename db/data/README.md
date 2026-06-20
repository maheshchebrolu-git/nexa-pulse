# Road data

`seed.py` snaps drivers onto real SF streets using TIGER/Line road data from
the US Census Bureau. Not committed here since it's just downloadable public
data — grab it yourself before running the seed script.

## Get it

1. https://www.census.gov/cgi-bin/geo/shapefiles/index.php
2. Layer type: Roads → All Roads → California → San Francisco County
3. Download the zip (looks like `tl_2025_06075_roads.zip`)

## Put it here

Unzip into `db/data/tiger_sf_roads/` so you end up with:

```
db/data/tiger_sf_roads/tl_2025_06075_roads.shp
db/data/tiger_sf_roads/tl_2025_06075_roads.shx
db/data/tiger_sf_roads/tl_2025_06075_roads.dbf
db/data/tiger_sf_roads/tl_2025_06075_roads.prj
...plus a few other companion files, keep them all together
```

If you download a different year, update `ROADS_PATH` in `seed.py` to match.

## Why not OSMnx

Tried OSM/Overpass first but it kept timing out, and the browser export caps
out at 50k nodes which isn't enough for a whole city. TIGER/Line is a flat
file, no API, no limits — way more reliable.

One gotcha: it comes in EPSG:4269, not 4326. `seed.py` reprojects it
automatically, don't skip that step or your coordinates will be slightly off.
