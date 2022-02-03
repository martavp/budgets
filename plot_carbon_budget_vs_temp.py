# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


plt.figure(figsize=(10, 7))
gs1 = gridspec.GridSpec(1, 1)
ax1 = plt.subplot(gs1[0,0])
#share of carbon budget corresponding to Europe (Raupach 2014, Alcaraz 2018)
share_Europe=0.06453
share_fair=0.055
share_unfair=0.11

# carbon budgets for different confident intervals (67%, 50%, 33%) and 
# temperature increas (IPCC Special Report Global warming 1.5ºC)
cb={}

cb[67]=[400, 550, 700, 850, 1000, 1150]
cb[50]=[500, 650, 850, 1000, 1200, 1350]
cb[33]=[650, 850, 1050, 1250, 1450, 1700]
T= [1.5, 1.6, 1.7, 1.8, 1.9, 2]
col = ['yellowgreen', 'blue', 'gold','orange', 'magenta', 'darkred']
m= ['o', '^', 'v','s', 'D', 'p']
s=[300, 300, 300, 300, 300, 500]

for _m, _col,_cb67, _cb50, _cb33, _T,_s in zip(m, col, cb[67], cb[50], cb[33], T, s):
    ax1.scatter(_cb67*share_Europe, _T, marker=_m, c=_col, s=_s)
    ax1.scatter(_cb50*share_Europe, _T, marker=_m, c=_col, s=_s, alpha=0.5)
    ax1.scatter(_cb33*share_Europe, _T, marker=_m, c=_col, s=_s, alpha=0.3)

ax1.set_ylabel('Temperature Increase ($^{\circ}$C)')
ax1.set_xlabel('Europe carbon budget (GtCO$_2$)') 
ax1.set_xlim(22, 112)
ax1.set_ylim(1.35, 2.05)

# budgets for Europe with other split criteria
ax1.plot(cb[67][2]*share_fair, T[2], marker=m[2], 
            markerfacecolor=col[2], markeredgecolor='black', markersize=16, )
ax1.plot(cb[67][2]*share_unfair, T[2], marker=m[2], 
            markerfacecolor=col[2], markeredgecolor='black', markersize=16, )
ax1.annotate('67% inequitable',xy=(cb[67][2]*share_unfair, 1.7),
             xytext=(cb[67][2]*share_unfair-5, 1.7-0.1),
             fontsize=18, color='black', zorder=-1,
             arrowprops=dict(facecolor='black', lw=0.5, arrowstyle='-'))
ax1.annotate('67% equitable',xy=(cb[67][2]*share_fair, 1.7),
             xytext=(cb[67][2]*share_fair-15, 1.7+0.1),
             fontsize=18, color='black', zorder=-1,
             arrowprops=dict(facecolor='black', lw=0.5, arrowstyle='-'))

ax1.text(cb[67][0]*share_Europe-3, 1.43, '67%', fontsize=18, color=col[0])
ax1.text(cb[50][0]*share_Europe-2, 1.43, '50%', fontsize=18, color=col[0])
ax1.text(cb[33][0]*share_Europe-2, 1.43, '33%', fontsize=18, color=col[0])

plt.savefig('figures/carbon_budget_vs_temperature.png', dpi=300, bbox_inches='tight') 



