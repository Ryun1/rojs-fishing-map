# Data sources for nearshore fishing conditions around Pico (Azores)

Research notes, probed 2026-11-22 (about 20:00 to 21:30 UTC) with `curl`, generic user agent
`Mozilla/5.0 (research-probe)` and `Origin: https://example.org` to read CORS headers.
No keys were used anywhere. Nothing in the project was changed.

Test points: Madalena 38.535, -28.53 (west coast, Faial-Pico channel) and Lajes do Pico 38.385, -28.26
(south coast). Seven more coastal points were used for the grid-cell test (section 2).

Legend: **CORS** = value of `Access-Control-Allow-Origin` actually returned. "Verified" = I called it and
saw the response. "Not verified" = taken from documentation, a web search, or memory.

---

## 1. Summary table

| Source | Key? | CORS header seen | Usable from a keyless static page? | What it gives | Resolution near Pico | Horizon / history | Licence / terms |
|---|---|---|---|---|---|---|---|
| Open-Meteo Forecast `api.open-meteo.com/v1/forecast` | No | `*` | **Yes** | wind, gusts, pressure, cloud, rain, air temp, visibility, sunrise/sunset | ECMWF IFS 9 km by default; 4 land cells or 6 sea cells cover the island | 16 days hourly, `past_days` up to 92 | CC BY 4.0, non-commercial free tier 600/min, 5 000/h, 10 000/day per IP |
| Open-Meteo Marine `marine-api.open-meteo.com/v1/marine` | No | `*` | **Yes** | total sea, wind sea, swell 1, swell 2 (swell 3 with GFS), SST, currents, sea level | MFWAM and SMOC 1/12 deg (about 8 km); 7 distinct cells for 9 coastal points | 10 days (MFWAM), 16 days (GFS wave); history: waves from Oct 2021, SST and sea level from Nov 2022 | same |
| Open-Meteo Archive `archive-api.open-meteo.com/v1/archive` | No | `*` | **Yes** | ERA5 / IFS weather history | ERA5 0.25 deg: the nine coastal points fall in three cells, all on latitude 38.5, so north and south coasts share cells; IFS 9 km | 1940 to now; **no SST, no waves** (null) | same |
| Open-Meteo Climate `climate-api.open-meteo.com/v1/climate` | No | `*` | Yes but not useful | CMIP6 daily air temp, wind, rain | 0.5 deg cell | 1950 to 2050; **no ocean variables** | same |
| IPMA open data `api.ipma.pt/open-data/...` | No | `*` | **Yes** | hourly station obs (Pico airfield, Horta), 3-day sea-state forecast for "Horta, costa", colour warnings, 5-day city forecast | stations; one sea point for the central group | obs last 24 h; forecasts 3 to 5 days | free, must cite IPMA, non-profit use, IPMA asks for an email to webmaster@ipma.pt; rate limit undocumented |
| Instituto Hidrografico tide table PDF (Loja do Navegante) | No | n/a (PDF, no CORS header) | **Pre-bake only** | official HW/LW for Horta, secondary-port corrections for Madalena, Lajes, Cais do Pico, Santo Antonio | port | 2027 volume is published (5 Nov 2026) | CC BY-NC-ND 4.0 |
| Instituto Hidrografico API `supportserver1.hidrografico.pt/geodata/...` | **Yes** (`x-api-key`) | none on the 401 | **No** | tides by port/location, buoys | | | key-gated; do not use |
| TICON-4 harmonic constants (via `openwatersio/slackwater-database` on GitHub) | No | `*` (raw.githubusercontent.com) | **Yes, or embed** | 50 constituents for Horta | port (Horta gauge, UHSLC 212a) | any year | CC BY 4.0 |
| Open Waters / Slackwater API `api.openwaters.io/tides` | No | `*` | **Yes** | HW/LW and timeline computed from TICON-4 Horta | port | any date | code MIT, data CC BY 4.0; beta; rate limit undocumented; `cache-control: max-age=3600` |
| Copernicus Marine WMTS `wmts.marine.copernicus.eu/teroWmts` (GetFeatureInfo) | No | `*` | **Yes** (point values as JSON) | chlorophyll, Secchi depth, KD490, OSTIA SST, model SST, currents, waves, monthly SST climatology | CHL 4 km and 1 km; SST 0.05 deg; model 1/12 deg | NRT ocean colour keeps about 8 days; models to +10 days; SST reprocessed back to 1981 | free, credit "Generated using E.U. Copernicus Marine Service Information" plus DOI; rate limit undocumented |
| Copernicus Marine data download (toolbox / STAC / S3) | Yes (account) | n/a | **No** (pre-bake from a script at best) | full grids | | | same |
| NOAA NCEI ERDDAP `www.ncei.noaa.gov/erddap` | No | `*` | **Yes** | OISST v2.1 daily `sst` and `anom` | 0.25 deg (6 cells cover the island area) | 2020-02-28 to now; final lags about 16 days, prelim about 4 days | free NOAA data |
| NOAA CoastWatch ERDDAP `coastwatch.pfeg.noaa.gov/erddap`, `coastwatch.noaa.gov/erddap`, `polarwatch.noaa.gov/erddap` | No | **none** | **No (blocked by CORS)**; fine for pre-baking with curl | OISST 1981 to now, MUR SST 1 km, blended SST, chlorophyll | 0.25 deg, 0.01 deg | 1981 / 2002 to now | free NOAA data |
| EMODnet Bathymetry REST `rest.emodnet-bathymetry.eu` | No | echoes the Origin | **Yes** (or pre-bake, depths do not change) | depth at a point, depth profile along a line | 1/16 arc-minute (about 115 m) | static | EMODnet open data (credit EMODnet Bathymetry Consortium); terms not re-read here |
| EMODnet Bathymetry WMS `ows.emodnet-bathymetry.eu/wms` | No | `*` | Yes | same depth through GetFeatureInfo, map tiles | same | static | same |
| EMODnet Physics ERDDAP `platform-erddap.emodnet-physics.eu` (redirects to `er3webapps.emodnet-physics.eu`) | No | `*` | **Yes** | CLIMAAT / Univ. Azores wave buoys: Graciosa (lagging about 16 days), Faial-Pico (archive 2012 to 2021 only) | point | 10-minute records | "Creative Commons Attribution Share-Alike" in dataset metadata |
| IOC Sea Level Station Monitoring `ioc-sealevelmonitoring.org/service.php` | No | `*` | **Yes** | 1-minute tide gauge, Ponta Delgada only (`pdas`); no Horta gauge | 250 km away | live | free, cite IOC/VLIZ |
| met.no Locationforecast 2.0 | No (identify via Origin) | `*` | Yes (low volume) | global forecast (ECMWF outside the Nordics) | about 9 km | 9 to 10 days | CC BY 4.0; ToS: under 20 req/s, respect `Expires`, max 4 decimals in coordinates |
| met.no Oceanforecast 2.0 | No | n/a | **No coverage** (HTTP 422 "only available for Northern/Western Europe") | | | | |
| met.no Sunrise 3.0 (`/sunrise/3.0/moon`, `/sun`) | No | `*` | Yes | moonrise, moonset, moon phase, sun | exact | any date | CC BY 4.0 |
| NASA GIBS WMS/WMTS `gibs.earthdata.nasa.gov` | No | `*` | Yes, **imagery only** | MUR SST and chlorophyll pictures | 1 km | daily | free NASA data |
| Stormglass `api.stormglass.io` | **Yes** | echoes Origin | No (key would be public) | multi-model marine point data | model-dependent | 10 days | free plan 10 requests/day, non-commercial (not verified by calling) |
| WorldTides `worldtides.info/api/v3` | **Yes** | `*` | No | tide predictions | | | paid credits (not verified) |
| Windy Point Forecast API | **Yes** | echoes Origin | No | GFS/ECMWF point forecast | | | trial key returns deliberately altered data (not verified by calling) |
| Windguru `windguru.cz/int/iapi.php` | **Yes** (401 "Unauthorized!") | `*` | No | no public forecast API | | | |
| SpotAzores webcams `spotazores.com` | No | n/a | Link out only | live cams: Porto da Madalena, Lajes do Pico, Porto de Sao Roque, Montanha do Pico | | | third-party site, not an API |

