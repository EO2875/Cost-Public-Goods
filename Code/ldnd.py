"""
There are 692 languages in EPR-ED. This amounts to (692 C 2) = 239086
combinations, which is a bit too much. Instead of calculating all possible
language pairs, we resolve it on the spot and cache the result.
"""
import json
import os

import Levenshtein
import pandas as pd

from utils import ldnd_db_fn, asjp_subset_fn, data_dir


class NoLang(Exception):
    msg = '{lang} is not in the database.'
    def __init__(self, lang) -> None:
        self.lang = lang
        super().__init__([self.msg.format(lang=lang)])


class BadLang(NoLang):
    msg = '{lang} has less than 40 words!'


def LDN(s1, s2):
    """ Normalized Levenshtein distance """
    return Levenshtein.distance(s1, s2) / max(len(s1), len(s2))

def _LDND_lambda(l1, l2):
    N = len(l1)
    assert N == len(l2)
    return sum(LDN(l1[i], l2[i]) for i in range(N)) / N

def _LDND_gamma(l1, l2):
    N = len(l1)
    assert N == len(l2)
    S = sum(
        sum(LDN(l1[i], l2[j]) for j in range(N) if j != i )
        for i in range(N)
    )
    return S / (N * (N - 1))


def calculate_ldnd(l1, l2):
    """ Calculate the LDND distance between two languages.
    Can be an expensive calculation.

    Parameters
    ----------
    l1 : Sequence[str]
        List with all words from first language.
    l2 : Sequence[str]
        List with all words from second language.

    Returns
    -------
    float
        LDND distance.
    """
    return _LDND_lambda(l1, l2) / _LDND_gamma(l1, l2)

lang_r_db = pd.read_csv(ldnd_db_fn)
lang_r_db.set_index('l2id', inplace=True)

# TODO - Na values may be XXX
asjp = pd.read_csv(asjp_subset_fn, keep_default_na=False, na_values=['_'])

def save_ldnd():
    lang_r_db.to_csv(ldnd_db_fn)

def get_ldnd(langcode1, langcode2):
    # Order alphabetically
    langcode1, langcode2 = sorted([langcode1, langcode2])
    key = f'{langcode1},{langcode2}'

    if key in lang_r_db.index:
        return lang_r_db.loc[key]['ldnd']

    l1 = list(asjp[asjp['LangCode'] == langcode1]['Word'])
    l2 = list(asjp[asjp['LangCode'] == langcode2]['Word'])
    if len(l1) == 0:
        raise NoLang(l1)
    if len(l2) == 0:
        raise NoLang(l2)
    if len(l1) != 40:
        raise BadLang(l1)
    if len(l2) != 40:
        raise BadLang(l2)

    r = calculate_ldnd(l1, l2)
    lang_r_db.loc[key] = r
    return r

def calculate_ling_resem():
    d = lang_r_db['ldnd'].max() - lang_r_db['ldnd'].min()
    lang_r_db['ling_resem'] = 1 - (lang_r_db['ldnd'] - lang_r_db['ldnd'].min()) / d

def get_ling_resem(langcode1, langcode2):
    if langcode1 == langcode2:
        return 1

    langcode1, langcode2 = sorted([langcode1, langcode2])
    key = f'{langcode1},{langcode2}'

    try:
        return lang_r_db.loc[key]['ling_resem']
    except KeyError as e:
        raise NoLang(key) from e
