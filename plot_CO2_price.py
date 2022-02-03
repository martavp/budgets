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
years=pd.Series(pd.date_range("2019", periods=7, freq="5Y"))
version='baseline' #'sensitivity-fixedcosts' 
for budget in budgets:
    metrics_df = pd.read_csv('results/version-{}/csvs/metrics.csv'.format(version),
                            index_col=list(range(1)), header=list(range(4)))
    opt ='3H-T-H-B-I-solar+p3-dist1-cb{}{}'.format(budget, decay)
    co2_price = metrics_df.loc[idx['co2_shadow'],idx[cluster, transmission, opt,:]].droplevel([0,1,2], axis=0)
    # Add one value per year to plot step-wise figures
    co2_price.index=[int(x) for x in co2_price.index]
    for year in range(2020,2055,5):
        for j in range(0,5):
            co2_price[year-2+j]=co2_price[year]
    co2_price=co2_price.reindex(sorted(co2_price.index), axis=1)
    co2_price=co2_price.drop(index=[2018,2019,2020,2051,2052])

    ax1.plot(pd.to_datetime(co2_price.index, format='%Y'), 
             co2_price.values, color=color[budget], 
             linewidth=3, label=label[budget])

# add historical CO2 prices
# data downloaded from https://sandbag.org.uk/carbon-price-viewer/
data=pd.read_csv('data/eua-price.csv', sep=',')
date= [datetime.strptime(hour, '%Y-%m-%d %H:%M:%S').date() for hour in data['Date']]
ax1.plot(date, data['Price'] , linewidth=2, color='black', label='EU-ETS')

ax1.set_ylabel('CO$_2$ price (€/ton)', fontsize=16)
ax1.grid(linestyle='--')
ax1.set_ylim([0, 500]) # ax1.set_ylim([0, 610])
ax1.set_xlim([datetime(2008,1,1,0,0,0), datetime(2050,1,1,0,0,0)]) 
ax1.legend(fancybox=False, fontsize=16, loc=(0.012,0.5), facecolor='white', frameon=True)
plt.savefig('figures/co2_price_{}.png'.format(version), dpi=300, bbox_inches='tight')



