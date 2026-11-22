# Faial-Pico wave buoy vs ERA5: how much does the channel shelter swell?

Analysis run 2026-11-22. Script: `docs/research/scripts/buoy.py` (stdlib only; pandas is not installed).
Outputs: `docs/research/data/buoy/` (`buoy_hourly.csv` 2.6 MB, `shelter_ratios.json`, `monthly_climatology.json`).
Labels as in `conditions.md`: **[V]** verified (computed or seen here), **[I]** inferred, **[U]** unverified.

## 1. Data

**Buoy** [V]. EMODnet Physics ERDDAP dataset `TS_70_6202404_MO_UND` (Copernicus Marine In Situ TAC format),
platform 6202404 "Faial Pico", 38.5877 N 28.5377 W, at the north mouth of the Faial-Pico channel.
`time_coverage` 2012-05-04T00:10Z to 2021-10-10T03:40Z. About 10-minute records. Each timestamp comes as two rows,
one with the wave fields and one with `TEMP`, so they have to be merged.

Variables actually present (from `/erddap/info/TS_70_6202404_MO_UND/index.csv`): `VAVH` (H1/3, m), `VDIR`
(wave direction relative to true north; values behave like "coming from"), `VTZA` (mean zero-crossing period Tz),
`VTMX` (max period), `VZMX` (Hmax), `VTZM` (period of highest wave), `TEMP` (water temperature, no depth given;
a buoy hull sensor, so near-surface [I]), `VGHS` (all NaN). **There is no peak period (`VTPK`) or `VTM02`.**
Every variable has a `_QC` flag (OceanSITES: 1 good, 2 probably good, 4 bad, ...) and a `_DM` flag.

Licence: **Creative Commons Attribution Share-Alike (CC BY-SA)** (dataset `license` attribute). Producer:
University of the Azores, Department of Oceanography and Fisheries (IMAR network), the CLIMAAT buoy network.
Citation attribute: "Data are the property of the producer/owner distributed through EMODnet Physics.
EMODnet Physics and the partners are not responsible for improper use." Suggested credit:
"Faial-Pico wave buoy (WMO 6202404), University of the Azores / CLIMAAT, via EMODnet Physics, CC BY-SA."
Because of share-alike, a redistributed derivative (the hourly CSV here) should carry the same licence.

Download (yearly chunks, ~1 to 3 min each, 92 MB of CSV in total, kept outside the repo in the session scratchpad):

```
https://platform-erddap.emodnet-physics.eu/erddap/tabledap/TS_70_6202404_MO_UND.csv?time,depth,TEMP,TEMP_QC,VAVH,VAVH_QC,VDIR,VDIR_QC,VTZA,VTZA_QC,VTMX,VTMX_QC,VZMX,VZMX_QC,VGHS,VGHS_QC,VTZM,VTZM_QC&time%3E=2014-01-01T00:00:00Z&time%3C2015-01-01T00:00:00Z&orderBy(%22time%22)
```

Hours with valid Hs per year [V]: 2012 4739 (from May), 2013 8386, 2014 8538, **2015 2781, 2016 4216, 2017 3544**,
2018 7286, 2019 6827, 2020 8778, 2021 6772 (to 10 Oct). 61 867 hours in total, about 7 full years equivalent.
Almost every record is flagged 1; only ~130 Hs and ~165 TEMP records were rejected. No values fell outside
Hs 0.05 to 20 m or TEMP 12 to 28 C, and the isolated-spike filter removed nothing.

**ERA5** [V]. Open-Meteo marine API with `models=era5_ocean`, hourly `wave_height, wave_direction,
wave_period, wave_peak_period`, 2012-05-01 to 2021-10-31, one request per point (83 304 hours, no nulls):

```
https://marine-api.open-meteo.com/v1/marine?latitude=38.5877&longitude=-28.5377&hourly=wave_height,wave_direction,wave_period,wave_peak_period&models=era5_ocean&start_date=2012-05-01&end_date=2021-10-31
```

