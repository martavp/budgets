# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
#params = {'legend.fontsize': 20,
#          'legend.handlelength': 2}
#plot.rcParams.update(params)

plt.rcParams['axes.titlesize'] = 14
plt.figure(figsize=(7, 5))
gs1 = gridspec.GridSpec(1, 1)
ax1 = plt.subplot(gs1[0,0])

cb=[420, 580, 800, 1170]
E_cb=[25, 34, 48, 70]
T= [1.5, 1.6, 1.7, 2]
col = ['blue', 'dodgerblue', 'lightcoral', 'darkred']
m= ['o', 's', '^', 'D']
s=150*np.ones(4)
for _m, _col, _cb, _T,_s in zip(m, col, E_cb, T, s):
    ax1.scatter(_cb, _T, marker=_m, c=_col, s=_s)
    
ax1.set_ylabel('Temperature Increase ($^{\circ}$C)', fontsize=14)    
ax1.set_xlabel('EU carbon budget (GtCO$_2$)', fontsize=14) 
ax1.grid(color='grey', linestyle='--') #, axis='y')
ax1.set_xlim(22, 80)
ax1.set_ylim(1.2, 2.2)

ax1.plot([41, 74.6], [1.7, 1.7], linewidth=3, color=col[2])
ax1.text(45, 1.72, 'per capita', fontsize=14, color='black')
ax1.text(40, 1.72, 'fair', fontsize=14, color='black')
ax1.text(74, 1.72, 'unfair', fontsize=14, color='black')

plt.savefig('figures/carbon_budget_vs_temperature.png', dpi=300, bbox_inches='tight') 



