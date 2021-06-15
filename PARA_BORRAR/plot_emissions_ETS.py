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
plt.figure(figsize=(12, 10))
gs1 = gridspec.GridSpec(4, 2)
gs1.update(wspace=0.3, hspace=0.4)

transmission='1.0'
cluster='37'
budgets = ['25', '34', '48', '70']
decays = ['ex0', 'be3' ]
 
e = {'electricity' : ['CCGT2',  'OCGT2', 'coal2', 'lignite2', 'nuclear2', 'oil2',],
     'heating' : ['residential rural gas boiler2',
                  'residential rural oil boiler2',
                  'residential urban decentral gas boiler2',
                  'residential urban decentral oil boiler2', 
                  'services rural gas boiler2',
                  'services rural oil boiler2', 
                  'services urban decentral gas boiler2',
                  'services urban decentral oil boiler2',
                  'urban central gas boiler2',
                  'urban central oil boiler2',],
     'road transport': [],
     'aviation':[],
     'industry': ['gas for industry CC2', 'gas for industry2', 
                  'process emissions CC1', 'process emissions1',
                  'solid biomass for industry CC2',
                  'SMR CC2', 'SMR2'],
    'CHP' : ['urban central gas CHP CC3',
             'urban central gas CHP3',
             'urban central solid biomass CHP CC3'],
    'other': [ 'co2 vent1',]}
colors={'electricity':'firebrick', 
        'heating':'orange', 
        'road transport': 'dodgerblue', 
        'aviation':'darkblue',
        'CHP': 'pink', 
        'industry':'dimgray', 
        'other':'black'}
sectors=['other', 'industry','road transport', 'aviation','heating', 'CHP', 'electricity',  ]

for i,budget in enumerate(budgets):  
    for j,decay in enumerate(decays):
        e_sectors=pd.DataFrame(columns=sectors)
        ax1 = plt.subplot(gs1[i,j])
        balances_df = pd.read_csv('results/version-cb{}{}/csvs/supply_energy.csv'.format(budget,decay),index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
        sel = 0.000001*balances_df.loc[idx['co2', 'links', :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
        for sector in sectors:
            e_sectors[sector]=sel.loc[e[sector]].sum().droplevel([0,1,2])
        #CHP is split 50/50 between electricity and heating
        e_sectors['electricity']=e_sectors['electricity']+0.5*e_sectors['CHP']
        e_sectors['heating']=e_sectors['heating']+0.5*e_sectors['CHP']
        e_sectors.drop('CHP',1, inplace=True)
        
        #Add kerosene for viation, land transport fossil, naphtha for industry
        CO2_int_oil=0.27 #tCO2/MWh_th
        oil = 0.000001*balances_df.loc[idx['Fischer-Tropsch', 'generators', 'oil'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]) #CO2 -> Mt CO2
        FT = 0.000001*balances_df.loc[idx['Fischer-Tropsch', 'links', 'Fischer-Tropsch1'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]) #CO2 -> Mt CO2
        
        sel2 = 0.000001*balances_df.loc[idx['Fischer-Tropsch', 'loads', :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
        
        e_sectors['road transport'] = [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['land transport fossil'].droplevel([0,1,2]), oil,FT)]
        e_sectors['aviation'] = [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['kerosene for aviation'].droplevel([0,1,2]), oil,FT)]
        e_sectors['industry'] += [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['naphtha for industry'].droplevel([0,1,2]), oil,FT)]
        #plot
        e_t=e_sectors.transpose()
        ax1.stackplot([int(x) for x in e_t.columns]
                    ,e_t, colors=[colors[s] for s in e_t.index])
        ax1.set_ylabel("Emissions [MtCO2/a]")
        ax1.set_ylim([0, 4000])
        ax1.set_xlim([2020, 2050])
        if i==0 and j==0:
            ax1.set_title('exponential decay')
        if i==0 and j==1:
            ax1.set_title('beta decay')
ax1.legend(fancybox=True, fontsize=14, loc=(-0.8, -1.2), facecolor='white', 
           frameon=True, ncol=2, labels=e_t.index)       
plt.savefig('figures/emissions_per_sector_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')
