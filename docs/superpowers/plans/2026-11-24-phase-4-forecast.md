# Phase 4: Forecast — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rank the five spots for a chosen day and time window (fishability first, then a picked species or the best species), rebuild "Best times" as fishability and species rating through the day, and finish the offline and "what if" behaviour from spec 7.7.

**Architecture:** Everything stays in `index.html` (one IIFE, ES5 style: `var`, `function`, string-built HTML; match it). New logic is built from the existing per-moment pipeline — `spotCond(spot, i, when)` → `rate()` → `scoreFor()` — evaluated at many moments through a `whenAt(utcMs)` helper. Tests are a browser test file loaded only when the page is opened with `?test`, driven headless with `playwright-cli`.

**Tech Stack:** Plain HTML/CSS/ES5 JS, no build, no dependencies. Open-Meteo hourly data already fetched for 7 days (`loadLive`).

**Spec:** `docs/superpowers/specs/2026-11-22-spot-forecast-design.md`, section 7.7 (Forecast), with 7.4 (Fishability) and 7.5 (ranking rule) for context. Read 7.7 before starting.

## What already exists (do not rebuild)

- 7-day hourly fetch: `loadLive()` (`forecast_days=7`), stored in `state.live` and saved to `localStorage['pico-live-v1']`; `restoreLive()` reloads it if under 7 days old.
- Per-moment conditions: `readWhen()` returns `{y, month, d, t, utc, local}`; `spotCond(spot, i, when)` returns `c` with `c.rating.level` (0 Good, 1 Fair, 2 Poor, 3 Unsafe), `c.raw`, `c.eff`, `c.phase`, `c.tide`, `c.sun`, or `null` when there is no data for that moment.
- Species score: `scoreFor(sp, spot, ctx)` → `{score 0-100, why}`; `ctx(cc)` is currently a nested function inside `render()`.
- "Best times" (`renderBest`) scores half hours from tide, light and moon, with a "Moon influence" select (`#f-moon`).
- "Enter conditions by hand" panel (`#whatif`), `state.source` = `'live' | 'manual' | 'example'`.

## Decisions made in this plan (calls, to list for the owner)

1. **Window** = start time (the existing Time field) plus a length select: 1, 2, 3 (default), 4 or 6 hours. "Dawn" and "Dusk" buttons set it to sunrise − 1 h for 3 h and sunset − 2 h for 3 h.
2. **A spot's fishability for a window is its worst half hour** in the window (cautious).
3. **A spot's species score for a window is the best half-hour score among half hours that are not Unsafe**, shown with that half hour's time. If every half hour is Unsafe there is no score.
4. **Ranking:** spots with data first; then by window fishability level ascending; then by score descending (no score sorts last); then by name.
5. **Partial data** (window runs past the end of the forecast): rate from the half hours that have data and say "The forecast covers only part of this window." A spot with no data at all shows "No data" and sorts last.
6. **Species picker** "Fish for" (Any species, or one species) drives both the ranking and the best-times species line. It is remembered on the phone (`localStorage['pico-prefs-v1']`); an unknown saved id falls back to Any.
7. **Best times**: moon leaves the timeline completely (selector, scoring, moon markers). Markers kept: sunrise, sunset, high and low tides. Moon phase stays in the sun line.
8. **IPMA warnings are saved with the forecast** so an offline phone still applies them (they carry their own start and end times).
9. **Typed "what if" values are not overwritten by the automatic forecast load on start**; only the "Load live forecast" button or the new "Use the forecast again" button clears them.

## Global Constraints

- No build step, no dependencies, no new runtime network calls.
- ES5 style inside the existing IIFE (`var`, `function`, no arrow functions, no template literals), matching surrounding code.
- Every commit that changes a shipped file bumps `CACHE` in `sw.js` by one (`pico-fc-v22` → `v23` → …). `tests/` is not shipped and is not added to `FILES`.
- Theme colours only through existing tokens (`--good`, `--warn`, `--bad`, `--muted`, `--accent`, `--surface`, `--line`); if a new token is needed, add it to `:root` and both dark-mode blocks.
- Copy: plain words, British spelling, sentence case, no exclamation marks. Wind in Beaufort forces as elsewhere. Times in Azores local time `HH:MM` via existing helpers (`hm`, `hmLocal`).
- Layout must work at 360 px wide with no horizontal page scroll.
- The rating disclaimer stays: the rating describes the forecast, not the rocks on the day.
- Commit messages: one plain sentence, like the existing history (e.g. "Rank spots for a chosen time window"). Work on branch `phase-4-forecast`.

## Review Focus

