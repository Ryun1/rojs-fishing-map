# Research notes

Background research for the spot forecast plan in
[`../superpowers/specs/2026-11-22-spot-forecast-design.md`](../superpowers/specs/2026-11-22-spot-forecast-design.md),
gathered on 2026-11-22.

| File | What it covers |
|---|---|
| `species.md` | Which species a shore angler catches on Pico, monthly landings, per-species ecology, occurrence records, whether conditions predict catch, regulations |
| `conditions.md` | Weather, wave, sea temperature, tide and bathymetry data sources a keyless static web app can call, with resolution limits around the island |
| `spots.md` | 43 candidate shore points with coordinates, computed facing and exposure, depth profiles, access, restrictions |
| `landings.md` | SREA monthly landings by species for Pico and Faial, 1994 to 2026, and the season profiles built from them |
| `recreational-catch.md` | Species shares and day/night catch rates from the Faial/Pico shore-angling survey (open companion papers) |
| `buoy.md` | Faial–Pico wave buoy 2012 to 2021 compared with ERA5: channel shelter by swell direction, monthly wave and water climate |
| `census.md` | Underwater fish census raw archive: presence only, west-coast dives, per-site species lists |
| `local-reports.md` | Competition results, clubs, forums and news: 22 Faial shore-championship records, contacts for Pico data |

Each note labels its claims as verified, inferred, anecdotal or unverified. Read those labels before relying on a figure.

## Kept files

- `scripts/tide.py`, `scripts/tide_cmp.py`: test of computing Horta tides from harmonic constants, and the comparison against the official tables.
- `scripts/parse_ih.py`: parser for the Instituto Hidrográfico tide table PDF. The extracted table itself is not kept here because its licence (CC BY-NC-ND 4.0) forbids derivatives.
- `scripts/clim.py`: builds the sea temperature climatology.
- `scripts/spots_*.py`: coastline fetch, exposure sectors and bathymetry profiles for the spots.
- `data/ticon4_horta.json`: TICON-4 tidal constituents for Horta (CC BY 4.0; Hart-Davis, Dettmering and Seitz 2025, doi 10.17882/109129).
- `data/oisst_clim_1991_2020.json`: daily sea surface temperature baseline 1991 to 2020 for the grid cells around Pico, derived from NOAA OISST.
- `data/srea/*.xlsx`: monthly landings by species and island from the Azores statistics service (SREA), as downloaded. Each file covers a rolling 12 months and older files disappear from the site, so these are worth keeping.
- `data/srea/srea_landings_pico_faial_1994-2026.csv`, `data/srea/season_profiles.json`, `scripts/srea.py`: the full monthly landings history and the derived season profiles (see `landings.md`).
- `data/buoy/`, `scripts/buoy.py`: hourly buoy series (CC BY-SA, University of the Azores / CLIMAAT via EMODnet Physics), shelter ratios and monthly climatology.
- `data/census/pico_census_sites.json`, `scripts/census.py`: per-site species presence from the dive census (CC BY 4.0, IMAR/DOP, doi 10.14284/210).
- `data/reports_found.json`: structured records from public competition reports (see `local-reports.md`).

The scripts were written to test methods, not as maintained tools. Paths written as `<scratch>/...` in the notes point to a temporary working folder that no longer exists; only the files listed above were kept.
