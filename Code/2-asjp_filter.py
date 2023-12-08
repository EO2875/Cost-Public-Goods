"""
We do not need the entire ASJP database. We filter out:
- Repeated languages. Ex: Spanish and Spanish 2.
- Languages not found in the EPR Ethnic Dimensions
- Words outside the ASJP-40 list.
"""
from itertools import combinations
import os

import pandas as pd

from utils import data_dir, asjp_clean_fn, asjp_40, asjp_subset_fn, ldnd_db_fn


asjp_full = pd.read_csv(asjp_clean_fn, keep_default_na=False, na_values=['_'])
# len(asjp_full) == 537_342

def drop_repeated_langs(df: pd.DataFrame):
    """ The ASJP has repeated languages. Ex: Spanish and Spanish 2.
    We keep only the first one that appears in the database. """
    # TODO: check that it's still the same number of languages
    langs = df.drop_duplicates(subset=['LangCode'])['LangName']
    return df[df['LangName'].isin(langs)]

asjp = drop_repeated_langs(asjp_full)

# all_langcodes = asjp.drop_duplicates(subset=['LangCode'])['LangCode']

epr_ed = pd.read_csv(os.path.join(data_dir, 'EPR-ED-2021.csv'))
epr_ed.set_index('gwgroupid', inplace=True)
# All languages found in EPR-ED
ed_langs = pd.concat([epr_ed['language1'], epr_ed['language2'], epr_ed['language3']])
ed_langs = ed_langs.unique()

# Subset of ASJP with only languages found in EPR-ED
asjp_subset = asjp[
    # only languages found in EPR-ED
    asjp['LangCode'].isin(ed_langs)
    # only words in the ASJP-40 list
    & asjp['Meaning'].isin(asjp_40)
]
# len(asjp_subset) == 24_879

asjp_subset.to_csv(asjp_subset_fn, index=False)


lang_r_db = pd.DataFrame(columns=['ldnd',])

def group_country_ethn(group: pd.DataFrame):

    langs = set(group['language1']) |  set(group['language2']) | set(group['language3'])
    langs = {l for l in langs if not pd.isna(l) }
    for lang1, lang2 in combinations(langs, 2):
        lang1, lang2 = sorted([lang1, lang2])
        key = f'{lang1},{lang2}'
        lang_r_db.loc[key] = [None]

    return group

epr_ed.groupby('gwid').apply(group_country_ethn)

lang_r_db.to_csv(ldnd_db_fn, index_label='l2id')
