#!/usr/bin/env python3

# IDE: PyCharm 2025.1.2 (Community Edition)
# Interpreter: Python 3.13
# Author: martin.korinek2@dhl.com
# Date: 2025-06-25

import argparse
import json
import traceback
from collections import Counter
from datetime import datetime

import pytz


def log(*print_args):
    timestamp = datetime.now(tz=pytz.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
    print_args = [timestamp] + list(print_args)
    print(*print_args, flush=True)


def debug(*print_args):
    if args.debug:
        log(*print_args)


class Meteorite:
    id: int
    mass: float  # grams
    name: str
    year: int

    def __init__(self, data: list):
        try:
            self.id = int(data[2][2].replace("'", ''))
            self.name = data[1][2].replace("'", '')

            self.mass = 0
            if data[5][1] == "'Mass'" and data[5][2][0] == 'Quantity':
                self.mass = data[5][2][1]

            self.year = 0
            if data[7][1] == "'Year'" and data[7][2][0] == 'DateObject':
                self.year = data[7][2][1][1]
        except Exception as e:
            log(f'Traceback:\n{traceback.format_exc()}')
            raise Exception(f'{self.__class__.__name__}.{self.__init__.__name__} failed with with Exception={e}')

    def __str__(self):
        return f'<{self.__class__.__name__} "{self.name}" Year={self.year} ID={self.id} Mass={self.mass}g>'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False, description='Earth Meteorite Landings Analysis',
                                     epilog='Without specifying --print-all, --search-id or --search-name\n'
                                            ' 1) parsed meteorite count will be printed\n'
                                            ' 2) name and mass of heaviest object will be printed\n'
                                            ' 3) most frequent year in dataset will be printed',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--file', default='Meteorite-Landings.json', type=str, help='file to parse')
    parser.add_argument('--debug', default=False, action='store_true', help='force debug prints')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--print-all', action='store_true', help='print all parsed meteorites')
    group.add_argument('--search-id', type=int, help='print meteorite details by ID')
    group.add_argument('--search-name', type=str, help='print meteorite details by name')
    args, unknown_args = parser.parse_known_args()

    if unknown_args:
        exit(f'ERROR Unknown arguments={unknown_args}')
    debug(f'parse_known_args={args}')
    del group, parser, unknown_args

    debug(f'Reading args.file={args.file}')
    try:
        with open(args.file, 'r', encoding='utf-8') as input_file:
            input_data = input_file.read()
            debug('Parsing input data.')
            json_data = json.loads(input_data.replace('\\', '\\\\'))
            meteorite_list = json_data[1]  # select correct list
            meteorite_list = meteorite_list[1:]  # skip first item
    except Exception as _e:
        log(f'Traceback:\n{traceback.format_exc()}')
        exit(f'ERROR Reading data from file={args.file} failed with Exception={_e}')

    debug('Parsing meteorites data')
    parsed_meteorites = []
    for meteorite_data in meteorite_list:  # skip first item
        try:
            meteorite = Meteorite(data=meteorite_data)
            parsed_meteorites.append(meteorite)
            if args.print_all:
                print(meteorite)
            elif (args.search_id and args.search_id == meteorite.id) or (args.search_name and args.search_name == meteorite.name):
                print(meteorite)
                log(f'Processing completed, meteorite found.')
                exit(0)
        except Exception as _e:
            log(f'ERROR Failed to parse meteorite_data={meteorite_data} with Exception={_e}')

    if args.search_name or args.search_id:
        exit('WARNING Processing completed, meteorite NOT found.')
    else:
        heaviest = parsed_meteorites[0]
        years = Counter()
        for meteorite in parsed_meteorites:
            if meteorite.mass > heaviest.mass:
                heaviest = meteorite
            years.update({meteorite.year: 1})
        most_frequent_year, frequency = years.most_common(1)[0]

        print(f'1) There are {len(parsed_meteorites)} entries in the dataset.')
        print(f'2) Heaviest object is [{heaviest.name}] with mass of {heaviest.mass:,} grams.')
        print(f'3) Most frequent year in dataset is {most_frequent_year} with {frequency} entries.')