The archive endpoint (`archive-api.open-meteo.com/v1/archive?...&hourly=wave_height`) still returns all nulls, so the
marine endpoint is the one that works. The buoy coordinates snap to the ERA5 cell **38.5, -28.5**, which is the
channel itself (Madalena is 38.535, -28.53): at 0.5 deg that cell is mostly "sea" but its centre is between the
two islands. Two open-ocean neighbours were fetched as a sensitivity check: **39.0, -28.5** (55 km north) and
**38.5, -29.0** (west of Faial).

## 2. Method

- Buoy 10-minute records with QC 1 or 2 averaged to the nearest hour (samples within +-30 min), direction by
  circular mean. ERA5 values are instantaneous on the hour.
- Ratio = buoy Hs / ERA5 Hs, reported two ways: ratio of means over the bin, and the median (and IQR) of hourly
  ratios. Bins use **ERA5** direction (the offshore "incoming" direction the app would know from a model) and
  **ERA5** Hs.
- Monthly climatology: mean of each year-month first (months with fewer than 10 days dropped), then averaged
  across years, so a well-covered year does not dominate. Medians and percentiles pool all hours.

## 3. Results

### 3.1 Overall [V]

| ERA5 reference cell | r (Hs) | r (log Hs) | bias buoy-ERA5 | RMSE | buoy/ERA5, ratio of means | median ratio (IQR) |
|---|---|---|---|---|---|---|
| 38.5, -28.5 (snapped, channel) | 0.85 | 0.88 | -0.28 m | 0.61 m | 0.86 | 0.83 (0.67-1.01) |
| 39.0, -28.5 (open ocean N) | 0.88 | 0.91 | -0.72 m | 0.92 m | 0.70 | 0.69 (0.57-0.81) |
| 38.5, -29.0 (open ocean W) | 0.84 | 0.88 | -0.67 m | 0.93 m | 0.72 | 0.70 (0.57-0.85) |

Mean Hs over the overlap: buoy 1.72 m, ERA5 channel cell 1.99 m, ERA5 N cell 2.44 m. Lagged correlation peaks
when the buoy is compared with ERA5 2 to 3 hours earlier (0.852 vs 0.847 at zero lag, channel cell): a small,
probably physical/model-timing offset, not worth correcting.

Periods are not directly comparable: the buoy gives Tz only. Mean buoy Tz 6.8 s vs ERA5 Tp 10.9 s; median Tz/Tp
= 0.64 (a typical swell-dominated ratio is 0.7 to 0.8 [I], so the buoy sees relatively more short-period sea).

### 3.2 By ERA5 mean wave direction (8 sectors) [V]

Median hourly ratio buoy/ERA5 (IQR), and ratio of means, against each reference cell.
Hours shown for the snapped cell.

| ERA5 dir | hours | vs channel cell 38.5,-28.5 | ratio of means | vs open N 39.0,-28.5 | vs open W 38.5,-29.0 |
|---|---|---|---|---|---|
| N | 10 110 | 1.03 (0.89-1.15) | 1.05 | 0.81 | 0.89 |
| NE | 3 870 | 0.80 (0.70-0.91) | 0.82 | 0.64 | 0.72 |
| E | 2 120 | 0.63 (0.55-0.72) | 0.66 | 0.56 | 0.59 |
| SE | 1 227 | 0.59 (0.53-0.68) | 0.60 | 0.56 | 0.54 |
| S | 1 955 | 0.57 (0.51-0.65) | 0.57 | 0.54 | 0.51 |
| SW | 5 562 | 0.60 (0.53-0.67) | 0.60 | 0.51 | 0.50 |
| W | 16 488 | 0.73 (0.64-0.84) | 0.74 | 0.57 | 0.58 |
| NW | 20 535 | 0.99 (0.87-1.11) | 1.02 | 0.76 | 0.81 |

