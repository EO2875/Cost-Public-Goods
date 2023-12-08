"""


Each Ethnicity has a unique:
- Ethnicity ID : int
- Status : 
    5 MONOPOLY
    4 DOMINANT
    3 SENIOR PARTNER
    2 JUNIOR PARTNER
    1 POWERLESS
    0 DISCRIMINATED
    - SELF-EXCLUSION
- Religion
- Language
- Phenotype

"""
import pandas as pd

from utils import ldnd_db_fn
from ldnd import get_ldnd, save_ldnd, NoLang

lang_r_db = pd.read_csv(ldnd_db_fn, keep_default_na=False, na_values=['_'])
lang_r_db.set_index('l2id', inplace=True)

missing_langs = []
for i in lang_r_db.index:
    i: str
    lang1, lang2 = i.split(',')
    try:
        get_ldnd(lang1, lang2)
    except NoLang as e:
        missing_langs.append(e.lang)

save_ldnd()
