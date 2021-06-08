#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 14:35:18 2021

@author: marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 14

def plot_exogenous_parameter(exogenous_parameter, data, y_title, 
                             exogeous_parameter2=None, data2=None):
    plt.figure(figsize=(7, 5))
    gs1 = gridspec.GridSpec(1, 1)
    ax1 = plt.subplot(gs1[0,0])
    ax1.plot(pd.Series(data), linewidth=3,label=exogenous_parameter)
    if data2!=None:
        ax1.plot(pd.Series(data2), linewidth=3, label=exogeous_parameter2)
        ax1.legend(loc='best')
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
                         snakemake.config['sector']['retrofitting']['dE'],
                         'Reduction of space heat demand (relative to 2020)')

plot_exogenous_parameter('land_transport_electric_share',
                         snakemake.config['sector']['land_transport_electric_share'],
                         'Share converted transport',
                         'land_transport_fuel_cell_share',
                         snakemake.config['sector']['land_transport_fuel_cell_share'],)

plot_exogenous_parameter('DRI_fraction',
                         snakemake.config['industry']['DRI_fraction'],
                         'Fraction of steel produced via DRI/secondary route',
                         'scrap_steel_fraction',
                         snakemake.config['industry']['scrap_steel_fraction'])

plot_exogenous_parameter('Al_primary_fraction' ,
                         snakemake.config['industry']['Al_primary_fraction'],
                         'Fraction of Aluminum produced by primary route')

plot_exogenous_parameter('shipping_fuel_cell_share',
                         snakemake.config['sector']['shipping_fuel_cell_share'],
                         'Share converted shipping')
