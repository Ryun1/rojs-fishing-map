# Island map

The coastlines drawn at the top of the page (`<svg id="map">` in `index.html`) come from the OpenStreetMap island polygons of Pico (relation 4822056), Faial (7393727) and São Jorge (7357093), fetched on 2026-11-22 through Nominatim with `polygon_geojson=1&polygon_threshold=0.0006`.

Each point was projected as

    x = (lon + 28.68) * cos(38.5°) * 1000
    y = (38.70 - lat) * 1000

then simplified (Douglas-Peucker, 0.45 units, about 45 m) and rounded to 0.1. `mapXY()` in `index.html` uses the same projection to place the spot markers, so a new spot only needs its latitude and longitude in `data/spots.json` (plus a `label` offset if its name would overlap another).

Map data © OpenStreetMap contributors, ODbL. The credit is shown under the map.
