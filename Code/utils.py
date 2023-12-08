
import csv
import json
import logging
import os
import requests
from tqdm import tqdm
from typing import Dict
from urllib.parse import (
    urlencode, unquote, urlparse, parse_qsl, ParseResult
)

import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_dir = os.path.join(BASE_DIR, 'Data')
code_dir = os.path.join(BASE_DIR, 'Code')
stata_dir = os.path.join(BASE_DIR, 'Stata')
viz_dir = os.path.join(BASE_DIR, 'Visuals')

asjp_clean_fn = os.path.join(data_dir, 'asjp_db.csv')
asjp_subset_fn = os.path.join(data_dir, 'asjp_subset.csv')
ldnd_db_fn = os.path.join(data_dir, 'Lang_Resemblance.csv')

# ASJP 40 can be found in: https://asjp.clld.org/static/Guidelines.pdf
asjp_40 = """blood
fish
mountain
star
bone
full
name
stone
breast
hand
new
sun
come
hear
night
tongue
die
horn
nose
tooth
dog
I
one
tree
drink
knee
path
two
ear
leaf
person
water
eye
liver
see
we
fire
louse
skin
you""".split('\n')

country_groups = """World
Africa Eastern and Southern
Africa Western and Central
Arab World
Caribbean small states
Central Europe and the Baltics
East Asia & Pacific
East Asia & Pacific (excluding high income)
Euro area
Europe & Central Asia
Europe & Central Asia (excluding high income)
East Asia & Pacific (IDA & IBRD countries)
Europe & Central Asia (IDA & IBRD countries)
European Union
Fragile and conflict affected situations
Heavily indebted poor countries (HI%)
Latin America & Caribbean
Latin America & Caribbean (excluding high income)
Least developed countries: UN classification
Middle East & North Africa
Middle East & North Africa (excluding high income)
North America
OECD members
Other small states
Pacific island small states
Small states
South Asia
Sub-Saharan Africa
Sub-Saharan Africa (excluding high income)
Sub-Saharan Africa (IDA & IBRD countries)
Middle East & North Africa (IDA & IBRD countries)
High income
Low & middle income
Low income
Lower middle income
Middle income
Upper middle income
Early-demographic dividend
Heavily indebted poor countries (HIPC)
IBRD only
IDA & IBRD total
IDA blend
IDA only
IDA total
Late-demographic dividend
Latin America & the Caribbean (IDA & IBRD countries)
Post-demographic dividend
Pre-demographic dividend
South Asia (IDA & IBRD)""".split('\n')
not_countries = set(country_groups)

