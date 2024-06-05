#!/usr/bin/env python

'''Generate random plates.'''

import argparse
import csv
import json
from pathlib import Path
import random
import sys

from params import AssayParams, load_params


MODEL = 'Weyland-Yutani 470'
PLATE_HEIGHT = 4
PLATE_WIDTH = 4


def main():
    '''Main driver.'''
    options = parse_args()
    random.seed(options.params.seed)
    create_files(options)


def create_files(options):
    '''Create randomized plate files.'''
    for filename, sample_id, kind in join_assay_data(options):
        make_plate(
            options.params,
            sample_id,
            kind,
            Path(options.designs, filename),
            Path(options.readings, filename),
        )


def generate(params, func):
    '''Make body of plate design or results.'''
    title_row = ['', *[chr(ord('A') + col) for col in range(PLATE_WIDTH)]]
    values = [
        [func(params, make_placement) for col in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]
    labeled = [[str(i + 1), *r] for (i, r) in enumerate(values)]
    return [title_row, *labeled]


def join_assay_data(options):
    '''Get experiment type and plate filename from data.'''
    assays = json.load(open(options.assays, 'r'))
    experiments = {x['sample_id']: x['kind'] for x in assays['experiment']}
    plates = {p['filename']: p['sample_id'] for p in assays['plate']}
    return ((f, plates[f], experiments[plates[f]]) for f in plates)


def make_head(kind, sample_id):
    '''Make head of plate.'''
    return [
        [MODEL, kind, sample_id],
        [],
    ]


def make_placement(kind):
    '''Generate random placement of samples.'''
    placement = [[False for col in range(PLATE_WIDTH)] for row in range(PLATE_HEIGHT)]
    if kind == 'calibration':
        return placement, []
    columns = list(c for c in range(PLATE_WIDTH))
    random.shuffle(columns)
    columns = columns[:PLATE_HEIGHT]
    for r, row in enumerate(placement):
        row[columns[r]] = True
    return placement, columns


def make_plate(params, sample_id, kind, design_file, readings_file):
    '''Generate an entire plate.'''
    placement, sample_locs = make_placement(kind)

    design = [*make_head('design', sample_id), *generate(params, make_treatment)]
    save_csv(design_file, normalize_csv(design))

    readings = [*make_head('readings', sample_id), *generate(params, make_reading)]
    save_csv(readings_file, normalize_csv(readings))


def make_reading(params, treated):
    '''Generate a single plate reading.'''
    mean = params.treated if treated else params.control
    value = max(0.0, random.gauss(mean, params.stdev))
    return f'{value:.02f}'


def make_treatment(params, treated):
    '''Generate a single plate treatment.'''
    return params.treatment if treated else random.choice(params.controls)


def normalize_csv(rows):
    required = max(len(r) for r in rows)
    for row in rows:
        row.extend([''] * (required - len(row)))
    return rows


def parse_args():
    '''Parse command-line arguments.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--assays', type=str, required=True, help='assays file')
    parser.add_argument('--designs', type=str, required=True, help='designs directory')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--readings', type=str, required=True, help='readings directory')
    options = parser.parse_args()
    options.params = load_params(AssayParams, options.params)
    return options


def save_csv(filename, rows):
    '''Save as CSV.'''
    if not filename:
        csv.writer(sys.stdout).writerows(rows)
    else:
        csv.writer(open(filename, 'w'), lineterminator='\n').writerows(rows)


if __name__ == '__main__':
    main()
