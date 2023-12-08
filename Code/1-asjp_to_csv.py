"""


The ASJP lists can be found in either of these:
- https://asjp.clld.org/help
- https://zenodo.org/records/7079637

Once the `lexibank/asjp-v20.zip` file has been downloaded, we extract the file
`raw/lists.txt`. We have renamed this file `asjp-lists.txt`. 

`asjp-lists.txt` has a unique format. This program transforms the original
list into a CSV file.
"""

import os
import re
import csv

from utils import data_dir, asjp_clean_fn

asjp_lists = os.path.join(data_dir, 'asjp-lists.txt')

i = 0
title_line = re.compile(r'(\w+)\{.+\}')
lang_code = None
lang_name = None
asjp_database = []
with open(asjp_lists) as list_f, open(asjp_clean_fn, 'w', newline='', encoding='utf-8') as clean_f:
    clean_writer = csv.writer(clean_f)
    clean_writer.writerow(('WordNo', 'Meaning', 'Word', 'LangCode', 'LangName'))

    for line in list_f.readlines():
        i += 1
        if i < 87: # Useless
            continue

        title_match = title_line.match(line)
        if title_match:
            lang_code = None
            lang_name = title_match.group(1)
            continue
        
        if lang_code == None:
            lang_code = line[-4:-1]
            continue

        if not re.compile(r'\d').match(line):
            continue

        no_mean, word = line[:-4].split('\t')
        number, meaning = no_mean.split(' ')
        word_0 = word.split(', ')[0] # There's sometimes multiple words

        clean_writer.writerow((number, meaning, word_0, lang_code, lang_name))
