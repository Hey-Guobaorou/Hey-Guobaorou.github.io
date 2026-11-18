from pathlib import Path
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator,FixedFormatter
p=Path(__file__).resolve().parent
rows=list(csv.DictReader((p/'epsilon.csv').open()))
data=sorted((float(r['min_coverage']),r['Pareto']) for r in rows if float(r['min_gain'])==.2 and float(r['tolerance'])==.01)
assert [d for _,d in data]==['D4','D4','None','None','None']
fig,ax=plt.subplots(figsize=(12,4.9))
fig.subplots_adjust(left=.065,right=.955,top=.7,bottom=.32)
fig.text(.055,.92,'7/5 survives through 54 of 81; any higher coverage requirement removes it.',fontsize=17,weight='bold')
fig.text(.055,.83,'Minimum improvement: 20%     |     Allowed excess regret: 0.01',fontsize=12)
cut=100*2/3
ax.axvline(cut,color='#217266',ls='--',lw=1.6)
ax.plot([50,cut],[0,0],lw=4,color='#217266');ax.plot([cut,100],[0,0],lw=2,color='#929899')
for i,(x,s) in enumerate(data):
 x*=100
 ax.scatter(x,0,s=100,facecolor='#217266' if s=='D4' else 'white',edgecolor='#217266' if s=='D4' else '#606766',lw=2,zorder=4)
 ax.annotate('{D4}' if s=='D4' else 'Empty',(x,0),xytext=(-9 if i==1 else 0,19 if i!=2 else -25),ha='center',textcoords='offset points',weight='bold',color='#174d44' if s=='D4' else '#4c5352')
ax.set(xlim=(48,102),ylim=(-.7,.7),yticks=[],xlabel='Required coverage across the 81 stress conditions')
ax.set_xticks([50,cut,70,75,100],['50%','2/3','70%','75%','100%'])
ax.spines[['top','left','right']].set_visible(False)
fig.text(.055,.125,'At 50%, D1 (51/81) and D4 (54/81) are feasible. D4 dominates D1, so only D4 is on the Pareto front.',fontsize=11)
fig.text(.055,.065,'D4 passes at equality. Above 2/3 the Pareto set is empty; the decision returns to the reference layout D0 (9/3).',fontsize=11)
for ext in ['png','svg']:fig.savefig(p/('coverage_strip.'+ext),dpi=200)
