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
cluster='37m'
decay='ex0'

budgets = ['27',
           '36.7',
           '51.4',
           '63',
           '75.2']

label_budget = {'27':'1.5$^{\circ}$C',
                '36.7':'1.6$^{\circ}$C', 
                '51.4':'1.75$^{\circ}$C', 
                '63':'1.87$^{\circ}$C', 
                '75.2':'2.0$^{\circ}$C', 
                '36.7-noH2network':'1.7$^{\circ}$C (wo H$_2$ network)',
                '36.7-wo_eff':'1.7$^{\circ}$C (no eff)',}

e = {'electricity' : ['CCGT2', 
                      'OCGT2',
                      'coal2',
                      'lignite2',
                      'nuclear2',
                      'oil2',],
     'heating':[],
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
     'shipping':[],
     'industry': ['gas for industry CC2',
                  'gas for industry2',
                  'process emissions CC1',
                  'process emissions1',
                  'solid biomass for industry CC2',
                  'SMR CC2',
                  'SMR2'],
    'CHP' : ['urban central gas CHP CC3',
             'urban central gas CHP3',
             'urban central solid biomass CHP CC3'],
    #'other': [ 'co2 vent1',]
    }

colors={'electricity':'firebrick', 
        'heating':'orange', 
        'road transport': 'dodgerblue', 
        'shipping':'purple',
        'aviation':'darkblue',
        'CHP': 'pink', 
        'industry':'dimgray', 
        'other':'black',
        'ETS':'sienna',
        'no_ETS':'teal'}

sectors=[
        #'other',  we ignore this for plotting
         'industry',
         'road transport', 
         'shipping',
         'aviation',
         'heating',
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
    balances_df = pd.read_csv('results/version-baseline/csvs/supply_energy.csv', #.format(budget,decay),
                              index_col=list(range(3)),
                              header=list(range(4)))
    if budget =='48-noH2network':
        opt ='3H-T-H-B-I-solar+p3-dist1-noH2network-cb48ex0'
    elif budget== '48-wo_eff':
        opt ='3H-T-H-B-I-solar+p3-dist1-cb48ex0'
    else:
        opt='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget,decay)
    sel =balances_df.loc[idx['co2', 'links', :],idx[cluster, transmission, opt,:]].droplevel([0,1]) 
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
    
    #Add kerosene for aviation and naphtha for industry
    #'oil emissions' includes naptha for industry and aviation
    CO2_int_oil=0.27 #tCO2/MWh_th
    oil = balances_df.loc[idx['oil', 'generators', 'oil'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]) 
    FT = balances_df.loc[idx['oil', 'links', 'Fischer-Tropsch1'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]) 
    sel2 = balances_df.loc[idx['oil', 'loads', :],idx[cluster, transmission, opt,:]].droplevel([0,1]) 
    
    #emissions in aviation = CO2_int_oil * oil consumption in aviation * share of oil with fossil origin
    e_sectors['aviation'] = [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['kerosene for aviation'].droplevel([0,1,2]), oil,FT)]
    e_sectors['industry'] += [CO2_int_oil*x*y/(y+z) for x,y,z in zip(-sel2.loc['naphtha for industry'].droplevel([0,1,2]), oil,FT)]
    
    e_ETS[idx[budget, decay, 'ETS']] += e_sectors['aviation'] + e_sectors['industry']
    
    # Add emissions for land transport and shipping using oil
    
    e_sectors['road transport'] = balances_df.loc[idx['co2', 'loads', 'land transport oil emissions'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]).fillna(0)
    e_sectors['shipping'] = balances_df.loc[idx['co2', 'loads', 'shipping oil emissions'],idx[cluster, transmission, opt,:]].droplevel([0,1,2]).fillna(0)
    
    e_ETS[idx[budget,decay, 'no_ETS']] += e_sectors['road transport'] + e_sectors['shipping']
    


    #plot
    e_t=e_sectors.transpose()
    ax1.stackplot([int(x) for x in e_t.columns],
                e_t*0.000000001,  #tCO2 -> Gt CO2
                colors=[colors[s] for s in e_t.index])
    ax1.set_ylim([0, 4])
    ax1.set_xlim([2020, 2050])
    ax1.set_yticks([1, 2, 3])
    ax1.set_ylabel("GtCO$_2$/a")
    ax1.text(2046, 3, label_budget[budget], fontsize=18)
    
    if i!=4:
        ax1.set_xticks([])
ax1.legend(fancybox=True, fontsize=18, loc=(0.4, 5.3), facecolor='white', 
           frameon=True, ncol=2, labels=e_t.index)
plt.savefig('figures/emissions_per_sector_transmission{}.png'.format(transmission),
            dpi=150, bbox_inches='tight')

#%%
plt.figure(figsize=(10, 20))
gs1 = gridspec.GridSpec(7, 1)
gs1.update(wspace=0.05, hspace=0.05)

for i,budget in enumerate(budgets):  
    ax1 = plt.subplot(gs1[i,0])
    e_t=e_ETS[idx[budget,decay]].transpose()
    ax1.stackplot([int(x) for x in e_t.columns],
                   e_t*0.000000001,  #tCO2 -> Gt CO2 
                   colors=[colors[s] for s in e_t.index])
    ax1.set_ylim([0, 4])
    ax1.set_xlim([2020, 2050])
    ax1.set_yticks([1, 2, 3])
    ax1.set_ylabel("GtCO$_2$/a")
    ax1.text(2046, 3, label_budget[budget], fontsize=18)
    if i!=4:
        ax1.set_xticks([])
ax1.legend(fancybox=True, fontsize=14, loc=(0.6, 5.3), facecolor='white', 
           frameon=True, ncol=2, labels=e_t.index)       
plt.savefig('figures/emissions_ETS_transmission{}.png'.format(transmission),
            dpi=150, bbox_inches='tight')