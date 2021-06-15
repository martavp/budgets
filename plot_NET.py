# -*- coding: utf-8 -*-
import pandas as pd
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
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18
plt.figure(figsize=(10, 21))
gs1 = gridspec.GridSpec(7, 1)
gs1.update(wspace=0.05, hspace=0.05)

transmission='1.0'
cluster='37'
decay='ex0'
budgets = ['25', '34', '48', '70', '48-noH2network','48-noBECC','48-wo_eff', ]
budget_name = {'25':'1.5$^{\circ}$C',
               '34':'1.6$^{\circ}$C',
               '48':'1.7$^{\circ}$C',
               '70':'2.0$^{\circ}$C',
               '48-noH2network': '1.7$^{\circ}$C (no H$_2$ network)' ,
               '48-wo_eff':'1.7$^{\circ}$C (no efficiency)',
               '48-noBECC':'1.7$^{\circ}$C (no BECC)'}
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
    ax1 = plt.subplot(gs1[i,0])
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
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2021, -600, budget_name[budget], fontsize=18)
    if i!=6:
        ax1.set_xticklabels([])
    ax1.set_ylim([-650, 0])
    ax1.set_xlim([2020, 2050])

ax1.legend(fancybox=True, fontsize=18, loc=(0, -1.01), facecolor='white', 
           frameon=True, ncol=2, labels=NET_names)       
plt.savefig('figures/NET_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')
