import importlib.util, json, sys, datetime as dt
spec = importlib.util.spec_from_file_location("tide", sys.argv[1]); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
ticon = json.load(open(sys.argv[2])); off = json.load(open(sys.argv[3])); year = off["year"]
OT, OH = off["t_min_since_jan1"], off["h_m"]
allc = {c["name"].upper(): (c["amplitude"], c["phase"]) for c in ticon["harmonic_constituents"]}
noseas = {k: v for k, v in allc.items() if k not in ("SA", "SSA")}
t0 = dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc)
q = lambda v, f: v[min(len(v) - 1, int(f * len(v)))]
for label, cons, z0 in (("TICON 29 incl SA/SSA, Z0=1.00", allc, 1.00), ("TICON 27 without SA/SSA, Z0=1.00", noseas, 1.00), ("TICON 27 without SA/SSA, Z0=0.96", noseas, 0.96),
                        ("TICON 11 (M2 S2 N2 K2 K1 O1 P1 Q1 MU2 NU2 2N2), Z0=0.96", {k: allc[k] for k in "M2 S2 N2 K2 K1 O1 P1 Q1 MU2 NU2 2N2".split()}, 0.96)):
    ex = T.extrema(T.series(cons, t0, 366 * 1440))
    j = 0; dts = []; dhs = []; state_ok = 0
    for tt, hh in zip(OT, OH):
        while j + 1 < len(ex) and abs(ex[j + 1][0] - tt) < abs(ex[j][0] - tt): j += 1
        if abs(ex[j][0] - tt) < 180: dts.append(ex[j][0] - tt); dhs.append(z0 + ex[j][1] - hh)
    a = sorted(abs(x) for x in dts); b = sorted(abs(x) for x in dhs)
    print("%d %-58s matched %d/%d | time err min: mean %+.1f med %.1f p90 %.1f p99 %.1f max %.1f | height err m: mean %+.3f med %.3f p90 %.3f max %.3f" % (year, label, len(dts), len(OT), sum(dts) / len(dts), q(a, .5), q(a, .9), q(a, .99), a[-1], sum(dhs) / len(dhs), q(b, .5), q(b, .9), b[-1]))
