#!/usr/bin/env python3
"""Read catch photos and list when and where each was taken (design 7.8).

Usage: python3 tools/photos.py PHOTO_FOLDER [OUT.json]

For every JPEG in PHOTO_FOLDER (searched recursively) it reads the photo's
own time and GPS position from its EXIF data and finds the nearest spot in
data/spots.json. Nothing is uploaded and the photos are not changed.

The output holds exact coordinates, so keep it OUT of the repository (the
repo is public). Only spot ids go into data/catches.json.

Photo times are local Azores time unless the camera wrote an offset; the
script converts them to UTC with the Azores rule (UTC-1, UTC+0 in summer).
"""
import json, math, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
NEAR_M, NEW_PLACE_M = 500, 2000  # first guesses; see design 7.8


def last_sunday(y, m):
    d = datetime(y, m + 1, 1) - timedelta(days=1) if m < 12 else datetime(y, 12, 31)
    return d - timedelta(days=(d.weekday() + 1) % 7)


def azores_to_utc(t):
    """Local Azores wall time to UTC. Summer time runs from 00:00 local on the
    last Sunday of March to 01:00 local on the last Sunday of October."""
    start = last_sunday(t.year, 3)
    end = last_sunday(t.year, 10) + timedelta(hours=1)
    off = 0 if start <= t < end else -1
    return t - timedelta(hours=off)


def dist_m(a, b, c, d):
    r = 6371000
    p1, p2 = math.radians(a), math.radians(c)
    dp, dl = p2 - p1, math.radians(d - b)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def dms(v, ref):
    x = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
    return -x if ref in ('S', 'W') else x


def read(path):
    rec = {'file': str(path), 'time_local': None, 'time_utc': None, 'lat': None, 'lon': None, 'camera': None}
    try:
        ex = Image.open(path).getexif()
    except Exception as e:
        rec['error'] = f'cannot read: {e}'
        return rec
    sub = ex.get_ifd(0x8769)
    gps = ex.get_ifd(0x8825)
    rec['camera'] = ' '.join(str(x).strip() for x in (ex.get(271), ex.get(272)) if x) or None
    raw = sub.get(36867) or ex.get(306)
    if raw:
        try:
            t = datetime.strptime(str(raw).strip()[:19], '%Y:%m:%d %H:%M:%S')
            rec['time_local'] = t.isoformat(timespec='minutes')
            off = sub.get(36881) or sub.get(36880)
            if off:
                sign = -1 if str(off).startswith('-') else 1
                hh, mm = str(off)[1:].split(':')
                u = t - sign * timedelta(hours=int(hh), minutes=int(mm))
                rec['time_source'] = 'camera offset ' + str(off)
            else:
                u = azores_to_utc(t)
                rec['time_source'] = 'assumed Azores time'
            rec['time_utc'] = u.replace(tzinfo=timezone.utc).isoformat(timespec='minutes').replace('+00:00', 'Z')
        except ValueError:
            pass
    if gps.get(2) and gps.get(4):
        rec['lat'] = round(dms(gps[2], gps.get(1, 'N')), 5)
        rec['lon'] = round(dms(gps[4], gps.get(3, 'E')), 5)
    return rec


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    spots = json.load(open(ROOT / 'data/spots.json', encoding='utf-8'))['spots']
    files = sorted(p for p in Path(sys.argv[1]).rglob('*') if p.suffix.lower() in ('.jpg', '.jpeg'))
    out = []
    for p in files:
        r = read(p)
        if r['lat'] is not None:
            best = min(spots, key=lambda s: dist_m(r['lat'], r['lon'], s['lat'], s['lon']))
            d = dist_m(r['lat'], r['lon'], best['lat'], best['lon'])
            r['nearest_spot'], r['nearest_m'] = best['id'], round(d)
            r['place'] = 'spot' if d <= NEAR_M else 'near a spot, check' if d <= NEW_PLACE_M else 'ask Roj'
        else:
            r['place'] = 'no location: ask Roj'
        out.append(r)
    skipped = [p.name for p in Path(sys.argv[1]).rglob('*') if p.suffix.lower() in ('.heic', '.heif', '.png')]
    dest = sys.argv[2] if len(sys.argv) > 2 else 'photos_read.json'
    json.dump({'photos': out, 'skipped_not_jpeg': skipped}, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n_t = sum(1 for r in out if r['time_utc'])
    n_g = sum(1 for r in out if r['lat'] is not None)
    print(f'{len(out)} photos: {n_t} with time, {n_g} with location; {len(skipped)} skipped (not JPEG). Wrote {dest}')


if __name__ == '__main__':
    main()
