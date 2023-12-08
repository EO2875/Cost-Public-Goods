import os

import pandas as pd

from utils import data_dir

wb_urbpop = pd.read_csv(os.path.join(data_dir, 'WB_UrbanPopPer.csv'))
# vdem_13 = pd.read_csv(os.path.join(data_dir, 'V-Dem-v13-CY-Full+Others.csv'))


wb_to_vdem = {
    'Gambia, The':'The Gambia',
    'United States':'United States of America',
    'Venezuela, RB':'Venezuela',
    'Ivory Coast':"Cote d'Ivoire",
    'Lao PDR':'Laos',
    'Hong Kong SAR, China':'Hong Kong',
    'Yemen, Rep.':'Yemen',
    'Turkiye':'Turkey',
    'Syrian Arab Republic':'Syria',
    'Czech Republic':'Czechia',
    'Russian Federation':'Russia',
    'Myanmar': 'Burma/Myanmar',
    'Congo, Rep.': 'Republic of the Congo',
    'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
    'Egypt, Arab Rep.': 'Egypt',
    'Iran, Islamic Rep.': 'Iran',
    "Korea, Dem. People's Rep.": 'North Korea',
    'Korea, Rep.': 'South Korea',
    'Kyrgyz Republic': 'Kyrgyzstan',
    'Slovak Republic': 'Slovakia',
    'Viet Nam':'Vietnam',
    'West Bank and Gaza': 'Palestine/West Bank',
}


wb_urbpop = wb_urbpop.drop(columns=['country_id'])
wb_urbpop = wb_urbpop.rename(columns={'SP.URB.TOTL.IN.ZS': 'wb_urbpop'})

wb_urbpop['country_name'] = wb_urbpop['country_name'].replace(wb_to_vdem)

wb_urbpop.to_csv(os.path.join(data_dir, 'CY-DATA-Urbpop.csv'), index=False)

# vdem_13_urbpop = pd.merge(vdem_13, wb_urbpop, how='inner', on=['country_name', 'year'])

# vdem_13_urbpop.to_csv(os.path.join(data_dir, 'VDem_13_urbpop.csv'))

