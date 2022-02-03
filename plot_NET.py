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
plt.figure(figsize=(10, 20))
gs1 = gridspec.GridSpec(7, 2)
gs1.update(wspace=0.05, hspace=0.1)

version='baseline' #'sensitivity-fixedcosts' #  #

transmission='1.0'
cluster='37m'
decay='ex0'

budgets = ['25.7',
           '35.4',
           '45.0',
           '54.7', 
           '64.3', 
           '73.9']
#           '45.0-noH2network',
#           '45.0-endo_efficiency',
#           '45.0-nobiomassCC']

label_budget={'25.7':'1.5$^{\circ}$C', 
             '35.4':'1.6$^{\circ}$C',
             '45.0':'1.7$^{\circ}$C',
             '54.7':'1.8$^{\circ}$C',
             '64.3':'1.9$^{\circ}$C',
             '73.9':'2.0$^{\circ}$C',
             '45.0-noH2network':'1.7$^{\circ}$C (no H$_2$ network)',
             '45.0-endo_efficiency':'1.7$^{\circ}$C (endog. eff.)',
             '45.0-nobiomassCC':'1.7$^{\circ}$C (no biomass CC)'}

NET=['DAC1', 'gas for industry CC3',
     'process emissions CC2', 'solid biomass for industry CC3',
     'urban central solid biomass CHP CC4',
     'SMR CC3','urban central gas CHP CC4',
     ]

NET_names=['DAC', 'gas for industry CC',
           'process emissions CC', 'solid biomass for industry CC',
           'solid biomass CHP CC',
           'SMR CC', 'gas CHP CC',
           ]

CCUS_names=['sequestered CO2','Fischer-Tropsch', 'Methanation', 'Helmeth']

colors=[color['DAC'],
        'gray', #color['gas for industry'],
        color['process emissions'], 
        'lightgreen', #color['solid biomass for industry'],
        'darkgreen', #color['biogas']
        color['SMR'],
        color['gas'],]

colors2=['darkorange', #color['co2 stored'], 
         'gold', #color['Fischer-Tropsch'], 
         color['Sabatier'], 
         color['helmeth']]

CCUS=[ 'co2 stored','Fischer-Tropsch2', 'Sabatier2', 'helmeth2']

