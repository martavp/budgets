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

plt.figure(figsize=(10, 7))
gs1 = gridspec.GridSpec(1, 1)
ax1 = plt.subplot(gs1[0,0])

budgets = ['27', '36.7', '51.4', '63' , '75.2']

color ={'27':'yellowgreen', 
        '36.7':'dodgerblue', 
        '51.4':'gold',
        '63': 'orange',
        '75.2':'darkred',
        '36.7-noH2network':'black',
        '36.7-wo_eff':'black',}

label={'27':'1.5$^{\circ}$C',
      '36.7':'1.6$^{\circ}$C', 
      '51.4':'1.75$^{\circ}$C', 
      '63':'1.87$^{\circ}$C', 
      '75.2':'2.0$^{\circ}$C'}

decay = 'ex0'
transmission='1.0'
cluster='37m'
years=pd.Series(pd.date_range("2019", periods=7, freq="5Y"))

for budget in budgets:
    metrics_df = pd.read_csv('results/version-baseline/csvs/metrics.csv',
                            index_col=list(range(1)), header=list(range(4)))
    opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget, decay)
    co2_price =  metrics_df.loc[idx['co2_shadow'],idx[cluster, transmission, opt,:]].droplevel([0,1])
    plt.plot(years, co2_price.values, color=color[budget], linewidth=3, label=label[budget])

# add historical CO2 prices
# data downloaded from https://sandbag.org.uk/carbon-price-viewer/
data=pd.read_csv('data/eua-price.csv', sep=',')
date= [datetime.strptime(hour, '%Y-%m-%d %H:%M:%S').date() for hour in data['Date']]
ax1.plot(date, data['Price'] , linewidth=2, color='black', label='EU-ETS')

ax1.set_ylabel('CO$_2$ price (€/ton)', fontsize=16)
ax1.grid(linestyle='--')
ax1.set_ylim([0, 450])  
ax1.set_xlim([datetime(2008,1,1,0,0,0), datetime(2051,1,1,0,0,0)]) 
ax1.legend(fancybox=False, fontsize=16, loc=(0.012,0.6), facecolor='white', frameon=True)
plt.savefig('figures/co2_price.png', dpi=300, bbox_inches='tight')



