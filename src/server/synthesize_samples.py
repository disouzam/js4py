'''Generate sample snails with genomes and locations.'''


import argparse
import json
from pathlib import Path
import pandas as pd
import random
import sys

from geopy.distance import lonlat, distance


CIRCLE = 360.0
LON_LAT_PRECISION = 5
READING_PRECISION = 1
MIN_SNAIL_SIZE = 0.5
MAX_SNAIL_SIZE = 5.0
SNAIL_PRECISION = 1


def main():
    '''Main driver.'''
    options = parse_args()
    random.seed(options.seed)
    genomes = json.loads(Path(options.genomes).read_text())
    geo_params = get_geo_params(options)
    samples = generate_samples(options, genomes, geo_params)
    save(options, samples)


def generate_samples(options, genomes, geo_params):
    '''Generate snail samples.'''
    samples = []
    for sequence in genomes['individuals']:
        point, scale = random_geo(geo_params)
        if sequence[genomes['susceptible_loc']] == genomes['susceptible_base']:
            limit = options.mutant
        else:
            limit = options.normal
        reading = random.uniform(
            MIN_SNAIL_SIZE, MIN_SNAIL_SIZE + MAX_SNAIL_SIZE * limit * scale
        )
        samples.append((point.longitude, point.latitude, sequence, reading))

    df = pd.DataFrame(samples, columns=('lon', 'lat', 'sequence', 'reading'))
    df['lon'] = df['lon'].round(LON_LAT_PRECISION)
    df['lat'] = df['lat'].round(LON_LAT_PRECISION)
    df['reading'] = df['reading'].round(SNAIL_PRECISION)

    return df


def get_geo_params(options):
    '''Get geographic parameters.'''
    sites = pd.read_csv(Path(options.sites))
    surveys = pd.read_csv(Path(options.surveys))
    return sites.merge(surveys, how='inner', on='site')


def parse_args():
    '''Parse command-line arguments.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--genomes', type=str, required=True, help='genome file')
    parser.add_argument(
        '--mutant', type=float, help='scaling factor for mutant genomes'
    )
    parser.add_argument(
        '--normal', type=float, help='scaling factor for normal genomes'
    )
    parser.add_argument('--outfile', type=str, help='output file')
    parser.add_argument('--sites', type=str, required=True, help='sites data file')
    parser.add_argument('--seed', type=int, required=True, help='RNG seed')
    parser.add_argument('--surveys', type=str, required=True, help='surveys data file')
    return parser.parse_args()


def random_geo(geo_params):
    '''Generate random geo point within radius of center of randomly-chosen site.'''
    row = random.randrange(geo_params.shape[0])
    center = lonlat(float(geo_params.at[row, 'lon']), float(geo_params.at[row, 'lat']))
    radius = float(geo_params.at[row, 'radius'])
    dist = random.random() * float(geo_params.at[row, 'radius'])
    bearing = random.random() * CIRCLE
    scale = dist / radius
    return distance(kilometers=dist).destination((center), bearing=bearing), scale


def save(options, samples):
    '''Save or show results.'''
    if options.outfile:
        Path(options.outfile).write_text(samples.to_csv(index=False))
    else:
        print(samples.to_csv(index=False))


if __name__ == '__main__':
    main()