16-sector detail against the channel cell (median ratio, and the buoy's own mean direction):

| ERA5 from | 0 | 22.5 | 45 | 67.5 | 90 | 112.5 | 135 | 157.5 | 180 | 202.5 | 225 | 247.5 | 270 | 292.5 | 315 | 337.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ratio | 1.02 | 0.94 | 0.79 | 0.67 | 0.62 | 0.62 | 0.59 | 0.58 | 0.57 | 0.58 | 0.59 | 0.64 | 0.71 | 0.86 | 1.00 | 1.06 |
| buoy dir | 4 | 8 | 10 | 18 | 19 | 19 | 11 | 347 | 312 | 296 | 307 | 330 | 337 | 341 | 346 | 353 |

The buoy direction stays between about 300 and 20 deg whatever ERA5 says: when the ocean swell is from the
south-west, what the buoy measures arrives from WNW to NW. Waves from S/SW only reach the north mouth after
wrapping round Faial or Pico (or are local wind sea), at roughly half to 60 % of the offshore height.

### 3.3 By ERA5 Hs class (channel cell; open-N cell in the last column) [V]

| ERA5 Hs | hours | ERA5 mean | buoy mean | ratio of means | median ratio (IQR) | median ratio vs open N |
|---|---|---|---|---|---|---|
| < 1 m | 7 129 | 0.84 | 0.64 | 0.76 | 0.74 (0.63-0.87) | 0.61 |
| 1-2 m | 28 938 | 1.47 | 1.25 | 0.85 | 0.84 (0.68-0.99) | 0.68 |
| 2-3 m | 16 491 | 2.42 | 2.13 | 0.88 | 0.88 (0.69-1.06) | 0.70 |
| 3-4 m | 6 772 | 3.40 | 3.01 | 0.88 | 0.89 (0.67-1.08) | 0.73 |
| 4-6 m | 2 442 | 4.57 | 3.84 | 0.84 | 0.82 (0.64-1.04) | 0.73 |
| > 6 m | 95 | 6.43 | 4.87 | 0.76 | 0.76 (0.56-0.86) | 0.62 |

The ratio is fairly flat with height; most of the variance is direction. Small seas are relatively more reduced
(sheltered short wind sea, or ERA5 being too high in calms [I]). The drop above 6 m rests on few hours.

Direction x height (channel cell, median ratio; hours in brackets) is in `shelter_ratios.json` (`by_dir8_x_hs`).
Notable: N and NW ratios rise from 0.93-0.98 below 2 m to 1.04-1.12 above 2 m (the north mouth is fully open
and slightly focuses big northerly swell [I]); S/SW/W stay at 0.51-0.75 at all heights.

### 3.4 Monthly climatology at the buoy [V]

Hs means are averages of monthly means; "years" = number of years with at least 10 days of data that month.

| Month | Hs mean (m) | Hs median | Hs p90 | P(Hs > 2 m) | years | Water temp mean (C) | range of monthly means | hourly p05-p95 |
|---|---|---|---|---|---|---|---|---|
| Jan | 2.07 | 1.84 | 3.45 | 0.42 | 7 | 15.7 | 15.3-16.0 | 15.1-16.2 |
| Feb | 2.36 | 2.21 | 3.77 | 0.56 | 8 | 15.3 | 14.6-15.8 | 14.3-15.9 |
| Mar | 2.00 | 1.85 | 3.27 | 0.44 | 8 | 15.2 | 14.9-15.7 | 14.6-15.9 |
| Apr | 1.91 | 1.70 | 3.20 | 0.36 | 8 | 15.4 | 14.9-16.0 | 14.6-16.1 |
| May | 1.45 | 1.36 | 2.27 | 0.16 | 8 | 16.6 | 15.9-17.3 | 15.4-17.8 |
| Jun | 1.08 | 0.96 | 1.71 | 0.06 | 7 | 18.7 | 17.7-19.9 | 17.1-20.9 |
| Jul | 0.89 | 0.82 | 1.46 | 0.02 | 8 | 20.8 | 20.4-21.2 | 19.6-22.1 |
| Aug | 0.97 | 0.85 | 1.57 | 0.03 | 8 | 22.3 | 21.7-22.8 | 21.3-23.5 |
| Sep | 1.47 | 1.28 | 2.52 | 0.18 | 6 | 21.8 | 21.2-22.8 | 20.2-23.4 |
| Oct | 2.12 | 1.88 | 3.62 | 0.45 | 6 | 20.1 | 19.5-20.8 | 18.7-21.4 |
| Nov | 2.24 | 2.06 | 3.81 | 0.52 | 7 | 18.1 | 17.7-18.5 | 16.9-18.9 |
| Dec | 2.34 | 2.16 | 3.71 | 0.57 | 7 | 16.6 | 15.8-17.1 | 15.6-17.7 |

Water temperature: coldest late Feb to Apr (about 15.2 C), warmest August (22.3 C), annual range about 7 C.
This is a nearshore in-situ series and can be cross-checked against the OISST climatology in the appendix of
`conditions.md` [U, not compared here].

## 4. Caveats

- **Location.** The buoy is at the *north mouth* of the channel, not inside it and not at any fishing spot. It is
  open to N and NW and shadowed from S, SW, and partly W by Faial and Pico. Madalena, ~6 km further south inside
  the channel, is likely *more* sheltered from N/NW than the buoy and similarly or more sheltered from W/SW [I].
  The ratios are a measured shelter factor for this point, an informed prior for nearby channel spots, and not
  applicable to Pico's south or east coasts.
- **The reference matters.** The ERA5 cell the buoy snaps to (38.5, -28.5) is itself in the channel, and ERA5's
  wave model already damps waves near unresolved islands [I], so against it the buoy looks only ~15 % lower.
  Against genuinely open-ocean cells the buoy is ~30 % lower. Use the open-ocean numbers when the input is a
  clean offshore value.
- **Gaps.** 2015 to 2017 are poorly covered (2.8 to 4.2 k hours per year) and September/October have only 6 years.
- **Period.** No peak period in the buoy data, so swell period cannot be validated; Tz vs Tp is only indicative.
- **Directions** are ERA5 mean wave direction (all components combined), so a mixed sea (NW swell plus SW
  wind sea) is binned by whichever dominates the mean.
- **No overlap with the app's actual forecast model.** Open-Meteo's default marine history (MFWAM 0.08 deg /
  `best_match`) starts in October 2021, the month the buoy record ends. So these ratios calibrate ERA5 (0.5 deg),
  not MFWAM. MFWAM's 8 km grid partly resolves Faial and Pico, so its channel cells already include some
  shelter; multiplying MFWAM output by these factors would double-count it [I]. The factors are only clean
  when applied to a coarse, open-ocean input (ERA5-like: `ecmwf_wam025` or `ncep_gfswave025` at an offshore cell
  such as 38.75, -28.5 or 39.0, -28.5). The CLIMAAT Graciosa buoy (6202400, still reporting) does overlap with
  Open-Meteo history and could be used to check MFWAM's open-ocean bias, but not channel shelter.

## 5. What this changes for the app

1. **A per-direction shelter factor for channel/north-mouth spots (Madalena, the Faial-facing west coast).**
   Applied to an *open-ocean* offshore Hs and *offshore* mean direction, measured at the buoy (vs ERA5 39.0, -28.5,
   rounded; W-cell values in brackets):

   | Offshore from | N | NE | E | SE | S | SW | W | NW |
   |---|---|---|---|---|---|---|---|---|
   | factor | 0.8 (0.9) | 0.65 (0.7) | 0.55 (0.6) | 0.55 | 0.55 (0.5) | 0.5 | 0.55 (0.6) | 0.75 (0.8) |

   For a finer curve use the 16-sector row in 3.2 (against the channel cell) scaled by about 0.8, or interpolate.
   Treat it as an upper bound for spots inside the channel (more sheltered than the buoy) [I].
2. **Don't stack factors.** If the app keeps using MFWAM (`best_match`) at a hand-picked channel cell, use at most a
   mild extra reduction for S-SW-W (where the north mouth is clearly in the lee) and none for N/NW, until the
   factor can be checked against a model whose history overlaps an observation.
3. **Direction rewrite.** Near the channel, waves arrive from WNW-N even when the offshore swell is SW. A spot
   exposure check should use the *local* direction (about 300-20 deg here), not the offshore one.
4. **Seasonal baseline.** "Normal" Hs at the channel mouth is ~0.9-1.1 m in Jun-Aug and 2.0-2.4 m Oct-Feb; more than
   half of Nov-Feb hours exceed 2 m. The monthly table (and water temperature 15-22 C) can feed a
   "rough / normal for the month" label or a seasonal default when the forecast is offline.
