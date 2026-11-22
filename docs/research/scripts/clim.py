import csv, glob, sys, json, datetime as dt, collections
d = sys.argv[1]
data = collections.defaultdict(dict)  # (lat,lon) -> date -> sst
for f in sorted(glob.glob(d + "/oisst_*.csv")):
    with open(f) as fh:
        r = csv.reader(fh); next(r); next(r)
        for row in r:
            if len(row) < 5 or row[4] in ("", "NaN"): continue
            data[(float(row[2]), float(row[3]))][dt.date.fromisoformat(row[0][:10])] = float(row[4])
cells = sorted(data)
alld = sorted(set().union(*[set(v) for v in data.values()]))
print("cells", cells); print("days", len(alld), alld[0], "..", alld[-1])
yrs = collections.Counter(x.year for x in alld); print("days per year (short years):", {y: n for y, n in sorted(yrs.items()) if n < 360})
base = (1991, 2020)
out = {}
for c in cells:
    acc = collections.defaultdict(list)
    for day, v in data[c].items():
        if base[0] <= day.year <= base[1]:
            doy = min(day.timetuple().tm_yday, 365); acc[doy].append(v)
    raw = [sum(acc[k]) / len(acc[k]) for k in range(1, 366)]
    sm = [sum(raw[(i + j) % 365] for j in range(-5, 6)) / 11 for i in range(365)]
    out["%.3f,%.3f" % c] = [round(x, 2) for x in sm]
    n = [len(acc[k]) for k in range(1, 366)]
    print(c, "samples per day-of-year min/max", min(n), max(n), "| min %.2f on doy %d, max %.2f on doy %d" % (min(sm), sm.index(min(sm)) + 1, max(sm), sm.index(max(sm)) + 1))
mid = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]
for k, v in out.items(): print(k, "mid-month:", [v[m - 1] for m in mid])
N = out["38.625,-28.375"]; S_ = out["38.375,-28.375"]
diff = [a - b for a, b in zip(N, S_)]; print("N minus S cell (38.625 vs 38.375 at -28.375): min %.2f max %.2f mean %.2f" % (min(diff), max(diff), sum(diff) / 365))
# interannual spread for a given day: std of anomalies
import math
c = (38.625, -28.625); an = [v - out["%.3f,%.3f" % c][min(day.timetuple().tm_yday, 365) - 1] for day, v in data[c].items() if base[0] <= day.year <= base[1]]
print("std of daily anomaly 1991-2020 at", c, round(math.sqrt(sum(x * x for x in an) / len(an)), 2))
last = max(data[c]); print("latest", last, data[c][last], "anomaly vs 1991-2020:", round(data[c][last] - out["%.3f,%.3f" % c][min(last.timetuple().tm_yday, 365) - 1], 2))
json.dump({"source": "NOAA OISST v2.1 (AVHRR-only) via coastwatch.pfeg.noaa.gov ERDDAP ncdcOisst21Agg_LonPM180", "baseline": "1991-2020, 11-day running mean", "units": "deg C", "index": "day of year 1..365", "cells": out}, open(sys.argv[2], "w"))
print("bytes", len(json.dumps(out)))
