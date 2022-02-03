# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
idx = pd.IndexSlice

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18
plt.figure(figsize=(20, 11))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)
ax1 = plt.subplot(gs1[0,0])

budgets = ['25.7',
           '35.4',
           '45.0',
           '54.7', 
           '64.3', 
           '73.9',
#           '45.0-noH2network',
#           '45.0-endo_efficiency',
#           '45.0-nobiomassCC'
           ]

color={'25.7':'yellowgreen',
     '35.4':'dodgerblue',
     '45.0':'gold',
     '54.7':'orange',
     '64.3':'darkred',
     '73.9':'magenta',
     '45.0-noH2network':'black',
     '45.0-endo_efficiency':'black',
     '45.0-nobiomassCC':'black'}

label_budget={'25.7':'1.5$^{\circ}$C', 
             '35.4':'1.6$^{\circ}$C',
             '45.0':'1.7$^{\circ}$C',
             '54.7':'1.8$^{\circ}$C',
             '64.3':'1.9$^{\circ}$C',
             '73.9':'2.0$^{\circ}$C',
             '45.0-noH2network':'1.7$^{\circ}$C (no H$_2$ network)',
             '45.0-endo_efficiency':'1.7$^{\circ}$C (endog. build. retro.)',
             '45.0-nobiomassCC':'1.7$^{\circ}$C (no biomass CC)'}

marker_cb = {'25.7':'o', 
            '35.4':'^', 
            '45.0':'v', 
            '54.7':'s',
            '64.3':'D',
            '73.9':'p',
            '45.0-noH2network':'+',
            '45.0-endo_efficiency':'x',
            '45.0-nobiomassCC':'1'}


x_pos = {'25.7':-0.2, 
         '35.4':-0.1, 
         '45.0':0, 
         '54.7':0.1,
         '64.3':0.15,
         '73.9':0.25,
         '45.0-noH2network':0,
         '45.0-endo_efficiency':0,
         '45.0-nobiomassCC':0}


transmission='1.0'
cluster='37m'
decay='ex0'

metrics = ['carbon neutral',
           'e_E',
           'electrification',
           'electrified heat',
           'gas origin',
           'H2',
           'Fischer-Tropsch',
           'DAC',
           'co2_stored', 
           'oil',]

decreasing_metrics = ['e_E', 'oil']

th = {'carbon neutral':0.05, # 5% total emissions, relative to 1990
      'e_E':62.5e+6, # 62.5MtCO2 = ~ 5% electricity emissions, relative to 1990 (1.25GtCO2/a)
      'electrification': 0.55, # renewable electricity share in final energy consumption
      'electrified heat': 0.7, # 'gas boilers' :100e+6,  # 100 TWh/year
      'gas origin' : 0.3, #30% gas from biogas or synthetic
      'H2' : 500e+6,  # 100 TWh/year
      'Fischer-Tropsch':100e+6,  # 100 TWh/year
      'DAC': 10e+6, # ~ 10 MtCO2/year
      'co2_stored' : 2e+8*0.99, # ~200MtCO2
      'oil': 1000e+6} # 1000 TWh/year



label={'carbon neutral': 'Total CO$_2$ emissions < ' + str(int(100*th['carbon neutral'])) +'% of 1990 level ',
       'e_E':'Electricity CO$_2$ emissions < 5% of 1990 level ',
       'electrification': 'Non-biomass renewable electricity supply > ' + str(int(100*th['electrification'])) +'% final demand ',
       'electrified heat': 'heat pumps/resistors supply >' + str(int(100*th['electrified heat'])) +'% heat demand ',
       'gas origin': 'biogas or synthetic gas > ' + str(int(100*th['gas origin'])) +'% gas demand ',
       'H2':'Electrolytic H$_2$ > ' + str(int(th['H2']/1000000)) +' TWh/a ',
       'Fischer-Tropsch':'Fischer-Tropsch > ' + str(int(th['Fischer-Tropsch']/1000000)) +' TWh/a ',
       'DAC':'DAC >  ' + str(int(th['DAC']/1000000)) +' MtCO$_2$/a ', 
       'co2_stored': 'CO$_2$ sequestration = 200 MtCO$_2$/a ',
       'oil': 'Fossil oil consumption < ' + str(int(th['oil']/1000000)) +' TWh/a '}


pos= {'H2' : ('H2', 'links', 'H2 Electrolysis1'),
      'Fischer-Tropsch':('oil', 'links', 'Fischer-Tropsch1'),
      'DAC':('co2', 'links', 'DAC0'),
      'co2_stored':('co2 stored', 'stores', 'co2 stored'),
      'oil': ('oil', 'generators', 'oil')}
version='sensitivity-costs2' #'sensitivity-costs' #'baseline' #'sensitivity-fixedcosts'
sensitivity_cost_option= '-battery+c0.8' #'-SMR CC+c0.8'

