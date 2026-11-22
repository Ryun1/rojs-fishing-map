import json,sys
r=json.load(open('bathy.json'))
def comp(b):
    n=["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]; return n[int((b%360)/22.5+0.5)%16]
order=["formosinha","barca","madalena","areialarga","criacaovelha","pocinho","calhau_w",
 "saomateus","ptasaomateus","coxos","pesqpedro","pontinha","saocaetano","admoiro","arinhas","fonte","lajes","castelete","arrife","ribeiras","mujas","calheta","feteira",
 "manhenha","pontadailha","engrade",
 "calhau_e","baixa","caisinho","santoamaro","prainha","canas","misterio","sma","pocassr","caisdopico","saoroque","santoantonio","cabrito","arcos","lajido","cachorro","mourato"]
grp={"formosinha":"WEST / FAIAL CHANNEL","saomateus":"SOUTH","manhenha":"EAST TIP","calhau_e":"NORTH / SAO JORGE CHANNEL (listed east to west)"}
def q(p):
    e=p['emodnet']; 
    if e is None: return "n/a"
    src=p['ref'] or 'no-src'
    flag='' if (p['ref'] and p['ref'].startswith(('hi','Azores','2019'))) and not p['interp'] else '?'
    return f"{round(e)}{flag}"
out=[]
out.append("| id | Spot | lat, lon | coord source | facing (deg) | open-ocean sector (fetch >= 40 km) | channel / fetch-limited sector (2-40 km) | profile bearing | EMODnet depth m @100 / @300 / @1000 m | GEBCO2020 @100/@300/@1000 | dist. to 20 / 50 / 100 m depth (m) | EMODnet source cells |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for sid in order:
    v=r[sid]
    if sid in grp: out.append(f"| | **{grp[sid]}** | | | | | | | | | | |")
    p=v['prof']
    em=" / ".join(q(p[d]) for d in ("100","300","1000"))
    gb=" / ".join(str(round(p[d]['gebco'])) if p[d].get('gebco') is not None else 'n/a' for d in ("100","300","1000"))
    srcs=", ".join(dict.fromkeys(str(p[d]['ref']) + ('(i)' if p[d]['interp'] else '') for d in ("100","300","1000")))
    dd=" / ".join(str(v[k]) if v[k] is not None else '>2000' for k in ('d20','d50','d100'))
    out.append(f"| {sid} | {v['name']} | {v['lat']:.5f}, {v['lon']:.5f} | {v['src']} | {v['facing']} ({comp(v['facing'])}) | {v['open']} | {v['chan']} | {v['prof_bearing']} | {em} | {gb} | {dd} | {srcs} |")
open('table_geo.md','w').write("\n".join(out)+"\n")
print(len(out))
