import re, sys, json, datetime as dt, calendar
d, year, first = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rows = []
for pi in range(4):
    lines = open("%s/p%03d.txt" % (d, first + pi), encoding="utf-8", errors="replace").read().split("\n")
    toks = []
    for ln in lines:
        for m in re.finditer(r"(?:(\d\d)\s+)?(\d\d):(\d\d)\s+(\d\.\d)(?!\d)", ln):
            toks.append((m.start(2), m.group(1), int(m.group(2)), int(m.group(3)), float(m.group(4))))
    xs = sorted(set(t[0] for t in toks))
    # cluster x positions into 6 columns by largest gaps
    gaps = sorted(range(1, len(xs)), key=lambda i: xs[i] - xs[i - 1], reverse=True)[:5]
    cuts = sorted(xs[i] for i in gaps)
    col = lambda x: sum(1 for c in cuts if x >= c)
    cur = {}
    for x, day, hh, mm, ht in toks:
        c = col(x)
        if day: cur[c] = int(day)
        month = pi * 3 + c // 2 + 1
        rows.append((month, cur[c], hh, mm, ht, c))
ok = True; out = []
for month, day, hh, mm, ht, c in rows:
    if day > calendar.monthrange(year, month)[1] or (c % 2 == 0 and day > 16) or (c % 2 == 1 and day < 17): ok = False
    t = dt.datetime(year, month, day, hh, mm)
    out.append((int((t - dt.datetime(year, 1, 1)).total_seconds() // 60), ht))
out.sort()
gaps = [b[0] - a[0] for a, b in zip(out, out[1:])]
alt = sum(1 for a, b, c in zip(out, out[1:], out[2:]) if (b[1] - a[1]) * (c[1] - b[1]) < 0)
print("rows", len(out), "consistent", ok, "gap min/max (min)", min(gaps), max(gaps), "alternating triples", alt, "of", len(out) - 2)
print("first", out[:4], "last", out[-2:])
json.dump({"year": year, "port": "Horta", "tz": "UTC", "datum": "ZH (chart datum, 1.00 m below MSL)", "source": "Instituto Hidrografico, Tabela de Mares Vol. I %d (CC BY-NC-ND 4.0)" % year, "t_min_since_jan1": [o[0] for o in out], "h_m": [o[1] for o in out]}, open(sys.argv[4], "w"))
