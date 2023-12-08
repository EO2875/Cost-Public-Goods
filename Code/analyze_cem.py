import os

from cem.match import match
from cem.imbalance import L1
import numpy as np
import pandas as pd
import statsmodels.api as sm

from utils import stata_dir, all_outcomes, negative_outcomes

database = pd.read_csv(os.path.join(stata_dir, 'Full_Database.csv'))

database['l_pwd_a'] = np.log(database['PWD_A'])
database['l_pwd_g'] = np.log(database['PWD_G'])
database['l_pwd_m'] = np.log(database['PWD_M'])


pop_densities = {
    'l_pwd_a': (pd.qcut, {'q': 4}),
    'l_pwd_g': (pd.qcut, {'q': 4}),
    'l_pwd_m': (pd.qcut, {'q': 4}),
    'wb_urbpop': (pd.cut, {'bins': 4}),
}

resemblances = {
    'Elr': (pd.qcut, {'q': 4}),
    'Epr': (pd.qcut, {'q': 4}),
    'Err': (pd.qcut, {'q': 4}),
    'Egr': (pd.cut, {'bins': 2}), # Most countries have Egr=1
}

educ = {
    'e_peaveduc': (pd.qcut, {'q': 4}),
}

controls = {
    'e_migdppcln': (pd.qcut, {'q': 4}),
    'logpop': (pd.qcut, {'q': 4}),
}

eras = [
    database['year'] <= 1890,
    (1890 < database['year']) & (database['year'] <= 1945),
    (1945 < database['year']) & (database['year'] <= 2000),
    2000 < database['year']
]
database['era'] = np.select(eras, [1,2,3,4])

all_controls = [
    'era',
    *controls.keys(),
    'wb_urbpop',
    list(resemblances.keys())[0],
    # list(democracies.keys())[0],
    list(educ.keys())[0],
]

schema = {
    **pop_densities,
    **resemblances,
    **educ,
    **controls,
}

for c in {*all_controls, *schema.keys(), *all_outcomes}:
    database[c] = pd.to_numeric(database[c])

for d in democracies.keys():
    if len(database['Dem6'].value_counts()) == 2:
        m = 0.5
    else:
        m = database[d].median()

    database[f'{d}_coarse'] = database[d].apply(lambda x: int(x >= m))
    print(d, 'median:', m)

def coarsen(x: pd.Series):
    if x.name in schema:
        return schema[x.name][0](np.array(x), **schema[x.name][1])
    # if x.name == 'year':
    #     return x
    else:
        return x


coarse_db = database.apply(coarsen)

for out in all_outcomes[:1]:
    if out not in database.columns:
        continue

    for d in list(democracies.keys())[:1]:

        treatment = f'{d}_coarse'

        c = [out, *all_controls]
        c.append(treatment)

        db = coarse_db[c] # lean
        valuefull = ~db.isnull().any(axis=1)
        db = db[valuefull]
        y = db[out]
        db = db.drop(columns=[out])

        weights = match(db, treatment)
        print(L1(db, treatment, weights))
        model = sm.WLS(y, sm.add_constant(database[valuefull][c]), weights=weights)
        results = model.fit()
        print(pd.DataFrame({
            'beta': results.params,
            'tvalue': results.tvalues
        }))
