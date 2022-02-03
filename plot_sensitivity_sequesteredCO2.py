# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import numpy as np
idx = pd.IndexSlice

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18

transmission='1.0'
cluster='37m'
decay='ex0'
budget = '45.0'
costs=[0.1, 0.5, 1, 5, 10, 100]
potentials=[1, 2, 5, 10, 100]
metrics=[
        'co2 stored', 
        'total costs', 
        'co2_shadow',
        'synthetic methane', 
        'synthetic oil',
        'SMR CC'
         ]
title={'co2 stored':'sequestered CO$_2$ (Mt CO$_2$/a) in 2050', 
       'total costs':'relative anual system cost in 2050',
       'co2_shadow': 'CO$_2$ price (€/t CO$_2$)',
       'synthetic methane' : 'synthetic methane (Mt CO$_2$/a) in 2050', 
       'synthetic oil': 'synthetic liquid fuels (Mt CO$_2$/a) in 2050',
       'SMR CC': 'H$_2$ via steam methane reforming \n with carbon capture (TWh/a) in 2050',}

for metric in metrics:
    if metric in [ 'co2 stored','synthetic methane', 'synthetic oil', 'SMR CC']:
        balances_df = pd.read_csv('results/version-sensitivity-cc/csvs/supply_energy.csv',
                              index_col=list(range(3)), header=list(range(4)))
        
        if metric=='co2 stored':
            #CO2 -> Mt CO2
            balances_df= -0.000001*balances_df.loc[idx['co2 stored', ['stores'], metric],idx[cluster, transmission, :,'2050']].droplevel([0,1],axis=0).droplevel([0,1,3], axis=1)
        elif metric=='synthetic methane':
            balances_df= -0.000001*balances_df.loc[idx['co2 stored', ['links'], 'Sabatier2'],idx[cluster, transmission, :,'2050']].droplevel([0,1],axis=0).droplevel([0,1,3], axis=1)
        elif metric=='synthetic oil':
            balances_df= -0.000001*balances_df.loc[idx['co2 stored', ['links'], 'Fischer-Tropsch2'],idx[cluster, transmission, :,'2050']].droplevel([0,1],axis=0).droplevel([0,1,3], axis=1)
        elif metric=='SMR CC':
            balances_df= 0.000001*balances_df.loc[idx['H2', ['links'], 'SMR CC1'],idx[cluster, transmission, :,'2050']].droplevel([0,1],axis=0).droplevel([0,1,3], axis=1)
        cmap=mpl.cm.summer
        fontcolor='black'

    else:
        cost_df = pd.read_csv('results/version-sensitivity-cc/csvs/metrics.csv',
                              index_col=list(range(1)), header=list(range(4)))
        cost_df = cost_df.loc[idx[metric],idx[cluster, transmission, :,'2050']].droplevel([0,1,3], axis=0)
        balances_df=cost_df
        cmap=mpl.cm.winter 
        fontcolor='white'
        
    data_df=pd.DataFrame(index=costs, columns=potentials)
    for c in costs:
        for e in potentials:
            opts='3H-T-H-B-I-solar+p3-dist1-cb45.0ex0-co2 stored+c{}-co2 stored+e{}'.format(c,e)
            data_df.loc[c,e] = float(balances_df[opts])
    if metric== 'total costs':
        data_df=100*data_df/data_df.loc[1,1]
    norm=mpl.colors.Normalize(data_df.min().min(), data_df.max().max())
    plt.figure(figsize=(10, 7))
    gs1 = gridspec.GridSpec(20, 21)
    gs1.update(wspace=0.2, hspace=0.2)
    ax1 = plt.subplot(gs1[0:20,0:20])

    suffix='%' if metric=='total costs' else ''
    for i, c in enumerate(costs):
        for j,e in enumerate(potentials):
            ax1.text(0.5+j, 0.5+i, str(round(data_df.loc[c,e],1)) +suffix, 
                     ha='center', va='center', color=fontcolor, 
                     fontsize=20)
    data_df=data_df.astype(float)
    ax1.pcolor(data_df, cmap=cmap, norm=norm)
    ax1.set_yticks(0.5+np.arange(len(costs)))
    ax1.set_yticklabels(costs)
    ax1.set_ylabel('Cost (relative to 20€/t CO$_2$)')
    ax1.set_xticks(0.5+np.arange(len(potentials)))
    ax1.set_xticklabels(potentials)
    ax1.set_xlabel('Potential (relative to 200 Mt CO$_2$/a)')
    ax11 = plt.subplot(gs1[0:20,20])
    cb1=mpl.colorbar.ColorbarBase(ax11, cmap=cmap, orientation='vertical', norm=norm) 
    cb1.set_label(title[metric])
    plt.savefig('figures/sensitivity-cc_{}.png'.format(metric), dpi=150, bbox_inches='tight')

