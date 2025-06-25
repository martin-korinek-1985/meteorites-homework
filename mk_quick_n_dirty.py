#!/usr/bin/env python3

# IDE: PyCharm 2025.1.2 (Community Edition)
# Interpreter: Python 3.13
# Author: martin.korinek2@dhl.com
# Date: 2025-06-25

import json
from collections import Counter

input_file_name = 'Meteorite-Landings.json'

print('Reading file:', input_file_name)
with open(input_file_name, 'r', encoding='utf-8') as input_file:
    input_data = input_file.read()
    print('Parsing input data.')
    json_data = json.loads(input_data.replace('\\', '\\\\'))
    meteorite_list = json_data[1]  # select correct list
    meteorite_list = meteorite_list[1:]  # skip first item

print(f'There are {len(meteorite_list)} entries in the dataset.')
del input_data, input_file, input_file_name, json_data

print('Extracting heaviest object and year frequency.')
heaviest_mass = 0
heaviest_name = ''
years = Counter()
for meteorite in meteorite_list:
    if meteorite[1][1] == "'Name'":
        name = meteorite[1][2].replace("'", '')
    else:
        print(f'Extraction of name failed meteorite={meteorite}')
        break

    mass = 0
    if meteorite[5][1] == "'Mass'" and meteorite[5][2][0] == 'Quantity':
        mass = meteorite[5][2][1]
        if meteorite[5][2][2] != "'Grams'":
            print('WARNING: We have multiple units here!')

    if mass > heaviest_mass:
        heaviest_mass = mass
        heaviest_name = name

    if meteorite[7][1] == "'Year'" and meteorite[7][2][0] == 'DateObject':
        year = meteorite[7][2][1][1]
        years.update({year: 1})

most_frequent_year, frequency = years.most_common(1)[0]
print(f'Heaviest object is [{heaviest_name}] with mass of {heaviest_mass:,} grams.')
print(f'Most frequent year in dataset is {most_frequent_year} with {frequency} entries.')
