import os

import pandas as pd

from utils import data_dir, ldnd_db_fn

lang_r_db = pd.read_csv(ldnd_db_fn, keep_default_na=False, na_values=['_'])
lang_r_db.set_index('l2id', inplace=True)


# epr_ed = pd.read_csv(os.path.join(data_dir, 'EPR-ED-2021.csv'))
# gwid = epr_ed['gwid']
# epr_ed.groupby('gwid')

# pd.DataFrame(gwid, columns=['gwid'])

epr_core = pd.read_csv(os.path.join(data_dir, 'EPR-Core-2021.csv'))

# Exclude the excluded groups
# epr_core = epr_core[~epr_core['status'].isin(['DISCRIMINATED', 'SELF-EXCLUSION'])]

def calc_E_r(group: pd.DataFrame):
    """Calculate Expected Resemblance
    """
    uncat_size = 1 - group['size'].sum() # Size of Uncategorized ethnicities
    if uncat_size > 0.05:
        # 'gwid', 'statename', 'from', 'to', 'group', 'groupid', 'gwgroupid', 'umbrella', 'size', 'status'
        new_row_data = [
            group['gwid'].iloc[0],
            group['statename'].iloc[0],
            group['from'].iloc[0],
            group['to'].iloc[0],
            'UNCATEGORIZED',
            0, # groupid
            0, # gwgroupid
            None,
            uncat_size,
            'POWERLESS',
            None,
        ]
        new_row = pd.DataFrame([new_row_data], columns=group.columns)
        group = pd.concat([group, new_row])

    return group

epr_r = epr_core.groupby(['gwid', 'from', 'to']).apply(calc_E_r)

epr_r.to_csv(os.path.join(data_dir, 'Try1.csv'))