---

## 2. Open-Meteo in detail

### 2.1 Headers (verified)

```
GET https://api.open-meteo.com/v1/forecast?latitude=38.535&longitude=-28.53&current=temperature_2m
HTTP/1.1 200 OK
X-RateLimit-Limit: 600.0
X-RateLimit-Remaining: 569.4286
X-RateLimit-Window: 60
access-control-allow-origin: *
access-control-expose-headers: x-ratelimit-cost, x-ratelimit-limit, x-ratelimit-remaining, x-ratelimit-reset, x-ratelimit-window, retry-after
```

`marine-api.open-meteo.com` returns `access-control-allow-origin: *` too, as does `archive-api.open-meteo.com`.
Terms page (fetched): "Less than 10'000 API calls per day, 5'000 per hour and 600 per minute", per IP;
data under CC BY 4.0; free tier is for non-commercial use (a personal app with no ads or subscriptions fits).
Requests with several coordinates or many variables cost more than 1 call (`X-RateLimit-Cost`).

### 2.2 Marine API: variables and which model fills them at Pico (verified by calling each model)

Request used:
`https://marine-api.open-meteo.com/v1/marine?latitude=38.56&longitude=-28.53&hourly=<all>&forecast_days=16&models=<m>`

| `models=` | Grid it snapped to | Native grid (docs) | Variables that came back non-null | Hours of forecast |
|---|---|---|---|---|
| `best_match` (default) | 38.542, -28.542 | mix of the two below | `wave_height/direction/period`, `wind_wave_height/direction/period`, `swell_wave_height/direction/period`, `secondary_swell_wave_height/period/direction`, `sea_level_height_msl`, `sea_surface_temperature`, `ocean_current_velocity/direction`, `invert_barometer_height` | 240 (SST 246) |
| `meteofrance_wave` (MFWAM) | 38.542, -28.542 | 0.08 deg, 3-hourly, 10 days, 2 runs/day | total sea, wind sea, swell 1, swell 2 | 240 |
| `meteofrance_currents` (SMOC + SST) | 38.542, -28.542 | 0.08 deg, hourly (SST 6-hourly), 10 days, 1 run/day | sea level, SST, currents, inverse barometer | 240 |
| `ecmwf_wam` | 38.559, -28.492 | 9 km, hourly, 15 days | `wave_height/direction/period`, `wave_peak_period` only (no swell split) | 373 |
| `ecmwf_wam025` | 38.75, -28.5 | 0.25 deg | same as above | 372 |
| `ncep_gfswave025` | 38.75, -28.5 | 0.25 deg, hourly, 16 days | total, wind sea, swell 1, swell 2, **swell 3** | 384 |
| `ncep_gfswave016` | 38.667, -28.5 | 0.16 deg, hourly, 16 days | total, wind sea, swell 1, swell 2, **swell 3** | 384 |
| `gwam` (DWD) | 38.5, -28.5 | 0.25 deg, 174 h | total, wind sea, swell 1, plus `wind_wave_peak_period`, `swell_wave_peak_period` | 186 |
| `ewam` (DWD Europe) | error "No data is available for this location" | | | |
| `era5_ocean` | 38.5, -28.5 | 0.5 deg | history only: `wave_height/direction/period` back to 1940 (verified for 1950-01); no swell split, no SST | |

Findings:

- Always-null with `best_match` at Pico: `wave_peak_period`, `wind_wave_peak_period`, `swell_wave_peak_period`,
  all three `tertiary_swell_*`. Three swell trains need `models=ncep_gfswave016` (16 km) or `ncep_gfswave025`.
- `minutely_15` marine data is documented as Central Europe and North America only.
- History through the same endpoint with `start_date`/`end_date` (verified): waves non-null from October 2021,
  currents from January 2022, secondary swell null in every historical sample tried (2022 to January 2025);
  **SST and sea level only from about 2022-11-23 onwards**. So Open-Meteo cannot supply a
  multi-year SST climatology (about 4 years at most). A full year of hourly SST for one point is a 25 KB gzip response.
- Example `current` response, Madalena, trimmed:

```json
{"latitude":38.541664,"longitude":-28.541656,
 "current":{"time":"2026-11-22T20:00","interval":900,"wave_height":1.22,"wave_direction":288,"wave_period":7.95,
  "wind_wave_height":0.02,"wind_wave_direction":257,"swell_wave_height":0.72,"swell_wave_direction":327,
  "swell_wave_period":8.60,"secondary_swell_wave_height":0.52,"secondary_swell_wave_period":7.25,
  "secondary_swell_wave_direction":274,"tertiary_swell_wave_height":null,
  "ocean_current_velocity":0.3,"ocean_current_direction":225,"sea_surface_temperature":19.1,"sea_level_height_msl":-0.56}}
```

Lajes at the same moment (grid 38.375, -28.291656): `wave_height` 1.20 from 277, `swell_wave_height` 1.08 from 276
at 5.95 s, secondary swell 0.44 m at 11.05 s from 228, SST 19.0, current 0.3 km/h.

### 2.3 Grid-cell snapping around the island (verified)

One multi-point request, nine coastal points, default `cell_selection`:

| Point (lat, lon) | Marine `best_match` cell | Swell seen | Forecast `best_match` cell (land default) | Forecast cell with `cell_selection=sea` |
|---|---|---|---|---|
| Madalena W (38.535, -28.53) | 38.5417, -28.5417 | 0.72 m from 327 | 38.4886, -28.4532 | 38.5589, -28.4919 |
| Cachorro NW (38.565, -28.44) | 38.5417, -28.4583 | 0.86 m from 336 | 38.4886, -28.4532 | 38.5589, -28.4919 |
| Sao Roque N (38.527, -28.32) | 38.5417, -28.4583 (12 km west of the point) | 0.86 m from 336 | 38.4886, -28.3311 | 38.5589, -28.3696 |
| Santo Amaro N (38.455, -28.16) | **38.3750, -28.1250 (a south-side cell)** | 0.98 m from 274 | 38.4183, -28.1707 | 38.4886, -28.2090 |
| Ponta da Ilha E (38.413, -28.03) | 38.3750, -28.0417 | 0.90 m from 271 | 38.4183, -28.1707 | 38.4183, -28.0488 |
| Calheta de Nesquim SE (38.403, -28.08) | 38.3750, -28.0417 | 0.90 m from 271 | 38.4183, -28.1707 | 38.4183, -28.0488 |
| Lajes S (38.385, -28.26) | 38.3750, -28.2917 | 1.08 m from 276 | 38.4183, -28.2927 | 38.3480, -28.2544 |
| Sao Mateus SW (38.425, -28.45) | 38.4583, -28.4583 | 1.00 m from 269 | 38.4886, -28.4532 | 38.4183, -28.4146 |
| Horta, Faial (38.53, -28.62) | 38.5417, -28.6250 | 0.92 m from 321 | 38.6292, -28.6530 | 38.5589, -28.6141 |

