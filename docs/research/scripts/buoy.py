#!/usr/bin/env python3
"""Faial-Pico wave buoy (WMO 6202404) vs ERA5 ocean waves: channel shelter analysis.

Stdlib only. Inputs (downloaded separately, see docs/research/buoy.md):
  RAW/raw/buoy_YYYY.csv   EMODnet Physics ERDDAP TS_70_6202404_MO_UND, yearly chunks, CSV
  RAW/era5/era5_buoy.json Open-Meteo marine API, models=era5_ocean, at the buoy (snaps to 38.5,-28.5)
  RAW/era5/era5_n.json    same, 39.0,-28.5 (open ocean north of the channel)
  RAW/era5/era5_w.json    same, 38.5,-29.0 (open ocean west of Faial)

Usage: python3 -I buoy.py RAW_DIR OUT_DIR
Writes OUT_DIR/{buoy_hourly.csv, shelter_ratios.json, monthly_climatology.json}
and prints the tables used in buoy.md.
"""
import csv, json, math, os, sys
from datetime import datetime, timedelta, timezone
from statistics import median

GOOD = {1, 2}  # OceanSITES QC: 1 good, 2 probably good
SECT8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
HS_CLASSES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 6), (6, 99)]


def fnum(s):
    try:
        v = float(s)
    except ValueError:
        return None
    return None if math.isnan(v) else v


def qc_ok(row, var):
    q = fnum(row[var + "_QC"])
    v = fnum(row[var])
    return v if (v is not None and q is not None and int(q) in GOOD) else None


def circ_mean(degs):
    s = sum(math.sin(math.radians(d)) for d in degs)
    c = sum(math.cos(math.radians(d)) for d in degs)
    return math.degrees(math.atan2(s, c)) % 360


def angdiff(a, b):
    return (a - b + 180) % 360 - 180


