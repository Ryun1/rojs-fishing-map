import json, math, sys, time, urllib.request, urllib.parse
res=json.load(open(sys.argv[1]))
LAT0, LON0 = 38.47, -28.3
KX = math.cos(math.radians(LAT0))*111320.0; KY = 110574.0
UA={"User-Agent":"research-script/1.0"}
def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30) as r: return r.read().decode()
        except Exception as e:
            err=str(e); time.sleep(2)
    return "ERR "+err
pts=[]
for sid,r in res.items():
    f=r['facing']; b=int(round(f/5.0)*5)%360
    st={int(k):v for k,v in r['start'].items()}
    # nearest bearing with a defined water start
    cand=sorted(st, key=lambda k: min((k-b)%360,(b-k)%360))
    b=[k for k in cand if st[k] is not None][0]
    s=st[b]; r['prof_bearing']=b; r['shore_exit_m']=round(s)
    r['prof']={}
    for d in (100,300,1000):
        dist=s+d
        x=(r['lon']-LON0)*KX+dist*math.sin(math.radians(b)); y=(r['lat']-LAT0)*KY+dist*math.cos(math.radians(b))
        lat=LAT0+y/KY; lon=LON0+x/KX
        url="https://rest.emodnet-bathymetry.eu/depth_sample?geom="+urllib.parse.quote(f"POINT({lon:.6f} {lat:.6f})")
        t=get(url)
        try:
            j=json.loads(t); em=j.get('avg'); emin=j.get('min'); emax=j.get('max'); interp=j.get('interpolationType'); ref=(j.get('reference') or {}).get('identifier')
        except Exception: em=emin=emax=interp=ref=None; print("bad",sid,d,t[:100],file=sys.stderr)
        r['prof'][d]=dict(lat=round(lat,6),lon=round(lon,6),emodnet=em,emin=emin,emax=emax,interp=interp,ref=ref)
        pts.append((sid,d,lat,lon))
        time.sleep(0.25)
    print(sid,b,r['shore_exit_m'],[r['prof'][d]['emodnet'] for d in (100,300,1000)],file=sys.stderr)
# GEBCO via opentopodata, 100 pts per request
for i in range(0,len(pts),90):
    chunk=pts[i:i+90]
    loc="|".join(f"{p[2]:.6f},{p[3]:.6f}" for p in chunk)
    t=get("https://api.opentopodata.org/v1/gebco2020?locations="+urllib.parse.quote(loc,safe="|,"))
    try:
        j=json.loads(t)
        for p,rr in zip(chunk,j['results']): res[p[0]]['prof'][p[1]]['gebco']=rr['elevation']
    except Exception as e: print("gebco fail",t[:200],file=sys.stderr)
    time.sleep(1.5)
json.dump(res,open(sys.argv[2],'w'))
