"""Pico subset of the IMAR/DOP underwater visual census (1997-2015) and the
Azores ports & marinas Rapid Assessment Survey (2023-2024).

Usage: python3 -I census.py <raw_dir> <out_json>
  <raw_dir> gets the downloads (created if missing; files reused if present).
  <out_json> is the compact per-site x species summary.
Prints the tables used in docs/research/census.md.

Sources (both CC BY 4.0):
  - Afonso P (2016) Underwater fish visual census in the Azores 1997-2015.
    IMAR/DOP, doi 10.14284/210, https://ipt.vliz.be/eurobis/resource?r=scuba_diving_visual_census
  - Marine Species Rapid Assessment Survey of Azorean Ports and Marinas (2023-2024).
    Universidade dos Acores, doi 10.15468/jwasph (GBIF dataset 9fe4e241-5b6b-46e3-a1f2-3c5d94478868)
"""
import ast, collections, csv, io, json, math, os, sys, urllib.request, zipfile

UA = {"User-Agent": "research-script/1.0"}
DWCA = "https://ipt.vliz.be/eurobis/archive.do?r=scuba_diving_visual_census"
OBIS = ("https://api.obis.org/v3/occurrence?datasetid=df1970cb-fd9a-440a-9547-7ee6ec2605bc"
        "&size=10000&extensions=MeasurementOrFact")
RAS = "https://api.gbif.org/v1/occurrence/search?datasetKey=9fe4e241-5b6b-46e3-a1f2-3c5d94478868&limit=300"
BOX = (38.35, 38.60, -28.60, -27.95)  # lat min, lat max, lon min, lon max
CLUSTER_M = 300  # dive coordinates within this distance are treated as one site

# species.md section 4.1, split as in section 7 (core = already in the app)
CORE = ["Diplodus sargus", "Sparisoma cretense", "Sphyraena viridensis", "Pomatomus saltatrix",
        "Seriola rivoliana", "Seriola dumerili", "Sarda sarda", "Muraena helena", "Muraena augusti",
        "Gymnothorax unicolor"]
SECONDARY = ["Serranus atricauda", "Trachurus picturatus", "Scomber colias", "Pagellus bogaraveo",
             "Pagellus acarne", "Pseudocaranx dentex", "Sarpa salpa", "Chelon labrosus",
             "Trachinotus ovatus", "Balistes capriscus", "Labrus bergylta", "Centrolabrus caeruleus", "Coris julis", "Thalassoma pavo", "Boops boops", "Loligo forbesii",
             "Octopus vulgaris", "Epinephelus marginatus", "Kyphosus sectatrix", "Bodianus scrofa",
             "Phycis phycis", "Conger conger", "Pagrus pagrus", "Mullus surmuletus",
             "Scorpaena maderensis", "Belone belone", "Abudefduf luridus", "Katsuwonus pelamis",
             "Sphoeroides marmoratus"]
TARGET = CORE + SECONDARY
# archive name -> name used in species.md. Centrolabrus trutta is not an Azores species; Azores records under
# that name are taken to be the endemic C. caeruleus (inference). Scomber japonicus = Atlantic S. colias.
SYN = {"Balistes carolinensis": "Balistes capriscus", "Belone belone gracilis": "Belone belone",
       "Centrolabrus trutta": "Centrolabrus caeruleus", "Kyphosus sectator": "Kyphosus sectatrix",
       "Pomatomus saltator": "Pomatomus saltatrix", "Pseudolepidaplois scrofa": "Bodianus scrofa",
       "Seriola dumerilii": "Seriola dumerili", "Trachynotus ovatus": "Trachinotus ovatus",
       "Scomber japonicus": "Scomber colias"}
# landmarks that are not candidate spots (Nominatim, OSM islet nodes, 2026-11-22)
LANDMARKS = [("ilheu_deitado", 38.53551, -28.54583), ("ilheu_em_pe", 38.53754, -28.54431)]


def fetch(url, path):
    if not os.path.exists(path):
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r, open(path, "wb") as f:
            f.write(r.read())
    return path


def dist_m(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


def load_spots():
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "spots_spots.py"), encoding="utf-8").read()
    node = next(n for n in ast.parse(src).body if isinstance(n, ast.Assign) and n.targets[0].id == "SPOTS")
    return [(s[0], s[1], s[3], s[4]) for s in ast.literal_eval(node.value)]


