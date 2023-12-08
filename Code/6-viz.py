"""
install:
pyogrio
fiona
"""

import os

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import data_dir, viz_dir, stata_dir

# Load the world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Load your CSV data
# Replace 'your_data.csv' with the path to your CSV file

vdem_to_geo = {
    'Burma/Myanmar': 'Myanmar',
    'Bosnia and Herzegovina': 'Bosnia and Herz.',
    'Ivory Coast': "Côte d'Ivoire",
    'Democratic Republic of the Congo': 'Dem. Rep. Congo',
    'Dominican Republic': 'Dominican Rep.',
    'Equatorial Guinea': 'Eq. Guinea',
    'The Gambia': 'Gambia',
    'South Sudan': 'S. Sudan',
    'Eswatini': 'eSwatini',
    'Solomon Islands': 'Solomon Is.',
    'Central African Republic': 'Central African Rep.',
    'Republic of the Congo': 'Congo',
    'Palestine/West Bank': 'Palestine',
}

def plot_year(data, year, myval, title=''):
    if not title:
        title = myval

    thisyear_data = data[data['year'] == year]

    # Merge the world map with your data based on the country name
    # merged_data = world.merge(thisyear_data, how='left', left_on='name', right_on='country_name')
    merged_data = world.merge(thisyear_data, how='left', left_on='name', right_on='country_name')
    merged_data = gpd.GeoDataFrame(merged_data)

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.set_title(f'World {title}')

    # Plot the map with colors based on 'myval'
    merged_data.plot(
        column=myval, cmap='RdYlGn', linewidth=0.8, ax=ax,
        edgecolor='0.8',
        # legend=True,
    )

    # Customize the colorbar
    cax = fig.add_axes([0.95, 0.2, 0.02, 0.6])
    sm = plt.cm.ScalarMappable(
        cmap='RdYlGn', 
        norm=plt.Normalize(vmin=merged_data[myval].min(), vmax=merged_data[myval].max())
    )
    sm._A = []
    fig.colorbar(sm, cax=cax)

    # Show the plot
    # plt.show()
    plt.savefig(os.path.join(viz_dir, f'{title}.png'))

# wb_urbpop = pd.read_csv(os.path.join(data_dir, 'CY-DATA-Urbpop.csv'))
# wb_urbpop['country_name'] = wb_urbpop['country_name'].replace(vdem_to_geo)
# plot_year(wb_urbpop, 2015, 'wb_urbpop', 'Urban Population')

# resem = pd.read_csv(os.path.join(data_dir, 'CY-DATA-Resemblance.csv'))
# resem['country_name'] = resem['country_name'].replace(vdem_to_geo)

# plot_year(resem, 2015, 'Elr', 'Linguistic Resemblance')
# plot_year(resem, 2015, 'Epr', 'Political Resemblance')
# plot_year(resem, 2015, 'Err', 'Religious Resemblance')
# plot_year(resem, 2015, 'Egr', 'Genetic Resemblance')
# resem['lr_norm'] = (resem['Elr'] - resem['Elr'].min()) / (resem['Elr'].max() - resem['Elr'].min())
# resem['pr_norm'] = (resem['Epr'] - resem['Epr'].min()) / (resem['Epr'].max() - resem['Epr'].min())
# resem['rr_norm'] = (resem['Err'] - resem['Err'].min()) / (resem['Err'].max() - resem['Err'].min())
# resem['gr_norm'] = (resem['Egr'] - resem['Egr'].min()) / (resem['Egr'].max() - resem['Egr'].min())

# resem['resem'] = (resem['lr_norm'] + resem['pr_norm'] + resem['rr_norm'] + resem['gr_norm']) / 4
# plot_year(resem, 2015, 'resem', 'Overall Resemblance')

# pwd = pd.read_csv(os.path.join(data_dir, 'CY-DATA-PWD.csv'))
# pwd['country_name'] = pwd['country_name'].replace(vdem_to_geo)
# pwd['PWD_A_l'] = np.log(pwd['PWD_A'])
# pwd['PWD_G_l'] = np.log(pwd['PWD_G'])
# pwd['PWD_M_l'] = np.log(pwd['PWD_M'])
# plot_year(pwd, 2015, 'PWD_A_l', 'Log Mean weighted Density (Arithmetic)')
# plot_year(pwd, 2015, 'PWD_G_l', 'Log Mean of weighted Density (Geometric)')
# plot_year(pwd, 2015, 'PWD_M_l', 'Log Median weighted Density')

# vdemw4 = pd.read_csv(os.path.join(data_dir, 'VDem_W4.csv'))
# vdemw4['country_name'] = vdemw4['country_name'].replace(vdem_to_geo)
# plot_year(vdemw4, 2015, 'W4', 'Coalition Size Index')

# vdem13 = pd.read_csv(os.path.join(data_dir, 'V-Dem-v13-CY-Full+Others.csv'))
# vdem13['country_name'] = vdem13['country_name'].replace(vdem_to_geo)
# plot_year(vdem13, 2015, 'v2xcl_dmove', 'Freedom of Movement')
# plot_year(vdem13, 2015, 'v2exthftps', 'Public Sector Theft')
# plot_year(vdem13, 2015, 'v2clrelig', 'Religious Freedom')
# plot_year(vdem13, 2015, 'v2mecenefm', 'Media Censored')

bdm_extras = pd.read_csv(os.path.join(stata_dir, 'CY-DATA-bdm-extras.csv'))
bdm_extras['country_name'] = bdm_extras['country_name'].replace(vdem_to_geo)
# plot_year(bdm_extras, 2015, 'Hygiene')
# plot_year(bdm_extras, 2015, 'FoodConsumption')
# plot_year(bdm_extras, 2015, 'ElectricAccess')
# plot_year(bdm_extras, 2015, 'SecondarySchool')
# plot_year(bdm_extras, 2010, 'Transparencyindex')
# plot_year(bdm_extras, 2015, 'PressFreedom')
# plot_year(bdm_extras, 2015, 'CorruptionTI')

