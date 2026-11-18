from pathlib import Path
import sys,json,csv,itertools,shutil
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
r=p.parent/'peoplecomfort/release/PeopleComfort_Pages_update'
sys.path.insert(0,str(r/'src'))
from peoplecomfort.core import analyze
j=json.loads((r/'examples/extended-a3/project.json').read_text())
a=analyze(j,True); worlds=a['uncertainty'];dev=a['selection']['T3']['scores'];h=a['selection']['holdout']['scores']
ids=sorted(dev,key=dev.get);gain={d:1-h[d]/h['D0'] for d in ids}
def coverage(d,t,group):
 return sum(w['holdout_regret_by_design'][d]<=w['holdout_regret_by_design']['D0']+t+1e-12 for w in group)/len(group)
def sets(g,t,c):
 cov={d:coverage(d,t,worlds) for d in ids}
 ok=[d for d in ids if gain[d]+1e-12>=g and cov[d]+1e-12>=c]
 def dominates(b,d):
  u=(dev[b],-gain[b],-cov[b]);v=(dev[d],-gain[d],-cov[d])
  return all(x<=y+1e-12 for x,y in zip(u,v)) and any(x<y-1e-12 for x,y in zip(u,v))
 return ok,[d for d in ok if not any(dominates(b,d) for b in ok)]
rows=[]
for g,t,c in itertools.product([0,.10,.20,.30,.35],[0,.01,.02,.05,.10],[.50,2/3,.70,.75,1]):
 ok,front=sets(g,t,c);rows.append([g,t,c,', '.join(ok) or 'None',', '.join(front) or 'None',ok[0] if ok else 'Keep D0'])
def write(name,head,rows):
 with (p/name).open('w',newline='',encoding='utf8') as f: csv.writer(f).writerows([head,*rows])
write('epsilon.csv',['min_gain','tolerance','min_coverage','feasible','Pareto','best_or_fallback'],rows)
write('options.csv',['design','development_regret','holdout_regret','relative_gain','worlds_passing_at_0.01'],[[d,dev[d],h[d],gain[d],round(coverage(d,.01,worlds)*81)] for d in ids])
groups=[]
for dt in [-.5,0,.5]:
 group=[w for w in worlds if w['temperature_offset']==dt]
 groups.append([dt,len(group),round(coverage('D4',.01,group)*len(group))])
write('temperature_check.csv',['common_offset_C','conditions','D4_passes'],groups)
assert round(coverage('D4',.01,worlds)*81)==54
fig,ax=plt.subplots(figsize=(8,3.2),layout='constrained')
ax.barh(['D4  7/5'],[54],height=.34,color='#256964');ax.axvline(61,color='#ad3a24',lw=2);ax.text(61.8,.16,'Required: 61 of 81',color='#963821');ax.text(52,0,'54 pass',ha='right',va='center',color='white');ax.set(xlim=(0,81),ylim=(-.35,.37),xlabel='Stress conditions meeting the D0 + 0.01 tolerance',title='Keep 9/3: the 7/5 candidate falls short of the coverage gate');fig.savefig(p/'threshold.png',dpi=180)
html="""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width, initial-scale=1"><title>PeopleComfort threshold flipbook</title><style>body{font:18px system-ui;max-width:850px;margin:5vh auto;padding:1em;color:#173c37}label{display:inline-block;margin:1em}select{font:inherit}output{display:block;background:#edf5f1;padding:1em} td,th{padding:.4em;text-align:left}</style><h1>Which seating options survive?</h1><p>Change one requirement at a time. Seven designs compete. The fallback is the 9/3 reference.</p><div id=controls></div><output id=result></output><h2>One-at-a-time flips</h2><p>Other controls stay at their current values.</p><div id=slices></div><script>const rows=DATA;let names=['Minimum gain','Allowed excess regret','Minimum coverage'];let s=names.map((n,i)=>{let l=document.createElement('label');l.textContent=n+' ';let e=document.createElement('select');for(let v of [...new Set(rows.map(r=>r[i]))])e.add(new Option(i==1?v:(v*100).toFixed(1)+'%',v));e.value=[.2,.01,.75][i];e.onchange=show;l.append(e);controls.append(l);return e});function show(){let v=s.map(e=>+e.value);let r=rows.find(r=>v.every((x,i)=>x==r[i]));result.textContent='Feasible: '+r[3]+' | Pareto: '+r[4]+' | Decision: '+r[5];slices.innerHTML=names.map((n,i)=>'<h3>'+n+'</h3><table><tr><th>Setting</th><th>Feasible</th><th>Pareto</th><th>Decision</th></tr>'+rows.filter(r=>v.every((x,k)=>k==i||r[k]==x)).map(r=>'<tr><td>'+(i==1?r[i]:(100*r[i]).toFixed(1)+'%')+'</td><td>'+r[3]+'</td><td>'+r[4]+'</td><td>'+r[5]+'</td></tr>').join('')+'</table>').join('')}show()</script>"""
(p/'flipbook.html').write_text(html.replace('DATA',json.dumps(rows)),encoding='utf8')
print('Groups',groups,'base',sets(.2,.01,.75),'relaxed',sets(.2,.01,2/3))
shutil.copy2(r/'coursework/extended_matrix.csv',p/'A3_matrix.csv')