def sector8(d):
    return SECT8[int(((d + 22.5) % 360) // 45)]


def load_buoy(raw):
    """Return dict hour(datetime) -> dict of hourly means, plus QC stats."""
    acc = {}
    stats = {"rows": 0, "hs_total": 0, "hs_good": 0, "hs_range_drop": 0,
             "temp_total": 0, "temp_good": 0, "temp_range_drop": 0}
    files = sorted(f for f in os.listdir(raw) if f.startswith("buoy_") and f.endswith(".csv"))
    for f in files:
        with open(os.path.join(raw, f), newline="") as fh:
            r = csv.DictReader(fh)
            next(r)  # units row
            for row in r:
                stats["rows"] += 1
                t = datetime.strptime(row["time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                # nearest hour: samples within +-30 min of the ERA5 instantaneous hour
                h = (t + timedelta(minutes=30)).replace(minute=0, second=0)
                a = acc.setdefault(h, {"hs": [], "dir": [], "tz": [], "tmax": [], "hmax": [], "temp": []})
                if fnum(row["VAVH"]) is not None:
                    stats["hs_total"] += 1
                hs = qc_ok(row, "VAVH")
                if hs is not None:
                    if 0.05 <= hs <= 20:
                        stats["hs_good"] += 1
                        a["hs"].append(hs)
                        d = qc_ok(row, "VDIR")
                        if d is not None and 0 <= d <= 360:
                            a["dir"].append(d)
                        tz = qc_ok(row, "VTZA")
                        if tz is not None and 1 <= tz <= 25:
                            a["tz"].append(tz)
                        tm = qc_ok(row, "VTMX")
                        if tm is not None and 1 <= tm <= 30:
                            a["tmax"].append(tm)
                        hm = qc_ok(row, "VZMX")
                        if hm is not None and 0 < hm <= 40:
                            a["hmax"].append(hm)
                    else:
                        stats["hs_range_drop"] += 1
                if fnum(row["TEMP"]) is not None:
                    stats["temp_total"] += 1
                te = qc_ok(row, "TEMP")
                if te is not None:
                    if 12 <= te <= 28:
                        stats["temp_good"] += 1
                        a["temp"].append(te)
                    else:
                        stats["temp_range_drop"] += 1
    hourly = {}
    for h, a in acc.items():
        o = {
            "hs": sum(a["hs"]) / len(a["hs"]) if a["hs"] else None,
            "dir": circ_mean(a["dir"]) if a["dir"] else None,
            "tz": sum(a["tz"]) / len(a["tz"]) if a["tz"] else None,
            "tmax": max(a["tmax"]) if a["tmax"] else None,
            "hmax": max(a["hmax"]) if a["hmax"] else None,
            "temp": sum(a["temp"]) / len(a["temp"]) if a["temp"] else None,
        }
        if any(v is not None for v in o.values()):
            hourly[h] = o
    # despike Hs: drop hours that jump >2x relative to both neighbours (isolated spikes)
    dropped = 0
    for h in sorted(hourly):
        o = hourly[h]
        if o["hs"] is None:
            continue
        p = hourly.get(h - timedelta(hours=1), {}).get("hs")
        n = hourly.get(h + timedelta(hours=1), {}).get("hs")
        if p and n and o["hs"] > 2 * max(p, n) and o["hs"] - max(p, n) > 0.5:
            o["hs"] = None
            dropped += 1
    stats["hs_spike_hours_dropped"] = dropped
    return hourly, stats


def load_era5(path):
    d = json.load(open(path))
    h = d["hourly"]
    out = {}
    for i, t in enumerate(h["time"]):
        dt = datetime.strptime(t, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        if h["wave_height"][i] is not None:
            out[dt] = {"hs": h["wave_height"][i], "dir": h["wave_direction"][i],
                       "tm": h["wave_period"][i], "tp": h["wave_peak_period"][i]}
    return out, (d["latitude"], d["longitude"])


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy)


def pct(v, p):
    v = sorted(v)
    k = (len(v) - 1) * p
    f = math.floor(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def ratio_stats(pairs):
    """pairs: list of (buoy_hs, era_hs). Ratio of means plus median/quartiles of hourly ratios."""
    if not pairs:
        return None
    b = [p[0] for p in pairs]
    e = [p[1] for p in pairs]
    r = [p[0] / p[1] for p in pairs if p[1] > 0]
    return {
        "n_hours": len(pairs),
        "buoy_mean": round(sum(b) / len(b), 2),
        "era5_mean": round(sum(e) / len(e), 2),
        "ratio_of_means": round(sum(b) / sum(e), 2),
        "ratio_median": round(median(r), 2),
        "ratio_p25": round(pct(r, 0.25), 2),
        "ratio_p75": round(pct(r, 0.75), 2),
    }


def compare(buoy, era, label):
    pairs = []  # (buoy_hs, era_hs, era_dir, buoy_dir, era_tp, buoy_tz, time)
    for h, o in buoy.items():
        if o["hs"] is None or h not in era:
            continue
        e = era[h]
        pairs.append((o["hs"], e["hs"], e["dir"], o["dir"], e["tp"], o["tz"], h))
    x = [p[1] for p in pairs]
    y = [p[0] for p in pairs]
    res = {"label": label, "n_hours": len(pairs),
           "first": min(p[6] for p in pairs).isoformat(), "last": max(p[6] for p in pairs).isoformat(),
           "pearson_r": round(pearson(x, y), 3),
           "pearson_r_log": round(pearson([math.log(v) for v in x], [math.log(v) for v in y]), 3),
           "bias_m": round(sum(b - a for a, b in zip(x, y)) / len(x), 2),
           "rmse_m": round(math.sqrt(sum((b - a) ** 2 for a, b in zip(x, y)) / len(x)), 2),
           "overall": ratio_stats([(p[0], p[1]) for p in pairs])}
    # lag check: correlation with buoy shifted by k hours
    lag = {}
    for k in range(-6, 7):
        xs, ys = [], []
        for p in pairs:
            o = buoy.get(p[6] + timedelta(hours=k))
            if o and o["hs"] is not None:
                xs.append(p[1]); ys.append(o["hs"])
        lag[k] = round(pearson(xs, ys), 3)
    res["lag_corr_buoy_minus_era_hours"] = lag
    # by ERA5 direction sector
    res["by_era5_dir8"] = {s: ratio_stats([(p[0], p[1]) for p in pairs if sector8(p[2]) == s]) for s in SECT8}
    # by ERA5 Hs class
    res["by_era5_hs"] = {f"{lo}-{hi if hi < 99 else ''}": ratio_stats([(p[0], p[1]) for p in pairs if lo <= p[1] < hi])
                         for lo, hi in HS_CLASSES}
    # direction x Hs (coarse: <2, 2-4, >=4)
    res["by_dir8_x_hs"] = {
        s: {c: ratio_stats([(p[0], p[1]) for p in pairs if sector8(p[2]) == s and lo <= p[1] < hi])
            for c, (lo, hi) in {"<2": (0, 2), "2-4": (2, 4), ">=4": (4, 99)}.items()}
        for s in SECT8}
    # 16-sector median ratio + buoy direction shift (refraction / sheltering)
    d16 = {}
    for i in range(16):
        c = i * 22.5
        sel = [p for p in pairs if abs(angdiff(p[2], c)) <= 11.25]
        if not sel:
            continue
        rs = ratio_stats([(p[0], p[1]) for p in sel])
        bd = [p[3] for p in sel if p[3] is not None]
        rs["buoy_dir_circmean"] = round(circ_mean(bd)) if bd else None
        d16[f"{c:05.1f}"] = rs
    res["by_era5_dir16"] = d16
    # ERA5 Tp vs buoy Tz (Tz ~ 0.7-0.8 Tp for typical spectra)
    tp = [(p[4], p[5]) for p in pairs if p[4] and p[5]]
    res["period"] = {"era5_tp_mean": round(sum(a for a, _ in tp) / len(tp), 2),
                     "buoy_tz_mean": round(sum(b for _, b in tp) / len(tp), 2),
                     "tz_over_tp_median": round(median(b / a for a, b in tp), 2)}
    return res, pairs


def monthly_clim(buoy):
    # per (year, month) means first, then average across years (so a well-covered year doesn't dominate)
    ym = {}
    for h, o in buoy.items():
        k = (h.year, h.month)
        d = ym.setdefault(k, {"hs": [], "temp": []})
        if o["hs"] is not None:
            d["hs"].append(o["hs"])
        if o["temp"] is not None:
            d["temp"].append(o["temp"])
    out = {}
    for m in range(1, 13):
        hs_means, t_means, hs_all, t_all, hs_years, t_years = [], [], [], [], [], []
        for (y, mm), d in sorted(ym.items()):
            if mm != m:
                continue
            if len(d["hs"]) >= 240:  # at least 10 days of hourly data
                hs_means.append(sum(d["hs"]) / len(d["hs"])); hs_all += d["hs"]; hs_years.append(y)
            if len(d["temp"]) >= 240:
                t_means.append(sum(d["temp"]) / len(d["temp"])); t_all += d["temp"]; t_years.append(y)
        out[m] = {
            "hs_years": hs_years,
            "hs_mean": round(sum(hs_means) / len(hs_means), 2) if hs_means else None,
            "hs_median": round(median(hs_all), 2) if hs_all else None,
            "hs_p90": round(pct(hs_all, 0.9), 2) if hs_all else None,
            "hs_frac_gt_2m": round(sum(v > 2 for v in hs_all) / len(hs_all), 2) if hs_all else None,
            "temp_years": t_years,
            "temp_mean": round(sum(t_means) / len(t_means), 1) if t_means else None,
            "temp_min_monthly_mean": round(min(t_means), 1) if t_means else None,
            "temp_max_monthly_mean": round(max(t_means), 1) if t_means else None,
            "temp_p05": round(pct(t_all, 0.05), 1) if t_all else None,
            "temp_p95": round(pct(t_all, 0.95), 1) if t_all else None,
        }
    return out


def coverage(buoy):
    cov = {}
    for h, o in buoy.items():
        c = cov.setdefault(h.year, [0, 0])
        c[0] += o["hs"] is not None
        c[1] += o["temp"] is not None
    return {y: {"hs_hours": a, "temp_hours": b} for y, (a, b) in sorted(cov.items())}


def fmt_row(name, s):
    if not s:
        return f"| {name} | 0 | | | | |"
    return (f"| {name} | {s['n_hours']} | {s['era5_mean']} | {s['buoy_mean']} | {s['ratio_of_means']} | "
            f"{s['ratio_median']} ({s['ratio_p25']}-{s['ratio_p75']}) |")


def main():
    raw, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    buoy, qstats = load_buoy(os.path.join(raw, "raw"))
    print("QC stats", qstats)
    print("coverage", coverage(buoy))
    results = {}
    for tag in ("buoy", "n", "w"):
        era, cell = load_era5(os.path.join(raw, "era5", f"era5_{tag}.json"))
        res, pairs = compare(buoy, era, f"ERA5 cell {cell[0]},{cell[1]}")
        results[tag] = res
        print(f"\n== ERA5 {tag} cell {cell}: n={res['n_hours']} r={res['pearson_r']} r_log={res['pearson_r_log']} "
              f"bias={res['bias_m']} rmse={res['rmse_m']} lag={res['lag_corr_buoy_minus_era_hours']}")
        print("period", res["period"])
        print("| ERA5 dir | hours | ERA5 mean Hs | buoy mean Hs | ratio of means | median ratio (IQR) |")
        print(fmt_row("all", res["overall"]))
        for s in SECT8:
            print(fmt_row(s, res["by_era5_dir8"][s]))
        print("| ERA5 Hs class | hours | ERA5 mean Hs | buoy mean Hs | ratio of means | median ratio (IQR) |")
        for k, s in res["by_era5_hs"].items():
            print(fmt_row(k, s))
        if tag == "buoy":
            print("dir16:", {k: (v["n_hours"], v["ratio_median"], v["buoy_dir_circmean"]) for k, v in res["by_era5_dir16"].items()})
            print("dir x hs median ratio:")
            for s in SECT8:
                print(s, {c: (v["n_hours"], v["ratio_median"]) if v else None for c, v in res["by_dir8_x_hs"][s].items()})
    clim = monthly_clim(buoy)
    print("\n| Month | Hs mean | Hs median | Hs p90 | P(Hs>2m) | years (Hs) | Temp mean | Temp range of monthly means | Temp p05-p95 | years (T) |")
    for m, c in clim.items():
        print(f"| {m} | {c['hs_mean']} | {c['hs_median']} | {c['hs_p90']} | {c['hs_frac_gt_2m']} | {len(c['hs_years'])} | "
              f"{c['temp_mean']} | {c['temp_min_monthly_mean']}-{c['temp_max_monthly_mean']} | {c['temp_p05']}-{c['temp_p95']} | {len(c['temp_years'])} |")

    meta = {
        "source": "EMODnet Physics ERDDAP dataset TS_70_6202404_MO_UND (Copernicus Marine In Situ TAC), "
                  "platform 6202404 'Faial Pico' wave buoy, 38.5877 N 28.5377 W, 2012-05-04 to 2021-10-10",
        "producer": "University of the Azores, Department of Oceanography and Fisheries (IMAR network) / CLIMAAT",
        "licence": "Creative Commons Attribution Share-Alike (CC BY-SA), per dataset metadata",
        "citation": "Data are the property of the producer/owner distributed through EMODnet Physics. "
                    "EMODnet Physics and the partners are not responsible for improper use",
        "era5": "Open-Meteo marine API, models=era5_ocean (ERA5 0.5 deg; Hersbach et al. 2020, Copernicus C3S), CC BY 4.0",
        "qc": "QC flags 1 or 2 only; Hs 0.05-20 m, TEMP 12-28 C; samples within +-30 min averaged to the hour; isolated Hs spikes removed",
        "qc_stats": qstats,
        "coverage_by_year": coverage(buoy),
    }
    json.dump({"meta": meta, "results": results}, open(os.path.join(out, "shelter_ratios.json"), "w"), indent=1)
    json.dump({"meta": meta, "monthly": clim}, open(os.path.join(out, "monthly_climatology.json"), "w"), indent=1)
    with open(os.path.join(out, "buoy_hourly.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["time_utc", "hs_m", "dir_deg", "tz_s", "tmax_s", "hmax_m", "temp_c"])
        for h in sorted(buoy):
            o = buoy[h]
            w.writerow([h.strftime("%Y-%m-%dT%H"),
                        "" if o["hs"] is None else f"{o['hs']:.2f}",
                        "" if o["dir"] is None else f"{o['dir']:.0f}",
                        "" if o["tz"] is None else f"{o['tz']:.1f}",
                        "" if o["tmax"] is None else f"{o['tmax']:.1f}",
                        "" if o["hmax"] is None else f"{o['hmax']:.2f}",
                        "" if o["temp"] is None else f"{o['temp']:.1f}"])


if __name__ == "__main__":
    main()
