import json,sys
res=json.load(open(sys.argv[1]))
def comp(b):
    names=["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return names[int((b%360)/22.5+0.5)%16]
def ranges(bs,step=5):
    bs=sorted(bs)
    if not bs: return "-"
    if len(bs)==360//step: return "all"
    s=set(bs); runs=[]
    # find run starts
    for b in bs:
        if (b-step)%360 not in s:
            e=b
            while (e+step)%360 in s: e=(e+step)%360
            runs.append((b,e))
    return ", ".join(f"{a:03d}-{e:03d} ({comp(a)}-{comp(e)})" if a!=e else f"{a:03d}" for a,e in runs)
out={}
for sid,r in res.items():
    f={int(k):v for k,v in r['fetch'].items()}
    openb=[b for b,v in f.items() if v>=40000]
    chan=[b for b,v in f.items() if 2000<=v<40000]
    r['open']=ranges(openb); r['chan']=ranges(chan); r['n_open']=len(openb)*5; r['n_chan']=len(chan)*5
    print(f"{sid:13} face {r['facing']:3d} {comp(r['facing']):3} | open>=40km [{r['n_open']:3d}deg]: {r['open']} | 2-40km [{r['n_chan']:3d}deg]: {r['chan']}")
json.dump(res,open(sys.argv[1],'w'))
