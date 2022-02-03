# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime
import seaborn as sns; sns.set()
idx = pd.IndexSlice

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18

plt.figure(figsize=(20, 25))
gs1 = gridspec.GridSpec(5, 4)
gs1.update(wspace=0.5, hspace=0.1)


budgets = ['25.7','35.4','45.0','54.7', '64.3', '73.9']

color={'25.7':'yellowgreen',
     '35.4':'dodgerblue',
     '45.0':'gold',
     '54.7':'orange',
     '64.3':'darkred',
     '73.9':'magenta'}
    
label={'25.7':'1.5$^{\circ}$C', 
        '35.4':'1.6$^{\circ}$C',
        '45.0':'1.7$^{\circ}$C',
        '54.7':'1.8$^{\circ}$C',
        '64.3':'1.9$^{\circ}$C',
        '73.9':'2.0$^{\circ}$C'}


decay = 'ex0'
transmission='1.0'
cluster='37m'

techs=['solar', 'onwind', 'offwind-ac', 'offwind-dc', 'solar rooftop', 'nuclear', 'coal', 'OCGT', 'CCGT',
       'H2 Electrolysis', 'H2 Fuel Cell', 'urban central air heat pump', 'urban central resistive heater', 
       'Sabatier', 'DAC', 'Fischer-Tropsch',
       'battery', 'home battery', 'H2',  'urban central water tanks', ]

tech_stores=['battery', 'home battery', 'H2',  'urban central water tanks']

tech_links=['nuclear', 'coal', 'OCGT', 'CCGT', 'H2 Electrolysis', 'H2 Fuel Cell', 
            'urban central air heat pump', 'urban central resistive heater',
            'Sabatier', 'DAC', 'Fischer-Tropsch',]

tech_eff=['nuclear', 'coal', 'OCGT', 'CCGT',]

efficiency={'nuclear':0.33,
            'coal':0.33,
            'OCGT': 0.41,
            'CCGT': 0.58}

for i, tech in enumerate(techs):
    ax1 = plt.subplot(gs1[int(i/4),i-4*int(i/4)])

    for budget in budgets:
        capacities_df = pd.read_csv('results/version-baseline/csvs/capacities.csv',#.format(budget,decay),
                            index_col=list(range(2)), header=list(range(4))) /1000 #MW -> GW
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget, decay)
        component='generators'
        unit ='GW'
        if tech in tech_stores:
            component = 'stores'
            unit='GWh'
        if tech in tech_links:
            component='links'
        eff = efficiency[tech] if tech in tech_eff else 1
        capacities =  eff*capacities_df.loc[idx[component, tech],idx[cluster, transmission, opt,:]].droplevel([0,1,2])
        capacities.index=[int(x) for x in capacities.index]
        
        for year in range(2020,2055,5):
            for j in range(0,5):
                capacities[year-2+j]=capacities[year]
        capacities = capacities.reindex(sorted(capacities.index), axis=1)
        capacities = capacities.drop(index=[2018,2019,2020,2051,2052])
        
        plt.plot(
                #pd.to_datetime(capacities.index, format='%Y'), 
                capacities.index,
                capacities.values, 
                 color=color[budget], linewidth=3, label=label[budget])

    ax1.set_ylabel(tech + ' (' + unit + ')', fontsize=18)
    ax1.grid(linestyle='--')
    ax1.set_xticks([2020, 2030, 2040, 2050])
    ax1.grid(linestyle='--')
    ax1.set_xlim([2020,2050])
    if int(i/4)==4:
        ax1.set_xticklabels([2020, 2030, 2040, 2050], rotation=45)
        ax1.grid(linestyle='--')
    else:
        ax1.set_xticklabels([])
        ax1.grid(linestyle='--')
    
    if i==0:
        ax1.legend(fancybox=False, fontsize=18, loc=(0.5,1.05), 
                   facecolor='white', ncol=7, frameon=True)
    
plt.savefig('figures/capacities.png', dpi=300, bbox_inches='tight')



