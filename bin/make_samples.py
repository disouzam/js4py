'''Generate sample snails with genomes and locations.'''


import argparse
import json
from pathlib import Path
import pandas as pd
import random

from geopy.distance import lonlat, distance

from params import SampleParams, load_params


CIRCLE = 360.0
LON_LAT_PRECISION = 5
READING_PRECISION = 1
MIN_SNAIL_SIZE = 0.5
MAX_SNAIL_SIZE = 5.0
SNAIL_PRECISION = 1


def main():
    '''Main driver.'''
    options = parse_args()
    random.seed(options.params.seed)
    genomes = json.loads(Path(options.genomes).read_text())
    geo_params = get_geo_params(options)
    samples = generate_samples(options, genomes, geo_params)
    save(options, samples)


def generate_samples(options, genomes, geo_params):
    '''Generate snail samples.'''
    samples = []
    for i, sequence in enumerate(genomes['individuals']):
        survey_id, point, scale = random_geo(geo_params)
        if sequence[genomes['susceptible_loc']] == genomes['susceptible_base']:
            limit = options.params.mutant
        else:
            limit = options.params.normal
        reading = random.uniform(
            MIN_SNAIL_SIZE, MIN_SNAIL_SIZE + MAX_SNAIL_SIZE * limit * scale
        )
        samples.append((i + 1, survey_id, point.longitude, point.latitude, sequence, reading))

    df = pd.DataFrame(samples, columns=('sample_id', 'survey_id', 'lon', 'lat', 'sequence', 'reading'))
    df['lon'] = df['lon'].round(LON_LAT_PRECISION)
    df['lat'] = df['lat'].round(LON_LAT_PRECISION)
    df['reading'] = df['reading'].round(SNAIL_PRECISION)

    return df


def get_geo_params(options):
    '''Get geographic parameters.'''
    sites = pd.read_csv(Path(options.sites))
    surveys = pd.read_csv(Path(options.surveys))
    return sites.merge(surveys, how='inner', on='site_id')


def parse_args():
    '''Parse command-line arguments.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--genomes', type=str, required=True, help='genome file')
    parser.add_argument('--outfile', type=str, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--sites', type=str, required=True, help='sites parameter file')
    parser.add_argument('--surveys', type=str, required=True, help='surveys parameter file')
    options = parser.parse_args()
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(SampleParams, options.params)
    return options


def random_geo(geo_params):
    '''Generate random geo point within radius of center of randomly-chosen site.'''
    row = random.randrange(geo_params.shape[0])
    survey_id = geo_params.at[row, 'survey_id']
    center = lonlat(float(geo_params.at[row, 'lon']), float(geo_params.at[row, 'lat']))
    radius = float(geo_params.at[row, 'radius'])
    dist = random.random() * float(geo_params.at[row, 'radius'])
    bearing = random.random() * CIRCLE
    scale = dist / radius
    point = distance(kilometers=dist).destination((center), bearing=bearing)
    return survey_id, point, scale


def save(options, samples):
    '''Save or show results.'''
    if options.outfile:
        Path(options.outfile).write_text(samples.to_csv(index=False))
    else:
        print(samples.to_csv(index=False))


if __name__ == '__main__':
    main()
