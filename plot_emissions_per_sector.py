# -*- coding: utf-8 -*-
"""
@author: Marta
"""
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
budgets = ['25', '34', '48', '70', '48-noH2network','48-wo_eff']
budget_name = {'25':'1.5$^{\circ}$C', 
               '34':'1.6$^{\circ}$C',  
               '48':'1.7$^{\circ}$C',  
               '70':'2.0$^{\circ}$C',  
               '48-noH2network': '1.7$^{\circ}$C (no H$_2$ network)' ,
               '48-wo_eff':'1.7$^{\circ}$C (no efficiency)'}

e = {'electricity' : ['CCGT2',  'OCGT2', 'coal2', 'lignite2', 'nuclear2', 'oil2',],
     'heating_individual' : ['residential rural gas boiler2',
                             'residential rural oil boiler2',
                             'residential urban decentral gas boiler2',
                             'residential urban decentral oil boiler2', 
                             'services rural gas boiler2',
                             'services rural oil boiler2', 
                             'services urban decentral gas boiler2',
                             'services urban decentral oil boiler2'],
     'heating_central' : ['urban central gas boiler2',
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
        'other':'black',
        'ETS':'sienna',
        'no_ETS':'teal'}

sectors=['other', 
         'industry',
         'road transport', 
         'aviation',
         'heating_individual',
         'heating_central', 
         'CHP', 
         'electricity',]

e_ETS=pd.DataFrame(columns=pd.MultiIndex.from_product([pd.Series(data=budgets, name='budget',),
                                                       pd.Series(data=['ex0'], name='decay',),
                                                       pd.Series(data=['ETS', 'no_ETS'])]))

for i,budget in enumerate(budgets):
    e_sectors=pd.DataFrame(columns=sectors)
    ax1 = plt.subplot(gs1[i,0])
    balances_df = pd.read_csv('results/version-cb{}{}/csvs/supply_energy.csv'.format(budget,decay),index_col=list(range(3)),
                              header=list(range(4)))
    if budget =='48-noH2network':
        opt ='3H-T-H-B-I-solar3-dist1-noH2network-cb48ex0'
    elif budget== '48-wo_eff':
        opt ='3H-T-H-B-I-solar3-dist1-cb48ex0'
    else:
        opt='3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
    sel = 0.000001*balances_df.loc[idx['co2', 'links', :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
    for sector in sectors:
        e_sectors[sector]=sel.loc[e[sector]].sum().droplevel([0,1,2])
    e_ETS[idx[budget,decay,'ETS']] = (e_sectors['electricity'] 
                                     + e_sectors['heating_central'] 
                                     + e_sectors['CHP']) #industry is added below
    e_ETS[idx[budget,decay,'no_ETS']] = e_sectors['heating_individual'] 
    #CHP is split 50/50 between electricity and heating
    e_sectors['electricity']=e_sectors['electricity']+0.5*e_sectors['CHP']
    e_sectors['heating_central']=e_sectors['heating_central']+0.5*e_sectors['CHP']
    e_sectors['heating']=e_sectors['heating_central']+e_sectors['heating_individual']
    e_sectors.drop(['CHP', 'heating_central', 'heating_individual'],1, inplace=True)
    #Add kerosene for viation, land transport fossil, naphtha for industry
    CO2_int_oil=0.27 #tCO2/MWh_th
    oil = 0.000001*balances_df.loc[idx['Fischer-Tropsch', 'generators', 'oil'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]) #CO2 -> Mt CO2
    FT = 0.000001*balances_df.loc[idx['Fischer-Tropsch', 'links', 'Fischer-Tropsch1'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]) #CO2 -> Mt CO2

    sel2 = 0.000001*balances_df.loc[idx['Fischer-Tropsch', 'loads', :],idx[cluster, transmission, opt,:]].droplevel([0,1]) #CO2 -> Mt CO2
    e_sectors['road transport'] = [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['land transport fossil'].droplevel([0,1,2]), oil,FT)]
    e_sectors['aviation'] = [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['kerosene for aviation'].droplevel([0,1,2]), oil,FT)]
    e_sectors['industry'] += [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['naphtha for industry'].droplevel([0,1,2]), oil,FT)]
    e_ETS[idx[budget,decay, 'ETS']] += e_sectors['aviation'] + e_sectors['industry']
    e_ETS[idx[budget,decay, 'no_ETS']] += e_sectors['road transport'] 
    #plot
    e_t=e_sectors.transpose()
    ax1.stackplot([int(x) for x in e_t.columns]
                ,e_t, colors=[colors[s] for s in e_t.index])
    ax1.set_ylim([0, 4000])
    ax1.set_xlim([2020, 2050])
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2045, 3500, budget_name[budget], fontsize=18)
    
    if i!=5:
        ax1.set_xticks([])
ax1.legend(fancybox=True, fontsize=18, loc=(0.4, 5.5), facecolor='white', 
           frameon=True, ncol=2, labels=e_t.index)       
plt.savefig('figures/emissions_per_sector_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')
#%%
plt.figure(figsize=(10, 20))
gs1 = gridspec.GridSpec(7, 1)
gs1.update(wspace=0.05, hspace=0.05)

for i,budget in enumerate(budgets):  
    ax1 = plt.subplot(gs1[i,0])
    e_t=e_ETS[idx[budget,decay]].transpose()
    ax1.stackplot([int(x) for x in e_t.columns],
                   e_t, colors=[colors[s] for s in e_t.index])
    ax1.set_ylim([0, 4000])
    ax1.set_xlim([2020, 2050])
    ax1.set_yticks([1000, 2000, 3000, 4000])
    ax1.set_ylabel("MtCO$_2$/a")
    ax1.text(2045, 3500, budget_name[budget], fontsize=18)
    if i!=5:
        ax1.set_xticks([])
ax1.legend(fancybox=True, fontsize=14, loc=(0.6, 5.7), facecolor='white', 
           frameon=True, ncol=2, labels=e_t.index)       
plt.savefig('figures/emissions_ETS_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')