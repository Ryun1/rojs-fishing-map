# Pico Fishing Forecast

A static, installable PWA (no build step) giving a fishing forecast for Pico, Azores: current conditions, a spot selector, ranked species per spot and a species-by-spot grid.

## Files

| File | Purpose |
|---|---|
| `index.html` | The whole app: markup, CSS and JS, including the tide calculation for Horta |
| `manifest.webmanifest` | PWA manifest (name, icons, theme) |
| `sw.js` | Service worker: caches app files for offline use; Open-Meteo requests always go to network |
| `icon-192.png`, `icon-512.png` | App icons |
| `img/` | Species photos (crops of own catch photos, location/date metadata removed; the moray is a drawing) |

## Ranking and best times

In the When panel, pick a start time, a length (1 to 6 hours, or the Dawn and Dusk buttons) and a fish, and "Best spots" ranks the five spots for that window. A spot is rated by its worst half hour. An orange or red sea warning makes every spot Unsafe; a yellow sea warning makes spots open to the swell Unsafe and the rest no better than Poor; any wind warning makes every spot no better than Poor. "Best times" shows fishability and the chosen fish through the day, with sunrise, sunset and the tides marked. The forecast is saved on the phone, so it still works offline and shows how old it is.

## Run locally

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. `localhost` counts as a secure context, so the service worker and geolocation work there.

## Tests

Open the app with `?test` on the end of the address (for example http://localhost:8000/?test) to run the browser tests. See `tests/README.md`.

## Deploy

Host the folder on any HTTPS static host (GitHub Pages, Netlify, Cloudflare Pages). HTTPS is required for GPS and install.

Install on Android: open the page in Chrome → menu → **Add to Home screen** / **Install app**. Open from the home screen, tap **Use my location** and allow location.

For a real APK (Play Store or sideloading): give the hosted URL to pwabuilder.com, or wrap the folder with Capacitor.

## Updating

After changing **any** file, bump `CACHE` in `sw.js` (e.g. `pico-fc-v8` → `pico-fc-v9`), or installed copies keep serving the old version. If you add a file under `img/`, add it to `FILES` in `sw.js` too.

## Data sources

- **Weather / marine:** Open-Meteo (`api.open-meteo.com`, `marine-api.open-meteo.com`), fetched live.
- **Tides:** computed in the app for any date from the TICON-4 tidal constants for Horta (Hart-Davis, Dettmering and Seitz 2025, doi 10.17882/109129, CC BY 4.0), with the seasonal SA/SSA terms left out and a mean level of 0.96 m above chart datum. Checked against the Instituto Hidrográfico 2026 table: all 1,411 high and low waters matched, median 2 minutes and 3 cm out, worst 16 minutes and 8 cm. No yearly update needed.
