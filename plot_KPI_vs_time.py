# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
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

gcb = [420, 580, 800, 1170]

budgets = ['25', '34', '48', '70', '48-noH2network','48-wo_eff']

marker_cb ={'25':'o', 
           '34':'s', 
           '48':'^', 
           '70':'D',
           '48-noH2network':'+',
           '48-wo_eff':'x'}
color ={'25':'yellowgreen', 
           '34':'dodgerblue', 
           '48':'gold',
           #'': 'orange',
           '70':'darkred',
           '48-noH2network':'black',
           '48-wo_eff':'black',}

x_pos ={'25':-0.6, 
        '34':-0.2, 
        '48':0.2, 
        '70':0.6,
        '48-noH2network':0,
        '48-wo_eff':0,}
cb2T={'25':'1.5$^{\circ}$C',
       '34':'1.6$^{\circ}$C', 
       '48':'1.7$^{\circ}$C', 
       '70':'2.0$^{\circ}$C', 
       '48-noH2network':'1.7$^{\circ}$C (wo H$_2$ network)',
       '48-wo_eff':'1.7$^{\circ}$C (no eff)',}


transmission='1.0'
cluster='37'
decay='ex0'
metrics = ['co2_stored', 'Fischer-Tropsch', 'DAC', 'gas boilers', 'H2', 'oil','e_E']

decreasing_metrics = ['gas boilers', 'oil', 'e_E']
th = {'co2_stored' : 2e+8*0.95, # ~200MtCO2
      'Fischer-Tropsch':100e+6,  # 100 TWh/year
      'DAC': 10e+6, # ~ 10 MtCO2/year
      'gas boilers' :100e+6,  # 100 TWh/year
      'H2' : 100e+6,  # 100 TWh/year
      'oil': 1000e+6, # 1000 TWh/year
      'e_E':50e+6} # ~20MtCO2
pos= {'co2_stored':('co2 stored', 'stores', 'co2 stored'),
      'Fischer-Tropsch':('Fischer-Tropsch', 'links', 'Fischer-Tropsch1'),
      'DAC':('co2', 'links', 'DAC0'),
      'gas boilers': ('residential rural heat','links','residential rural gas boiler1'),
      'H2' : ('H2', 'links', 'H2 Electrolysis1'),
      'oil': ('Fischer-Tropsch', 'generators', 'oil')}
for budget in budgets:
    balances_df = pd.read_csv('results/version-cb{}{}/csvs/supply_energy.csv'.format(budget,decay),index_col=list(range(3)),
                              header=list(range(4)))
    if budget=='48-noH2network':
        opt='3H-T-H-B-I-solar3-dist1-noH2network-cb48ex0'
    elif budget=='48-wo_eff':
        opt='3H-T-H-B-I-solar3-dist1-cb48ex0'
    else:
        opt ='3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
    facecolor=color[budget] if decay=='ex0' else "white"
    y_pos= 0.1 if decay=='be3' else -0.1  
    
    for i,metric in enumerate(metrics):
        if metric=='e_E':
            sel = balances_df.loc[idx['co2', 'links', ['CCGT2',  'OCGT2', 'coal2', 'lignite2', 'nuclear2', 'oil2',]],idx[cluster, transmission, opt,:]].sum().droplevel([0,1,2]) #CO2 -> Mt CO2
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
        label_name=cb2T[budget] if metric==metrics[0] else None
        ax1.plot([sel_year+x_pos[budget]], [1+i+y_pos], 
                 linewidth=0,
                 markersize=20,
                 marker=marker_cb[budget],
                 markeredgecolor=color[budget],
                 markerfacecolor=facecolor,
                 alpha=0.9,label=label_name)
 

ax1.set_xlim([2020, 2050])
ax1.set_ylim([0, len(metrics)+1]) 
ax1.set_yticks(range(1,len(metrics)+1))
ax1.set_yticklabels(['CO$_2$ storage =  200 MtCO$_2$/a', 
                     'Fischer-Tropsch >  100 TWh/a', 
                     'DAC >  10 MtCO$_2$/a', 
                     'Heating electrification  gas boilers in residential \n rural heat < 100 TWh/a',
                     'Electrolytic H$_2$ > 500 TWh/a',
                     'Reduced exterior dependence  oil consumption < 1000 TWh/a',
                     'Electricity  emissions < 50 MtCO$_2$/a'])
ax1.grid(color='grey', linestyle='--', axis='y')
ax1.legend(fancybox=True, fontsize=20, loc='best', facecolor='white', 
           frameon=True, ncol=1)
plt.savefig('figures/KPI_transmission{}.png'.format(transmission),
            dpi=600, bbox_inches='tight')
