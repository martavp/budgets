# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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
gs1.update(wspace=0.2, hspace=0.2)


ax1 = plt.subplot(gs1[0,0])
cb = [25, 34, 48, 70]
T = [1.5, 1.6, 1.7, 2.0]
discount_rates = [0.0, 0.02, 0.04, 0.06, 0.08]
budgets = ['25', '34', '48', '70']

color_dr ={0: 'sienna',
          0.02: 'darkgoldenrod',
          0.04:'tan',
          0.06: 'lightseagreen',
          0.08: 'darkcyan',
          0.10 : 'darkslategray'}
marker_cb ={'25':'o', 
           '34':'s', 
           '48':'^', 
           '70':'D',
           'noH2network':'+',
           'wo_eff':'x',
           'noBECC':'1'}
style_decay={'be3':'--', 
             'ex0':'-'}

cb2gcb=pd.Series(cb,index=budgets).to_dict()
# data to calculate social cost of carbon
social_cost_carbon=100 #€/tonne CO2
opts='H-T-I'
countries=pd.read_csv('results/countries.csv',  index_col=1) 
cts=countries.index.to_list()
from prepare_sector_network import co2_emissions_year
e_1990 = co2_emissions_year(cts, opts, year=1990)

transmission=1.0
cluster=37
decay = 'ex0'
for discount_rate in discount_rates:
    to_plot=[]
    for budget in budgets:
        #calculate social cost of carbon (relative to the lowest carbon budget)
        path_cb =  'results/version-cb{}{}/csvs/'.format(budget,decay)
        CO2_CAP=pd.read_csv(path_cb + 'carbon_budget_distribution.csv',  
                    index_col=0)
        path_cb_ref =  'results/version-cb{}{}/csvs/'.format('25', 'ex0')
        CO2_CAP_ref=pd.read_csv(path_cb_ref + 'carbon_budget_distribution.csv',  
                    index_col=0) 
        timestep=CO2_CAP.index[1]-CO2_CAP.index[0]
        carbon_cost=sum([(CO2_CAP.loc[year, 'cb'+budget+decay]-CO2_CAP_ref.loc[year, 'cb25ex0'])*e_1990*timestep*social_cost_carbon/(1+discount_rate)**(year-CO2_CAP.index[0]) for year in CO2_CAP.index])/1000 #Gt to tonnes compensates € to B€ 
        
        cumulative_cost_df = pd.read_csv('results/version-cb{}{}/csvs/cumulative_cost.csv'.format(budget,decay))
        cumulative_cost_df = cumulative_cost_df.set_index(['cluster', 'lv', 'opt', 'planning_horizon']).sort_index()
        opt ='3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
        cumulative_system_cost = cumulative_cost_df.loc[idx[cluster,transmission,opt, 'cumulative cost'],str(discount_rate)]/1000000000000 #€ to 10⁶M€ 
        cumulative_system_cost +=carbon_cost
        to_plot.append(cumulative_system_cost)  
        facecolor=color_dr[discount_rate] if decay=='be3' else 'white'
        ax1.plot(cb2gcb[budget], cumulative_system_cost,
                 markersize=10,
                 marker=marker_cb[budget],
                 markeredgecolor=color_dr[discount_rate],
                 markerfacecolor=facecolor)
    ax1.plot(cb, to_plot, 
             zorder=-1,
             color=color_dr[discount_rate],
             linestyle=style_decay[decay],
             label=discount_rate) 

for scenario in ['noH2network','wo_eff','noBECC']:
    discount_rate=0.02
    budget='48'
    path_cb =  'results/version-cb{}{}/csvs/'.format(budget,decay)
    CO2_CAP=pd.read_csv(path_cb + 'carbon_budget_distribution.csv',  
                    index_col=0)
    path_cb_ref =  'results/version-cb{}{}/csvs/'.format('25', 'ex0')
    CO2_CAP_ref=pd.read_csv(path_cb_ref + 'carbon_budget_distribution.csv',  
                index_col=0) 
    timestep=CO2_CAP.index[1]-CO2_CAP.index[0]
    carbon_cost=sum([(CO2_CAP.loc[year, 'cb'+budget+decay]-CO2_CAP_ref.loc[year, 'cb25ex0'])*e_1990*timestep*social_cost_carbon/(1+discount_rate)**(year-CO2_CAP.index[0]) for year in CO2_CAP.index])/1000 #Gt to tonnes compensates € to B€ 
        
    cumulative_cost_df = pd.read_csv('results/version-cb{}-{}{}/csvs/cumulative_cost.csv'.format(budget,scenario,decay))
    cumulative_cost_df = cumulative_cost_df.set_index(['cluster', 'lv', 'opt', 'planning_horizon']).sort_index()

    opt ='3H-T-H-B-I-solar3-dist1-{}-cb{}{}'.format(scenario,budget,decay) if scenario=='noH2network' else '3H-T-H-B-I-solar3-dist1-cb{}{}'.format(budget,decay)
    cumulative_system_cost = cumulative_cost_df.loc[idx[cluster,transmission,opt, 'cumulative cost'],str(discount_rate)]/1000000000000 #€ to 10⁶ M€ 
    cumulative_system_cost +=carbon_cost
    ax1.plot(cb2gcb[budget], cumulative_system_cost,
             markersize=10,
             linewidth=0,
             marker=marker_cb[scenario],
             markeredgecolor='black', 
             markerfacecolor=None,
             label=scenario) 

ax1.set_ylabel('Cumulative System Costs (10$^6$M€)')   
ax1.set_xlabel('Temperature increase ($^{\circ}$C)') 
ax1.set_xlim(20, 75)
ax2=ax1.twiny()
ax2.set_xlim(20, 75)
ax2.set_xlabel('Europe carbon budget (GtCO$_2$)') 
ax1.set_xticks(cb)
ax1.set_xticklabels(T)
ax1.legend(fancybox=True, fontsize=16, loc='best',#(1.01,0), 
           facecolor='white', 
           frameon=True, ncol=1)
plt.savefig('figures/cumulative_system_cost_transmission{}_scc{}.png'.format(transmission,social_cost_carbon), dpi=600, bbox_inches='tight')