What this means:

- **Waves:** Madalena and Lajes do land in different cells, and the model does give the two sides a different
  primary swell (north-west to north-north-west on the north side, west on the south side). So north versus south is
  distinguishable at the 8 km scale. But the cells sit 4 to 9 km offshore, the island is only about 15 km wide, and
  nothing inside a cell (headland shadow, refraction into a bay, the 6 km wide channel, harbour walls) is resolved.
- **Mis-snapping:** a north-coast point (Santo Amaro) was assigned a **south-coast** sea cell, and Sao Roque was
  assigned a cell 12 km to the west. The app should not send the spot's own coordinates. It should send a
  hand-picked offshore sample point per spot, 5 to 8 km off the coast on the correct side, and confirm the returned
  `latitude`/`longitude`.
- `cell_selection=nearest` on the marine API returned `null` for wave height at Sao Roque and Santo Amaro and
  `null` SST at Cachorro and Horta (the wave grid and the ocean grid have different land masks). Keep the default.
- **Weather:** the default land selection puts Madalena, Cachorro and Sao Mateus in the same cell
  (38.4886, -28.4532), which is the flank of Pico mountain. `cell_selection=sea` gives six distinct cells and
  separates north from south. Same instant, Madalena: land cell wind 4.6 kn gusting 16.3, sea cell 5.9 kn gusting 9.3.
  Lajes: land cell 4.0 kn, sea cell 8.9 kn. For shore fishing the sea cell is the better default; neither captures
  the wind acceleration through the channel or the lee of a 2 351 m mountain.
- **SST:** 18.9 to 19.2 deg C at every point. The data cannot tell coasts apart, and the real difference is small.

### 2.4 Weather models available at Pico (verified with `&models=`)

| `models=` | Cell for Madalena | Notes |
|---|---|---|
| `best_match`, `ecmwf_ifs`, `metno_seamless` | 38.4886, -28.4532 | identical coordinates and values, so the default here is ECMWF IFS 9 km (inferred from the match, not stated by the API); visibility present |
| `ecmwf_ifs025` | 38.5, -28.5 | 0.25 deg, no visibility |
| `gfs_global` / `gfs_seamless` | 38.4836, -28.4766 | about 13 km, visibility present |
| `icon_global` | 38.625, -28.625 | 0.125 deg regrid, no visibility |
| `meteofrance_arpege_europe` | 38.5, -28.5 | 0.1 deg grid does cover the Azores, no visibility |
| `meteofrance_arpege_world` | 38.5, -28.5 | 0.25 deg |
| `ukmo_global_deterministic_10km` | 38.5312, -28.5469 | about 10 km, visibility present |
| `gem_global`, `jma_gsm`, `cma_grapes_global` | coarse | work |
| `bom_access_global` | | all values null |
| `meteofrance_arome_france`, `icon_eu`, `knmi_harmonie_arome_europe` | | "No data is available for this location" |

No kilometre-scale model covers the Azores in Open-Meteo. IPMA runs AROME for the islands but does not expose it
as point data (section 3).

Forecast horizon check: `forecast_days=16&past_days=2` returned 432 hourly values, all non-null, for
`temperature_2m, wind_speed_10m, wind_gusts_10m, pressure_msl, surface_pressure, cloud_cover, cloud_cover_low,
visibility, precipitation, precipitation_probability, weather_code, cape, uv_index, is_day`, plus
`daily=sunrise,sunset`. Pressure trend is `pressure_msl[now] - pressure_msl[now - 3 h]` from the same response.
`past_days=92` is accepted, but with the default model only the most recent 74 days (1 776 of 2 232 hours) held
values; the older hours were null.

### 2.5 Archive and Climate APIs (verified)

- `archive-api.open-meteo.com/v1/archive?...&hourly=sea_surface_temperature,wave_height` for 1990 returns the
  keys but every value is null. Weather variables work (ERA5 at 38.5, -28.5; `models=ecmwf_ifs` at 9 km; `cerra`
  has no coverage). Useful for wind and pressure history, not for the sea.
- `climate-api.open-meteo.com/v1/climate` works (CMIP6, 38.5/-28.5) but has no ocean variables.

### 2.6 Open-Meteo sea level as a tide source (verified against the official table)

Hourly `sea_level_height_msl` at Horta (cell 38.5417, -28.625) for 2026-11-10 to 2026-11-30, extremes found by
parabolic fit, compared with the 81 official IH high/low waters in the app's embedded 2026 table:

- mean tidal range matches (0.84 m both);
- **times are early by 33 minutes on average** (median 30, max 51);
- levels sit about 0.22 m below "mean level", because the datum is the global geoid plus dynamic topography and
  inverse barometer, not chart datum.

So the current 2027 fallback will show high and low water roughly half an hour early. The harmonic method in
section 4 was within 2 minutes (median) over the same 81 events.

---

## 3. IPMA (verified)

All of these returned `HTTP 200`, `Access-Control-Allow-Origin: *`, no key:

| URL | Content |
|---|---|
| `https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json` | last 24 hourly timestamps for every station, about 1 MB JSON |
| `https://api.ipma.pt/open-data/observation/meteorology/stations/obs-surface.geojson` | last 3 h, about 440 KB |
| `https://api.ipma.pt/open-data/observation/meteorology/stations/stations.json` | station list |
| `https://api.ipma.pt/open-data/forecast/oceanography/daily/hp-daily-sea-forecast-day{0,1,2}.json` | sea state, 3 days (day3 is 404) |
| `https://api.ipma.pt/open-data/sea-locations.json` | the 12 sea-forecast points |
| `https://api.ipma.pt/open-data/forecast/warnings/warnings_www.json` | colour warnings, 3 days, by area |
| `https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/3460200.json` | 5-day daily forecast for Madalena |
| `https://api.ipma.pt/open-data/distrits-islands.json` | location ids |

Stations near Pico (from `stations.json`):

| id | Name | Lat, lon | Pressure? |
|---|---|---|---|
| 1200504 | Pico (Aerodromo) | 38.55219, -28.44137 | yes |
| 1200506 | Horta (Obs. Principe Alberto) | 38.540781, -28.63225 | yes |
| 1200505 | Horta / Aeroporto | 38.5211, -28.7128 | yes |
| 1200510 | Sao Jorge | 38.66, -28.17 | yes |
| 11217645 | Pico / Cabecinho (DROTRH) | 38.4338, -28.1141 | no (-99) |
| 11217625 | Pico / Cabeco do Teicho (DROTRH) | 38.489, -28.3534 | no (-99), inland and high |

Example observation (2026-11-22T19:00 UTC, Pico Aerodromo):
`{"intensidadeVentoKM": 9.4, "temperatura": 15.5, "radiacao": 30.4, "idDireccVento": 6, "precAcumulada": 0.0, "intensidadeVento": 2.6, "humidade": 75.0, "pressao": 1020.5}`.
Wind direction is an 8-point class (1 or 9 = N, 2 = NE, ... 6 = SW, 7 = W, 8 = NW, 0 = none); `-99.0` means missing;
there is **no gust field**. Twenty-four hourly pressure readings give a real observed pressure trend.

