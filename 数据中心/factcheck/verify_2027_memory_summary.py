#!/usr/bin/env python3
"""Reproduce order-of-magnitude estimates and their explicit assumptions.
Inputs are registered in ../存储与NAND/HBM/2027HBM与普通DRAM出货预测.md.
Only prints results, does not modify source data.
"""
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / '存储与NAND/HBM/2027HBM与普通DRAM出货预测.md'

def main():
    if not REPORT.exists():
        raise FileNotFoundError(REPORT)
    bases = {'Samsung':13.2, 'SK':12.8, 'Micron':8.4, 'Other':5.6}
    growth = {'Samsung':(.10,.20), 'SK':(.10,.22), 'Micron':(.15,.25), 'Other':(.20,.40)}
    for scenario, fraction in [('low',0),('mid',.5),('high',1)]:
        values = {k:b*(1+growth[k][0]+fraction*(growth[k][1]-growth[k][0])) for k,b in bases.items()}
        print('Company scenario EB:',scenario,values,'total',sum(values.values()))
    print('HBM supply envelope:',3.6*1.5,4*1.6)
    for total,hbm in [(45,5.5),(47,6),(50,6.5)]:
        print('Paired DRAM/HBM/conventional EB:',total,hbm,total-hbm)
    print('NVIDIA HBM with Ultra sensitivity:',.93312+27000*72*512/1e9,1.099008+32000*72*768/1e9)
    print('Rubin CPU sensitivity:',45000*54*.5/1e6,50000*54/1e6)
    print('Samsung annual average WPM:', 8175000/12, 8280000/12)
    print('Samsung growth %:', (8280000/8175000-1)*100)
    for end, efficiency, drag in [(80,.04,.02),(90,.08,.02),(120,.12,.025)]:
        avg=500+(40+end)/2
        print('SK avg kWSPM, delta, wafer %, bit %:', avg,avg-520,(avg/520-1)*100,(avg/520*(1+efficiency)*(1-drag)-1)*100)
    for factor in [.25,.5]:
        print('Tongluo project average threshold kWSPM:',factor,[base*.1*factor for base in [375,385]])
    components=[14.90,14.25,9.40,3.90,.75,1.92]
    print('MemoryTicker total EB, delta, %:',sum(components),sum(components)-39.85,(sum(components)/39.85-1)*100)
    print('UBS demand EB 2026,2027,delta,%:',32.9/8,58/8,(58-32.9)/8,(58/32.9-1)*100)
    print('Old mixed-source HBM growth %:',(1.24*.13/.09-1)*100)
    print('Rubin HBM EB:',[r*72*288/1e9 for r in [45000,50000]])
    print('GB300 tail HBM EB:',3000*72*288/1e9)
    print('Ultra conditional HBM EB:',[r*72*768/1e9 for r in [27000,32000]])
    print('10GW blueprint HBM EB, max CPU EB:',10*3200*72*288/1e9,10*3200*54/1e6)

if __name__=='__main__':
    main()
