"""Dependency-free harmonic tide synthesis, to check what a browser could do offline.
Constituents: TICON-4 (Horta, UHSLC 212a), phases = Greenwich lag (deg), UTC."""
import json, math, sys, re, datetime as dt

D = math.pi / 180.0

def astro(t):  # t: datetime UTC -> s,h,p,N,p1 (deg), T (deg)
    j2000 = dt.datetime(2000, 1, 1, 12, tzinfo=dt.timezone.utc)
    d = (t - j2000).total_seconds() / 86400.0
    Tc = d / 36525.0
    s = 218.3164477 + 481267.88123421 * Tc
    h = 280.4664567 + 36000.76982779 * Tc
    p = 83.3532465 + 4069.0137287 * Tc
    N = 125.0445479 - 1934.1362891 * Tc
    p1 = 282.93768 + 1.71946 * Tc
    hrs = t.hour + t.minute / 60.0 + t.second / 3600.0
    T = 15.0 * hrs + 180.0
    return s, h, p, N, p1, T

# name: (coefT, cs, ch, cp, cp1, const, nodal-class)
C = {
 "M2": (2, -2, 2, 0, 0, 0, "m2"), "S2": (2, 0, 0, 0, 0, 0, "1"), "N2": (2, -3, 2, 1, 0, 0, "m2"),
 "K2": (2, 0, 2, 0, 0, 0, "k2"), "K1": (1, 0, 1, 0, 0, -90, "k1"), "O1": (1, -2, 1, 0, 0, 90, "o1"),
 "P1": (1, 0, -1, 0, 0, 90, "1"), "Q1": (1, -3, 1, 1, 0, 90, "o1"), "MU2": (2, -4, 4, 0, 0, 0, "m2"),
 "NU2": (2, -3, 4, -1, 0, 0, "m2"), "2N2": (2, -4, 2, 2, 0, 0, "m2"), "T2": (2, 0, -1, 0, 1, 0, "1"),
 "R2": (2, 0, 1, 0, -1, 180, "1"), "L2": (2, -1, 2, -1, 0, 180, "m2"), "LAMBDA2": (2, -1, 0, 1, 0, 180, "m2"),
 "SA": (0, 0, 1, 0, 0, 0, "1"), "SSA": (0, 0, 2, 0, 0, 0, "1"), "MM": (0, 1, 0, -1, 0, 0, "mm"),
 "MF": (0, 2, 0, 0, 0, 0, "mf"), "MSF": (0, 2, -2, 0, 0, 0, "m2"), "J1": (1, 1, 1, -1, 0, -90, "j1"),
 "OO1": (1, 2, 1, 0, 0, -90, "oo1"), "2Q1": (1, -4, 1, 2, 0, 90, "o1"), "RHO1": (1, -3, 3, -1, 0, 90, "o1"),
 "M4": (4, -4, 4, 0, 0, 0, "m4"), "MS4": (4, -2, 2, 0, 0, 0, "m2"), "MN4": (4, -5, 4, 1, 0, 0, "m4"),
 "M3": (3, -3, 3, 0, 0, 0, "m3"), "S1": (1, 0, 0, 0, 0, 0, "1"),
}

def nodal(N):
    n = N * D
    c1, c2, c3 = math.cos(n), math.cos(2 * n), math.cos(3 * n)
    s1, s2, s3 = math.sin(n), math.sin(2 * n), math.sin(3 * n)
    fm2 = 1.0004 - 0.0373 * c1 + 0.0002 * c2; um2 = -2.14 * s1
    r = {"1": (1.0, 0.0), "m2": (fm2, um2), "m4": (fm2 ** 2, 2 * um2), "m3": (fm2 ** 1.5, 1.5 * um2),
         "k1": (1.0060 + 0.1150 * c1 - 0.0088 * c2 + 0.0006 * c3, -8.86 * s1 + 0.68 * s2 - 0.07 * s3),
         "o1": (1.0089 + 0.1871 * c1 - 0.0147 * c2 + 0.0014 * c3, 10.80 * s1 - 1.34 * s2 + 0.19 * s3),
         "k2": (1.0241 + 0.2863 * c1 + 0.0083 * c2 - 0.0015 * c3, -17.74 * s1 + 0.68 * s2 - 0.04 * s3),
         "mm": (1.0 - 0.1300 * c1 + 0.0013 * c2, 0.0),
         "mf": (1.0429 + 0.4135 * c1 - 0.004 * c2, -23.74 * s1 + 2.68 * s2 - 0.38 * s3),
         "j1": (1.0129 + 0.1676 * c1 - 0.0170 * c2 + 0.0016 * c3, -12.94 * s1 + 1.34 * s2 - 0.19 * s3),
         "oo1": (1.1027 + 0.6504 * c1 + 0.0317 * c2 - 0.0014 * c3, -36.68 * s1 + 4.02 * s2 - 0.57 * s3)}
    return r

