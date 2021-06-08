# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
idx = pd.IndexSlice

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 14
plt.figure(figsize=(10, 7))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)



ax1 = plt.subplot(gs1[0,0])
gcb = [420, 580, 800, 1170]
T = [1.5, 1.6, 1.7, 2.0]
discount_rates = [0.0, 0.02, 0.04, 0.06, 0.08]
budgets = ['25', '34', '48', '70']
decays = ['ex0'] #'be3'

color_dr ={0: 'sienna',
          0.02: 'darkgoldenrod',
          0.04:'tan',
          0.06: 'lightseagreen',
          0.08: 'darkcyan',
          0.10 : 'darkslategray'}
marker_cb ={'25':'o', 
           '34':'s', 
           '48':'^', 
           '70':'D',
           'noH2network':'+',
           'wo_eff':'x',
           'noBECC':'1'}
style_decay={'be3':'--', 
             'ex0':'-'}

cb2gcb=pd.Series(gcb,index=budgets).to_dict()

transmission=1.0
cluster=37
for discount_rate in discount_rates:    
    for decay in decays:
        to_plot=[]
        for budget in budgets:
            cumulative_cost_df = pd.read_csv('results/version-cb{}{}/csvs/cumulative_cost.csv'.format(budget,decay))
            cumulative_cost_df = cumulative_cost_df.set_index(['cluster', 'lv', 'opt', 'planning_horizon']).sort_index()
            opt ='3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
            cumulative_system_cost = cumulative_cost_df.loc[idx[cluster,transmission,opt, 'cumulative cost'],str(discount_rate)]/1000000000 #€ to B€ 
            to_plot.append(cumulative_system_cost)  
            facecolor=color_dr[discount_rate] if decay=='be3' else 'white'
            ax1.plot(cb2gcb[budget], cumulative_system_cost,
                     markersize=10,
                     marker=marker_cb[budget],
                     markeredgecolor=color_dr[discount_rate],
                     markerfacecolor=facecolor)
        ax1.plot(gcb, to_plot, 
                 zorder=-1,
                 color=color_dr[discount_rate],
                 linestyle=style_decay[decay],
                 label=discount_rate) 

for scenario in ['noH2network','wo_eff','noBECC']:
    discount_rate=0.02
    budget='48'
    cumulative_cost_df = pd.read_csv('results/version-cb{}-{}{}/csvs/cumulative_cost.csv'.format(budget,scenario,decay))
    cumulative_cost_df = cumulative_cost_df.set_index(['cluster', 'lv', 'opt', 'planning_horizon']).sort_index()

    opt ='3H-T-H-B-I-solar3-dist1-{}-cb{}{}'.format(scenario,budget,decay) if scenario=='noH2network' else '3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
    cumulative_system_cost = cumulative_cost_df.loc[idx[cluster,transmission,opt, 'cumulative cost'],str(discount_rate)]/1000000000 #€ to B€ 
    ax1.plot(cb2gcb[budget], cumulative_system_cost,
             markersize=10,
             linewidth=0,
             marker=marker_cb[scenario],
             markeredgecolor='black', #color_dr[discount_rate],
             markerfacecolor=None,
             label=scenario) 

ax1.set_ylabel('Cumulative System Costs (B€)')   
ax1.set_xlabel('Temperature increase ($^{\circ}C$)') 
ax1.set_xlim(300, 1300)
#ax1.set_ylim(1.2, 2.2) 

ax2=ax1.twiny()
ax2.set_xlim(300, 1300)
ax2.set_xlabel('Global carbon budget (GtCO$_2$)') 
ax1.set_xticks([420, 580, 800, 1170])
ax1.set_xticklabels(T)
#ax1.set_ylim([15000, 17000])
ax1.legend(fancybox=True, fontsize=16, loc=(-0.1, -0.25), facecolor='white', 
           frameon=True, ncol=6)       
plt.savefig('figures/cumulative_system_cost_transmission{}.png'.format(transmission), dpi=600, bbox_inches='tight')