Model versus station, one day only (24 hourly values, 2026-11-21 20:00 to 2026-11-22 19:00 UTC, a light-wind day with
observed wind 4 to 13 km/h at Pico Aerodromo), Open-Meteo queried at the station's coordinates:

| Open-Meteo cell | Wind bias / MAE (km/h) | Pressure bias / MAE (hPa) | Air temp MAE (deg C) | Direction MAE |
|---|---|---|---|---|
| land cell 38.4886, -28.4532 | +5.2 / 5.6 | +0.46 / 0.46 | 0.6 | 23 deg |
| sea cell 38.5589, -28.4919 | +7.6 / 7.6 | +0.17 / 0.23 | 0.8 | 23 deg |

Pressure and temperature agree closely. The model read 5 to 8 km/h windier than the land station, which is what
you expect over open water against a sheltered airfield, but one calm day proves nothing about strong-wind days.

Sea-state forecast: the only central-group point is "Horta, costa", `globalIdLocal` 3470126, at 38.57, -28.47
(which is actually off the north-west coast of Pico). Example day 0:
`{"totalSeaMin": 1.5, "totalSeaMax": 2.0, "waveHighMin": "1.6", "waveHighMax": "2.2", "wavePeriodMin": "8.2", "wavePeriodMax": "8.7", "predWaveDir": "N", "sstMin": "18.4", "sstMax": "18.5"}`.
Per the docs `waveHigh*` is swell height, `totalSea*` significant wave height, direction is an 8-point class.
It is daily min/max only, one point, three days.

Warnings: Pico is in area `ACE` (Grupo Central). Types present: Agitacao Maritima, Vento, Precipitacao,
Trovoada, Nevoeiro, Tempo Quente, Tempo Frio, Neve; levels green/yellow/orange/red with start and end times.
Example: `{"awarenessTypeName": "Agitacao Maritima", "idAreaAviso": "ACE", "startTime": "2026-11-22T12:18:00", "awarenessLevelID": "green", "endTime": "2026-11-25T12:00:00"}`.

Terms (from api.ipma.pt, fetched): no named open licence. "O Utilizador deve referir, sempre, a fonte de informacao";
free reuse for personal or public use "desde que dessa utilizacao nao decorram finalidades lucrativas ou ofensivas";
IPMA asks API users to email webmaster@ipma.pt; no rate limit documented; service can change without notice.

---

## 4. Tides

### 4.1 Instituto Hidrografico: what exists now (verified)

- The old JSON endpoints (`www.hidrografico.pt/json/mare.port.val.php` and friends) are gone: all return the
  site's 404 page. The site was rebuilt.
- The new "Hidrografico+" portal (`geomar.hidrografico.pt`) calls
  `https://supportserver1.hidrografico.pt/geodata/tides/getTides|getBmPm|getTidesByLocation|getPortNameById`
  and `.../geodata/buoys/...`. Called without credentials these return **`401 Invalid API KEY`** with no
  `Access-Control-Allow-Origin`. The key lives in their app; I did not extract or use it. Not a usable source.
