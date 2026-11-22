"""Monthly season profiles from the SREA landings export (1994-2026).

Input: docs/research/data/srea/srea_landings_pico_faial_1994-2026.csv
  island,category,species,year,month,kg,eur   (month in Portuguese, blank = no landings)
Output: docs/research/data/srea/season_profiles.json and a text summary on stdout.

Usage: python3 -I srea.py <csv> <out_json>
"""
import csv
import json
import statistics
import sys
from collections import defaultdict

MONTHS = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
          "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
TARGETS = ["Veja", "Sargo Sarguete", "Bicuda", "Serra", "Lírio - Írio", "Anchova",
           "Encharéu", "Taínha Muja", "Salema", "Cavala", "Chicharro", "Boga",
           "Besugo", "Garoupa", "Congro", "Moreia Pintada", "Moreia Preta Viúva",
           "Moreão", "Bonito Gaiado"]
PERIODS = {"1994-2009": range(1994, 2010), "2010-2025": range(2010, 2026)}


def num(s):
    s = (s or "").strip()
    return float(s) if s else 0.0


def main(src, dst):
    # kg[island][species][year][month]
    kg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0.0] * 12)))
    last_month = {}
    with open(src, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m = MONTHS.index(r["month"])
            y = int(r["year"])
            kg[r["island"]][r["species"]][y][m] += num(r["kg"])
            if num(r["kg"]) > 0:
                last_month[y] = max(last_month.get(y, -1), m)
    out = {"source": "SREA report server, 'Total da pesca descarregada, por espécie e por ilha', "
                     "exported 2026-11-22. Commercial landings in kg.",
           "method": "Each complete year is turned into monthly shares (month kg / year kg); the profile is "
                     "the mean share per month across years with landings, scaled so the top month = 1.",
           "islands": {}}
    for island in ("Pico", "Faial"):
        out["islands"][island] = {}
        for sp in TARGETS:
            years = kg[island].get(sp, {})
            entry = {"annual_kg": {}, "profiles": {}}
            for y in sorted(years):
                entry["annual_kg"][y] = round(sum(years[y]))
            for label, rng in list(PERIODS.items()) + [("all", range(1994, 2026))]:
                shares = []
                for y in rng:
                    tot = sum(years.get(y, [0] * 12))
                    if tot > 0:
                        shares.append([v / tot for v in years[y]])
                if not shares:
                    continue
                mean = [statistics.mean(s[m] for s in shares) for m in range(12)]
                top = max(mean) or 1
                entry["profiles"][label] = {"years": len(shares),
                                            "rel": [round(v / top, 2) for v in mean]}
            out["islands"][island][sp] = entry
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    # stdout summary for Pico
    print("Pico, profile over complete years 1994-2025 (J F M A M J J A S O N D, 9 = peak)")
    for sp in TARGETS:
        e = out["islands"]["Pico"][sp]
        p = e["profiles"].get("all")
        ann = list(e["annual_kg"].values())[:32]
        if not p:
            print(f"{sp:20s} no landings")
            continue
        bars = "".join(str(min(9, int(v * 9.999))) for v in p["rel"])
        med = statistics.median(ann) if ann else 0
        print(f"{sp:20s} {bars}  yrs={p['years']:2d} median_kg/yr={med:9.0f}  "
              f"94-09 peak={peak(e,'1994-2009')} 10-25 peak={peak(e,'2010-2025')}")


def peak(e, label):
    p = e["profiles"].get(label)
    if not p:
        return "-"
    return MONTHS[p["rel"].index(1.0)][:3]


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
