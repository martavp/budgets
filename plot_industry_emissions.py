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

color['solid (coal)']='black'
color['liquid (oil)']='gray'
color['waste']='brown'
color['biomass']='green'
color['electricity']='blue'
color['gas']='orange'
color['hydrogen']='m'
color['heat']='red'

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18

plt.figure(figsize=(21, 10))
gs1 = gridspec.GridSpec(1, 1)
ax1 = plt.subplot(gs1[0,0])

# Energy consumption in industrial subsectors today
energy_today=pd.read_csv('results/resources/industrial_energy_demand_per_country_today.csv',
                        header=list(range(2)), index_col=0).droplevel([0], axis=1)
energy_today['DRI+Electric arc']=0
energy_today=energy_today.groupby(energy_today.columns, axis=1).sum()
energy_today=energy_today.drop(index='other')
energy_today.rename(index={'solid':'solid (coal)', 
                            'liquid':'liquid (oil)'},
                     inplace=True)

energy_today.sort_index().T.plot(kind='bar', stacked=True, ax=ax1, position=1.1, width=0.3,
                    color=[color[x] for x in energy_today.sort_index().T.columns],
                    legend=False)

# Energy consumption in industrial subsectors in 2050
industrial_production=pd.read_csv('results/resources/industrial_production_elec_s370_37m_2050.csv',
                        header=0, index_col=0).sum(axis=0)
sector_ratios=pd.read_csv('results/resources/industry_sector_ratios.csv',
                        header=0, index_col=0)
energy_future=industrial_production*sector_ratios

emissions=energy_future.loc[['process emission', 'process emission from feedstock']]
energy_future=energy_future.drop(index=['process emission', 'process emission from feedstock'])
energy_future*=0.001 #to TWh/a
energy_future.rename(index={'elec':'electricity', 
                            'methane':'gas', 
                            'coal':'solid (coal)', 
                            'coke':'solid (coal)', 
                            'naphtha':'liquid (oil)'},
                     inplace=True)

energy_future.loc['waste']=0 #waste only used today but added for the legend
energy_future=energy_future.groupby(level=0).sum()

energy_future.sort_index().T.plot(kind='bar', stacked=True, ax=ax1, position=-0.1, width=.3,
                     color=[color[x] for x in energy_future.sort_index().T.columns])

ax1.set_xlim([-0.5, 22.5])
ax1.set_ylabel('Final energy and non-energy (TWh/a)')
plt.savefig('figures/industry_energy.png', dpi=300, bbox_inches='tight')
#%%
plt.figure(figsize=(21, 10))
gs1 = gridspec.GridSpec(1, 1)
ax1 = plt.subplot(gs1[0,0])

ax1.set_ylabel('Emissions (Mt CO2)')
emissions*=0.001
emissions.sum(axis=0).T.plot(kind='bar', stacked=True, ax=ax1, width=0.4)
ax1.text(0.7, 0.9, 
         'Total process emissions = ' + str(round(emissions.sum(axis=0).sum(),1))+ 'MtCO$_2$/a',
         fontsize=18,
         transform=ax1.transAxes)
plt.savefig('figures/industry_process_emissions.png', dpi=300, bbox_inches='tight')