def series(cons, t0, minutes, step=1):
    """cons: {name: (amp, G)}; returns list of heights relative to MSL, sampled every `step` min.
    Nodal factors frozen at mid-interval (fine for <= 1 year)."""
    tm = t0 + dt.timedelta(minutes=minutes / 2)
    nod = nodal(astro(tm)[3])
    s, h, p, N, p1, T = astro(t0)
    # speeds deg/hour
    ds, dh, dp, dp1 = 0.54901653, 0.04106864, 0.00464183, 0.00000196
    terms = []
    for name, (A, G) in cons.items():
        if name not in C: continue
        cT, cs, ch, cp, cp1, k, cls = C[name]
        f, u = nod[cls]
        V0 = cT * T + cs * s + ch * h + cp * p + cp1 * p1 + k
        sp = cT * 15.0 + cs * ds + ch * dh + cp * dp + cp1 * dp1
        terms.append((f * A, (V0 + u - G) * D, sp * D / 60.0 * step))
    out = []
    for i in range(0, minutes // step + 1):
        out.append(sum(a * math.cos(ph + w * i) for a, ph, w in terms))
    return out

def extrema(y, step=1):
    ex = []
    for i in range(1, len(y) - 1):
        if (y[i] - y[i - 1]) * (y[i + 1] - y[i]) <= 0 and y[i] != y[i - 1]:
            # parabolic refine
            den = (y[i - 1] - 2 * y[i] + y[i + 1])
            off = 0.5 * (y[i - 1] - y[i + 1]) / den if den else 0
            ex.append(((i + off) * step, y[i]))
    return ex

if __name__ == "__main__":
    ticon = json.load(open(sys.argv[1]))
    html = open(sys.argv[2], encoding="utf-8").read()
    m = re.search(r"var HORTA = \{ t: \[([^\]]+)\], h: \[([^\]]+)\]", html)
    OT = [int(x) for x in m.group(1).split(",")]; OH = [int(x) / 10 for x in m.group(2).split(",")]
    print("official 2026 extrema:", len(OT), "first", OT[:3], OH[:3])
    allc = {c["name"].upper(): (c["amplitude"], c["phase"]) for c in ticon["harmonic_constituents"]}
    unsupported = sorted(((a, n) for n, (a, g) in allc.items() if n not in C), reverse=True)
    print("TICON constituents not implemented here (amp m):", [(n, round(a, 4)) for a, n in unsupported[:12]])
    t0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    sets = {
      "TICON all supported (%d)" % sum(1 for n in allc if n in C): allc,
      "TICON top 8 (M2 S2 N2 K2 K1 O1 P1 Q1)": {k: allc[k] for k in ("M2", "S2", "N2", "K2", "K1", "O1", "P1", "Q1")},
      "TICON top 8 + SA SSA": {k: allc[k] for k in ("M2", "S2", "N2", "K2", "K1", "O1", "P1", "Q1", "SA", "SSA")},
      "IH published 4 (M2 S2 K1 O1, zone -1 -> UTC)": {"M2": (0.419, 30.2 + 28.9841042), "S2": (0.153, 48.0 + 30.0), "K1": (0.043, 69.3 + 15.0410686), "O1": (0.020, 314.1 + 13.9430356)},
    }
    Z0 = 1.00
    for label, cons in sets.items():
        y = series(cons, t0, 366 * 1440)
        ex = extrema(y)
        j = 0; dts = []; dhs = []
        for tt, hh in zip(OT, OH):
            while j + 1 < len(ex) and abs(ex[j + 1][0] - tt) < abs(ex[j][0] - tt): j += 1
            if abs(ex[j][0] - tt) < 180:
                dts.append(ex[j][0] - tt); dhs.append(Z0 + ex[j][1] - hh)
        a = sorted(abs(x) for x in dts); b = sorted(abs(x) for x in dhs)
        q = lambda v, f: v[min(len(v) - 1, int(f * len(v)))]
        print("%-46s n=%d matched=%d | time err min: mean %+.1f, median|.| %.1f, p90 %.1f, p99 %.1f, max %.1f | height err m: mean %+.3f, median|.| %.3f, p90 %.3f, max %.3f" % (
            label, len(ex), len(dts), sum(dts) / len(dts), q(a, .5), q(a, .9), q(a, .99), a[-1], sum(dhs) / len(dhs), q(b, .5), q(b, .9), b[-1]))
