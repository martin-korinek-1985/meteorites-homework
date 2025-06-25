#!/usr/bin/env python3

# IDE: PyCharm 2025.1.2 (Community Edition)
# Interpreter: Python 3.13
# Author: martin.korinek2@dhl.com
# Date: 2025-06-25


import json

import pandas

input_file_name = 'Meteorite-Landings.json'

print('Reading file:', input_file_name)
with open(input_file_name, 'r', encoding='utf-8') as input_file:
    input_data = input_file.read()
    print('Parsing input data.')
    json_data = json.loads(input_data.replace('\\', '\\\\'))
    data_frame = pandas.DataFrame(json_data[1])

print(f'There are {data_frame.size - 1} entries in the dataset.')
