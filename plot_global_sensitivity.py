# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
idx = pd.IndexSlice
import numpy as np

metrics = [
           'NPV1.5',
           'NPV1.6',
           'NPV2.0',
           'ratio-nonbiomass-RES',
           'ratio-solar',
           'ratio-wind',
           'ratio-nuclear',
           'H2_electrolytic',
           'H2_SMR_CC',
           'synthetic_oil',
           'synthetic_methane',
           'biomethane',
           'CO2_sequestered',
           ]

sensitivities=['baseline', 
               'sensitivity-fixedcosts',
               #'sensitivity-noH2network',
               #'sensitivity-endo_efficiency',
               #'sensitivity-nobiomassCC',
               'solar+c0.8',
               'solar+c1.2',
               'onwind+c0.8',
               'onwind+c1.2',
               'nuclear+c0.8',
               'nuclear+c1.2',
               'battery+c0.8',
               'battery+c1.2',
               'DAC+c0.8',
               'DAC+c1.2',
               'Sabatier+c0.8',
               'Sabatier+c1.2',
               'H2 Electrolysis+c0.8',
               'H2 Electrolysis+c1.2',
               'SMR CC+c0.8',
               'SMR CC+c1.2',
               'SMR CC+c0.8-H2 Electrolysis+c1.2']

version={'baseline':'baseline',
         'sensitivity-fixedcosts':'sensitivity-fixedcosts',
         'sensitivity-noH2network':'sensitivity-noH2network',
         'sensitivity-endo_efficiency':'sensitivity-endo_efficiency',
         'sensitivity-nobiomassCC':'sensitivity-nobiomassCC',
         'solar+c0.8':'sensitivity-costs',
         'solar+c1.2':'sensitivity-costs',
         'onwind+c0.8':'sensitivity-costs',
         'onwind+c1.2':'sensitivity-costs',
         'nuclear+c0.8':'sensitivity-costs',
         'nuclear+c1.2':'sensitivity-costs',
         'battery+c0.8':'sensitivity-costs2',
         'battery+c1.2':'sensitivity-costs2',
         'DAC+c0.8':'sensitivity-costs2',
         'DAC+c1.2':'sensitivity-costs2',
         'Sabatier+c0.8':'sensitivity-costs',
         'Sabatier+c1.2':'sensitivity-costs',
         'H2 Electrolysis+c0.8':'sensitivity-costs',
         'H2 Electrolysis+c1.2':'sensitivity-costs',
         'SMR CC+c0.8':'sensitivity-costs',
         'SMR CC+c1.2':'sensitivity-costs',
         'SMR CC+c0.8-H2 Electrolysis+c1.2':'sensitivity-costs',}


opts_prefix={'baseline':'3H-T-H-B-I-solar+p3-dist1',
              'sensitivity-fixedcosts': '3H-T-H-B-I-solar+p3-dist1',
              #'sensitivity-noH2network':'3H-T-H-B-I-solar+p3-dist1',
              #'sensitivity-endo_efficiency':'3H-T-H-B-I-solar+p3-dist1',
              #'sensitivity-nobiomassCC':'3H-T-H-B-I-solar+p3-dist1',
              'solar+c0.8':'3H-T-H-B-I-solar+p3-dist1-solar+c0.8',
              'solar+c1.2':'3H-T-H-B-I-solar+p3-dist1-solar+c1.2',
              'onwind+c0.8':'3H-T-H-B-I-solar+p3-dist1-onwind+c0.8',
              'onwind+c1.2':'3H-T-H-B-I-solar+p3-dist1-onwind+c1.2',
              'nuclear+c0.8':'3H-T-H-B-I-solar+p3-dist1-nuclear+c0.8',
              'nuclear+c1.2':'3H-T-H-B-I-solar+p3-dist1-nuclear+c1.2',
              'battery+c0.8':'3H-T-H-B-I-solar+p3-dist1-battery+c0.8',
              'battery+c1.2':'3H-T-H-B-I-solar+p3-dist1-battery+c1.2',
              'DAC+c0.8':'3H-T-H-B-I-solar+p3-dist1-DAC+c0.8',
              'DAC+c1.2':'3H-T-H-B-I-solar+p3-dist1-DAC+c1.2',
              'Sabatier+c0.8':'3H-T-H-B-I-solar+p3-dist1-Sabatier+c0.8',
              'Sabatier+c1.2':'3H-T-H-B-I-solar+p3-dist1-Sabatier+c1.2',
              'H2 Electrolysis+c0.8':'3H-T-H-B-I-solar+p3-dist1-H2 Electrolysis+c0.8',
              'H2 Electrolysis+c1.2':'3H-T-H-B-I-solar+p3-dist1-H2 Electrolysis+c1.2',
              'SMR CC+c0.8':'3H-T-H-B-I-solar+p3-dist1-SMR CC+c0.8',
              'SMR CC+c1.2':'3H-T-H-B-I-solar+p3-dist1-SMR CC+c1.2',
              'SMR CC+c0.8-H2 Electrolysis+c1.2':'3H-T-H-B-I-solar+p3-dist1-SMR CC+c0.8-H2 Electrolysis+c1.2',}