for budget in budgets:
    if budget=='45.0-noH2network':
        sensitivity=budget.split('-')[1]
        balances_df = pd.read_csv('results/version-sensitivity-{}/csvs/supply_energy.csv'.format(sensitivity),
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}-{}'.format(budget.split('-')[0],decay, sensitivity)
    elif budget=='45.0-endo_efficiency':
        sensitivity=budget.split('-')[1]
        balances_df = pd.read_csv('results/version-sensitivity-{}/csvs/supply_energy.csv'.format(sensitivity),
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget.split('-')[0],decay)

    elif budget=='45.0-nobiomassCC':
        sensitivity=budget.split('-')[1]
        balances_df = pd.read_csv('results/version-sensitivity-{}/csvs/supply_energy.csv'.format(sensitivity),
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget.split('-')[0],decay)
    else:
        balances_df = pd.read_csv('results/version-{}/csvs/supply_energy.csv'.format(version),
                                  index_col=list(range(3)),
                                  header=list(range(4)))
        opt ='3H-T-H-B-I-solar+p3-dist1{}-cb{}{}'.format(sensitivity_cost_option,budget,decay)
        
    for i,metric in enumerate(metrics):
        if metric=='carbon neutral':
            path_cb =  'results/version-{}/csvs/'.format(version)
            CO2_CAP=pd.read_csv(path_cb + 'carbon_budget_distributioncb' + budget.split('-')[0] + decay+'.csv', 
                                index_col=0)['cb'+ budget.split('-')[0] + decay]
            try:
                sel_year=min(CO2_CAP[CO2_CAP<th[metric]].index)
            except:
                sel_year=0
                print('In budget ' + budget +', '+metric + ' does not happen < 2050')
                
        elif metric=='electrification':
            loads = balances_df.loc[idx[:,'loads',:], idx[cluster, transmission, opt,:]]
            loads.drop(['co2','process emissions'], axis=0, level=0, inplace=True)
            loads = -loads.sum().droplevel([0,1,2])

            electricity =  balances_df.loc[idx[['AC','low voltage'],'generators' , :],
                                      idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            electricity += balances_df.loc[idx[['AC'],'storage_units' , 'hydro'],
                                      idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            # only non-biomass renewable electricity is included
            #electricity += balances_df.loc[idx['AC', 'links', ['nuclear1', 'CCGT1','OCGT1', 'coal1', 'lignite1', 'oil1']],
            #                          idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            ratio_elec=electricity/loads
            try:
                sel_year=float(min(ratio_elec[ratio_elec>th[metric]].index))
            except:
                sel_year=0
                print('In budget ' + budget +', '+metric + ' does not happen < 2050')
        
        elif metric=='electrified heat':
            loads_index=list(set([x for x in balances_df.index.get_level_values(0) if 'heat' in x]))
            loads_heat = - balances_df.loc[idx[loads_index,'loads',:],idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            links_index=(list(set([x for x in balances_df.index.get_level_values(2) if 'heat pump1'in  x])) +
                         list(set([x for x in balances_df.index.get_level_values(2) if 'resistive heater1'in  x])))
            elec_heat = balances_df.loc[idx[:,'links',links_index], idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            ratio_elec_heat=elec_heat/loads_heat
            try:
                sel_year=float(min(ratio_elec_heat[ratio_elec_heat>th[metric]].index))
            except:
                sel_year=0
                print('In budget ' + budget +', '+metric + ' does not happen < 2050')
        
        elif metric=='gas origin':
            gas_demand = - balances_df.loc[idx['gas','links', ['CCGT0', 
                                                               'OCGT0', 
                                                               'SMR CC0', 
                                                               'SMR0', 
                                                               'gas for industry CC0', 
                                                               'gas for industry0', 
                                                               'residential rural gas boiler0',
                                                               'residential urban decentral gas boiler0',
                                                               'services rural gas boiler0',
                                                               'services urban decentral gas boiler0', 
                                                               'urban central gas CHP CC0',
                                                               'urban central gas CHP0', 
                                                               'urban central gas boiler0']],
                                            idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            nonfossil_gas = balances_df.loc[idx['gas','links', ['Sabatier1',
                                                                'biogas to gas1',
                                                                'helmeth1',]],
                                           idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            ratio_nonfossil_gas=nonfossil_gas/gas_demand
            try:
                sel_year=float(min(ratio_nonfossil_gas[ratio_nonfossil_gas>th[metric]].index))
            except:
                sel_year=0
                print('In budget ' + budget +', '+metric + ' does not happen < 2050')
            
        else: 
            if metric=='e_E':
                sel = balances_df.loc[idx['co2', 'links', ['nuclear2','CCGT2', 'OCGT2', 'coal2', 'lignite2', 'oil2',]],
                                      idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
                # plus 50% of emissions from gas CHP are accounted as electricity emissions
                # I don't include here emissions from urban central solid biomass 
                # CHP to avoid negative emissions from BECCS obscure this metric
                sel += 0.5*balances_df.loc[idx['co2', 'links', ['urban central gas CHP3', 'urban central gas CHP CC3']],
                                      idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2])
            else:
                sel = balances_df.loc[idx[pos[metric]],idx[cluster, transmission, opt,:]].droplevel([0,1,2])
                
            if metric in decreasing_metrics:
                try:
                    sel_year = float(min(sel[abs(sel)<th[metric]].index))
                except:
                    sel_year=0
                    print('In budget ' + budget +', '+metric + ' does not happen < 2050')
            else:
                try:
                    sel_year = float(min(sel[abs(sel)>th[metric]].index))
                except:
                    sel_year=0
                    print('In budget ' + budget +', '+metric + ' does not happen < 2050')
        label_name=label_budget[budget] if metric==metrics[0] else None
        
        ax1.plot([sel_year+x_pos[budget]], [len(metrics) - i], 
                 linewidth=0,
                 markersize=20,
                 marker=marker_cb[budget],
                 markeredgecolor=color[budget],
                 markerfacecolor=color[budget],
                 alpha=0.9,label=label_name)

ax1.set_xlim([2028, 2052])
ax1.set_ylim([0, len(metrics)+1]) 
ax1.set_yticks(range(1,len(metrics)+1))
ax1.set_yticklabels([label[metric] for metric in reversed(metrics) ])
ax1.grid(color='grey', linestyle='--', axis='y')
ax1.legend(fancybox=True, fontsize=20, loc=(1.01,0.5), facecolor='white', 
           frameon=True, ncol=1)
plt.savefig('figures/KPI_transmission{}_{}_{}.png'.format(transmission,version,sensitivity_cost_option),
            dpi=600, bbox_inches='tight')
