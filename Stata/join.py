

import os

import pandas as pd

STATA_DIR = os.path.dirname(os.path.abspath(__file__))

vdem_renamed = pd.read_csv(os.path.join(STATA_DIR, 'CY-DATA-V-Dem-13-renames-w4.csv'))

bdm_extras = pd.read_csv(os.path.join(STATA_DIR, 'CY-DATA-bdm-extras.csv')) # Other Democracy Indexes
pwd = pd.read_csv(os.path.join(STATA_DIR, 'CY-DATA-PWD.csv'))
resem = pd.read_csv(os.path.join(STATA_DIR, 'CY-DATA-Resemblance.csv'))
urbpop = pd.read_csv(os.path.join(STATA_DIR, 'CY-DATA-Urbpop.csv'))

together = vdem_renamed

for df in (bdm_extras, pwd, resem, urbpop):
    together = pd.merge(together, df, how='outer', on=['year', 'country_name'])

together.to_csv(os.path.join(STATA_DIR, 'Full_Database.csv'), index=False)

