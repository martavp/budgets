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
plt.figure(figsize=(10, 30))
gs1 = gridspec.GridSpec(7, 1)
gs1.update(wspace=0.05, hspace=0.1)

transmission='1.0'
cluster='37m'
decay='ex0'
budgets = ['27', '36.7', '51.4', '63' , '75.2']

label_budget = {'27':'1.5$^{\circ}$C',
                '36.7':'1.6$^{\circ}$C', 
                '51.4':'1.75$^{\circ}$C', 
                '63':'1.87$^{\circ}$C', 
                '75.2':'2.0$^{\circ}$C',
                '51.4-low_biomass':'1.75$^{\circ}$C low biomass', 
                '51.4-high_biomass':'1.75$^{\circ}$C high biomass', 
                '51.4-nobiomassCC':'1.75$^{\circ}$C no biomass CC'}

NET=['DAC1', 'SMR CC3', 'gas for industry CC3',
     'process emissions CC2', 'solid biomass for industry CC3',
     'urban central gas CHP CC4','urban central solid biomass CHP CC4']

NET_names=['DAC', 'SMR CC', 'gas for industry CC',
     'process emissions CC', 'solid biomass for industry CC',
     'urban central gas CHP CC','urban central solid biomass CHP CC']

CCUS_names=['co2 stored','Fischer-Tropsch', 'Sabatier', 'Helmeth']

colors=[color['DAC'], 
        color['SMR'], 
        'gray', #color['gas for industry'],
        color['process emissions'], 
        'lightgreen', #color['solid biomass for industry'],
        color['gas'], 'darkgreen']  #color['biogas']

colors2=['darkorange', #color['co2 stored'], 
         'gold', #color['Fischer-Tropsch'], 
         color['Sabatier'], 
         color['helmeth']]

CCUS=[ 'co2 stored','Fischer-Tropsch2', 'Sabatier2', 'helmeth2']

for i,budget in enumerate(budgets):
    ax1 = plt.subplot(gs1[i,0])
    balances_df = pd.read_csv('results/version-baseline/csvs/supply_energy.csv', #.format(budget,decay),
                              index_col=list(range(3)), header=list(range(4)))
    NET2=NET
    opt='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget,decay)
    
    sel = -0.000001*balances_df.loc[idx['co2 stored', ['links','stores'], :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
    
    ax1.stackplot([int(x) for x in sel.columns.get_level_values(3)], sel.loc[NET2], colors=colors) 
    ax1.stackplot([int(x) for x in sel.columns.get_level_values(3)], sel.loc[CCUS], colors=colors2) 
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2021, -900, label_budget[budget], fontsize=18)
    if i!=(len(budgets)-1):
        ax1.set_xticklabels([])
    ax1.set_ylim([-1100, 1100])
    ax1.set_xlim([2020, 2050])

ax1.legend(fancybox=True, fontsize=18, loc=(-0.1, -1.0), facecolor='white', 
           frameon=True, ncol=2, labels=NET_names+CCUS_names)       
plt.savefig('figures/NET_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')
#%%
plt.figure(figsize=(10, 30))
gs1 = gridspec.GridSpec(7, 1)
gs1.update(wspace=0.05, hspace=0.1)
sensitivities=['51.4', 
               #'51.4-low_biomass',
               #'51.4-high_biomass',
               '51.4-nobiomassCC']

for i,budget in enumerate(sensitivities):
    ax1 = plt.subplot(gs1[i,0])
    if budget!='51.4':
        sensitivity=budget.split('-')[1]
        balances_df = pd.read_csv('results/version-sensitivity-{}/csvs/supply_energy.csv'.format(sensitivity),
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='168H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget.split('-')[0],decay)
        
        if budget=='51.4-nobiomassCC':
            NET2=['DAC1', 'SMR CC3', 'gas for industry CC3',
                  'process emissions CC2', 'urban central gas CHP CC4']

    else:
        balances_df = pd.read_csv('results/version-baseline/csvs/supply_energy.csv',
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget,decay)
        NET2=NET

    
    sel = -0.000001*balances_df.loc[idx['co2 stored', ['links','stores'], :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
    
    ax1.stackplot([int(x) for x in sel.columns.get_level_values(3)], sel.loc[NET2], colors=colors) 
    ax1.stackplot([int(x) for x in sel.columns.get_level_values(3)], sel.loc[CCUS], colors=colors2) 
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2021, -500, label_budget[budget], fontsize=18)
    if i!=(len(sensitivities)-1):
        ax1.set_xticklabels([])
    ax1.set_ylim([-600, 600])
    ax1.set_xlim([2020, 2050])

ax1.legend(fancybox=True, fontsize=18, loc=(-0.1, -1.0), facecolor='white', 
           frameon=True, ncol=2, labels=NET_names+CCUS_names)       
plt.savefig('figures/NET_sensitivity_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')