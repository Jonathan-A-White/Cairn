"""Ensemble built from the three PUBLISHED transcriptions plus hybrids over the
20 positions contested by every independent transcriber."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from compare import load_all, disputed

CORE=[6,13,22,23,25,26,29,31,33,43,45,53,54,57,66,69,77,80,84,85]

def variants():
    T=load_all(); T.pop('_conf')
    cons,sch,dc = T['consensus'], T['schmeh'], T['dcode']
    V={'E0_consensus':list(cons), 'E1_schmeh':list(sch), 'E2_dcode':list(dc)}
    # hybrid: consensus everywhere, dcode's reading at the contested positions
    for nm,src in (('E3_cons_dcodeCore',dc), ('E4_cons_schmehCore',sch)):
        v=list(cons)
        for i in CORE: v[i]='X'+str(src[i])      # foreign label, kept distinct
        V[nm]=v
    # collapse: contested positions blanked to a single 'unknown' symbol, which
    # is the most conservative reading (they carry no information either way)
    v=list(cons)
    for i in CORE: v[i]='??'
    V['E5_cons_coreMasked']=v
    return V

if __name__=='__main__':
    from collections import Counter
    for k,v in variants().items():
        print(f"{k:20s} n={len(v)} distinct={len(set(v))}")