1. **Window past the end of the forecast**: a spot must not look Good from one surviving half hour without saying so → partial-data note (Task 2 test `partial window`).
2. **Window crossing midnight or a clock change**: times and dates of later half hours must come from `whenAt`, not by adding minutes to the start's local fields (Task 1 test `whenAt across DST`, Task 2 test `window across midnight`).
3. **Island-wide warning makes every spot Unsafe**: ranking must still list all five, all Unsafe, with no species score, and never present a "best" spot as fishable (Task 2 test `all unsafe`).
4. **Manual (what-if) mode with no live forecast**: ranking and timeline must work from the typed values for every half hour (Task 2 test `manual mode`, Task 3 test `timeline manual`).
5. **Saved forecast hours old, phone offline**: the status must show the age, and saved warnings must still apply (Task 4 tests).

---

### Task 1: Test harness and `whenAt`

**Files:**
- Modify: `index.html` (script bootstrap near the end; new helper next to `readWhen`)
- Create: `tests/forecast.test.js`, `tests/README.md`
- Modify: `sw.js` (CACHE bump)

**Interfaces:**
- Produces:
  - `var TEST = /[?&]test\b/.test(location.search);` — in test mode: do not register the service worker, do not call `loadLive()` from `init()`, and after `init()` append `<script src="tests/forecast.test.js">`.
  - `whenAt(utcMs) -> {y, month, d, t, utc, local}` with exactly the shape of `readWhen()` (`local` = `'YYYY-MM-DDTHH:MM'` Azores time), built from `azParts(new Date(utcMs))`.
  - `window.pico` (always set at the end of `init()`), an object exposing: `SPOTS, SPECIES, state, whenAt, readWhen, spotCond, scoreFor, render, setStatus` and every function later tasks add (each task adds its own).
  - In `tests/forecast.test.js`: `test(name, fn)`, `eq(actual, expected, msg)`, `ok(cond, msg)`, and `liveFixture(startUtcMs, hours, fn)` where `fn(spotIdx, hourIdx)` returns `{wave, waveDir, per, wind, windDir, gust, sst}` and the result is a `state.live`-shaped object `{at: Date.now(), m: [5 hourly objects], w: [5 hourly objects]}` with `time` arrays in unix seconds and every field `rawFor` reads (swell fields copy wave fields; `wind_wave_height` 0). The file runs all tests after a microtask and sets `window.picoTestResult = {pass, fail, failures: [{name, msg}]}` and also writes it into a `<pre id="test-out">` appended to the body.

- [ ] **Step 1: Write the failing tests** in `tests/forecast.test.js`:
  - `whenAt matches readWhen`: set `#f-date`=`2026-11-24`, `#f-time`=`07:30`; `eq(JSON.stringify(pico.whenAt(pico.readWhen().utc)), JSON.stringify(pico.readWhen()))`.
  - `whenAt across DST`: Azores clocks go back at 01:00 local on 2026-10-25 (UTC−0 → UTC−1). `eq(pico.whenAt(Date.UTC(2026,9,25,0,30)).local, '2026-10-25T00:30')` and `eq(pico.whenAt(Date.UTC(2026,9,25,2,30)).local, '2026-10-25T01:30')`.
  - `fixture feeds spotCond`: with `state.live = liveFixture(Date.UTC(2026,10,24,0), 48, () => ({wave:0.5, waveDir:315, per:9, wind:8, windDir:90, gust:12, sst:19}))`, `state.source='live'`, `spotCond(SPOTS[0], 0, whenAt(Date.UTC(2026,10,24,10)))` is not null and `c.raw.src === 'live'`.
- [ ] **Step 2: Run and see it fail.** `python3 -m http.server 8000 &` then `playwright-cli open 'http://localhost:8000/?test'` and `playwright-cli eval "() => JSON.stringify(window.picoTestResult)"`. Expected: `undefined` or failures (no `whenAt`, no test loader).
- [ ] **Step 3: Implement** `TEST`, the test loader, `whenAt`, and `window.pico`. Write `tests/README.md` (5 lines: how to run the two commands above and what the result object means).
- [ ] **Step 4: Run again.** Expected: `{"pass":3,"fail":0,...}`. Also open `http://localhost:8000/` (no `?test`) and confirm with `playwright-cli eval "() => !!document.getElementById('test-out')"` → `false`.
- [ ] **Step 5: Commit** — bump `CACHE` to `pico-fc-v23`; `git add index.html sw.js tests/`; message "Add a browser test harness and a whenAt helper".

### Task 2: Species picker and ranked spots for a time window

