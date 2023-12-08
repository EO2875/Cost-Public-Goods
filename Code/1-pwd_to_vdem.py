
import os

import pandas as pd

from utils import data_dir


pwd00 = pd.read_csv(os.path.join(data_dir, 'PWD_1km_national_CSV', 'PWD_2000_national_1km.csv'))

pwd_to_vdem = {
    'Myanmar': 'Burma/Myanmar',
    'Czech Republic': 'Czechia',
    'Swaziland': 'Eswatini',
    'CIte dIvoire': 'Ivory Coast',
    'Gambia': 'The Gambia',
    'United States': 'United States of America',
    'East Timor': 'Timor-Leste',
    'Macedonia': 'North Macedonia',
    'Republic of Congo': 'Republic of the Congo',
    'Palestina': 'Palestine/West Bank',
}

pwd05 = pd.read_csv(os.path.join(data_dir, 'PWD_1km_national_CSV', 'PWD_2005_national_1km.csv'))
pwd10 = pd.read_csv(os.path.join(data_dir, 'PWD_1km_national_CSV', 'PWD_2010_national_1km.csv'))
pwd15 = pd.read_csv(os.path.join(data_dir, 'PWD_1km_national_CSV', 'PWD_2015_national_1km.csv'))
pwd20 = pd.read_csv(os.path.join(data_dir, 'PWD_1km_national_CSV', 'PWD_2020_national_1km.csv'))

pwd = pd.concat([pwd00, pwd05, pwd10, pwd20], ignore_index=True)
pwd = pwd.reset_index(drop=True)
pwd = pwd.rename(columns={'Name': 'country_name'})
pwd['country_name'] = pwd['country_name'].replace(pwd_to_vdem)
pwd.to_csv('pwd-try-1.csv', index=False)

static_cols = ('ISO','ISO_No','country_name',)

def linear_interpolation(group: pd.DataFrame):
    ymax = group['year'].max()
    ymin = group['year'].min()
    yhav = set(group['year'])
    missing_y = [y for y in range(ymin, ymax) if y not in yhav]

    missing_g = pd.DataFrame({
        'year': missing_y,
        **{
            c: group.iloc[0][c]
            for c in static_cols
        }
    })
    group = pd.concat([group, missing_g], ignore_index=True)
    group = group.sort_values('year')
    group = group.interpolate(
        method='linear',
        axis=0,
    )

    return group

pwd_full = pwd.groupby('country_name').apply(linear_interpolation)

keep_columns = ['Pop','Density','Area','PWD_A','PWD_G','PWD_M']
keep_columns = ['year', 'country_name', *keep_columns]
# keep_columns = pwd_full.columns

pwd_full[keep_columns].to_csv(os.path.join(data_dir, 'CY-DATA-PWD.csv'), index=False)

