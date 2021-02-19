
import numpy as np
import pandas as pd
#import matplotlib

import matplotlib.pyplot as plt

from prepare_sector_network import co2_emissions_year

def historical_emissions(cts):
    """
    read historical emissions to add them to the carbon budget plot
    """
    #https://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-16
    #downloaded 201228 (modified by EEA last on 201221)
    fn = "data/eea/UNFCCC_v23.csv"
    df = pd.read_csv(fn, encoding="latin-1")
    df.loc[df["Year"] == "1985-1987","Year"] = 1986
    df["Year"] = df["Year"].astype(int)
    df = df.set_index(['Year', 'Sector_name', 'Country_code', 'Pollutant_name']).sort_index()

    e = pd.Series()
    e["electricity"] = '1.A.1.a - Public Electricity and Heat Production'
    e['residential non-elec'] = '1.A.4.b - Residential'
    e['services non-elec'] = '1.A.4.a - Commercial/Institutional'
    e['rail non-elec'] = "1.A.3.c - Railways"
    e["road non-elec"] = '1.A.3.b - Road Transportation'
    e["domestic navigation"] = "1.A.3.d - Domestic Navigation"
    e['international navigation'] = '1.D.1.b - International Navigation'
    e["domestic aviation"] = '1.A.3.a - Domestic Aviation'
    e["international aviation"] = '1.D.1.a - International Aviation'   
    e['total energy'] = '1 - Energy'
    e['industrial processes'] = '2 - Industrial Processes and Product Use'
    e['agriculture'] = '3 - Agriculture'
    e['LULUCF'] = '4 - Land Use, Land-Use Change and Forestry'
    e['waste management'] = '5 - Waste management'
    e['other'] = '6 - Other Sector'
    e['indirect'] = 'ind_CO2 - Indirect CO2'
    e["total wL"] = "Total (with LULUCF)"
    e["total woL"] = "Total (without LULUCF)"
       
    pol = ["CO2"] # ["All greenhouse gases - (CO2 equivalent)"] 
    cts
    if "GB" in cts:
        cts.remove("GB")
        cts.append("UK")
         
    year = np.arange(1990,2018).tolist()

    idx = pd.IndexSlice
    co2_totals = df.loc[idx[year,e.values,cts,pol],"emissions"].unstack("Year").rename(index=pd.Series(e.index,e.values)) 
    
    co2_totals = (1/1e6)*co2_totals.groupby(level=0, axis=0).sum() #Gton CO2

    co2_totals.loc['industrial non-elec'] = co2_totals.loc['total energy'] - co2_totals.loc[['electricity', 'services non-elec','residential non-elec', 'road non-elec',
                                                                              'rail non-elec', 'domestic aviation', 'international aviation', 'domestic navigation',
                                                                              'international navigation']].sum()

    emissions = co2_totals.loc["electricity"]   
    if "T" in opts:
        emissions += co2_totals.loc[[i+ " non-elec" for i in ["rail","road"]]].sum()
    if "H" in opts:
        emissions += co2_totals.loc[[i+ " non-elec" for i in ["residential","services"]]].sum()
    if "I" in opts:
        emissions += co2_totals.loc[["industrial non-elec","industrial processes",
                                          "domestic aviation","international aviation",
                                          "domestic navigation","international navigation"]].sum()           
    return emissions



def plot_carbon_budget_distribution():
    """
    Plot historical carbon emissions in the EU and decarbonization path
    """ 
    
    import matplotlib.gridspec as gridspec
    import seaborn as sns; sns.set()
    sns.set_style('ticks')
    plt.style.use('seaborn-ticks')
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 20   

    plt.figure(figsize=(10, 7))
    gs1 = gridspec.GridSpec(1, 1)
    ax1 = plt.subplot(gs1[0,0])
    ax1.set_ylabel('CO$_2$ emissions (Gt per year)',fontsize=22)
    ax1.set_ylim([0,5])
    ax1.set_xlim([1990,2051])
    countries=pd.read_csv('results/countries.csv',  index_col=1) 
    cts=countries.index.to_list()
    e_1990 = co2_emissions_year(cts, opts, year=1990)
    budgets = ['cb25be3', 'cb25be3','cb25ex0','cb34be3','cb34ex0','cb48be3',
               'cb48ex0','cb70be3','cb70ex0']
    col={'cb25be3':'blue',
         'cb25ex0':'blue',
         'cb34be3':'dodgerblue',
         'cb34ex0':'dodgerblue',
         'cb48be3':'lightcoral',
         'cb48ex0':'lightcoral',
         'cb70be3':'darkred',
         'cb70ex0':'darkred'}
    for budget in budgets:
        path_cb =  'results/version-{}/csvs/'.format(budget)
        CO2_CAP=pd.read_csv(path_cb + 'carbon_budget_distribution.csv',  
                        index_col=0) 
        ls='--' if 'ex' in budget else '-'
        ax1.plot(e_1990*CO2_CAP[budget],linewidth=3, 
                 color=col[budget], linestyle=ls, label=None)
            
    emissions = historical_emissions(cts)

    ax1.plot(emissions, color='black', linewidth=3, label=None) 
    
    #plot commited and uder-discussion targets  
    #(notice that historical emissions include all countries in the
    # network, but targets refer to EU)
    ax1.plot([2020],[0.8*emissions[1990]],
                     marker='*', markersize=12, markerfacecolor='black',
                     markeredgecolor='black')    
            
    ax1.plot([2030],[0.45*emissions[1990]],
                     marker='*', markersize=12, markerfacecolor='white',
                     markeredgecolor='black')    
            
    ax1.plot([2030],[0.6*emissions[1990]],
                     marker='*', markersize=12, markerfacecolor='black',
                     markeredgecolor='black')
            
    ax1.plot([2050, 2050],[x*emissions[1990] for x in [0.2, 0.05]],
                  color='gray', linewidth=2, marker='_', alpha=0.5) 
            
    ax1.plot([2050],[0.01*emissions[1990]],
                     marker='*', markersize=12, markerfacecolor='white', 
                     linewidth=0, markeredgecolor='black', 
                     label='EU under-discussion target', zorder=10, 
                     clip_on=False) 
            
    ax1.plot([2050],[0.125*emissions[1990]],'ro',
                     marker='*', markersize=12, markerfacecolor='black',
                     markeredgecolor='black', label='EU commited target')
            
    ax1.legend(fancybox=True, fontsize=18, loc=(0.01,0.01), 
                       facecolor='white', frameon=True) 
            
    path_cb_plot = 'figures/'             
    plt.savefig(path_cb_plot+'carbon_budgets.png', dpi=300) 

opts='H-T-I'
plot_carbon_budget_distribution()