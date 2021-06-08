# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
idx = pd.IndexSlice

from vresutils import Dict
import yaml
snakemake = Dict()
with open('config.yaml', encoding='utf8') as f:
    snakemake.config = yaml.safe_load(f)
color=snakemake.config['plotting']['tech_colors']

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 14
plt.figure(figsize=(12, 15))
gs1 = gridspec.GridSpec(7, 2)
gs1.update(wspace=0.05, hspace=0.05)

transmission='1.0'
cluster='37'
budgets = ['25', '34', '48', '70', '48-noH2network','48-noBECC','48-wo_eff', ]
budget_name = {'25':'1.5$^{\circ}$', 
               '34':'1.6$^{\circ}$',  
               '48':'1.7$^{\circ}$',  
               '70':'2.0$^{\circ}$',  
               '48-noH2network': '1.7$^{\circ}$ \n (no H$_2$ network)' ,
               '48-wo_eff':'1.7$^{\circ}$ \n (no efficiency)',
               '48-noBECC':'1.7$^{\circ}$ \n (no BECC)'}
decays = {'25':['be3', 'ex0'], 
        '34':['be3', 'ex0'],
        '48':['be3', 'ex0'], 
        '48-noH2network':['ex0'], 
        '48-wo_eff':['ex0'], 
        '48-noBECC':['ex0'], 
        '70':['be3', 'ex0']}
NET=['DAC1', 'SMR CC3', 'gas for industry CC3',
     'process emissions CC2', 'solid biomass for industry CC3',
     'urban central gas CHP CC4','urban central solid biomass CHP CC4']
NET_names=['DAC', 'SMR CC', 'gas for industry CC',
     'process emissions CC', 'solid biomass for industry CC',
     'urban central gas CHP CC','urban central solid biomass CHP CC']
colors=[color['DAC'], color['SMR'], 'gray',#color['gas for industry'],
        color['process emissions'], 'lightgreen',#color['solid biomass for industry'],
        color['gas'], 'darkgreen'#color['biogas']
        ]

for i,budget in enumerate(budgets):  
    for j,decay in enumerate(decays[budget]):
        ax1 = plt.subplot(gs1[i,j])
        balances_df = pd.read_csv('results/version-cb{}{}/csvs/supply_energy.csv'.format(budget,decay),index_col=list(range(3)),
                                  header=list(range(4)))
        if budget =='48-noH2network':
            NET2=NET
            opt ='3H-T-H-B-I-solar3-dist1-noH2network-cb48ex0'
        elif budget== '48-wo_eff':
            NET2=NET
            opt ='3H-T-H-B-I-solar3-dist1-cb48ex0'
        elif budget== '48-noBECC':
            opt ='3H-T-H-B-I-solar3-dist1-cb48ex0'
            NET2=['DAC1', 'SMR CC3', 'gas for industry CC3',
                'process emissions CC2', 'urban central gas CHP CC4']
        else:
            NET2=NET
            opt='3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
        sel = -0.000001*balances_df.loc[idx['co2 stored', 'links', :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
        ax1.stackplot([int(x) for x in sel.columns.get_level_values(3)], sel.loc[NET2], colors=colors)
        if j==0:
            ax1.set_ylabel("MtCO$_2$/a")
            ax1.text(2005, -300, budget_name[budget], fontsize=14)
        if j==1:
            ax1.set_yticklabels([])
        if i!=6:
            ax1.set_xticklabels([])
        ax1.set_ylim([-650, 0])
        ax1.set_xlim([2020, 2050])
        if i==0 and j==0:
            ax1.set_title('exponential decay')
        if i==0 and j==1:
            ax1.set_title('beta decay')
ax1.legend(fancybox=True, fontsize=14, loc=(0.2, -1.01), facecolor='white', 
           frameon=True, ncol=2, labels=NET_names)       
plt.savefig('figures/NET_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')
