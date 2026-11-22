import json, math, sys
sys.path.insert(0, sys.argv[1])
from spots import SPOTS
LAT0, LON0 = 38.47, -28.3
KX = math.cos(math.radians(LAT0))*111320.0; KY = 110574.0
def xy(lat,lon): return ((lon-LON0)*KX, (lat-LAT0)*KY)
def ll(x,y): return (LAT0+y/KY, LON0+x/KX)
d=json.load(open(sys.argv[2]))
segs=[]
for e in d['elements']:
    g=e['geometry']
    pts=[xy(p['lat'],p['lon']) for p in g]
    for a,b in zip(pts,pts[1:]): segs.append((a[0],a[1],b[0],b[1]))
print("segments",len(segs),file=sys.stderr)
L=300000.0
def crossings(ox,oy,brg):
    r=math.radians(brg); dx=math.sin(r); dy=math.cos(r)
    out=[]
    for ax,ay,bx,by in segs:
        ex=bx-ax; ey=by-ay
        den=dx*ey-dy*ex
        if den==0: continue
        wx=ax-ox; wy=ay-oy
        t=(wx*ey-wy*ex)/den
        if t<0 or t>L: continue
        u=(wx*dy-wy*dx)/den
        if 0<=u<1: out.append(t)
    out.sort(); return out
def water_intervals(cs):
    iv=[]
    if len(cs)%2==0:
        prev=0.0; i=0
        while i<len(cs):
            iv.append((prev,cs[i])); 
            if i+1<len(cs): prev=cs[i+1]
            i+=2
        iv.append(((cs[-1] if cs else 0.0), float('inf'))) if not cs or len(cs)%2==0 else None
        if cs: iv[-1]=(cs[-1],float('inf'))
    else:
        i=0
        while i+1<len(cs):
            iv.append((cs[i],cs[i+1])); i+=2
        iv.append((cs[-1],float('inf')))
    # merge across land gaps <150 m
    m=[]
    for a,b in iv:
        if m and a-m[-1][1] < 150: m[-1]=(m[-1][0],b)
        else: m.append((a,b))
    return m
res={}
STEP=5
for sid,name,coast,lat,lon,src in SPOTS:
    ox,oy=xy(lat,lon)
    fetch={}; start={}
    for brg in range(0,360,STEP):
        cs=crossings(ox,oy,brg)
        iv=water_intervals(cs)
        f=0.0; s=None
        for a,b in iv:
            if a<=300: f=min(b,L)-a; s=a; break
        fetch[brg]=f; start[brg]=s
    # facing bearing: mean of bearings weighted by min(fetch,40km)
    sx=sum(min(f,40000)*math.sin(math.radians(b)) for b,f in fetch.items())
    sy=sum(min(f,40000)*math.cos(math.radians(b)) for b,f in fetch.items())
    facing=(math.degrees(math.atan2(sx,sy))+360)%360
    res[sid]=dict(name=name,coast=coast,lat=lat,lon=lon,src=src,fetch=fetch,start=start,facing=round(facing))
    print(sid,round(facing),file=sys.stderr)
json.dump(res,open(sys.argv[3],'w'))