for i,budget in enumerate(budgets):
    ax1 = plt.subplot(gs1[i,0])
    ax2 = plt.subplot(gs1[i,1])
    balances_df = pd.read_csv('results/version-{}/csvs/supply_energy.csv'.format(version),
                              index_col=list(range(3)), header=list(range(4)))
    NET2=NET
    opt='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget,decay)
    
    sel = 0.000001*balances_df.loc[idx['co2 stored', ['links','stores'], :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
    
    # Add one value per year to plot step-wise figures
    data=sel.loc[NET2]
    data.columns=[int(x) for x in data.columns.get_level_values(3)]
    for year in range(2020,2055,5):
        for j in range(0,5):
            data[year-2+j]=data[year]
    data=data.reindex(sorted(data.columns), axis=1)
    data.drop(columns=[2018,2019,2020,2051,2052])
    ax1.stackplot(data.columns, data, colors=colors)
    
     # Add one value per year to plot step-wise figures
    data=-sel.loc[CCUS]
    data.columns=[int(x) for x in data.columns.get_level_values(3)]
    for year in range(2020,2055,5):
        for j in range(0,5):
            data[year-2+j]=data[year]
    data=data.reindex(sorted(data.columns), axis=1)
    data.drop(columns=[2018,2019,2020,2051,2052])
    ax2.stackplot(data.columns, data, colors=colors2)
    
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2021, 750, label_budget[budget], fontsize=18)
    ax2.text(2021, 750, label_budget[budget], fontsize=18)
    
    ax1.set_xticks([2030, 2040, 2050])
    ax2.set_xticks([2030, 2040, 2050])
    if i!=(len(budgets)-1):
        ax1.set_xticklabels([])
        ax2.set_xticklabels([])
    else:
        ax1.set_xticklabels(['2030', '2040', '2050'])
        ax2.set_xticklabels(['2030', '2040', '2050'])
        
    ax1.set_yticks([0, 200, 400, 600, 800])
    ax2.set_yticks([0, 200, 400, 600, 800])
    ax2.set_yticklabels([])
    ax1.set_ylim([0, 900])
    ax2.set_ylim([0, 900])
    ax1.set_xlim([2020, 2050])
    ax2.set_xlim([2020, 2050])

ax1.legend(fancybox=True, fontsize=16, loc=(-0.1, -1.3), facecolor='white', 
           frameon=True, ncol=1, labels=NET_names)
ax2.legend(fancybox=True, fontsize=16, loc=(0.1, -1.0), facecolor='white', 
           frameon=True, ncol=1, labels=CCUS_names)
plt.savefig('figures/NET_transmission{}_{}.png'.format(transmission,version),
            dpi=600, bbox_inches='tight')
#%%
"""
Sensitivity no biomass with cc scenario
"""
plt.figure(figsize=(10, 20))
gs1 = gridspec.GridSpec(7, 2)
gs1.update(wspace=0.05, hspace=0.1)
sensitivities=['45.0', 
               '45.0-nobiomassCC']

for i,budget in enumerate(sensitivities):
    ax1 = plt.subplot(gs1[i,0])
    ax2 = plt.subplot(gs1[i,1])
    if budget!='45.0':
        sensitivity=budget.split('-')[1]
        balances_df = pd.read_csv('results/version-sensitivity-{}/csvs/supply_energy.csv'.format(sensitivity),
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget.split('-')[0],decay)
        
        if budget=='45.0-nobiomassCC':
            NET2=['DAC1', 'gas for industry CC3',
                  'process emissions CC2', 'SMR CC3', 'urban central gas CHP CC4']


    else:
        balances_df = pd.read_csv('results/version-baseline/csvs/supply_energy.csv',
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget,decay)
        NET2=NET

    
    sel = 0.000001*balances_df.loc[idx['co2 stored', ['links','stores'], :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
    
    # Add one value per year to plot step-wise figures
    data=sel.loc[NET2]
    data.columns=[int(x) for x in data.columns.get_level_values(3)]
    for year in range(2020,2055,5):
        for j in range(0,5):
            data[year-2+j]=data[year]
    data=data.reindex(sorted(data.columns), axis=1)
    data.drop(columns=[2018,2019,2020,2051,2052])
    ax1.stackplot(data.columns, data, colors=colors)
    
     # Add one value per year to plot step-wise figures
    data=-sel.loc[CCUS]
    data.columns=[int(x) for x in data.columns.get_level_values(3)]
    for year in range(2020,2055,5):
        for j in range(0,5):
            data[year-2+j]=data[year]
    data=data.reindex(sorted(data.columns), axis=1)
    data.drop(columns=[2018,2019,2020,2051,2052])
    ax2.stackplot(data.columns, data, colors=colors2)
    
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2021, 750, label_budget[budget], fontsize=18)
    ax2.text(2021, 750, label_budget[budget], fontsize=18)
    
    ax1.set_xticks([2030, 2040, 2050])
    ax2.set_xticks([2030, 2040, 2050])
    if i!=(len(budgets)-1):
        ax1.set_xticklabels([])
        ax2.set_xticklabels([])
    else:
        ax1.set_xticklabels(['2030', '2040', '2050'])
        ax2.set_xticklabels(['2030', '2040', '2050'])
        
    ax1.set_yticks([0, 200, 400, 600, 800])
    ax2.set_yticks([0, 200, 400, 600, 800])
    ax2.set_yticklabels([])
    ax1.set_ylim([0, 900])
    ax2.set_ylim([0, 900])
    ax1.set_xlim([2020, 2050])
    ax2.set_xlim([2020, 2050])


NET=['DAC1', 'gas for industry CC3',
     'process emissions CC2', 'solid biomass for industry CC3',
     'urban central solid biomass CHP CC4',
     'SMR CC3','urban central gas CHP CC4',
     ]

NET_names2=['DAC', 'gas for industry CC',
           'process emissions CC', 'solid biomass for industry CC',
           'solid biomass CHP CC',
           'SMR CC', 'gas CHP CC',
           ]

ax1.legend(fancybox=True, fontsize=16, loc=(-0.1, -1.1), facecolor='white', 
           frameon=True, ncol=1, labels=NET_names)
ax2.legend(fancybox=True, fontsize=16, loc=(0.1, -1.0), facecolor='white', 
           frameon=True, ncol=1, labels=CCUS_names)

plt.savefig('figures/NET_sensitivity_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')

#%%
"""
Sensitivity CO2 sequestration cost and potential
"""

label_budget={'45.0':'1.7$^{\circ}$C, potential*1, cost*1',
             'potential1_cost100': '1.7$^{\circ}$C, potential*1, cost*100',
             'potential100_cost1': '1.7$^{\circ}$C, potential*100, cost*1',
             'potential100_cost0.1': '1.7$^{\circ}$C, potential*100, cost*0.1',}

plt.figure(figsize=(10, 20))
gs1 = gridspec.GridSpec(7, 2)
gs1.update(wspace=0.05, hspace=0.1)
sensitivities=['45.0', 
               'potential1_cost100',
               'potential100_cost1',
               'potential100_cost0.1']

for i,budget in enumerate(sensitivities):
    ax1 = plt.subplot(gs1[i,0])
    ax2 = plt.subplot(gs1[i,1])
    if budget=='potential1_cost100':
        balances_df = pd.read_csv('results/version-sensitivity-cc/csvs/supply_energy.csv',
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt= '3H-T-H-B-I-solar+p3-dist1-cb45.0ex0-co2 stored+c100-co2 stored+e1'
    
    elif budget=='potential100_cost1':
        balances_df = pd.read_csv('results/version-sensitivity-cc/csvs/supply_energy.csv',
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt= '3H-T-H-B-I-solar+p3-dist1-cb45.0ex0-co2 stored+c1-co2 stored+e100'
    
    elif budget=='potential100_cost0.1':
        balances_df = pd.read_csv('results/version-sensitivity-cc/csvs/supply_energy.csv',
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt= '3H-T-H-B-I-solar+p3-dist1-cb45.0ex0-co2 stored+c0.1-co2 stored+e100'

    else:
        balances_df = pd.read_csv('results/version-baseline/csvs/supply_energy.csv',
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget,decay)
        NET2=NET

    
    sel = 0.000001*balances_df.loc[idx['co2 stored', ['links','stores'], :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
    
    # Add one value per year to plot step-wise figures
    data=sel.loc[NET2]
    data.columns=[int(x) for x in data.columns.get_level_values(3)]
    for year in range(2020,2055,5):
        for j in range(0,5):
            data[year-2+j]=data[year]
    data=data.reindex(sorted(data.columns), axis=1)
    data.drop(columns=[2018,2019,2020,2051,2052])
    ax1.stackplot(data.columns, data, colors=colors)
    
     # Add one value per year to plot step-wise figures
    data=-sel.loc[CCUS]
    data.columns=[int(x) for x in data.columns.get_level_values(3)]
    for year in range(2020,2055,5):
        for j in range(0,5):
            data[year-2+j]=data[year]
    data=data.reindex(sorted(data.columns), axis=1)
    data.drop(columns=[2018,2019,2020,2051,2052])
    ax2.stackplot(data.columns, data, colors=colors2)
    
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2021, 1150, label_budget[budget], fontsize=18)
    ax2.text(2021, 1150, label_budget[budget], fontsize=18)
    
    ax1.set_xticks([2030, 2040, 2050])
    ax2.set_xticks([2030, 2040, 2050])
    if i!=(len(budgets)-1):
        ax1.set_xticklabels([])
        ax2.set_xticklabels([])
    else:
        ax1.set_xticklabels(['2030', '2040', '2050'])
        ax2.set_xticklabels(['2030', '2040', '2050'])
        
    ax1.set_yticks([0, 200, 400, 600, 800,1000, 1200])
    ax2.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
    ax2.set_yticklabels([])
    ax1.set_ylim([0, 1350])
    ax2.set_ylim([0, 1350])
    ax1.set_xlim([2020, 2050])
    ax2.set_xlim([2020, 2050])


NET=['DAC1', 'gas for industry CC3',
     'process emissions CC2', 'solid biomass for industry CC3',
     'urban central solid biomass CHP CC4',
     'SMR CC3','urban central gas CHP CC4',
     ]

NET_names2=['DAC', 'gas for industry CC',
           'process emissions CC', 'solid biomass for industry CC',
           'solid biomass CHP CC',
           'SMR CC', 'gas CHP CC',
           ]

ax1.legend(fancybox=True, fontsize=16, loc=(-0.1, -1.3), facecolor='white', 
           frameon=True, ncol=1, labels=NET_names)
ax2.legend(fancybox=True, fontsize=16, loc=(0.1, -1.0), facecolor='white', 
           frameon=True, ncol=1, labels=CCUS_names)

plt.savefig('figures/NET_sensitivity-cc_potential1_cost100.png',
            dpi=600, bbox_inches='tight')