- The printed tide table is now digital only and free. **The 2027 volume is out:**
  - product page: `https://loja.hidrografico.pt/produto/https-loja-hidrografico-pt-ln-web-wp-content-uploads-0202-11-tabela_mares_2027_vol_i-pdf/` (price "EUR 0.00", posted 05 Nov)
  - download: `https://loja.hidrografico.pt/?sdm_process_download=1&download_id=44965`, which 302s to
    `https://loja.hidrografico.pt/ln/web/wp-content/uploads/0202/11/Tabela_Mares_2027_Vol_I.pdf` (10 272 239 bytes, 205 pages)
  - 2026 volume for reference: `https://loja.hidrografico.pt/ln/web/wp-content/uploads/2023/11/TabelaMare_I_2026_signed.pdf`
  - licence printed on the download page: **CC BY-NC-ND 4.0** ("copiar e redistribuir o material em qualquer
    suporte ou formato, sem adaptacoes e apenas para fins nao comerciais"). Extracting one port's numbers into an
    app is arguably an adaptation; the app already does this for 2026, so this is a judgement call for the owner,
    not something I can settle.
- Horta is PDF pages 181 to 186 (printed 2-159 to 2-164). Times are UTC ("Horas do Fuso: 0 (TU)"), heights in
  metres to 0.1 above chart datum (ZH), which is "1,00 m abaixo do nivel medio adotado (Horta, 1935)". Harmonic
  analysis was done on gauge data from 1 Sep 2003 to 30 Aug 2004; gauge at 38 31.99 N, 28 37.24 W.
- Text extraction works with Ghostscript: `gs -q -dSAFER -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=p%03d.txt file.pdf`.
  I parsed pages 183 to 186 into **1 411 high/low waters for 2027**, all strictly alternating, gaps 351 to 409
  minutes. Saved in the same shape as the app's `HORTA` table (minutes after 1 Jan 00:00 UTC, heights in m):
  `<scratch>/probe/horta_2027_ih_extremes.json`
  First rows: 03:00 0.7, 09:17 1.3, 15:51 0.7, 22:05 1.2 on 1 January 2027.
  Parser: `scripts/parse_ih.py`.

Secondary ports referred to Horta (PDF page 195, printed 3-3, read from the rendered page):

| Port | Lat N, Lon W | HW time, neaps / springs | LW time, neaps / springs | Amplitude ratio, neaps / springs |
|---|---|---|---|---|
| Madalena do Pico | 38 32.1, 28 31.8 | -0:07 / +0:04 | -0:02 / +0:07 | 1.06 / 1.04 |
| S. Antonio (Pico, north coast) | 38 32.2, 28 20.2 | 0:00 (single value) | 0:00 | 1.13 |
| Lajes (Pico) | 38 23.9, 28 15.4 | 0:00 | 0:00 | 1.03 |
| Porto do Cais (Pico), i.e. Cais do Pico / Sao Roque | 38 31.9, 28 19.3 | +0:28 | +0:28 | 1.05 |

Horta reference levels: HW springs 1.57, HW neaps 1.27, mean level 1.00, LW neaps 0.73, LW springs 0.43 m.
2027 extremes for Horta: highest 1.81 m on 22 Feb 02:59, lowest 0.27 m on 1 Sep 20:52.

Harmonic constants printed by IH (PDF page 196, "Constantes harmonicas fundamentais"): only four per port.
Horta: M2 0.419 m / 30.2 deg, S2 0.153 / 48.0, K1 0.043 / 69.3, O1 0.020 / 314.1. These phases differ from the
TICON Greenwich phases by exactly one hour of each constituent's speed (29, 30, 15, 14 deg), so they are referred
to the Azores zone (UTC-1). That is my inference from the numbers; the table does not say so.

### 4.2 TICON-4 constants for Horta (verified)

`https://raw.githubusercontent.com/openwatersio/slackwater-database/main/data/ticon/horta_azores-212a-prt-uhslc_rq.json`
(`access-control-allow-origin: *`; licence field `cc-by-4.0`; source TICON-4, https://www.seanoe.org/data/00980/109129/,
citation Hart-Davis, Dettmering, Seitz 2025, doi 10.17882/109129). The repo was formerly `neaps/tide-database`.
50 constituents, Greenwich phase lags in degrees, UTC. Largest:

```
M2  0.4137 m  59.47    S2  0.1527  78.44    N2  0.0913  44.71    SA  0.0468 208.00
K2  0.0425    75.14    K1  0.0416  84.26    SSA 0.0214  15.18    O1  0.0199 326.81
MU2 0.0184    13.57    NU2 0.0165  45.05    2N2 0.0136  28.04    P1  0.0128  76.65
T2  0.0097    77.34    MM  0.0091 279.25    L2  0.0085  59.74    Q1  0.0083 247.74
```

Other Azores stations in the same set: Ponta Delgada (211), Angra do Heroismo (215), Flores Santa Cruz (210),
Flores Lajes (213). Nothing on Pico itself.

### 4.3 Can the browser compute tides offline? Yes (verified numerically)

I wrote a dependency-free harmonic synthesis (astronomical arguments s, h, p, N, p1 from polynomial formulas,
Schureman-style nodal factors f and u for the M2, K1, O1, K2, Mm, Mf, J1, OO1 families, sum of
`f*A*cos(V+u-G)`), about 80 lines, and compared its high/low waters with the official IH tables for two full years.
Script: `scripts/tide.py`
(comparison driver `tide_cmp.py` next to it). It is Python, written only to test the method; it ports to JS line for line.

| Constituent set | Year | Matched | Time error, minutes: median / 90 % / 99 % / max | Height error, m: mean / median abs / 90 % / max |
|---|---|---|---|---|
| TICON, 27 constituents (all I implemented, **without SA and SSA**), mean level 0.96 m above ZH | 2027 | 1411/1411 | 1.7 / 4.2 / 7.1 / 10.9 | +0.004 / 0.025 / 0.049 / 0.076 |
| same | 2026 | 1411/1411 | 1.8 / 4.5 / 9.9 / 15.6 | +0.004 / 0.025 / 0.050 / 0.083 |
| TICON, 11 constituents (M2 S2 N2 K2 K1 O1 P1 Q1 MU2 NU2 2N2), 0.96 m | 2027 | 1411/1411 | 2.6 / 6.6 / 11.8 / 18.7 | -0.001 / 0.026 / 0.052 / 0.082 |
| same | 2026 | 1411/1411 | 2.6 / 6.7 / 12.4 / 21.2 | 0.000 / 0.026 / 0.051 / 0.077 |
| TICON top 8 only, mean level 1.00 | 2026 | 1411/1411 | 4.3 / 13.6 / 22.4 / 27.8 | +0.040 / 0.040 / 0.088 / 0.130 |
| IH's four published constants (shifted one hour to UTC) | 2026 | 1411/1411 | 16.7 / 44.4 / 67.0 / 73.9 | +0.040 / 0.060 / 0.142 / 0.229 |
| TICON with SA and SSA left in, mean level 1.00 | 2027 | 1411/1411 | 1.7 / 4.3 / 7.0 / 10.9 | +0.044 / 0.042 / 0.111 / 0.180 |

Reading the table:

- The official table rounds heights to 0.1 m, so a 0.05 m error is the floor. With 27 constituents the heights are
  at that floor and 90 % of times are within about 4.5 minutes, worst case 11 to 16 minutes, in both years.
- Two empirical adjustments were needed to match IH: drop the seasonal SA/SSA terms (IH evidently does not
  include TICON's seasonal cycle) and use a mean level of **0.96 m** above chart datum rather than the stated 1.00.
  Both were fitted on 2026 and then held for 2027, where they gave the same result.
- IH's own four constants are not enough (half the events are more than 17 minutes out).
- Not implemented in my test and therefore omitted: MB2 (7 mm), MTM (5 mm), M1 (4 mm), EP2 (4 mm) and smaller.
- Nodal factors were frozen at mid-year in the test; in the app compute them per day or per month.
- The formulas are valid for decades, so this removes the yearly table chore. It predicts the astronomical tide
  only; a 1 hPa pressure change moves the sea about 1 cm and winter storms add more.

Ready-made alternative (verified): `https://api.openwaters.io/tides/extremes?latitude=38.53&longitude=-28.62&start=2027-01-01T00:00:00Z&end=2027-01-06T00:00:00Z`
returns `access-control-allow-origin: *`, no key, station `ticon/horta_azores-212a-prt-uhslc_rq`, datum LAT:

```json
{"time":"2027-01-01T02:58:00.928Z","level":0.5065,"high":false,"low":true,"label":"Low"}
{"time":"2027-01-01T09:20:21.553Z","level":1.1210,"high":true,"low":false,"label":"High"}
{"time":"2027-01-01T15:45:29.933Z","level":0.4859,"high":false,"low":true,"label":"Low"}
{"time":"2027-01-01T22:01:48.501Z","level":1.0318,"high":true,"low":false,"label":"High"}
```

IH for the same day: 03:00 0.7, 09:17 1.3, 15:51 0.7, 22:05 1.2 (add about 0.20 m to convert their LAT datum to
IH chart datum). Other paths: `/timeline`, `/stations`, `/stations/{source}/{id}/extremes`, `/openapi.json`.
Version "1.0.0-beta.6", behind Cloudflare, `cache-control: public, max-age=3600`; no published rate limit or uptime
promise. The engine is on npm as `@slackwater/engine` (MIT, no dependencies, 217 KB unpacked, 1.0.0-beta.0) and the
older `@neaps/tide-predictor` 0.11.0 (MIT, no dependencies).

### 4.4 Other tide routes

- **Open-Meteo `sea_level_height_msl`**: keyless and CORS-enabled but about 30 minutes early at Horta and on a
  different datum (section 2.6). Keep only as a last resort.
- **IOC sea level monitoring** (verified): `https://www.ioc-sealevelmonitoring.org/service.php?query=data&code=pdas&timestart=...&timestop=...&format=json`,
  CORS `*`, 1-minute data. The only live Azores gauge listed is Ponta Delgada (`pdas`). No Horta gauge in the
  station list of 2 345 entries. Could show the regional surge (observed minus predicted) but not Pico's tide.
- **WorldTides, Stormglass tide endpoints**: key required (verified 400 / 403 without one).
- **FES2014 / FES2022 (AVISO), TPXO (OSU), EOT20 (DGFI-TUM)**: gridded constituent atlases that could give
  constants at Lajes or Sao Roque rather than Horta. Not probed. From memory: FES and TPXO need registration and
  restrict redistribution; EOT20 is openly licensed. They need an offline extraction step (for example pyTMD), then
  the numbers are embedded exactly like the TICON set. Given IH says Lajes and Santo Antonio have zero time
  difference from Horta, the gain would be small.

---

## 5. Sea surface temperature

Same evening, four sources near Madalena: Open-Meteo 19.1 deg C (22 Nov), MUR 18.95 (21 Nov), OSTIA 18.78
(21 Nov), Mercator model 18.93, IPMA forecast 18.4 to 18.5; OISST prelim 19.61 (18 Nov). Spread about +/-0.5 deg C.

### 5.1 Forecast and current

- Open-Meteo marine `sea_surface_temperature`: hourly, 10 days, 1/12 deg (section 2).
- IPMA `sstMin`/`sstMax` for "Horta, costa": daily, 3 days (section 3).
- Copernicus WMTS GetFeatureInfo (verified, keyless, CORS `*`):
  - OSTIA analysis, 0.05 deg, daily, 2024-01-17 to yesterday: layer
    `SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2/analysed_sst` gave 291.93 K at 38.575, -28.525.
  - Mercator model `GLOBAL_ANALYSISFORECAST_PHY_001_024/cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_202406/thetao`,
    hourly, 2022-06-01 to +10 days: 18.93 deg C; `&time=2026-12-01T12:00:00Z` returned 18.47.

URL pattern (tile indices computed from lat/lon; `EPSG:4326` matrix `z` has tiles of `180/2^z` degrees, 256 px):

```
https://wmts.marine.copernicus.eu/teroWmts?SERVICE=WMTS&REQUEST=GetFeatureInfo&VERSION=1.0.0
  &LAYER=<product>/<dataset>/<variable>&TILEMATRIXSET=EPSG:4326&TILEMATRIX=8
  &TILEROW=73&TILECOL=215&I=108&J=40&INFOFORMAT=application/json[&time=2026-11-21T00:00:00Z][&elevation=...]
```

Response, trimmed:
`{"type":"FeatureCollection","features":[{"properties":{"lat":38.5625,"lon":-28.5208,"variableId":"CHL","value":0.1684,"units":"milligram m-3"}}]}`

Caveats: dataset ids carry a version suffix (`_202311`, `_202406`) that Copernicus changes from time to time; a
wrong id returns an XML `InvalidParameterValue`. The full GetCapabilities is **83 MB** (never fetch it in the app);
the per-product one is small, e.g. `https://wmts.marine.copernicus.eu/teroWmts/OCEANCOLOUR_GLO_BGC_L4_NRT_009_102?SERVICE=WMTS&REQUEST=GetCapabilities`
is 554 KB. Land-masked cells return `"value": null` (the Mercator cell at 38.4167, -28.25 just off Lajes is land),
so query a point a few kilometres offshore. No rate limit is documented; responses came back in 0.15 to 0.6 s.

### 5.2 Climatology and anomaly

| Route | Verified result | Browser-usable live? |
|---|---|---|
| NCEI ERDDAP OISST `anom` variable | `https://www.ncei.noaa.gov/erddap/griddap/ncdc_oisst_v2_avhrr_by_time_zlev_lat_lon.json?sst%5B(last)%5D%5B(0.0)%5D%5B(38.625)%5D%5B(331.375)%5D,anom%5B(last)%5D%5B(0.0)%5D%5B(38.625)%5D%5B(331.375)%5D` gave 2026-11-06: sst 20.78, anom +1.35. The `_prelim_` dataset gave 2026-11-18: sst 19.61, anom +0.93. Longitude is 0 to 360 (331.375 = -28.625). CORS `*`. Covers 2020-02-28 onwards only. | **Yes.** Climatology for that day = sst - anom, with no baked data. Lags 4 days (prelim) or 16 days (final). |
| Copernicus WMTS monthly model climatology | layer `GLOBAL_MULTIYEAR_PHY_001_030/cmems_mod_glo_phy_my_0.083deg-climatology_P1M-m_202311/thetao`, `&time=2004-MM-01T00:00:00Z`, at 38.58, -28.50: Jan 16.46, Feb 15.93, Mar 15.82, Apr 16.31, May 17.48, Jun 19.36, Jul 22.03, Aug 23.54, Sep 22.95, Oct 21.10, Nov 19.08, Dec 17.47 deg C | **Yes**, 12 requests, or bake these 12 numbers per sample point. Monthly, model-based (GLORYS12 reanalysis; baseline period not checked). |
| Copernicus WMTS daily SST history | `SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/METOFFICE-GLO-SST-L4-REP-OBS-SST_202003/analysed_sst&time=1995-08-15T00:00:00Z` gave 296.36 K. Range 1981-10-01 to 2026-06-30. | Technically yes, but one request per day per point; a 30-year daily climatology is about 11 000 requests. Pre-bake. |
| NOAA CoastWatch ERDDAP OISST 1981 to now | `https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.csv?sst%5B(1982-01-01):1:(1986-12-31)%5D%5B(0.0)%5D%5B(38.375):1:(38.625)%5D%5B(-28.625):1:(-28.125)%5D` returned 5 years x 6 cells in 65 to 120 s (500 KB CSV). One 45-year request timed out, so chunk it. | **No** (no CORS header). Fine from a script. |
| Open-Meteo marine history | SST only from 2022-11-23 | Yes, but too short for a climatology |
| EMODnet Physics, Faial-Pico buoy water temperature | `https://platform-erddap.emodnet-physics.eu/erddap/tabledap/TS_70_6202404_MO_UND.json?time,TEMP&time>=...`, 10-minute, 2012-05-04 to 2021-10-10, at 38.5877, -28.5377 | Yes. The only **measured** in-channel water temperature record I found; useful to check any climatology. |

OISST cells that matter: centres at 38.375 and 38.625 N, 28.625, 28.375 and 28.125 W. The whole island sits inside
a 2 x 3 block; the latest values across the six cells differ by 0.2 deg C. A daily climatology from one or two of
those cells is all the resolution there is.

Pre-baked daily climatology: see the appendix at the end of this file.

---

## 6. Chlorophyll, water clarity, turbidity

Copernicus WMTS GetFeatureInfo is the only route I found that is keyless, CORS-enabled and returns numbers.
Values on 2026-11-21:

| Layer | North of Madalena (38.56, -28.53) | South of Lajes (38.36, -28.26) | Near-shore points |
|---|---|---|---|
| `OCEANCOLOUR_GLO_BGC_L4_NRT_009_102/cmems_obs-oc_glo_bgc-plankton_nrt_l4-gapfree-multi-4km_P1D_202311/CHL` (4 km, gap-filled, daily) | 0.168 mg/m3 | 0.188 | 0.206 at 38.39, -28.255 |
| `OCEANCOLOUR_ATL_BGC_L4_NRT_009_116/cmems_obs-oc_atl_bgc-plankton_nrt_l4-gapfree-multi-1km_P1D_202511/CHL` (1 km, gap-filled) | 0.172 | 0.195 | 0.221 at 38.39, -28.255 |
| `OCEANCOLOUR_ATL_BGC_L3_NRT_009_111/cmems_obs-oc_atl_bgc-plankton_nrt_l3-olci-300m_P1D_202611/CHL` (300 m, cloud gaps) | null | 0.187 | null at both |
| `OCEANCOLOUR_GLO_BGC_L4_NRT_009_102/cmems_obs-oc_glo_bgc-transp_nrt_l4-gapfree-multi-4km_P1D_202311/ZSD` (Secchi depth) | 23.3 m | 22.1 m | 21.1 m |
| same product, `/KD490` | 0.040 1/m | 0.042 | 0.043 |
| `OCEANCOLOUR_ATL_BGC_L3_NRT_009_111/cmems_obs-oc_atl_bgc-transp_nrt_l3-multi-1km_P1D_202311/ZSD` (1 km, cloud gaps) | null | 21.7 m | 20.3 m |

Also present in the capabilities: `SPM` and `KD490` in the Atlantic 1 km L3 product; `TUR` only in the regional
high-resolution products (I did not check whether any of those reaches the Azores); a 0.25 deg model chlorophyll
forecast (`GLOBAL_ANALYSISFORECAST_BGC_001_028/.../chl`, returned null at the test point).

Limits: NRT ocean-colour layers only keep the last 8 to 19 days in WMTS. These are open-ocean numbers (clear,
oligotrophic water, Secchi depth over 20 m). The thing a shore angler cares about, coloured water after swell or
rain within a few hundred metres of the rocks, is below the pixel size and the coastal pixels are masked. Treat
chlorophyll as a slow regional background signal, not a per-spot clarity reading.

Others:

- NASA GIBS (verified): `https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=GHRSST_L4_MUR_Sea_Surface_Temperature&SRS=EPSG:4326&BBOX=-29.0,38.0,-27.5,39.0&WIDTH=300&HEIGHT=200&FORMAT=image/png&TRANSPARENT=true&TIME=2026-11-19`
  returns a PNG with CORS `*`. For chlorophyll I tried the layer names `MODIS_Aqua_L2_Chlorophyll_A` and
  `VIIRS_NOAA20_Chlorophyll_a`; both answered 200 with an empty 310-byte PNG, so either there was no data that day
  or my layer names are wrong (not resolved). Pictures only, no numbers, either way.
- NOAA CoastWatch ERDDAP chlorophyll: no CORS (section 1).
- Copernicus numeric download (toolbox, STAC, S3): needs an account. Not usable from the page.

---

## 7. Currents

- Open-Meteo marine `ocean_current_velocity` / `ocean_current_direction` (SMOC, 1/12 deg, hourly, includes tides
  per the docs): 0.3 km/h at both test points.
- Copernicus WMTS `GLOBAL_ANALYSISFORECAST_PHY_001_024/cmems_mod_glo_phy_anfc_0.083deg_PT1H-m_202406/sea_water_velocity`:
  0.075 m/s with `uo` and `vo` components; the `merged-uv` dataset adds tide and wave drift.
- Both are 8 km models. The Faial-Pico channel is about 6 km wide and under 100 m deep (section 9), so it is one
  cell at most. I found no current observations to check against. Do not present these as the current at a spot;
  tide state from section 4 is a better proxy for water movement at the shore.

---

## 8. Real observations near Pico

| What | Where | Status (verified) |
|---|---|---|
| IPMA weather stations | Pico Aerodromo, Horta observatory, Horta airport, Sao Jorge | live, hourly, CORS `*` (section 3) |
| CLIMAAT / Univ. Azores wave buoy "Faial Pico", WMO 6202404 | 38.5877 N, 28.5377 W (north mouth of the channel) | **archive only: 2012-05-04 to 2021-10-10.** Hs, direction, periods, water temp every 10 min. `https://platform-erddap.emodnet-physics.eu/erddap/tabledap/TS_70_6202404_MO_UND.json?time,VAVH,VDIR,TEMP&time%3E=2021-10-09&orderBy(%22time%22)` returned 334 rows, last `2021-10-10T03:40Z`. |
| CLIMAAT wave buoy "Graciosa", WMO 6202400 | 39.0868 N, 27.9622 W (about 60 km north-east of Pico) | newest record `2026-11-06T05:20Z` when probed on 22 Nov, i.e. 16 days behind. Example row: `["2026-11-04T00:00:00Z", 1.78, null, 311, null]` (Hs m, peak period, direction). Dataset `TS_70_6202400_MO_UND`. |
| Other CLIMAAT buoys | Praia da Vitoria 6202401, Ponta Delgada 6202402, Lajes das Flores 6202403, Vila do Porto 6202405 | last records between May and September 2025 |
| Tide gauge | Ponta Delgada `pdas` via IOC, live. UHSLC 211 Ponta Delgada to 2026-09. | no live Horta gauge found |
| CLIMAAT site `https://www.climaat.angra.uac.pt/` | | loads (old frameset). I could not find a machine-readable real-time feed. **Not verified** whether newer buoy data is published anywhere else. |
| IH buoys | behind the key-gated API | not usable |

The ERDDAP request first answers `302` to `https://er3webapps.emodnet-physics.eu/platforms3/erddap/...`; both hops
send `Access-Control-Allow-Origin: *`. Station discovery query that worked:
`https://erddap.emodnet-physics.eu/erddap/tabledap/EP_PLATFORMS_METADATA_V2.json?PLATFORMCODE,call_name,latitude,longitude,firstdateobservation,lastdateobservation,parameters,platformtypecode&latitude%3E=36.5&latitude%3C=40&longitude%3E=-32&longitude%3C=-24.5&platformtypecode!=%22DB%22`

Practical consequence: there is no live wave measurement for Pico. The nine years of Faial-Pico buoy data are
still valuable offline: compare them with the Open-Meteo marine history (which starts October 2021, so there is
no overlap) or with ERA5 waves (`models=era5_ocean`, 0.5 deg, 1940 on) to learn how much the channel shelters.

---

## 9. Bathymetry (EMODnet, verified)

- `https://rest.emodnet-bathymetry.eu/depth_sample?geom=POINT(-28.53%2038.545)` returned
  `{"min":-21.0,"max":-20.2,"avg":-20.7,"stdev":0.28,"smoothed":-20.93,...,"reference":{"identifier":"hi057_1983","type":"CDI"}}`
  with `access-control-allow-origin: https://example.org` (echoes the caller).
- `https://rest.emodnet-bathymetry.eu/depth_profile?geom=LINESTRING(-28.535%2038.536,-28.56%2038.545)` returns an array of depths along the line.
- `https://ows.emodnet-bathymetry.eu/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&LAYERS=emodnet:mean&QUERY_LAYERS=emodnet:mean&CRS=EPSG:4326&BBOX=38.54,-28.535,38.55,-28.525&WIDTH=101&HEIGHT=101&I=50&J=50&INFO_FORMAT=application/json`
  returned `{"properties":{"Depth":-20.7}}`, CORS `*`.

Depth (m, negative is below datum) along rough offshore transects. Start points were approximate, so the nearest
samples may be on land (positive values); the pattern is what matters:

| Transect | 100 m | 250 m | 500 m | 1 km | 2 km | 4 km |
|---|---|---|---|---|---|---|
| Madalena, heading west into the channel | -9.7 | -7.7 | -5.5 | +2.8 (the Madalena islets) | -49 | -142 |
| Lajes, heading south | -0.8 | +1.1 | -1.0 | -15 | -164 | -421 |
| Sao Roque, heading north | +0.3 | +0.2 | -189 | -328 | -644 | -1 061 |
| Calheta de Nesquim, heading south | no data | 0.0 | no data | -496 | no data | no data |
| Sao Mateus, heading south-west | +15 (land) | no data | -99 | no data | -606 | no data |

So: the north coast drops to about 190 m within half a kilometre; Lajes has a shallow reef platform for the first
kilometre; the channel off Madalena stays under 150 m for 4 km. Some cells return no value. Depth does not change,
so sample each spot once and store "depth at 100 m, 250 m, 500 m" in the spot list rather than calling at run time.

---

## 10. Sun and moon

Computable locally; no network needed. The app already derives moon phase. For moonrise and moonset a small
algorithm (SunCalc is the usual one; npm `suncalc` 2.1.4) is enough.
Cross-check source (verified): `https://api.met.no/weatherapi/sunrise/3.0/moon?lat=38.535&lon=-28.53&date=2026-11-22&offset=-01:00`
returned moonrise 15:51, moonset 05:12, high moon 23:03 (local, UTC-1), CORS `*`. Open-Meteo `daily=sunrise,sunset`
also works.

---

## 11. Webcams

SpotAzores (`https://spotazores.com/webcams/pico/`) lists four Pico cameras:

- `https://spotazores.com/webcam/pico/madalena/porto-da-madalena/`
- `https://spotazores.com/webcam/pico/lajes-do-pico/lajes/`
- `https://spotazores.com/webcam/pico/sao-roque-do-pico/porto-de-sao-roque/`
- `https://spotazores.com/webcam/pico/sao-roque-do-pico/montanha/`

and `https://spotazores.com/webcam/faial/horta/horta/` across the channel. The pages returned HTTP 200 with no
`X-Frame-Options` header, but the stream is injected by script and I found no documented embed or image URL.
Link out per spot; do not scrape. Whether each camera is currently live was not checked.

---

## 12. Things that do not work for this app

- **Keyed services** (Stormglass, WorldTides, Windy, Windguru, IH API): any key placed in a static page is public.
  Stormglass free plan is reported as 10 requests/day, WorldTides sells credits, Windy's trial key is documented to
  return altered data. These three facts come from their sites via search, not from calls.
- **NOAA CoastWatch ERDDAP** from the browser: no `Access-Control-Allow-Origin` on pfeg, coastwatch.noaa.gov or
  polarwatch. Other ERDDAPs checked: `oceanwatch.pifsc.noaa.gov` allows only `https://ahi.pifsc.gov`; NCEI,
  EMODnet Physics, Marine Institute IE, BCO-DMO send `*`; `erddap.sensors.ioos.us` echoes the Origin.
- **met.no Oceanforecast**: HTTP 422 outside north-west Europe.
- **Copernicus IBI regional products**: the Iberia-Biscay-Ireland domain was not tested at the Azores; I used global
  and Atlantic products only.

---

## 13. Offline behaviour

Every usable endpoint above sends a permissive CORS header, so responses are readable (not opaque) and a service
worker can cache them with a timestamp. Static or slow data is better embedded: tide constituents (about 1 KB),
port corrections, SST climatology (366 numbers per cell), depths per spot. Live data then degrades gracefully to
"last fetched at ..." when offline, and tides, sun, moon and seasonal baselines keep working with no network.

---

## 14. Not verified, or inferred

- Rate limits for IPMA, Copernicus WMTS, EMODnet (REST, WMS, ERDDAP), IOC and the Open Waters API: none documented, none tested.
- Open Waters API long-term availability (beta, single small project).
- That Open-Meteo `best_match` at Pico is ECMWF IFS 9 km: inferred from identical grid coordinates and values.
- That IH's printed harmonic phases are in zone UTC-1: inferred from the phase differences.
- Why IH predictions match a 0.96 m mean level and no seasonal terms: empirical fit only.
- Stormglass, WorldTides and Windy plan details; FES / TPXO / EOT20 licensing and practicality.
- Whether a live CLIMAAT feed exists outside EMODnet; whether the SpotAzores cameras are up.
- Accuracy of modelled currents and of modelled waves at the shore: no observations to compare with.
- EMODnet Bathymetry licence wording and vertical datum were not re-read.
- The legal reading of CC BY-NC-ND for embedding a table extracted from the IH PDF.

---

## 15. Files produced

All under `<scratch>/`:

- `research-conditions.md` (this file)
- `probe/horta_2027_ih_extremes.json`: 1 411 official 2027 high/low waters for Horta, parsed from the IH PDF
- `dl_ih2027/tm2027_vol1.pdf`: the IH 2027 tide table as downloaded; `ih2027_txt/p181.txt` to `p197.txt` hold the text of the Horta pages
- `dl_ticon/horta.json`: TICON-4 constituents for Horta
- `scripts/tide.py`, `scripts/tide_cmp.py`, `scripts/sl_cmp.py`, `scripts/parse_ih.py`: the test code behind sections 2.6 and 4
- `probe/ih_p195.png`: rendered secondary-port table
- `probe/oisst_clim_1991_2020.json` and `scripts/clim.py`: the SST climatology in the appendix; raw CSV chunks in `dl_oisst/`

The scratchpad is temporary; copy anything worth keeping.

---

## Appendix: OISST daily climatology for the cells around Pico

Built as a test of the pre-bake route. Source: NOAA OISST v2.1 from
`coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180` (no CORS, so fetched with curl in 5-year chunks,
25 to 120 s each), six 0.25 deg cells, baseline 1991 to 2020, mean per day of year with an 11-day running mean.
Script `scripts/clim.py`; result `probe/oisst_clim_1991_2020.json` (6 cells x 365 values, 15 KB of JSON).

Caveat found while doing it: this aggregated dataset is **missing days in 1992 to 1998** (138 to 325 days per year
instead of 365), so each day of year has 24 to 33 samples rather than 30. Good enough for a baseline; for a
complete record use the Copernicus OSTIA reprocessed layer or NCEI's own files.

Mid-month values, deg C:

| Cell centre | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 38.625 N, 28.625 W (north-west, Madalena side) | 16.63 | 16.12 | 15.97 | 16.29 | 17.18 | 19.20 | 21.76 | 23.33 | 22.73 | 21.03 | 19.21 | 17.66 |
| 38.625 N, 28.375 W (north) | 16.60 | 16.11 | 15.98 | 16.27 | 17.19 | 19.19 | 21.76 | 23.30 | 22.70 | 21.01 | 19.15 | 17.63 |
| 38.625 N, 28.125 W (north-east) | 16.59 | 16.08 | 15.97 | 16.25 | 17.19 | 19.16 | 21.71 | 23.27 | 22.65 | 20.97 | 19.10 | 17.58 |
| 38.375 N, 28.625 W (south-west) | 16.78 | 16.27 | 16.12 | 16.46 | 17.35 | 19.32 | 21.88 | 23.43 | 22.88 | 21.21 | 19.36 | 17.80 |
| 38.375 N, 28.375 W (south, Lajes side) | 16.77 | 16.25 | 16.12 | 16.46 | 17.35 | 19.32 | 21.88 | 23.39 | 22.85 | 21.19 | 19.32 | 17.78 |
| 38.375 N, 28.125 W (south-east) | 16.76 | 16.22 | 16.11 | 16.43 | 17.35 | 19.29 | 21.84 | 23.37 | 22.80 | 21.15 | 19.28 | 17.75 |

- Annual minimum about 16.0 deg C in late February to mid March, maximum about 23.4 in mid to late August.
- The northern row is 0.09 to 0.20 deg C cooler than the southern row all year (mean 0.15). That is the entire
  north-south signal available at this resolution.
- Standard deviation of the daily anomaly, 1991 to 2020, north-west cell: 0.73 deg C. An anomaly needs to be
  around 1 deg C before it means much.
- It agrees with the Copernicus model climatology in section 5.2 to within about 0.2 deg C in every month.
- Cross-check of the live route: NCEI gave sst 20.78 and anom +1.35 for 2026-11-06, implying a baseline of
  19.43 for that day (NOAA's anomaly uses an older baseline, 1971 to 2000 as far as I remember; not checked);
  this climatology gives 19.64 for 6 November, so the two routes differ by 0.2 deg C.
- Worked example: the last final OISST day in the download, 2026-11-05, is 20.87 deg C in the north-west cell,
  +1.2 against this 1991 to 2020 baseline (NOAA's own `anom` said +1.35 a day later). By 18 to 22 November the
  sources in section 5 read 19.0 to 19.6 against a baseline of 19.0, so 0 to +0.6.

Updating it: rerun the same chunked curl requests and `scripts/clim.py` every few years; nothing here needs a server.
