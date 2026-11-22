import json, math, sys, time, urllib.request, urllib.parse
res=json.load(open(sys.argv[1]))
LAT0, LON0 = 38.47, -28.3
KX = math.cos(math.radians(LAT0))*111320.0; KY = 110574.0
UA={"User-Agent":"research-script/1.0"}
def pt(r,b,dist):
    x=(r['lon']-LON0)*KX+dist*math.sin(math.radians(b)); y=(r['lat']-LAT0)*KY+dist*math.cos(math.radians(b))
    return LAT0+y/KY, LON0+x/KX
for sid,r in res.items():
    b=r['prof_bearing']; s=r['shore_exit_m']
    a=pt(r,b,s); e=pt(r,b,s+2000)
    url="https://rest.emodnet-bathymetry.eu/depth_profile?geom="+urllib.parse.quote(f"LINESTRING({a[1]:.6f} {a[0]:.6f},{e[1]:.6f} {e[0]:.6f})")
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=40) as resp: arr=json.loads(resp.read().decode())
    except Exception as ex:
        print(sid,"ERR",ex,file=sys.stderr); arr=[]
    n=len(arr); r['profile2km']=arr
    def dist_to(depth):
        for i,v in enumerate(arr):
            if v is not None and v<=-depth: return round(2000.0*i/(n-1)) if n>1 else None
        return None
    r['d20']=dist_to(20); r['d50']=dist_to(50); r['d100']=dist_to(100)
    print(f"{sid:13} n={n:4d} d20={r['d20']} d50={r['d50']} d100={r['d100']} end={arr[-1] if arr else None}",file=sys.stderr)
    time.sleep(0.3)
json.dump(res,open(sys.argv[1],'w'))
