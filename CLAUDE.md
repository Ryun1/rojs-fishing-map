# CLAUDE.md

Static PWA, no build step or dependencies. Everything lives in `index.html` (HTML + CSS + JS + embedded 2026 Horta tide table).

- Run: `python3 -m http.server 8000` and open http://localhost:8000.
- Whenever any shipped file changes, bump `CACHE` in `sw.js`; new assets must also be added to its `FILES` list.
- Keep the theme tokens on `:root` with the dark-mode overrides in sync (both the `prefers-color-scheme` block and `[data-theme="dark"]`).
- Fish photos in `img/` must have EXIF/GPS metadata stripped before committing.
- 2027 tide predictions still need adding to `index.html` (app falls back to Open-Meteo until then).
