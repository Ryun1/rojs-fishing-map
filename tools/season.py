"""Write the 12-month season curves in data/species.json from SREA landings.

Source: docs/research/data/srea/season_profiles.json (built by
docs/research/scripts/srea.py from the SREA 1994-2026 monthly landings export;
see docs/research/landings.md). Uses the Pico profile over all complete years.

For each species:
  1. take the month-of-year profile (mean monthly share of each year's landings,
     scaled so the top month = 1),
  2. smooth it once around the year with weights 1/4, 1/2, 1/4 and rescale to top = 1,
     so one odd month does not dominate,
  3. lift it onto a floor: season = floor + (1 - floor) * curve.
     Resident reef fish (sargo, veja, moray, comber, scorpionfish, grouper,
     two-banded seabream, bogue) are on the coast all year and the
     landings mainly show when they are targeted and most active, so they get a
     floor of 0.4. Visiting pelagics get 0.1.

Usage (from the repository root): python3 -I tools/season.py
Then bump CACHE in sw.js.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILES = os.path.join(ROOT, "docs", "research", "data", "srea", "season_profiles.json")
SPECIES = os.path.join(ROOT, "data", "species.json")

# app species id -> (SREA species label, floor)
MAP = {
    "amberjack": ("Lírio - Írio", 0.1),
    "bluefish": ("Anchova", 0.1),
    "barracuda": ("Bicuda", 0.1),
    "bonito": ("Serra", 0.1),
    "sargo": ("Sargo Sarguete", 0.4),
    "veja": ("Veja", 0.4),
    "moray": ("Moreia Pintada", 0.4),
    "comber": ("Garoupa", 0.4),
    "triggerfish": ("Peixe Porco", 0.1),
    "pompano": ("Prombeta", 0.1),
    "jackmackerel": ("Chicharro", 0.1),
    "scorpionfish": ("Rocaz", 0.4),
    "grouper": ("Badejo", 0.4),
    "safia": ("Safia", 0.4),
    "bogue": ("Boga", 0.4),
}
# lizardfish has no usable landings (18 kg in 32 years as "lagarto da costa"), so its flat season is set by hand.
SOURCE = "SREA Pico landings 1994-2025"


def smooth(v):
    n = len(v)
    s = [0.25 * v[(i - 1) % n] + 0.5 * v[i] + 0.25 * v[(i + 1) % n] for i in range(n)]
    top = max(s) or 1
    return [x / top for x in s]


def main():
    prof = json.load(open(PROFILES, encoding="utf-8"))["islands"]["Pico"]
    species = json.load(open(SPECIES, encoding="utf-8"))
    for sp in species:
        if sp["id"] not in MAP:
            print("no landings mapping, left as is:", sp["id"])
            continue
        label, floor = MAP[sp["id"]]
        rel = prof[label]["profiles"]["all"]["rel"]
        sp["season"] = [round(floor + (1 - floor) * x, 2) for x in smooth(rel)]
        sp["seasonSrc"] = SOURCE
        print(f"{sp['id']:10s} {' '.join(f'{x:.2f}' for x in sp['season'])}")
    # keep one species per line, as the file is hand-read
    body = ",\n".join("  " + json.dumps(sp, ensure_ascii=False, separators=(",", ":")) for sp in species)
    with open(SPECIES, "w", encoding="utf-8") as f:
        f.write("[\n" + body + "\n]\n")


if __name__ == "__main__":
    main()
