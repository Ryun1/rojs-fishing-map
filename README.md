# Pico Fishing Forecast

A static, installable PWA (no build step) giving a fishing forecast for Pico, Azores: current conditions, a spot selector, ranked species per spot and a species-by-spot grid.

## Files

| File | Purpose |
|---|---|
| `index.html` | The whole app: markup, CSS and JS, plus built-in 2026 Horta tide predictions |
| `manifest.webmanifest` | PWA manifest (name, icons, theme) |
| `sw.js` | Service worker: caches app files for offline use; Open-Meteo requests always go to network |
| `icon-192.png`, `icon-512.png` | App icons |
| `img/` | Species photos (crops of own catch photos, location/date metadata removed; the moray is a drawing) |

## Run locally

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. `localhost` counts as a secure context, so the service worker and geolocation work there.

## Deploy

Host the folder on any HTTPS static host (GitHub Pages, Netlify, Cloudflare Pages). HTTPS is required for GPS and install.

Install on Android: open the page in Chrome → menu → **Add to Home screen** / **Install app**. Open from the home screen, tap **Use my location** and allow location.

For a real APK (Play Store or sideloading): give the hosted URL to pwabuilder.com, or wrap the folder with Capacitor.

## Updating

After changing **any** file, bump `CACHE` in `sw.js` (e.g. `pico-fc-v8` → `pico-fc-v9`), or installed copies keep serving the old version. If you add a file under `img/`, add it to `FILES` in `sw.js` too.

## Data sources

- **Weather / marine:** Open-Meteo (`api.open-meteo.com`, `marine-api.open-meteo.com`), fetched live.
- **Tides:** 2026 predictions for Horta from the Instituto Hidrográfico tide table, embedded in `index.html`. From 2027 the app falls back to the Open-Meteo model until the 2027 table is added.
