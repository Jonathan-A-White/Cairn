"""Summary figure: where Dorabella falls in each null distribution."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import ensemble
from phase23 import null_dist, eng_sample, shorthand, mono_encipher, uniform_sym, melody, ic
import corpus

def panelA(ax):
    d=corpus.get(); text=d['text']
    models=[('English',        lambda: eng_sample(text)),
            ('English abbrev.',lambda: shorthand(eng_sample(text,140))[:87]),
            ('mono-enciph. Eng',lambda: mono_encipher(eng_sample(text))),
            ('melody',         lambda: melody()),
            ('uniform 18',     lambda: uniform_sym(18)),
            ('uniform 24',     lambda: uniform_sym(24))]
    data=[]; names=[]
    for nm,g in models:
        data.append(null_dist(g, reps=3000)['ic']); names.append(nm)
    parts=ax.violinplot(data, vert=False, showmeans=False, showextrema=False, widths=.9)
    for b in parts['bodies']: b.set_alpha(.45); b.set_facecolor('#5b8db8')
    obs=[ic(v) for v in ensemble.variants().values()]
    for o in obs: ax.axvline(o, color='#c0392b', alpha=.5, lw=1)
    ax.axvline(obs[0], color='#c0392b', lw=2.2, label='Dorabella (T0)')
    ax.set_yticks(range(1,len(names)+1)); ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('index of coincidence at n=87'); ax.legend(fontsize=8, loc='upper right')
    ax.set_title('A. IC: the hypotheses that matter overlap; only uniform is excluded',
                 fontsize=10, loc='left')

def parse_solver2(path):
    txt=open(path).read()
    def grab(pat):
        m=re.search(pat, txt)
        return float(m.group(1)) if m else None
    out={}
    out['eng']   =(grab(r'enciphered real English : mean=(-?\d+\.\d+)'), grab(r'enciphered real English : mean=-?\d+\.\d+ sd=(\d+\.\d+)'))
    out['shuf']  =(grab(r'shuffled Dorabella      : mean=(-?\d+\.\d+)'), grab(r'shuffled Dorabella      : mean=-?\d+\.\d+ sd=(\d+\.\d+)'))
    out['unif']  =(grab(r'uniform random          : mean=(-?\d+\.\d+)'), grab(r'uniform random          : mean=-?\d+\.\d+ sd=(\d+\.\d+)'))
    obs=re.findall(r'\s+(T\d_\w+)\s+(-\d+\.\d+)\s+(-\d+\.\d+)\s+', txt)
    out['obs']=[(a,float(b),float(c)) for a,b,c in obs]
    return out

def panelB(ax, s2):
    ys={'enciphered\nreal English':s2['eng'],'shuffled\nDorabella':s2['shuf'],'uniform\nrandom':s2['unif']}
    for i,(nm,(m,sd)) in enumerate(ys.items(),1):
        if m is None: continue
        x=np.linspace(m-3.2*sd, m+3.2*sd, 200)
        y=np.exp(-0.5*((x-m)/sd)**2); y=y/y.max()*.38
        ax.fill_between(x, i-y, i+y, alpha=.45, color='#5b8db8')
        ax.plot([m,m],[i-.38,i+.38], color='#34495e', lw=1)
    for nm,f,r in s2['obs']:
        ax.axvline(f, color='#c0392b', alpha=.45, lw=1)
    if s2['obs']:
        ax.axvline(s2['obs'][0][1], color='#c0392b', lw=2.2, label='Dorabella (T0)')
    ax.set_yticks(range(1,len(ys)+1)); ax.set_yticklabels(list(ys), fontsize=9)
    ax.set_xlabel('best quadgram score per gram, matched search budget')
    ax.legend(fontsize=8, loc='upper left')
    ax.set_title("B. Solver: Dorabella sits in the null's upper tail, nowhere near English",
                 fontsize=10, loc='left')

def parse_noise(path):
    rows=[]
    for l in open(path):
        m=re.match(r'\s+(\d\.\d\d)\s+(-\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', l)
        if m: rows.append(tuple(float(x) for x in m.groups()))
    return rows

def panelC(ax, noise, s2):
    r=[x[0] for x in noise]; s=[x[1] for x in noise]; sd=[x[2] for x in noise]; acc=[x[3] for x in noise]
    ax.errorbar(r, s, yerr=sd, marker='o', color='#2c3e50', lw=1.6, capsize=3,
                label='enciphered English, corrupted at rate r')
    if s2['obs']:
        o=s2['obs'][0][1]
        ax.axhline(o, color='#c0392b', lw=2, label=f'Dorabella observed ({o:.2f})')
    if s2['shuf'][0]:
        ax.axhline(s2['shuf'][0], color='#7f8c8d', ls='--', lw=1.4,
                   label=f"shuffled-text null ({s2['shuf'][0]:.2f})")
    ax.axvspan(0.21, 0.45, color='#e67e22', alpha=.15)
    ax.text(0.33, s[0]-0.15, "this transcription's\nown ambiguity rate", ha='center',
            fontsize=8, color='#a04000')
    ax2=ax.twinx(); ax2.plot(r, acc, marker='s', ms=4, color='#27ae60', lw=1.2, alpha=.8)
    ax2.set_ylabel('solver char-accuracy', color='#27ae60', fontsize=9)
    ax2.tick_params(axis='y', colors='#27ae60'); ax2.set_ylim(0,1.05)
    ax.set_xlabel('symbol-confusion (transcription error) rate')
    ax.set_ylabel('best quadgram score/gram')
    ax.legend(fontsize=8, loc='lower left')
    ax.set_title('C. Transcription noise alone reproduces Dorabella\'s unsolvability',
                 fontsize=10, loc='left')

if __name__=='__main__':
    s2=parse_solver2('out/solver2.log')
    noise=parse_noise('out/noise.log')
    fig,axes=plt.subplots(3,1, figsize=(9,10.5))
    panelA(axes[0]); panelB(axes[1], s2); panelC(axes[2], noise, s2)
    for a in axes[:2]: a.grid(alpha=.2, axis='x')
    axes[2].grid(alpha=.2)
    fig.suptitle('Dorabella cipher against simulated nulls at n = 87', fontsize=12)
    fig.tight_layout()
    fig.savefig('out/summary.png', dpi=140)
    print("wrote out/summary.png"); print(s2)