**Files:**
- Modify: `index.html` (When panel markup, new "Best spots" section right after the When panel, CSS, `ctx` lifted out of `render()`, new functions, `render()`, `init()`)
- Modify: `tests/forecast.test.js`, `sw.js`

**Interfaces:**
- Consumes: `whenAt`, `spotCond`, `scoreFor`, `window.pico`, `liveFixture`.
- Produces:
  - `ctxFor(when, cc) -> ctx` — the current nested `ctx(cc)` lifted to top level, same body, taking `when` explicitly. `render()` calls it.
  - Markup: in the When panel, `<select id="f-len">` (options 1,2,3,4,6; label "For", option text "1 hour", "2 hours"…; default 3), `<select id="f-fish">` (label "Fish for"; first option value `""` "Any species", then one per `SPECIES` in file order, text `sp.name`), buttons `#b-dawn` "Dawn" and `#b-dusk` "Dusk". Section `<section aria-labelledby="h-rank">` with `<h2 id="h-rank">` and `<ol class="ranked" id="ranked">`.
  - `state.fish` (`''` or a species id), `state.len` (hours, number). Saved to and read from `localStorage['pico-prefs-v1']` as `{fish, len}`, wrapped in try/catch; unknown fish id → `''`.
  - `windowSamples(fromUtc, hours) -> [utcMs]` — every 30 minutes from `fromUtc`, `hours*2` values, end exclusive.
  - `spotWindow(spot, i, fromUtc, hours, fishId) -> {level: 0-3|null, worstWhy: string|null, samples: n, missing: n, score: number|null, sp: species|null, at: utcMs|null}` — `level` is the max `rating.level` over samples with data (null if none); `worstWhy` is `rating.why[0]` of the first sample at that level when level ≥ 1; `score/sp/at` is the best `scoreFor(sp, spot, ctxFor(w, c)).score` over non-Unsafe samples, for species `fishId` or, when `fishId` is `''`, over all species.
  - `rankSpots(fromUtc, hours, fishId) -> [{spot, i, ...spotWindow fields}]` sorted per call 4.
  - `renderRanked(when)` writes `#ranked` and the heading text `Best spots, <Ddd D Mmm> HH:MM–HH:MM` (end time = start + hours; append "next day" when the end falls on a later date). Each `<li>` holds a `<button type="button" class="spotrow" data-spot="<id>">` (the existing document click handler selects the spot) showing: rank number, spot name, badge `l<level>` with `LEVELS[level]` (or `lx` "No data"), a line `<sp.name> <score> at HH:MM` (or "No species score: unsafe for the whole window" when score is null and level is 3), `worstWhy` when level ≥ 1 prefixed by "At worst: ", and the partial note when `missing > 0 && samples > missing`.
  - `#b-dawn`: set `#f-time` to sunrise − 60 min rounded down to 15 min and `state.len = 3`; `#b-dusk`: sunset − 120 min, `state.len = 3`. Use `sunTimes` for the chosen date at the selected spot. Then `render()`.

- [ ] **Step 1: Write the failing tests** (each sets its own fixture and `state.source`, then calls `pico.rankSpots`):
  - Calm in these tests means `{wave:0.2, waveDir:315, per:8, wind:8, windDir:90, gust:12, sst:19}`, and windows are in daylight (12:00 UTC = 11:00 Azores in November), so the after-dark wave cut does not apply. Half hours read the nearest forecast hour (`Math.round`), so hh:30 reads hour hh+1.
  - `ranks by fishability then score`: fixture where spot index 2 has wave 2.5 (Unsafe) at all hours, spot 0 has wind force 6 and gusts force 7 (`wind: 45, gust: 55`, Poor), others calm. `rankSpots(Date.UTC(2026,10,24,12), 3, '')`: last entry's `spot.id === SPOTS[2].id` with `level === 3` and `score === null`; entry with `SPOTS[0]` has `level === 2`; first three entries have `level === 0` and are sorted by `score` descending.
  - `worst half hour wins`: spot 1 calm except hour 13 (UTC) wave 2.5; window 12:00 UTC for 3 h → spot 1 `level === 3`; `at` is neither 12:30 nor 13:00 UTC (the two half hours that read hour 13).
  - `picked species`: `rankSpots(…, 3, SPECIES[0].id)` → every entry with a score has `sp.id === SPECIES[0].id`.
  - `partial window`: fixture of 24 hours (indices 0–23) from 2026-11-24 00:00 UTC; window from 22:00 UTC for 3 h → `samples === 6`, `missing === 3`, `level` not null; rendered `#ranked` text contains "covers only part".
  - `window across midnight`: window from 23:00 Azores time on 2026-11-24 for 3 h renders a heading containing "23:00–02:00" and "next day".
  - `all unsafe`: set `state.warn = [{awarenessLevelID:'red', awarenessTypeName:'Agitação Marítima', idAreaAviso:'ACE', startTime:'2026-11-24T00:00:00', endTime:'2026-11-25T00:00:00'}]` → all 5 entries `level === 3`, all `score === null`.
  - `manual mode`: `state.live = null; state.source = 'manual'` (form defaults) → 5 entries, none with `level === null`.
  - `bad saved fish`: `localStorage['pico-prefs-v1'] = '{"fish":"nosuchfish","len":3}'`, call the prefs loader → `state.fish === ''`.