data=pd.DataFrame(index=sensitivities, columns=metrics)

transmission='1.0'
cluster='37m'
decay = 'ex0'

for sensitivity in sensitivities:
    
    """
    NPV System cost
    """
    #calculate social cost of carbon (relative to the lowest carbon budget)
    cb = [
          25.7, 
          35.4, 
          #45.0, 
          #54.7, 
          #64.3, 
          73.9
          ]
    label_cb={'25.7' : 'NPV1.5', 
              '35.4' : 'NPV1.6', 
              '45.0' : 'NPV1.7', 
              '54.7' : 'NPV1.8', 
              '64.3' :'NPV1.9', 
              '73.9' :'NPV2.0'}
    budgets = [str(x) for x in cb]
    social_cost_carbon=120 #€/tonne CO2
    discount_rate=0.02
    from prepare_sector_network import co2_emissions_year
    opts='H-T-I'
    countries=pd.read_csv('results/countries.csv',  index_col=1) 
    cts=countries.index.to_list()
    e_1990 = co2_emissions_year(cts, opts, year=1990)
    path_cb =  'results/version-{}/csvs/'.format(version[sensitivity])
    for budget in budgets:
        CO2_CAP=pd.read_csv(path_cb 
                            + 'carbon_budget_distributioncb{}{}.csv'.format(budget, decay),
                            index_col=0)
            
        CO2_CAP_ref=pd.read_csv(path_cb 
                                + 'carbon_budget_distributioncb25.7ex0.csv',
                                index_col=0) 
        timestep=CO2_CAP.index[1]-CO2_CAP.index[0]
        carbon_cost=sum([(CO2_CAP.loc[year, 'cb'+budget+decay]-CO2_CAP_ref.loc[year, 'cb25.7ex0'])*e_1990*timestep*social_cost_carbon/(1+discount_rate)**(year-CO2_CAP.index[0]) for year in CO2_CAP.index])/1000 #Gt to tonnes compensates € to B€ 
        
        cumulative_cost_df = pd.read_csv('results/version-{}/csvs/cumulative_cost.csv'.format(version[sensitivity]))
        cumulative_cost_df = cumulative_cost_df.set_index(['cluster', 'lv', 'opt', 'planning_horizon']).sort_index()
        opt =opts_prefix[sensitivity]+'-cb{}{}-{}'.format(budget,decay,sensitivity) if sensitivity=='noH2network' else opts_prefix[sensitivity]+'-cb{}{}'.format(budget,decay)
        cumulative_system_cost = cumulative_cost_df.loc[idx[cluster,float(transmission),opt, 'cumulative cost'],str(discount_rate)]/1000000000000 #€ to 10⁶M€ 
        cumulative_system_cost +=carbon_cost
        data.loc[sensitivity,label_cb[budget]]=cumulative_system_cost
        
    data['1.5/2.0'] = data['NPV1.5']/data['NPV2.0']
    data['1.6/2.0'] = data['NPV1.6']/data['NPV2.0']


    balances_df = pd.read_csv('results/version-{}/csvs/supply_energy.csv'.format(version[sensitivity]),
                              index_col=list(range(3)),
                              header=list(range(4)))
    budget='45.0'
    year='2050'
    opt=opts_prefix[sensitivity]+'-cb{}{}'.format(budget,decay)

    data.loc[sensitivity,'H2_electrolytic'] = balances_df.loc[idx['H2','links', 'H2 Electrolysis1'],
                                              idx[cluster, transmission, opt,year]] *0.000001 # MWh -> TWh
             
    data.loc[sensitivity,'H2_SMR_CC'] = balances_df.loc[idx['H2','links', 'SMR CC1'],
                                        idx[cluster, transmission, opt,year]] *0.000001 # MWh -> TWh
    
    data.loc[sensitivity,'synthetic_methane'] = balances_df.loc[idx['gas','links', 'Sabatier1'],
                                        idx[cluster, transmission, opt,year]] *0.000001 # MWh -> TWh

    data.loc[sensitivity,'biomethane'] = balances_df.loc[idx['gas','links', 'biogas to gas1'],
                                 idx[cluster, transmission, opt,year]] *0.000001 # MWh -> TWh

    data.loc[sensitivity,'synthetic_oil'] = balances_df.loc[idx['oil','links', 'Fischer-Tropsch1'],
                                        idx[cluster, transmission, opt,year]] *0.000001 # MWh -> TWh

    data.loc[sensitivity,'CO2_sequestered'] = - balances_df.loc[idx['co2 stored','stores', 'co2 stored'],
                                            idx[cluster, transmission, opt,year]] *0.000001 # t -> Mt
    """
    Percentaje of final demand electrified
    """
    loads = balances_df.loc[idx[:,'loads',:], idx[cluster, transmission, opt,:]]
    loads.drop(['co2','process emissions'], axis=0, level=0, inplace=True)
    loads = -loads.sum().droplevel([0,1,2])

    electricity =  balances_df.loc[idx[['AC','low voltage'],'generators' , :],
                                   idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
    electricity += balances_df.loc[idx[['AC'],'storage_units' , 'hydro'],
                                      idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
    data.loc[sensitivity,'ratio-nonbiomass-RES']=electricity[year]/loads[year]
    
    electricity_solar= balances_df.loc[idx[['AC','low voltage'],'generators' , ['solar', 'solar rooftop']],
                                   idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
    data.loc[sensitivity,'ratio-solar']=electricity_solar[year]/loads[year]
    
    electricity_wind= balances_df.loc[idx[['AC','low voltage'],'generators' , ['offwind-ac', 'offwind-dc', 'onwind']],
                                   idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
    data.loc[sensitivity,'ratio-wind']=electricity_wind[year]/loads[year]
    
    electricity_nuclear = balances_df.loc[idx['AC', 'links', ['nuclear1', ]],
                                          idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
     
    data.loc[sensitivity,'ratio-nuclear']=electricity_nuclear[year]/loads[year]
     
#%%
plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18
plt.figure(figsize=(30, 30))
gs1 = gridspec.GridSpec(15, 2)
gs1.update(wspace=0.1, hspace=0.2)

colors={'baseline':'black',
         'sensitivity-fixedcosts':'orange',
         #'sensitivity-noH2network':'sensitivity-noH2network',
         #'sensitivity-endo_efficiency':'sensitivity-endo_efficiency',
         #'sensitivity-nobiomassCC':'sensitivity-nobiomassCC',
         'solar+c0.8':'gold',
         'solar+c1.2':'gold',
         'onwind+c0.8':'dodgerblue',
         'onwind+c1.2':'dodgerblue',
         'nuclear+c0.8':'firebrick',
         'nuclear+c1.2':'firebrick',
         'battery+c0.8':'yellowgreen',
         'battery+c1.2':'yellowgreen',
         'DAC+c0.8':'darkblue',
         'DAC+c1.2':'darkblue',
         'Sabatier+c0.8':'peru',
         'Sabatier+c1.2':'peru',
         'H2 Electrolysis+c0.8':'pink',
         'H2 Electrolysis+c1.2':'pink',
         'SMR CC+c0.8':'gray',
         'SMR CC+c1.2':'gray',
         'SMR CC+c0.8-H2 Electrolysis+c1.2':'pink',}

label_sensitivity ={'baseline':'Baseline',
                    'sensitivity-fixedcosts':'fixed costs',
                    'sensitivity-noH2network':'',
                    'sensitivity-endo_efficiency':'',
                    'sensitivity-nobiomassCC':'',
                    'solar+c0.8':'solar-20%',
                    'solar+c1.2':'solar+20%',
                    'onwind+c0.8':'onwind-20%',
                    'onwind+c1.2':'onwind+20%',
                    'nuclear+c0.8':'nuclear-20%',
                    'nuclear+c1.2':'nuclear+20%',
                    'battery+c0.8':'battery+20%',
                    'battery+c1.2':'battery-20%',
                    'DAC+c0.8':'DAC+20%',
                    'DAC+c1.2':'DAC-20%',
                    'Sabatier+c0.8':'methanation-20%',
                    'Sabatier+c1.2':'methanation+20%',
                    'H2 Electrolysis+c0.8':'Electrolytic H2-20%',
                    'H2 Electrolysis+c1.2':'Electrolytic H2+20%',
                    'SMR CC+c0.8':'SMR CC H2-20%',
                    'SMR CC+c1.2':'SMR CC H2+20%',
                    'SMR CC+c0.8-H2 Electrolysis+c1.2': 'Electrolytic H2+20% \n SMR CC H2-20%'}

label_metric ={'NPV1.5': 'NPV 1.5$^{\circ}$C \n (10$^6$M€)',
               'NPV1.6': 'NPV 1.6$^{\circ}$C \n (10$^6$M€)',
               'NPV2.0': 'NPV  2.0$^{\circ}$C \n (10$^6$M€)',
               '1.5/2.0': 'NPV 1.5$^{\circ}$C, \n rel. to 2.0$^{\circ}$C',
               '1.6/2.0': 'NPV 1.6$^{\circ}$C, \n rel. to 2.0$^{\circ}$C',
               'ratio-nonbiomass-RES':'ratio \n nonbiomass \n RES',
               'ratio-solar':'ratio-solar',
               'ratio-wind':'ratio-wind',
               'ratio-nuclear':'ratio-nuclear',
               'H2_electrolytic': 'electrolitic H$_2$ \n 2050 1.7$^{\circ}$C \n (TWh/a)',
               'H2_SMR_CC': 'SMR-CC H$_2$ \n (TWh/a)',
               'synthetic_oil':'synthetic \n oil \n (TWh/a)',
               'synthetic_methane': 'synthetic \n methane \n (TWh/a)',
               'biomethane':'bio-methane \n (TWh/a)',
               'CO2_sequestered' :'CO$_2$ seq. \n (MtCO$_2$/a)'
              }

dic_ylim ={'NPV1.5': [15,22],
           'NPV1.6': [15,22],
           'NPV2.0': [15,22],
           '1.5/2.0': [1, 1.15],
           '1.6/2.0': [0.9, 1.1],
           'ratio-nonbiomass-RES':[0.6,0.8],
            'ratio-solar':[0.1,0.4],
            'ratio-wind':[0.3,0.6],
            'ratio-nuclear':[0.06,0.13],
            'H2_electrolytic': [2000,3000],
            'H2_SMR_CC': [0,0.0002],
            'synthetic_oil':[1000,1500],
            'synthetic_methane': [0, 5],
            'biomethane':[200,400],
             'CO2_sequestered' :[100,300],
              }

for i,metric in enumerate(data.columns):
    ax1 = plt.subplot(gs1[i,0])
    index=np.arange(len(sensitivities))
    
    ax1.bar(index+0.3,data[metric],
            width=0.4,
            color=[colors[s] for s in sensitivities])
    ax1.set_xticks(index+0.3)
    
    if i != len(data.columns)-1:
        ax1.set_xticklabels([])
    else:
        ax1.set_xticklabels([label_sensitivity[s] for s in sensitivities], rotation=90, fontsize=18)
    ax1.set_ylabel(label_metric[metric])
    ax1.axhline(y=data.loc['baseline', metric], 
               color='black',
               linestyle='--')
    ax1.set_ylim(dic_ylim[metric])
plt.savefig('figures/global_sensitivity.png',
            dpi=600, bbox_inches='tight')

