#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 14:35:18 2021

@author: marta
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 18

def plot_exogenous_parameter(exogenous_parameter, data, y_title, 
                             exogeous_parameter2=None, data2=None,
                             exogeous_parameter3=None, data3=None,
                             labels=None):
    plt.figure(figsize=(10, 7))
    gs1 = gridspec.GridSpec(1, 1)
    ax1 = plt.subplot(gs1[0,0])
    ax1.plot(pd.Series(data), linewidth=3,label=exogenous_parameter)
    if exogeous_parameter3!=None:
        ax1.plot(pd.Series(data3), linewidth=3, label=exogeous_parameter3)
    if exogeous_parameter2!=None:
        ax1.plot(pd.Series(data2), linewidth=3, label=exogeous_parameter2)
        ax1.legend(labels, 
                   fancybox=True,
                   frameon=True,
                   loc='best')
    ax1.grid()
    ax1.set_xlim([2020,2050])
    ax1.set_ylabel(y_title)
    plt.savefig('figures/{}.png'.format(exogenous_parameter), dpi=300, bbox_inches='tight') 


from vresutils import Dict
import yaml
snakemake = Dict()
with open('config.yaml') as f:
     snakemake.config = yaml.safe_load(f)

plot_exogenous_parameter('reduction_space_heat_demand',
                         snakemake.config['sector']['reduce_space_heat_exogenously_factor'],
                         'Reduction of space heat demand (relative to 2020)')

plot_exogenous_parameter('land_transport_electric_share',
                         snakemake.config['sector']['land_transport_electric_share'],
                         'Share converted transport',
                         'land_transport_fuel_cell_share',
                         snakemake.config['sector']['land_transport_fuel_cell_share'],
                         labels=['electric share', 'fuel cell share'])

frac_DRI=pd.Series(snakemake.config['industry']['DRI_fraction']).multiply(pd.Series(snakemake.config['industry']['St_primary_fraction']))
frac_steelworks =(1-pd.Series(snakemake.config['industry']['DRI_fraction'])).multiply(pd.Series(snakemake.config['industry']['St_primary_fraction']))
frac_secondary = 1-pd.Series(snakemake.config['industry']['St_primary_fraction'])
plot_exogenous_parameter('DRI+EAF', frac_DRI, 'Fraction of steel produced with different routes',
                         'Steelworks', frac_steelworks,
                         'scrap+EAF',frac_secondary,
                         labels=['DRI+EAF', 'scrap+EAF','Steelworks', ])


plot_exogenous_parameter('Al_primary_fraction' ,
                         snakemake.config['industry']['Al_primary_fraction'],
                         'Fraction of Aluminum produced by primary route')

plot_exogenous_parameter('shipping_hydrogen_share',
                         snakemake.config['sector']['shipping_hydrogen_share'],
                         'Share converted shipping')