- [ ] **Step 2: Run** (Task 1 commands). Expected: these 8 fail, earlier 3 pass.
- [ ] **Step 3: Implement** the interfaces above. Style `.ranked` like `.spotlist` rows (reuse `.spotrow`); the rank number in `var(--font-data)`.
- [ ] **Step 4: Run.** Expected: all pass. Screenshot at 360×800 (`playwright-cli resize 360 800`, `playwright-cli screenshot`) without `?test`, with the fixture loaded via `eval`, and check there is no horizontal scroll: `eval "() => document.documentElement.scrollWidth <= innerWidth"` → `true`.
- [ ] **Step 5: Commit** — CACHE `v24`; "Rank spots for a chosen time window, with a species picker".

### Task 3: Best times as fishability and species through the day

**Files:**
- Modify: `index.html` (`renderBest`, Best times markup, `init()`, the "How the ratings and scores work" list, CSS), `tests/forecast.test.js`, `sw.js`

**Interfaces:**
- Consumes: `whenAt`, `spotCond`, `ctxFor`, `scoreFor`, `state.fish`, `state.len`.
- Produces:
  - `dayTimeline(spot, i, y, month, d, fishId) -> [{utc, t, level: 0-3|null, score: number|null}]` — one cell per 30 min from local midnight of that date to the next local midnight (46, 48 or 50 cells on clock-change days; compute both midnights with the `readWhen`-style local-to-UTC conversion and step 30 min in UTC). `t` = local minutes from `whenAt`. `score` only when `fishId` is set and the cell has data; `null` otherwise.
  - `renderBest(when, spot, i)` replaces the old one. Contents in order: eyebrow "Through the day at <spot.name>"; a summary list: when a fish is picked, the top 3 windows of that species (reuse the existing run-finding logic on `score`, treating Unsafe or no-data cells as 0), each "HH:MM–HH:MM  <sp.name> <peak score>  <fishability label>"; when no fish is picked, stretches of equal level, e.g. "06:00–14:30 Good" (merge consecutive cells with the same level; skip null stretches). Then a fishability strip (`<div class="strip">`, one cell per entry, class `l0`–`l3` or `lx`); when a fish is picked, the existing `.bars` with heights from `score` and colour classes from `labelOf`; cells inside the chosen window get class `inwin`, the cell containing the chosen time gets `sel`. An axis 00/06/12/18/24. Key times: sunrise, sunset, high and low tide (existing code, moon removed). A note: "Fishability for each half hour from the forecast. Pick a fish above to see its score through the day."
  - Remove `#f-moon` and its listener, the moon weighting, the moon key times, and `moonEvents`, `moonPos`, `MOONNAME` if nothing else calls them (`grep` first). Keep `moonInfo` and the sun line.
  - How-to list: replace the sentence "Moon phase is shown for planning and feeds the best-times timeline, but does not change the species scores." with "Moon phase is shown for planning only; it does not change any rating or score."

- [ ] **Step 1: Write the failing tests:**
  - `timeline has 48 cells`: `dayTimeline(SPOTS[0], 0, 2026, 11, 24, '').length === 48`, first cell `t === 0`, last `t === 1410`.
  - `timeline on clock change`: `dayTimeline(SPOTS[0], 0, 2026, 10, 25, '').length === 50` (Azores clocks go back at 01:00 UTC that day: local 00:30 occurs twice).
  - `timeline levels follow forecast`: calm fixture except wave 2.5 for hours 12 and 13 UTC at spot 0 → cells at 12:00, 12:30 and 13:00 UTC have `level === 3`; the cell at 16:00 UTC has `level === 0`.
  - `timeline species scores`: with `fishId = SPECIES[0].id`, cells with data have numeric `score`; with `''`, every `score === null`.
  - `timeline manual`: `state.live = null; state.source = 'manual'` → every cell has a non-null `level`.
  - `no moon selector`: `document.getElementById('f-moon') === null`, and `#besttimes` text does not contain "Moon".
