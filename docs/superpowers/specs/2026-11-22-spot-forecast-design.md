# Pico spot forecast: design and plan

- **Date:** 2026-11-22
- **Status:** draft, waiting for the owner's approval. Nothing here is built yet. Owner's answers of 2026-11-22 are folded in (section 9).
- **Research behind it:** [`docs/research/`](../../research/README.md) (species, conditions, spots)

Items marked **(call)** are decisions made while writing this document, not ones the owner made. They are listed together in [Calls to check](#calls-to-check).

## 1. Intent

A phone-friendly web app that helps one shore angler, fishing with lures and bait, decide where to fish on Pico. For each spot it answers two questions:

1. **What are the conditions at this spot?** Wind, swell, tide and sea temperature there, and whether it is fishable.
2. **Which species are likely at this spot?** A likelihood for each fish, given the season, the time of day, the spot's geography and the conditions.

The owner asked for the predictions to rest on real data where it exists, for each spot's geography to be looked up and used, and for a geographical map at the top of the page to navigate between spots.

## 2. What exists today

A static installable web app with no build step and no backend. Everything is in `index.html`.

- 5 spots (Madalena, São Roque, Lajes do Pico, Calheta de Nesquim, Ponta da Ilha), each with an approximate position, a facing bearing and a type of "harbour" or "rock".
- 7 species scored 0 to 100 from season, sea temperature, wave height at the spot, wind, time of day, tide movement and spot type (`scoreFor` in `index.html`).
- One set of live conditions from Open-Meteo. Only swell is adjusted per spot, from the spot's facing.
- The official 2026 tide table for Horta is embedded. Other years fall back to the Open-Meteo sea level model.
- Every species number (season curve, temperature band, wave band, weights) is a hand estimate.

The app was created on 2026-11-22 and has not been used in the field.

## 3. What the research found

Full detail and sources are in the research notes. The findings that shape the design:

### Species

- **Season can be grounded.** The Azores statistics service (SREA) publishes monthly fish-auction landings by species and island, including Pico. The full monthly series from January 1994 to October 2026 is in hand (`docs/research/landings.md`). Each species' timing is the same in 1994–2009 as in 2010–2025; amounts change a lot over the years.

  | Species | Months with most landings on Pico |
  |---|---|
  | Anchova (bluefish) | July to September |
  | Írio (amberjack) | June to September |
  | Bicuda (barracuda) | May to November, peak August to October |
  | Veja (parrotfish) | March to September, peak June to July |
  | Sargo (white seabream) | October to February |
  | Serra (Atlantic bonito) | spring to autumn, small and noisy |

  Landings are commercial catch, so they reflect effort, gear and quotas as well as abundance. There is no line for morays.
- **Time of day is measured** for most species: veja strictly by day, morays and conger by night, bicuda at twilight, sargo mostly by day with conflicting studies.
- **Temperature bands, wave bands, tide weights and moon are mostly guesswork.** No study measures shore catch against swell or tide for these species. Tests of solunar tables find no effect. Environmental variables typically explain under 10% of catch variation; site and angler dominate.
- **Two names in the app are wrong for the Azores.** "Bonito" locally means skipjack tuna; *Sarda sarda* is "serra". "Charuteiro" is not an Azores name; *Seriola* is "írio" or "lírio".
- **Occurrence databases (GBIF, OBIS, iNaturalist) are too sparse** for anything beyond a species checklist: 3 to 97 records per species around Pico, mostly from summer surveys.

### Conditions

- **Everything needed can be fetched from the browser with no key and no server.** Open-Meteo for weather and waves, IPMA for warnings and the Pico airport station.
- **Resolution is coarse.** Waves are on an 8 km grid, weather on about 9 km. North and south coasts get different values; neighbouring spots share a cell. Wind funnelling in the channels and shelter behind the mountain are not modelled.
- **Two faults in the current fetch.** Weather for Madalena comes from a land cell on the mountain flank; `cell_selection=sea` fixes this. Some coastal points snap to a wave cell on the wrong coast, so each spot needs a hand-picked offshore sample point.
- **Tides can be computed in the app** from TICON-4 harmonic constants for Horta (CC BY 4.0). A test matched the official 2026 and 2027 tables with a median time error of 1.7 minutes and heights within the table's 0.1 m rounding. The Open-Meteo fallback used today runs about 33 minutes early.
- **Port differences against Horta:** Madalena within 7 minutes, Lajes 0, Cais do Pico (São Roque) about 28 minutes later.
- **Sea temperature does not separate spots.** It differs by 0.1 to 0.2 °C around the island.
- **Satellite water clarity and model currents describe open ocean**, not the water at the rocks.
- **No live wave buoy exists for Pico.**

### Spots

- **43 candidate shore points** were identified with coordinates, facing and exposure computed from the coastline.
- **Only a handful are documented as fished.** No forum, blog, app listing or video naming Pico shore marks was found.
- **Geography that can be derived from open data:** coordinates, facing, which wind and swell directions reach a spot, distance offshore to the 20, 50 and 100 m depths, navigation lights, bathing-water status. Seabed type (rock, sand, mixed) should also come from open data: seabed substrate and habitat maps (for example EMODnet Geology and Seabed Habitats) and the bathymetry grid's slope. How fine these are close to the Pico shore has not been checked.
- **Geography that needs local knowledge:** the exact place on the wall or rocks where Roj stands, depth within casting range, footing and access, lighting, night practicality, snags, species seen there.
- **The app's current facings are off.** By open-water fetch Madalena faces north-west, Lajes south-west, São Roque north-north-east.
- **Two of the candidate spots have records of shore anglers lost:** Manhenha in January 2024 (cause not reported) and São Miguel Arcanjo in October 2021 (went out at night). Neither is in the starting set.

## 4. Goals, non-goals, anti-goals

**Goals**

- A map of the island at the top of the page, used to pick a spot and to see all spots at a glance.
- Per-spot conditions and a per-spot fishability rating.
- Per-spot species likelihoods built from the best evidence available, with the app honest about which inputs are measured and which are estimates.
- Tides correct for any year without a yearly table update.
- A forecast for the coming days, so the owner can choose the day as well as the spot.
- A catch log that sharpens the per-spot ratings over time.
- Works on a phone, installed, with the last loaded data available offline.

**Non-goals for now**

- Boat fishing.
- More than the starting spots (the owner chose to start with the documented spots and add others later).
- Accounts, sync between devices, or any backend.
- A zoomable street or satellite map **(call)**; see 7.2.

**Anti-goals**

- Presenting a guess as a measurement. A likelihood shown as "40%" would claim a calibration that does not exist.
- Implying a spot is safe. The rating describes forecast conditions; it cannot see a rogue set or a wet ledge.
- Automated scraping of Facebook.
- Stating a legal rule that has not been checked against the current text.

## 5. Constraints

From `CLAUDE.md`:

- Static app, no build step, no dependencies.
- Any change to a shipped file needs a `CACHE` bump in `sw.js`; new shipped files go in its `FILES` list.
- Theme tokens on `:root` stay in sync with both dark-mode blocks.
- Photos in `img/` must have EXIF and GPS data stripped.

Others:

- The repository is public, so third-party data committed to it must be licensed for that.
- No API keys, because there is nowhere to keep them secret.

## 6. Approaches

Three ways to build this were considered.

**A. Static app plus data files (chosen, call).** Keep the app as it is, and move the reference data (spots, species, season curves, tide constants) into JSON files under `data/` that `index.html` loads and the service worker caches. Small one-off scripts under `tools/` regenerate those files from the sources (for example season curves from the SREA landings export). The scripts are run by hand and are not a build step. Catch logs stay on the phone.

- For: fits the no-build, no-backend constraint; data can be updated without touching app code; the sources and the derivation are reproducible.
- Against: a few more files to keep in the service worker list; logs do not sync between devices.

**B. Everything inline in `index.html`.** As today, with the new tables pasted into the script.

- For: simplest deployment, matches the current `CLAUDE.md` wording.
- Against: `index.html` is already 62 KB; regenerating data means editing code by hand; hard to see what changed.

**C. Add a small backend.** A scheduled job that fetches forecasts, landings and community reports, and serves a ready-made bundle.

- For: could gather community reports automatically, pre-compute forecasts and sync logs.
- Against: breaks the project's main constraint, adds hosting and upkeep, and the research found nothing it would fetch that the browser cannot fetch itself. Community reports for Pico are too scarce to justify it.

A was chosen because nothing in the research needs a server, and separating data from code makes the evidence easy to update. `CLAUDE.md` will need its "everything lives in `index.html`" line updated.

## 7. Design

### 7.1 Spots

**Starting set:** the five spots already in the app. The owner confirmed this on 2026-11-22; others are added later. The five further spots that the research found documented as fished are listed second, as the first to add. The remaining 33 candidates stay in [`docs/research/spots.md`](../../research/spots.md) as the backlog.

| Spot | Position | Faces | Open ocean from | Offshore to 20 / 50 / 100 m depth | Tide vs Horta | Notes |
|---|---|---|---|---|---|---|
| Madalena breakwater | 38.53622, -28.53302 | 322° NW | SSW–WSW, NW–NE | 735 m / 1.9 km / over 2 km | ±7 min | Shallow rocky shelf. Most exposed to the dominant NW swell. Fishing limits around the islets (see 7.9). |
| Cais do Pico, São Roque | 38.52714, -28.31907 | 46° NE | E–ESE, NNW–N | 160 m / 310 m / 460 m | +28 min | Old quay; very steep bay. Bathing place beside it. Replaces the app's "São Roque". |
| Lajes do Pico breakwater | 38.39780, -28.25637 | 228° SW | S–W | 440 m / 840 m / 1.0 km | 0 | Shallow lava shelf. Two bathing places. In a resource-management area. |
| Calheta de Nesquim port | 38.40257, -28.07973 | 150° SSE | E–SSW | deep within about 250 m | as Lajes | Nearshore depth unknown; deep water close in. |
| Ponta da Ilha | 38.41251, -28.03047 | 147° SSE | ENE–WSW | 290 m / 370 m / 680 m | as Lajes | Low lava point open through 190°. Dangerous in any swell. |

**Next to add (documented as fished):**

| Spot | Position | Faces | Open ocean from | Offshore to 20 / 50 / 100 m depth | Tide vs Horta | Notes |
|---|---|---|---|---|---|---|
| Coxos (São Caetano) | 38.42019, -28.43587 | 183° S | ESE–W | 130 m / 130 m / 240 m | as Lajes | Mapped as a fishing place. Very steep. |
| Pesqueiro Pedro (São Caetano) | 38.42043, -28.43400 | 183° S | ESE–W | 170 m / 170 m / 360 m | as Lajes | Mapped as a fishing place. 170 m from Coxos. |
| Pontinha (São Caetano) | 38.42152, -28.42677 | 179° S | ESE–WSW | 170 m / 170 m / 400 m | as Lajes | Mapped as a fishing place. |
| Manhenha | 38.41025, -28.03748 | 160° SSE | E–WSW | 450 m / 690 m / 1.2 km | as Lajes | Small port and sea pool. Angler lost here in January 2024. Bathing place. |
| São Miguel Arcanjo shore | 38.507, -28.289 (approximate) | 17° NNE | NW–N | 260 m / 490 m / 1.1 km | as Cais do Pico | Open rock. Night-fishing fatality in October 2021. |

Coordinates and geometry come from OpenStreetMap and are inferred from maps, not checked on the ground. Where the three depth distances are equal, the bathymetry grid jumps from the coast straight to deep survey data, so only "deep water within that distance" can be concluded. The three São Caetano marks would share identical forecast conditions.

**Data held per spot:**

- name, coast, coordinates
- type (harbour wall, pier, rock ledge, lava platform)
- facing bearing, open-ocean sector, channel sector (limited fetch)
- offshore sample point for wave data, and one for weather, chosen by hand 5 to 8 km off the correct coast and checked against the cell the service returns
- distance to the 20, 50 and 100 m depths, with a flag where it is unreliable
- tide time offset against Horta
- seabed type near the spot, scraped from open seabed substrate and habitat maps, with its source and resolution; Roj's own description overrides it where he gives one
- local-knowledge fields, empty until Roj supplies them: exact fishing position, depth in casting range, access, lighting, night practicality, snags
- notes: hazards, bathing-place status, restrictions

**Roj's precise positions and local geography.** Roj will give a more exact location for each spot (where on the breakwater, quay or rocks he actually fishes), along with the geography that cannot be scraped: depth in casting range, footing and access, lighting, snags, night practicality and what he has seen caught there. His position replaces the OpenStreetMap one, and facing, sectors, depth distances and seabed are recomputed from it. A spot with a position from Roj is marked as checked on the ground. The seabed is scraped first so Roj only has to confirm or correct it.

**Where this data is edited (call).** In the repository's data files, not in the app. The owner tells Claude what to change (local knowledge, corrected thresholds, a new spot) and the data file is updated and pushed. The only thing entered in the app is the catch log. This avoids building an editing layer on the phone.

### 7.2 Map

The owner asked for a geographical map at the top of the page to navigate by. It replaces the row of spot chips as the main way to choose a spot.

**What it shows.**

- The outline of Pico, with the near shores of Faial and São Jorge for orientation, north up.
- A marker for each spot. Tapping a marker selects the spot and scrolls to its detail.
- Marker colour follows the spot's fishability (7.4) once that exists, always paired with a shape or label so it does not rely on colour alone.
- An arrow each for wind and swell direction, so it is plain at a glance which coasts are sheltered.
- The selected spot is highlighted; with location turned on, the owner's own position is shown.
- A list of the same spots stays below the map for screen readers and for markers that are hard to tap once spots close to each other are added.

**How it is built (call).** An inline SVG drawn from the OpenStreetMap coastline, simplified to a few kilobytes and shipped with the app.

- For: no dependency, works offline, follows the light and dark theme tokens, loads instantly, and the app controls exactly what is drawn on it.
- Against: no zooming into streets or satellite imagery; the coastline is generalised, so it shows where a spot is on the island, not the path down to it.
- The alternative is a tiled map library such as Leaflet with OpenStreetMap tiles. It gives pan, zoom and street detail, but adds a dependency, needs a connection for tiles, and works against the no-dependency and offline constraints. Each spot can carry a link that opens its coordinates in the phone's own maps app, which covers finding the way there.

OpenStreetMap data is under the ODbL, so the app must credit "© OpenStreetMap contributors" near the map. The coastline is already in hand from the spots research (`docs/research/scripts/spots_fetch.py` downloads it).

### 7.3 Conditions per spot

Fetched live, one batched request per service covering all sample points.

| Value | Source | How it becomes per-spot |
|---|---|---|
| Wind speed, direction, gusts | Open-Meteo forecast, `cell_selection=sea` | Value at the spot's weather sample point, then classed as onshore, offshore or cross from the spot's facing |
| Swell and wind-wave height, direction, period | Open-Meteo marine | Value at the spot's wave sample point, reduced by how far the direction lies outside the spot's open sector |
| Sea temperature | Open-Meteo marine | Island-wide value; not varied by spot |
| Pressure and trend, cloud, rain | Open-Meteo forecast | Island-wide |
| Tide height and times | Computed in the app (7.6) | Horta prediction plus the spot's offset |
| Sun and moon | Computed in the app, as today | Island-wide |
| Warnings | IPMA warnings for the central group (`ACE`) | Shown on every spot when active |
| Observed wind | IPMA station at Pico airport | Shown once as a check on the forecast |

The wave reduction replaces today's `effWave`, which uses a single facing and a cosine. The new version uses the spot's open-ocean and channel sectors: full height inside the open sector, a channel-limited height inside the fetch-limited sector, and a small residual outside both, because swell wraps around headlands. The exact curve is left to the builder.

### 7.4 Fishability

A per-spot rating of **Good, Fair, Poor or Unsafe**, separate from species.

- Inputs: effective wave height and period at the spot, wind speed and gusts, whether the wind is onshore, any active warning, and daylight.
- **Unsafe** overrides everything else and is shown first. It applies when the effective swell at the spot passes a threshold, or on an official IPMA warning for the central group **(call, to be confirmed by the owner)**:
  - orange or red sea-state warning: every spot is Unsafe;
  - yellow sea-state warning: spots whose open sector includes the swell direction are Unsafe, and the rest can be no better than Poor;
  - wind warnings of any level: no spot can be better than Poor;
  - green entries in the feed mean no warning and are ignored.
- Spots with a recorded fatality or loss carry a standing hazard note.
- Starting thresholds are the builder's to set and should err on the cautious side; the owner corrects them from experience.
- The app states in plain words that the rating describes the forecast, not the rocks on the day.

### 7.5 Species likelihood

A rating per species per spot, shown as a five-step scale with a one-line reason, not as a percentage **(call)**. Superseded 2026-11-24: a 0–100 score with Likely / Possible / Unlikely words, from the UI review.

The scale is comparable across species **(call)**: five dots means "one of the likeliest catches here now", so a species that is rarely taken from the shore, such as írio, does not sit beside sargo just because it is in season. This needs a base-rate factor per species (how common it is in shore catches), taken from the tiering in the species research. Spots are ranked for a chosen window by fishability first, then by the rating of the species the owner picks, or by the best-rated species if none is picked.

**Factors, in order of weight:**

0. **Base rate.** How often the species is taken from the shore at all, from the species research.
1. **Season.** A 12-month curve per species from the SREA Pico landings for 1994–2025 (`docs/research/data/srea/season_profiles.json`), cross-checked against the published biology. Species landed in tiny amounts on Pico (under about 500 kg a year, for example salema and most morays) use Faial or Azores-wide landings or a biology-based curve instead.
2. **Time of day.** From the measured activity pattern of each species.
3. **Habitat fit.** How well the spot's geography suits the species: steep and deep close in for the pelagics (bicuda, anchova, írio, serra), shallow rocky reef for sargo and veja, harbour walls and lights for night species. This replaces the current "harbour or rock" flag.
4. **Conditions.** A small adjustment only. Sea temperature is used as "warmer or cooler than normal for the date" against the 1991 to 2020 baseline, and only a difference of about 1 °C or more counts. Swell and tide keep a light, clearly labelled "angler lore" weight.
5. **Own catches.** Once the log has enough entries (7.8).

**Changes to the current model:**

- The temperature band stops being a gate. For resident species temperature is mostly a stand-in for season.
- Moon influence is removed from scoring; the phase is still shown.
- Each factor carries an evidence label (measured, estimated, lore) that the "why" line and the "how the scores work" section use.

**Species.** Roj's photo upload (7.8) sets the species list: every species he has caught gets an entry, and he confirms the list. Until that import is done the app keeps the seven current species with corrected names: sargo, veja, bicuda, anchova, írio (was "charuteiro"), serra (was "bonito"), moreia. A current species that is not in Roj's photos is kept only if he says he fishes for it. Each species on the list gets a season curve from the landings where Pico has one, and a biology-based curve otherwise. Mero and badejo are shown as release-only if they appear.

### 7.6 Tides

- Compute the Horta tide in the app from the TICON-4 constituents, using the 27-constituent set without the seasonal SA and SSA terms and a mean level of 0.96 m above chart datum, as validated in the research.
- Apply the per-spot time offset. The +28 minutes for Cais do Pico is the outlier among Pico ports: the same table gives Santo António, 1.4 km along the same coast, as 0. Recheck it against the printed table before use.
- Remove the embedded 2026 table **(call)**. The computed tide matches it closely, works for every year, and avoids the open question of whether embedding a table published under CC BY-NC-ND 4.0 is allowed in a public repository.
- Remove the Open-Meteo sea-level fallback.
- Show the result as a prediction of the astronomical tide; weather can shift the real level.
- This closes the "2027 tide predictions still need adding" item in `CLAUDE.md`.

### 7.7 Forecast

- Hourly data for the next 7 days **(call)**; the wave forecast reaches 10 days and the weather 16, but skill drops off.
- A view that ranks the spots for a chosen day and time window, by fishability first and then by the species the owner selects or by overall likelihood.
- The "best times" timeline stays **(call)**. For the selected spot it shows fishability through the day with sunrise, sunset and tide turns marked, and, when a species is picked, that species' rating through the day. The moon-influence selector goes, because moon leaves the scoring.
- Hand-entered conditions stay as a collapsed "what if" panel **(call)**. It is already built and is useful with no connection. Values typed there apply island-wide and replace the fetched ones until cleared.
- The last successful forecast is kept on the phone and shown, with its age, when offline.

### 7.8 Catch log and other people's catches

**Own log.** Changed 2026-11-24 by the owner: catches are logged through Claude, not in the app. The in-app "My catches" log (photos read on the phone, stored in the browser) was removed.

- Roj tells Claude about a session, with photos if he has them, and Claude adds it to `data/catches.json` using the same steps as the photo archive below. The same privacy rules apply: spot ID only, no coordinates, no photos committed.
- Fields: date and time, spot, species, count, rough size, method, notes, and the conditions at that time.
- Blank sessions are logged too. Without them the log only shows what was caught, never how often.
- Effect on ratings: per spot and species, the logged catch rate nudges the rating once there are enough sessions. The size of the nudge grows with the number of sessions. The exact rule is left to the builder.

**Roj's photo archive.**

Roj's past catch photos are the best record we have of what is caught where and when. They are processed once, in a Claude session, not in the app.

- Roj uploads his catch photos to his own Claude session. They must be unmodified originals: photos sent through WhatsApp or Facebook, and many shared albums, have their location and time removed.
- Claude reads the location, time and camera details from each photo, and identifies the species from the picture. Roj confirms or corrects the species.
- The upload is also how Roj names every species he catches. At the end Claude lists all the species found, Roj confirms the list and adds any he catches but has no photo of, and that list becomes the app's species list (7.5).
- Each photo is placed by its location:
  - **Close to the sea** (within about 300 m of the coastline): matched to the nearest spot in the spot list. A location close to the sea but more than about 500 m from any listed spot is shown to Roj, who names the place, and it can be added to the spot backlog.
  - **Not close to the sea, or no location** (for example the photo was taken at home after the trip): Claude asks Roj where the fish was caught and when. The photo time is kept only if Roj says it is roughly right.
- Photo times are local time (Azores, UTC−1, or UTC in summer) and are converted to UTC before conditions are looked up.
- Each record gets the conditions at the time it was caught:
  - Weather from the Open-Meteo archive.
  - Swell from the Open-Meteo marine history from October 2021, and from ERA5 for older photos.
  - Tide computed from the Horta constants.
  - Sea temperature compared with its 1991–2020 average.
- Records go into `data/catches.json` with spot ID, species, date and time, rough size where it can be seen, and where the place came from (photo location or Roj's answer). Exact coordinates and the photos themselves are not committed. Any photo added to `img/` has its location and other metadata stripped first.
- Photos only record days when something was caught. These records feed the species list per spot and the season curves. They do not feed catch rates, which need the blank sessions from the own log.

**Other people's catches.**

- The owner asked for Facebook and forum reports to be used. The research found no public forum, blog or video corpus for Pico, so the material is in Facebook groups.
- Automated scraping of Facebook is out: it needs a login, breaks Meta's terms and risks the owner's account.
- Instead: the owner pastes or screenshots posts, and they are turned into records of species, spot, date and method. No names or photos of the people posting are kept.
- The conversion happens in a Claude session, not in the app: the owner shares the posts, and Claude writes the records and pushes the file.
- Records go into a `data/reports.json` file and feed the species checklist per spot and the season curves. They do not feed likelihood directly, because people post good days and hide their marks.

### 7.9 Rules and safety notes

Shown per spot or per species where they apply. Each must be checked against the current legal text before the app states it. Until then, a spot where the research found a possible restriction carries only a neutral line, "Local restrictions may apply here; check before fishing", with no rule stated **(call)**.

| Rule | Status |
|---|---|
| Shore angling needs no licence | Read in the law text |
| No fishing within 50 m of official bathing places, 1 June to 30 September | Read in a government proposal that republishes the law; consolidated 2026 text not obtained |
| Minimum sizes: veja 30 cm, sargo 15 cm, garoupa 30 cm, mero 60 cm | Table as of May 2020; later amendments not checked |
| Daily bag limit | **Conflicting readings**: 7.5 kg of fish under 40 cm plus 5 larger fish (2007 decree) against 3.5 kg plus 3 (later proposal text). Unresolved |
| Veja fishing closes on an island when its commercial quota is used up | Read in the October 2026 order; the app cannot know the quota status live |
| Fishing limits around the Madalena islets (Portaria 53/2016) | Seen only as a search summary; the permitted stretch of shore is unknown |
| Three resource-management areas in the Pico Nature Park (Faial–Pico channel off Madalena, Porto das Lajes, Ponta da Ilha) | The park decree was read and contains no angling ban for any of them; any rules made under it were not retrieved |

The Azores government sites refuse automated requests, so these need the owner or a manual browser session.

### 7.10 What the page looks like

```
        wind SW ↗            swell NW ↘
                 ______________________
   Faial )   ___/      ◆ Cais do Pico (São Roque)
            /                              \___
  Madalena ▲          P I C O                   \
            \__                              ___/
               \____________●________●______/   ● Ponta da Ilha
                           Lajes    Calheta de Nesquim

   ● good   ▲ fair   ◆ selected   ✕ unsafe
```

Tapping a marker opens that spot below the map:

```
Cais do Pico · north coast                    Fishable: Good
Wind 14 km/h SW (offshore) · gusts 22
Swell 1.4 m NW, 11 s · about 0.8 m here
Tide rising, high 18:42 (+28 min on Horta) · Sea 19.1 °C (normal)
Deep water close in: about 40 m at 300 m out

Likely now
  sargo    ●●●●○  in season, daytime
  bicuda   ●●○○○  late in its season
  veja     ●●○○○  out of season
  moreia   ●○○○○  feeds at night
```

The map sketch is schematic and the positions are not to scale. Layout and styling are open; these show the content only.

## 8. Phases

Each phase leaves the app working and is worth using on its own.

1. **Correct the foundations.**
   - Rename the two misnamed species.
   - Move spots and species into data files; load the five starting spots with corrected positions, facings and sectors.
   - Compute tides in the app with per-spot offsets; remove the embedded table and the fallback.
   - Fetch weather from sea cells and waves from hand-picked offshore points.
   - The island map at the top of the page as the spot selector.
2. **Per-spot conditions and fishability.**
   - Conditions shown for every spot.
   - Sector-based swell reduction.
   - Fishability rating, warnings, hazard notes.
   - Map markers coloured by fishability, with wind and swell arrows.
   - Seabed type per spot scraped from open seabed maps.
   - Roj's precise positions and local geography loaded into `data/spots.json`, with the derived geometry recomputed (7.1). This needs no app changes and can be done whenever he supplies them.
3. **Evidence-based species model.** Done 2026-11-24 (plan: `docs/superpowers/plans/2026-11-24-phase-3-species-model.md`).
   - Season curves generated from the SREA 1994–2026 landings export by a script in `tools/` (starting from `docs/research/scripts/srea.py`).
   - Time-of-day and habitat factors; conditions demoted; evidence labels.
4. **Forecast.** Done 2026-11-24 (plan: `docs/superpowers/plans/2026-11-24-phase-4-forecast.md`).
   - Seven days, ranked spots for a chosen window, offline copy.
5. **Catch log.**
   - Logging through Claude into `data/catches.json` (the in-app log was removed on 2026-11-24), and the nudge to ratings.
   - Import of pasted community reports.
   - Import of Roj's photo archive into `data/catches.json` (7.8). This can be done before the other phases because it needs no app changes, and its records improve the season curves and species lists per spot. It also sets the app's species list (7.5), so ideally it comes before phase 3.
6. **Rules.**
   - Only after the legal checks in 7.9 are done.

Later: more species, more spots from the backlog.

## 9. Questions for the owner

**Answered on 2026-11-22**

- **How do you fish?** From the shore, with lures and bait.
- **Which fish is in `img/bonito.jpg`?** The owner confirmed the photo when asked. It shows barred markings on the upper sides and no stripes on the belly, which fits Atlantic bonito (*Sarda sarda*, "serra" in the Azores) and not skipjack. The species entry stays *Sarda sarda*; only its Portuguese name changes.
- **Which spots to start with?** The five already in the app.

**Open**

1. **Facebook groups and forums for Azores fishing.** The owner follows some and will provide them. Until then the import of community reports (7.8) stays unscoped.
2. **Local knowledge for each spot:** Roj will supply the exact position he fishes from, plus depth in casting range, access, lighting, snags, whether he would fish it at night, and a check of the scraped seabed type.
3. **The legal items in 7.9** that need a person to open the government sites.

## 10. Calls to check

Decisions made in writing this document that the owner has not confirmed:

- Approach A: data files under `data/` and scripts under `tools/`, with `CLAUDE.md` updated to match.
- "São Roque" becomes the old quay at Cais do Pico, not the commercial port breakwater, whose access may be controlled.
- Spots without a published tide difference use the nearest port's.
- Likelihood is a five-step scale, not a percentage, and is comparable across species through a base-rate factor.
- Which official warnings make a spot Unsafe (7.4). This is a safety decision and most needs the owner's eye.
- Spot data, local knowledge and community reports are edited in the repository through Claude, not in the app.
- Hand-entered conditions are kept as a "what if" panel.
- "Best times" shows fishability and one picked species through the day.
- Before the legal checks, restricted spots show only a neutral "check locally" line.
- Moon is removed from scoring.
- The embedded 2026 tide table is removed in favour of computed tides.
- Forecast horizon of seven days.
- Catch log stored on the phone only, with file export as the backup. Superseded 2026-11-24: catches are logged through Claude into `data/catches.json`.
- Photo catches are stored by spot ID only, with no exact coordinates, because the repository is public. The distances for "close to the sea" (300 m) and "a new place" (500 m) are first guesses.
- The map is a drawn outline of the island shipped with the app, not a zoomable tiled map.
- The species list is whatever Roj confirms from his photo upload; new species are added after the model is rebuilt, not before.

From phase 4 (2026-11-24):

- The window is the start time plus a length of 1, 2, 3 (default), 4 or 6 hours; "Dawn" and "Dusk" set it to sunrise minus 1 hour and sunset minus 2 hours, for 3 hours.
- A spot's fishability for a window is its worst half hour in the window.
- A spot's species score for a window is the best half-hour score among half hours that are not Unsafe, shown with that half hour's time; if every half hour is Unsafe there is no score.
- Spots are ranked with data first, then by window fishability, then by score (no score last), then by name.
- If the window runs past the end of the forecast, the spot is rated from the half hours that have data and says the forecast covers only part of the window; a spot with no data shows "No data" and sorts last.
- The "Fish for" picker (Any species or one species) drives both the ranking and the best-times species line, and is remembered on the phone.
- In best times the moon leaves the timeline completely (selector, scoring and markers); sunrise, sunset and the tides stay, and the moon phase stays in the sun line.
- IPMA warnings are saved with the forecast, so an offline phone still applies them.
- Typed "what if" values are not overwritten by the automatic forecast load on start; only "Load live forecast" or "Use the forecast again" clears them.
- Window half hours past the end of the live forecast count as missing, not as example values.
- Dawn and Dusk round down to 15 minutes.

From phase 3 (2026-11-24):

- Score = 100 × shore catch rate × season × time of day × habitat fit × conditions, clamped to 0–100; Unsafe still caps it at 15.
- Shore catch rates are kept close together because Roj has caught all seven from the shore (owner, 2026-11-24): sargo 1.0, veja 0.9, bicuda 0.85, anchova 0.8, moreia 0.75, írio 0.65, serra 0.6. Every fish can reach at least Possible at its peak.
- Time of day from the research: veja scores 0 after dark; bicuda's night weight drops from 0.9 to 0.4. Labelled measured for sargo, veja, bicuda and moreia, estimated for the others.
- Habitat fit = depth fit (from the distance to the 50 m depth, against each fish's preference for deep or shallow water) × the old harbour / rock weight.
- Conditions: sea temperature counts only at 1 °C or more off the 1991–2020 normal for the date (up to ±10%); swell and tide are angler lore (up to −10% and −5%). Wind leaves the species score.
- Season is labelled measured, with the boat-landings caveat kept.
- The 0–100 score and Likely / Possible / Unlikely words stay; the five-dot scale is not brought back.
- With no forecast, fish are ranked by shore catch rate × season.
- The sea temperature normal is the mean of the six OISST cells around Pico, one value per day; 31 December of a leap year uses day 365.

## 11. Left to the builder

- The swell-reduction curve and the fishability thresholds.
- How the season curve is taken from the 1994–2025 landings (all years, or recent years weighted more), and how it is blended with the biology.
- The habitat-fit scoring from the spot's geography.
- Factor weights in the species model.
- The rule that turns logged sessions into a rating nudge.
- Storage mechanism for the log and the cached forecast.
- Screen layout and the look of the map, within the existing theme tokens.
- The exact offshore sample points, confirmed against the cells the services return.

## 12. Not verified

- Licence of the SREA landings spreadsheets and the 1994–2026 CSV export kept in `docs/research/data/srea/`. They are official public statistics, but no licence statement was seen. Remove them from the repository if that is a concern; the monthly figures used are also in `docs/research/species.md`.
- The +28 minute tide offset for Cais do Pico (see 7.6).
- Rate limits for IPMA and the other keyless services.
- The Faial and Pico shore-angling catch study (Diogo and Pereira 2014) has no open copy; its open companion paper (Diogo and Pereira 2016) was read instead, see `docs/research/recreational-catch.md`.
- Open-Meteo wind was compared with the Pico airport station on one calm day only.
- All spot geometry is derived from maps and has not been checked on the ground, until Roj supplies precise positions.
- Whether open seabed substrate and habitat maps resolve the seabed within casting range of the Pico shore.