def main(raw, out):
    os.makedirs(raw, exist_ok=True)
    z = zipfile.ZipFile(fetch(DWCA, os.path.join(raw, "dwca.zip")))
    print("archive members:", z.namelist())
    meta = z.read("meta.xml").decode()
    print("extensions in meta.xml:", meta.count("<extension"))
    rows = list(csv.DictReader(io.TextIOWrapper(z.open("occurrence.txt"), encoding="utf-8"),
                               delimiter="\t", quoting=csv.QUOTE_NONE))
    filled = {k for r in rows for k, v in r.items() if v}
    print("records:", len(rows), "| populated columns:", sorted(filled))

    obis = json.load(open(fetch(OBIS, os.path.join(raw, "obis.json")), encoding="utf-8"))["results"]
    mof = collections.Counter(m["measurementType"] for r in obis for m in r.get("mof", []))
    print("OBIS copy:", len(obis), "records; eMoF types:", dict(mof))
    env = {r["occurrenceID"]: (r.get("bathymetry"), r.get("shoredistance")) for r in obis}

    lat0, lat1, lon0, lon1 = BOX
    pico = [r for r in rows if lat0 <= float(r["decimalLatitude"]) <= lat1 and lon0 <= float(r["decimalLongitude"]) <= lon1]
    print("Pico box records (all taxa):", len(pico))

    # events = unique (date, coordinate); sites = events clustered by CLUSTER_M
    events = collections.defaultdict(set)
    for r in pico:
        events[(r["eventDate"], float(r["decimalLatitude"]), float(r["decimalLongitude"]))].add(SYN.get(r["scientificName"], r["scientificName"]))
    sites = []
    for ev in sorted(events, key=lambda e: (e[1], e[2])):
        for s in sites:
            if dist_m(s["c"], ev[1:]) <= CLUSTER_M:
                s["ev"].append(ev)
                s["c"] = (sum(e[1] for e in s["ev"]) / len(s["ev"]), sum(e[2] for e in s["ev"]) / len(s["ev"]))
                break
        else:
            sites.append({"c": ev[1:], "ev": [ev]})
    spots = load_spots()
    bathy = collections.defaultdict(list)
    for r in pico:
        b, sd = env.get(r["occurrenceID"], (None, None))
        bathy[(r["eventDate"], float(r["decimalLatitude"]), float(r["decimalLongitude"]))] = (b, sd)

    out_sites = []
    sites.sort(key=lambda s: -s["c"][1])  # west to east
    for i, s in enumerate(sites, 1):
        near = sorted((dist_m(s["c"], (la, lo)), sid, name) for sid, name, la, lo in spots)[:2]
        sp = collections.Counter(n for ev in s["ev"] for n in events[ev] if n in TARGET)
        bs = [bathy[ev][0] for ev in s["ev"] if bathy[ev][0] is not None]
        sds = [bathy[ev][1] for ev in s["ev"] if bathy[ev][1] is not None]
        out_sites.append({
            "site": "S%02d" % i, "lat": round(s["c"][0], 5), "lon": round(s["c"][1], 5),
            "dives": len(s["ev"]), "days": len({ev[0] for ev in s["ev"]}),
            "years": sorted({int(ev[0][:4]) for ev in s["ev"]}),
            "months": dict(sorted(collections.Counter(int(ev[0][5:7]) for ev in s["ev"]).items())),
            "taxa_all": len({n for ev in s["ev"] for n in events[ev]}),
            "nearest_spot": near[0][1], "nearest_m": round(near[0][0]), "second_spot": near[1][1], "second_m": round(near[1][0]),
            "obis_bathy_m": [min(bs), max(bs)] if bs else None,
            "obis_shore_m": [min(sds), max(sds)] if sds else None,
            "species": {k: sp[k] for k in TARGET if sp[k]},
        })
        o = out_sites[-1]
        lm = min((dist_m(s["c"], (la, lo)), n) for n, la, lo in LANDMARKS)
        o["nearest_landmark"], o["landmark_m"] = lm[1], round(lm[0])
        o["flags"] = [f for f, ok in (
            ("on_land_coordinate", bs and max(bs) < 0),
            ("offshore_gt_1km", sds and min(sds) > 1000),
            ("no_spot_within_2km", near[0][0] > 2000),
            ("west_of_-28.59_faial_side?", s["c"][1] < -28.59)) if ok]

    # ---- printed tables ----
    print("\n## sites (dives = unique date+coordinate)")
    print("| Site | Lat, lon | Dives | Days | Years | Months (dives) | Nearest spot (m) | 2nd (m) | OBIS bathymetry m | OBIS shore dist m | Taxa | Islet (m) | Flags |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for s in out_sites:
        print("| %s | %.4f, %.4f | %d | %d | %s | %s | %s (%d) | %s (%d) | %s | %s | %d | %d | %s |" % (
            s["site"], s["lat"], s["lon"], s["dives"], s["days"], ",".join(str(y) for y in s["years"]),
            " ".join("%d:%d" % kv for kv in s["months"].items()), s["nearest_spot"], s["nearest_m"],
            s["second_spot"], s["second_m"], "-".join("%g" % v for v in s["obis_bathy_m"] or []),
            "-".join("%g" % v for v in s["obis_shore_m"] or []), s["taxa_all"], s["landmark_m"], ", ".join(s["flags"])))

    tot = sum(s["dives"] for s in out_sites)
    print("\n## species: dives present / %d Pico dives, sites present / %d" % (tot, len(out_sites)))
    print("| Species | Tier | Dives present | % dives | Sites present | Dive months (Jan..Dec) |")
    print("|---|---|---|---|---|---|")
    for sp in TARGET:
        evs = [ev for ev in events if sp in events[ev]]
        m = collections.Counter(int(ev[0][5:7]) for ev in evs)
        print("| *%s* | %s | %d | %.0f%% | %d | %s |" % (sp, "core" if sp in CORE else "secondary", len(evs),
              100 * len(evs) / tot, sum(1 for s in out_sites if sp in s["species"]), " ".join(str(m[i]) for i in range(1, 13))))
    allm = collections.Counter(int(ev[0][5:7]) for ev in events)
    print("all Pico dives by month:", " ".join(str(allm[i]) for i in range(1, 13)))
    print("all Pico dives by year:", dict(sorted(collections.Counter(int(ev[0][:4]) for ev in events).items())))

    print("\n## site x core/secondary matrix (dives present / dives)")
    cols = [sp for sp in TARGET if any(sp in s["species"] for s in out_sites)]
    print("| Site | n | " + " | ".join(c.split()[0][:3] + "." + c.split()[1][:4] for c in cols) + " |")
    print("|---" * (len(cols) + 2) + "|")
    for s in out_sites:
        print("| %s | %d | " % (s["site"], s["dives"]) + " | ".join(str(s["species"].get(c, "")) for c in cols) + " |")

    # ---- ports & marinas RAS ----
    ras = json.load(open(fetch(RAS, os.path.join(raw, "ras.json")), encoding="utf-8"))
    print("\n## RAS ports and marinas: %d records; localities:" % ras["count"],
          dict(collections.Counter((r.get("island"), r.get("locality")) for r in ras["results"])))
    pico_ras = [r for r in ras["results"] if r.get("island") == "Pico" or (
        lat0 <= r.get("decimalLatitude", 0) <= lat1 and lon0 <= r.get("decimalLongitude", 0) <= lon1)]
    print("RAS records on Pico / in Pico box:", len(pico_ras))
    fish = collections.defaultdict(dict)
    for r in ras["results"]:
        if r.get("class") in ("Teleostei", "Actinopterygii", "Elasmobranchii") or (r.get("phylum") == "Chordata" and r.get("class") != "Ascidiacea"):
            ab = [e.get("http://rs.tdwg.org/dwc/terms/measurementValue") for e in
                  r.get("extensions", {}).get("http://rs.iobis.org/obis/terms/ExtendedMeasurementOrFact", [])
                  if "SACFOR" in e.get("http://rs.tdwg.org/dwc/terms/measurementType", "")]
            fish[r.get("species") or r["scientificName"]]["%s %s" % (r["locality"], r["year"])] = ab[0] if ab else "present"
    locs = sorted({k for v in fish.values() for k in v})
    print("| Species | " + " | ".join(locs) + " |")
    print("|---" * (len(locs) + 1) + "|")
    for sp in sorted(fish):
        print("| *%s* | " % sp + " | ".join(fish[sp].get(l, "") for l in locs) + " |")

    json.dump({
        "source": "Afonso P (2016) Underwater fish visual census in the Azores 1997-2015, IMAR/DOP, doi 10.14284/210, CC BY 4.0",
        "derived_by": "docs/research/scripts/census.py",
        "synonyms_merged": SYN, "notes": "Presence only. dives = unique (eventDate, coordinate); species values = dives with the species recorded. "
                 "Sites = dive coordinates clustered within %d m. obis_* = OBIS-derived bathymetry and distance to shore at the "
                 "dive coordinate (not the transect depth, which is not published)." % CLUSTER_M,
        "box": BOX, "core": CORE, "sites": out_sites,
    }, open(out, "w", encoding="utf-8"), separators=(",", ":"))
    print("\nwrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