def add_url_params(url: str, params: Dict):
    """Add GET params to provided URL being aware of existing.

    Parameters
    ----------
    url : str
        string of target URL
    params : _type_
        dict containing requested params to be added.
        The values should _not_ be URL-encoded, since they will be
        encoded by this function

    Example
    -------
    ```py
    >> url = 'http://stackoverflow.com/test?answers=true'
    >> new_params = {'answers': False, 'data': ['some','values']}
    >> add_url_params(url, new_params)
    'http://stackoverflow.com/test?data=some&data=values&answers=false'
    ```

    Reference
    -----------
    https://stackoverflow.com/a/25580545/6739891

    Returns
    -------
    str
        final URL
    """

    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    # Merging URL arguments dict with new params
    parsed_get_args.update(params)

    # Bool and dict values should be converted to json-friendly values
    # you may throw this part away if you don't like it :)
    parsed_get_args.update(
        {k: json.dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
    )

    # Converting URL argument to proper query string
    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url



def get_wb_data(url):
    """ Get and concatenate paginated data from the World Bank

    Reference
    ---------
    https://datahelpdesk.worldbank.org/knowledgebase/articles/898581
    """
    page = 1
    total_pages = None
    joined_data = []
    url = add_url_params(url, {'per_page': 1000, 'format': 'JSON'})
    logger = logging.getLogger('downloads')

    progress_bar = tqdm(
        1, unit='pages',
        disable=not logger.isEnabledFor(logging.DEBUG),
    ) # type: ignore

    #      first loop     or   we're still receiving stuff
    while total_pages is None or page <= total_pages:
        response = requests.get(
            add_url_params(url, {'page': page})
        )

        data = response.json()
        joined_data.extend(data[1])
        page += 1

        if total_pages is None:
            total_pages = data[0]['pages']
            progress_bar.reset(total=total_pages)

        progress_bar.update(1)

    return joined_data

def download_db_data(indicator, output_file):

    logger = logging.getLogger('downloads')
    logger.debug(f'Downloading {indicator}')

    output_file = os.path.join(data_dir, output_file)
    wb_data = get_wb_data(f'http://api.worldbank.org/v2/country/all/indicator/{indicator}')

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(
            csvfile,
            fieldnames=['country_id', 'country_name', 'year', indicator],
        )
        csvwriter.writeheader()

        for obj in wb_data:
            if obj['value'] is None or obj['country']['value'] in not_countries:
                continue
            csvwriter.writerow({
                'country_id': obj['countryiso3code'],
                'country_name': obj['country']['value'],
                'year': obj['date'],
                indicator: obj['value'],
            })


def compare_values(df1: pd.DataFrame, df2: pd.DataFrame, col: str):
    df1_c = set(df1[col])
    df2_c = set(df2[col])

    print('Found in df1 but not in df2:', len(df1_c - df2_c))
    # print(sorted(df1_c - df2_c))
    print('New size of DF1', len(df1[df1[col].isin(df2_c)]))

    print('Found in df2 but not in df1:', len(df2_c - df1_c))
    # print(sorted(df2_c - df1_c))


cat2out = {
    'EndogPublicGoods':  {
        'PublicGood',   'GoodsRatio',  'PrivateorPublicGoods',
        'EliteWantCommonGood',  'PublicWantCommonGood',},
    'KeyPublicGoods':  {
        'TransparentLaws',  'JudicialIndep',  'FreeExpression', },
    'EndogCorruptions':  {
        'Corruption',  'ExecutiveCorrupt',  'PublicSectorTheft',
        'Clientelism',  'CorruptionTI',},
    'KeyCorruptions':  {
        'StateOwnsEconomy',  'JudgeCorrupt', },
    'Freedoms':  {
        'RespectConstitution',  'RuleofLaw',  'FreeElections',  'FreeMovement',
        'CivilLiberties',  'PolRights',  'ReligiousFreedom',  'PropertyRights', },
    'Abuse':  {
        'MediaCensored',  'PackCourts',  'Torture',  'SlaveLabor', },
    'EndogPublicEducation':  {
        'CampusFree',  'AcademicFreedom',  'EducExpend',  'SecondarySchool', },
    'OtherMeasures':  {
        'InfantMortality',  'HealthCare',  'LifeExpect',  'Vaccination',
        'CleanWater',  'Hygiene',  'HealthExpend',  'FoodConsumption',
        'ElectricAccess',  'Transparency',  'PressFreedom', },
}

out2cat: dict[str, str] = {}
for cat, outs in cat2out.items():
    out2cat.update({ out: cat for out in outs })

positive_outcomes = [
    'PublicGood',
    'GoodsRatio',
    'PrivateorPublicGoods',
    'EliteWantCommonGood',
    'PublicWantCommonGood',
    'TransparentLaws',
    'JudicialIndep',
    'FreeExpression',
    'CorruptionTI', #
    'RespectConstitution',
    'RuleofLaw',
    'FreeElections',
    'FreeMovement',
    'CivilLiberties',
    'PolRights',
    'ReligiousFreedom',
    'PropertyRights',
    'MediaCensored', # v2mecenefm
    'CampusFree',
    'AcademicFreedom',
    'EducExpend',
    'SecondarySchool',
    'HealthCare',
    'LifeExpect',
    'Vaccination',
    'CleanWater',
    'Hygiene',
    'HealthExpend',
    'FoodConsumption',
    'ElectricAccess',
    'Transparency',
]

negative_outcomes = [
    'StateOwnsEconomy',
    'Corruption',
    'ExecutiveCorrupt',
    'PublicSectorTheft',
    'Clientelism',
    'JudgeCorrupt',
    'Torture',
    'SlaveLabor',
    'PackCourts',
    'InfantMortality',
    'PressFreedom',
]

all_outcomes = positive_outcomes + negative_outcomes

democracies = [
    'W4', 'W_old',
    'support', 'normpolity', 'Dem6', 'e_boix_regime', 'Przeworski',
    'gwf_party', 'gwf_military', 'gwf_monarchy', 'gwf_personal', 'gwf_demo',
]

costs_raw = [
    'l_pwd_a', 'l_pwd_g', 'l_pwd_m', 'wb_urbpop',
    'Elr', 'Epr', 'Err', 'Egr',
    'e_peaveduc'
]

costs = [
    'ln_pwd_a', 'ln_pwd_g', 'ln_pwd_m', 'wb_urbpop',
    'l_res_norm', 'p_res_norm', 'r_res_norm', 'g_res_norm',
    'e_peaveduc'
]


# democracies = {
#     'W4': (pd.qcut, {'q': 4}),
#     'support': (pd.qcut, {'q': 4}),
#     'W_old': (pd.qcut, {'q': 4}),
#     'normpolity': (pd.qcut, {'q': 4}),
#     'Dem6': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
#     'e_boix_regime': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
#     'Przeworski': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
#     'gwf_party': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
#     'gwf_military': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
#     'gwf_monarchy': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
#     'gwf_personal': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
#     'gwf_demo': (pd.cut, {'bins': 4}), # throws "Bin edges must be unique" otherwise
# }
