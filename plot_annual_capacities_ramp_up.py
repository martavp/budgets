# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import seaborn as sns; sns.set()
idx = pd.IndexSlice
import pypsa

years=np.arange(2001, 2053, 1)
techs = ['Solar', 'Rooftop Solar', 'Onshore Wind', 'Offshore Wind', 
         'Battery', 'Home Battery', 'Electrolysis', 'Fuel Cell', 'H2 Store',
         'OCGT', 'Methanation', 'Direct Air Capture', 'Fischer-Tropsch',
         'central heat pump','central resistive heater',
          'urban central water tanks']
techs_stores = ['Battery', 'Home Battery', 'H2 Store', 'urban central water tanks']

budgets = ['historical']+['25.7','35.4','45.0','54.7','64.3','73.9']

data = pd.DataFrame(index=pd.MultiIndex.from_product([pd.Series(data=years, name='year'),
                                         pd.Series(data=budgets, name='budgets',)]), 
                    columns=pd.Series(data=techs, name='technology'))

# PV capacities read from IRENA database 
# https://www.irena.org/statistics
pv_df = pd.read_csv('data/PV_capacity_IRENA.csv', sep=';',
                    index_col=0, encoding="latin-1")
onwind_df = pd.read_csv('data/OnshoreWind_capacity_IRENA.csv', sep=';',
                    index_col=0, encoding="latin-1")
offwind_df = pd.read_csv('data/OffshoreWind_capacity_IRENA.csv', sep=';',
                    index_col=0, encoding="latin-1")

for year in np.arange(2001, 2021, 1):
    data.loc[idx[year,'historical'],'Solar'] =  (pv_df[str(year)]['EU 28']-pv_df[str(year-1)]['EU 28'])
    data.loc[idx[year,'historical'],'Onshore Wind'] = (onwind_df[str(year)]['EU 28']-onwind_df[str(year-1)]['EU 28'])
    data.loc[idx[year,'historical'],'Offshore Wind'] =  (offwind_df[str(year)]['EU 28']-offwind_df[str(year-1)]['EU 28'])
for budget in budgets[1:]:
    years = np.arange(2020, 2055,5)
    for year in years:
        n =pypsa.Network("results/version-baseline/postnetworks/elec_s370_37m_lv1.0__3H-T-H-B-I-solar+p3-dist1-cb{}ex0_{}.nc".format(budget,year))
        #0.2 coefficient due to 5-years periods
        data.loc[idx[np.arange(year-2,year+3),budget],'Solar'] = 0.2* n.generators.p_nom_opt[[i for i in n.generators.index if 'solar-{}'.format(year) in i and 'rooftop' not in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Onshore Wind'] = 0.2* n.generators.p_nom_opt[[i for i in n.generators.index if 'onwind-{}'.format(year) in i ]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Offshore Wind'] = ( 0.2* n.generators.p_nom_opt[[i for i in n.generators.index if 'offwind-ac-{}'.format(year) in i ]].sum()
                                                     + 0.2* n.generators.p_nom_opt[[i for i in n.generators.index if 'offwind-dc-{}'.format(year) in i ]].sum())
        data.loc[idx[np.arange(year-2,year+3),budget],'Rooftop Solar'] = 0.2* n.generators.p_nom_opt[[i for i in n.generators.index if 'solar rooftop-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Battery'] = 0.2* n.stores.e_nom_opt[[i for i in n.stores.index if 'battery-{}'.format(year) in i and 'home battery' not in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Home Battery'] = 0.2* n.stores.e_nom_opt[[i for i in n.stores.index if 'home battery-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Electrolysis'] = 0.2* n.links.p_nom_opt[[i for i in n.links.index if 'H2 Electrolysis-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Fuel Cell'] = 0.2* n.links.p_nom_opt[[i for i in n.links.index if 'H2 Fuel Cell-{}'.format(year) in i]].sum()
        eff_OCGT=0.41
        data.loc[idx[np.arange(year-2,year+3),budget],'OCGT'] = 0.2*eff_OCGT*n.links.p_nom_opt[[i for i in n.links.index if 'OCGT-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Methanation'] = 0.2*eff_OCGT*n.links.p_nom_opt[[i for i in n.links.index if 'Sabatier-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Direct Air Capture'] = 0.2*n.links.p_nom_opt[[i for i in n.links.index if 'DAC-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'Fischer-Tropsch'] = 0.2*n.links.p_nom_opt[[i for i in n.links.index if 'Fischer-Tropsch-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'central heat pump'] = 0.2*n.links.p_nom_opt[[i for i in n.links.index if 'urban central air heat pump-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'central resistive heater'] = 0.2*n.links.p_nom_opt[[i for i in n.links.index if 'urban central resistive heater-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'urban central water tanks'] = 0.2*n.stores.e_nom_opt[[i for i in n.stores.index if 'urban central water tanks'.format(year) in i]].sum()
        
        #H2 storage is missing lifetime attribute and hence it is not saved in the myopic optimization
        #data.loc[idx[np.arange(year-4,year+1),budget],'H2 Store'] = 0.2*n.stores.e_nom_opt[[i for i in n.stores.index if 'H2 Store-{}'.format(year) in i]].sum()
        data.loc[idx[np.arange(year-2,year+3),budget],'H2 Store'] = 0.2*n.stores.e_nom_opt[[i for i in n.stores.index if 'H2 Store' in i]].sum()
        if year != 2025:
            data.loc[idx[np.arange(year-2,year+3),budget],'H2 Store'] = max(data.loc[idx[year-6,budget],'H2 Store'],
                                                                         data.loc[idx[year-1,budget],'H2 Store'])

data.to_csv('data/annual_capacities_ramp_up.csv', sep=',')

#%%

"""
Plotting
"""
data=pd.read_csv('data/annual_capacities_ramp_up.csv', sep=',', header=0, index_col=(0,1))
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
        '73.9':'2.0$^{\circ}$C', 
        '45.0-noH2network':'1.7$^{\circ}$C (wo H$_2$ network)',
        '45.0-wo_eff':'1.7$^{\circ}$C (no eff)',}

data*=0.001 #MW ->GW
for i, tech in enumerate(techs):
    ax1 = plt.subplot(gs1[int(i/4),i-4*int(i/4)])

    if tech in ['Solar', 'Onshore Wind', 'Offshore Wind']:
        plt.plot(np.arange(2001, 2019, 1),
                 data.loc[idx[np.arange(2001, 2019, 1),'historical'],tech].values, 
                 color='black', linewidth=3, label='historical')
    unit ='GWh' if tech in techs_stores else 'GW'
    ax1.set_ylabel(tech + ' (' + unit + ')', fontsize=18)
    for budget in budgets[1:]:
        plt.plot(np.arange(2020,2051,1),
              data.loc[idx[np.arange(2020,2051,1),budget],tech].values , 
              color=color[budget], linewidth=3, label=label[budget])
    ax1.set_xticks([2010, 2020, 2030, 2040, 2050])
    
    if int(i/4)==3:
        ax1.set_xticklabels(['2010', '2020', '2030', '2040', '2050'], rotation=45)
    else:
        ax1.set_xticklabels([])
    
    if i==0:
        ax1.legend(fancybox=False, fontsize=18, loc=(0.5,1.05), 
                   facecolor='white', ncol=7, frameon=True)
    ax1.grid(linestyle='--' ) #, axis='y')
    ax1.set_xlim([2010,2050])
plt.savefig('figures/per_year_new_capacities.png', dpi=300, bbox_inches='tight')







