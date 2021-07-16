
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from descartes import PolygonPatch
import geojson
import pypsa

plt.figure(figsize=(10,12))
gs1 = gridspec.GridSpec(24, 1)
ax1 = plt.subplot(gs1[0:22,0])
ax2 = plt.subplot(gs1[23,0])
n=pypsa.Network("results/version-baseline/postnetworks/elec_s370_37m_lv1.0__3H-T-H-B-I-solar+p3-dist1-cb51.4ex0_2050.nc")
tech='solar'
regions='../pypsa-eur/resources/regions_offshore_elec_s370.geojson' if tech=='offwind-ac' else '../pypsa-eur/resources/regions_onshore_elec_s370.geojson'
ax1.set_xlim(-11., 32.)
ax1.set_ylim(34., 70)
vmin = {'solar' : 0,
        'onwind': 0,
        'offwind-ac': 0,} 
vmax = {'solar' : 100,
        'onwind': 90,
        'offwind-ac': 17,}

cmap=mpl.cm.YlOrRd if tech=='solar' else mpl.cm.Greens

norm=mpl.colors.Normalize(vmin[tech], vmax[tech])
p_s=[]
with open(regions) as json_file:
    json_data = geojson.load(json_file)
    for i in range(len(json_data['features'])):
        node=json_data.features[i]['properties']['name']
        indices=[x for x in n.generators.index.to_list() if tech in x and node in x]
        p =n.generators.p_nom_opt[indices].sum()/1000 #MW to GW

        poly=json_data.features[i]['geometry'] 
        ax1.add_patch(PolygonPatch(poly,
                    fc=cmap((p-vmin[tech])/(vmax[tech]-vmin[tech])), 
                    ec='black',
                    linewidth=0.1))
        p_s.append(p)
print(max(p_s))
print(min(p_s))
cb1=mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal')

plt.savefig('figures/map_capacities_'+ tech +'.png', dpi=150, bbox_inches='tight')