- [ ] **Step 2: Run.** Expected: these 6 fail, earlier tests pass.
- [ ] **Step 3: Implement.** Strip cells: height 14 px, same flex layout as `.bars`, colours `.l0` `--good`, `.l1` `--warn`, `.l2` `--bad`, `.l3` `--bad` with a diagonal stripe (`repeating-linear-gradient` using `--bad` and `--surface`), `.lx` `--line`. `.inwin` adds a 3 px `--accent` underline (border-bottom) so it shows on both strip and bars.
- [ ] **Step 4: Run.** Expected: all pass. Screenshot at 360 px with a fish picked and with Any species; check the width test as in Task 2.
- [ ] **Step 5: Commit** — CACHE `v25`; "Best times: fishability and the picked fish through the day; moon removed".

### Task 4: Offline copy with its age, saved warnings, and clearing "what if"

**Files:**
- Modify: `index.html` (`setStatus`, `loadLive`, `restoreLive`, what-if panel markup and text, `init()`), `tests/forecast.test.js`, `sw.js`

**Interfaces:**
- Consumes: `state`, `setStatus`, `render`.
- Produces:
  - `statusText(source, liveAt, nowMs) -> string`: `'live'` and age < 90 min → `"Forecast loaded HH:MM"`; `'live'` and older → `"Forecast from <Ddd> HH:MM, <N> h old"` (N rounded, Azores time); `'manual'` → `"Entered by hand"`; otherwise the existing texts. `setStatus` uses it and adds class `stale` to `#status` when age ≥ 24 h (style: `color: var(--bad)`).
  - Warnings saved to `localStorage['pico-warn-v1']` as `{at, list}` whenever fetched; `restoreWarn()` at start loads them if `at` is under 48 h old. `loadLive` failure message for a saved forecast becomes "Could not reach Open-Meteo, so the forecast saved on this phone <N> h ago is shown." (or "… at HH:MM" when under 90 min).
  - `loadLive(explicit)`: the automatic call from `init()` passes `false` and does not switch `state.source` from `'manual'` to `'live'`; the button passes `true` and does.
  - Button `#b-clear` "Use the forecast again" in the what-if panel's `.actions`, shown only when `state.source === 'manual' && state.live`; click sets `state.source = 'live'` and renders. What-if intro text becomes: "For when there is no connection, or to try "what if". These open-sea values are applied to every spot, then reduced for each spot's shelter. They replace the forecast until you press "Use the forecast again" or load the live forecast."

- [ ] **Step 1: Write the failing tests:**
  - `status fresh`: `statusText('live', now - 30*60000, now)` starts with "Forecast loaded ".
  - `status old`: `statusText('live', now - 5*3600000, now)` ends with "5 h old".
  - `stale class`: with `state.live.at = Date.now() - 30*3600000`, `state.source='live'`, after `render()`, `#status` has class `stale`.
  - `saved warnings restore`: write `pico-warn-v1` with `{at: Date.now(), list: [the red warning from Task 2]}`, set `state.warn = null`, call `restoreWarn()` → `state.warn.length === 1`; and with `at` 49 h ago → `state.warn === null`.
  - `clear what-if`: with a fixture as `state.live` and `state.source = 'manual'`, after `render()` `#b-clear` is visible; click it → `state.source === 'live'` and the button is hidden.
  - `auto load keeps manual`: stub `window.fetch` to resolve fixture JSON for both Open-Meteo URLs and `[]` for IPMA, set `state.source='manual'`, call `loadLive(false)`, await → `state.source === 'manual'`; `loadLive(true)` → `'live'`. Restore `fetch` after.
- [ ] **Step 2: Run.** Expected: these 6 fail.
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run.** Expected: all tests pass. Then a real-network smoke check: open `http://localhost:8000/` (no `?test`), wait for the forecast, `eval "() => document.getElementById('status').textContent"` starts with "Forecast loaded", and `#ranked` has 5 items.
- [ ] **Step 5: Commit** — CACHE `v26`; "Forecast offline: show its age, keep warnings, and let typed values be cleared".

### Task 5: Docs

**Files:** `README.md` (one paragraph on the ranking and best times; how to run tests), `CLAUDE.md` (one line: tests run with `?test`, see `tests/README.md`), spec section 8 phase 4 marked done with the date and a pointer to this plan, and the calls above appended to spec section 10. No `sw.js` bump (not shipped files).

- [ ] **Step 1:** Edit the four files.
- [ ] **Step 2:** Run the full test page once more; all pass.
- [ ] **Step 3: Commit** — "Document phase 4: forecast ranking, best times and tests".
