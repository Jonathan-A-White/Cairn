"""TRANS+MASC: transposition composed with simple substitution.

Documented in Elgar's library (Schooling Article IV, No. 46, the Pack of Cards
cipher: message written down columns, order restored by rhyme -- columnar
transposition). Never swept by anyone, including this report.

The signature it predicts matches the observation: transposition leaves
single-symbol frequencies untouched (Dorabella's are English-like) while
destroying bigram and quadgram structure (the solver deficit). And unlike the
dial, it stays inside the unicity bound: MASC 27.3 chars + <=15.3 bits of
column-order entropy ~ 32 chars against 87 available.

Each candidate inverse permutation is applied, then the residual solved as a
MASC. The null runs the identical best-of-family procedure on shuffled text.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from compare import load_all
from solver import solve, norm
N=87; ROWS=[29,31,27]
SCAN_R=8; SCAN_I=9000
RNG=np.random.default_rng(1896)

def columnar(n,k,order=None):
    """indices read out column-by-column from a k-column row-wise fill."""
    order = list(range(k)) if order is None else list(order)
    rows=(n+k-1)//k
    idx=[]
    for c in order:
        for r in range(rows):
            p=r*k+c
            if p<n: idx.append(p)
    return idx

def rowgrid_perms(n):
    """route variants over the 29/31/27 line structure."""
    out={}
    rows=[]; k=0
    for L in ROWS: rows.append(list(range(k,k+L))); k+=L
    out['reverse']=list(range(n))[::-1]
    out['row_boustro']=rows[0]+rows[1][::-1]+rows[2]
    out['rows_reversed_each']=rows[0][::-1]+rows[1][::-1]+rows[2][::-1]
    out['row_order_312']=rows[2]+rows[0]+rows[1]
    out['row_order_231']=rows[1]+rows[2]+rows[0]
    # column read across the three lines (ragged)
    col=[]
    for i in range(max(ROWS)):
        for r in rows:
            if i<len(r): col.append(r[i])
    out['column_read']=col
    return out

def family(n=N):
    F={'identity':list(range(n))}
    for k in range(2,9):
        F[f'col{k}']=columnar(n,k)
        F[f'col{k}_rev']=columnar(n,k,order=list(range(k))[::-1])
    F.update(rowgrid_perms(n))
    return F

def apply_perm(seq, idx):
    return [seq[i] for i in idx]

def best_of_family(seq, seed0, F, ret_all=False):
    out=[]
    for j,(name,idx) in enumerate(F.items()):
        s=apply_perm(seq,idx)
        b,pt,_,_=solve(s,restarts=SCAN_R,iters=SCAN_I,seed=seed0+j)
        out.append((norm(b,len(seq)),name,pt))
    out.sort(key=lambda t:-t[0])
    return out if ret_all else out[0][0]

if __name__=='__main__':
    T=load_all(); cons=T['consensus']
    F=family()
    print("="*78); print("TRANS+MASC SWEEP (Schooling No. 46, Pack of Cards)"); print("="*78)
    print(f"\nfamily size: {len(F)} permutations; budget {SCAN_R}x{SCAN_I} everywhere\n")
    res=best_of_family(cons,500,F,ret_all=True)
    print(f"{'rank':>4s} {'permutation':>20s} {'score/gram':>11s}   plaintext")
    for r,(sc,nm,pt) in enumerate(res[:10],1):
        tag='  <- identity' if nm=='identity' else ''
        print(f"{r:4d} {nm:>20s} {sc:11.3f}   {pt}{tag}")
    ident=[t for t in res if t[1]=='identity'][0][0]
    print(f"\nidentity: {ident:.3f}    best-of-family: {res[0][0]:.3f} ({res[0][1]})")
    print(f"\nnull: identical best-of-{len(F)} procedure on shuffled text (10 reps)")
    nulls=[]
    for t in range(10):
        s=list(cons); RNG.shuffle(s)
        nulls.append(best_of_family(s,9000+t*100,F))
        print(f"  rep {t+1:2d}: {nulls[-1]:.3f}", flush=True)
    nulls=np.array(nulls)
    print(f"\n  null mean={nulls.mean():.3f} sd={nulls.std():.3f} max={nulls.max():.3f}")
    print(f"  observed={res[0][0]:.3f}  z={(res[0][0]-nulls.mean())/nulls.std():+.2f}"
          f"  p={(nulls>=res[0][0]).mean():.3f}")
    print(f"\n  Reference: enciphered real English at n=87 ~ -4.20/gram.")
