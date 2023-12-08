import os

import pandas as pd

from utils import data_dir


epr_to_vdem = {
    'Belarus (Byelorussia)': 'Belarus',
    'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
    'Burkina Faso (Upper Volta)': 'Burkina Faso',
    'Cambodia (Kampuchea)': 'Cambodia',
    'Czech Republic': 'Czechia',
    'Congo': 'Republic of the Congo',
    'Congo, Democratic Republic of (Zaire)': 'Democratic Republic of the Congo',
    "Cote D'Ivoire": 'Ivory Coast',
    'East Timor': 'Timor-Leste',
    'Iran (Persia)': 'Iran',
    'Italy/Sardinia': 'Italy',
    'Gambia': 'The Gambia',
    'German Federal Republic': 'Germany',
    'Kyrgyz Republic': 'Kyrgyzstan',
    "Korea, People's Republic of": 'North Korea',
    'Korea, Republic of': 'South Korea',
    'Madagascar (Malagasy)': 'Madagascar',
    'Macedonia (FYROM/North Macedonia)': 'North Macedonia',
    'Myanmar (Burma)': 'Burma/Myanmar',
    'Rumania': 'Romania',
    'Russia (Soviet Union)': 'Russia',
    'Sri Lanka (Ceylon)': 'Sri Lanka',
    'Surinam': 'Suriname',
    'Swaziland (Eswatini)': 'Eswatini',
    'Tanzania (Tanganyika)': 'Tanzania',
    'Turkey (Ottoman Empire)': 'Turkey',
    'Vietnam, Democratic Republic of': 'Vietnam', # We disregard Republic of Vietnam
    'Vietnam, Republic of': 'Republic of Vietnam',
    'Yemen (Arab Republic of Yemen)': 'Yemen',
    "Yemen, People's Republic of": 'South Yemen',
    'Zimbabwe (Rhodesia)': 'Zimbabwe',
}

resemblance = pd.read_csv(os.path.join(data_dir, 'Full-Resemblance-ul=0.12-up=0.40-ur=1.00-ug=1.00.csv'))

resemblance = resemblance.drop('gwid', axis=1)
resemblance = resemblance.rename(columns={'statename': 'country_name'})
resemblance['country_name'] = resemblance['country_name'].replace(epr_to_vdem)

resemblance.to_csv(os.path.join(data_dir, 'CY-DATA-Resemblance.csv'))


