'''Initialize database with previous experimental data.'''

import argparse
from datetime import date, datetime, timedelta
import json
import pandas as pd
from pathlib import Path
import random
import string

from faker import Faker

from params import AssayParams, load_params


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()


def main():
    '''Main driver.'''
    options = parse_args()
    individuals = make_individuals(options)
    random.seed(options.params.seed)
    fake = Faker(options.params.locale)
    result = {
        'staff': make_staff(options.params, fake),
        **make_experiments(options.params, fake, individuals)
    }
    save(options.outfile, result)


def make_experiments(params, fake, individuals):
    '''Create experiments and their data.'''
    kinds = list(params.experiments.keys())
    staff_ids = list(range(1, params.staff + 1))
    experiments = []
    performed = []
    plates = []

    random_filename = make_random_filename(params)
    for i, flag in enumerate(individuals):
        sample_id = i + 1
        kind = random.choice(kinds)

        started, ended = random_experiment_duration(params, kind)
        experiments.append(
            {'sample_id': sample_id, 'kind': kind, 'start': round_date(started), 'end': round_date(ended)}
        )

        num_staff = random.randint(*params.experiments[kind]['staff'])
        performed.extend(
            [{'staff_id': s, 'sample_id': sample_id} for s in random.sample(staff_ids, num_staff)]
        )

        if ended is not None:
            plates.extend(
                random_plates(params, kind, sample_id, len(plates), started, random_filename)
            )

    invalidated = invalidate_plates(params, plates)

    return {
        'experiment': experiments,
        'performed': performed,
        'plate': plates,
        'invalidated': invalidated
    }


def make_individuals(options):
    '''Re-create individual genomic information.'''
    genomes = json.loads(Path(options.genomes).read_text())
    samples = pd.read_csv(options.samples)
    susceptible_loc = genomes['susceptible_loc']
    susceptible_base = genomes['susceptible_base']
    return [g[susceptible_loc] == susceptible_base for g in samples['sequence']]


def make_staff(params, fake):
    '''Create people.'''
    return [
        {'staff_id': i, 'personal': fake.first_name(), 'family': fake.last_name()}
        for i in range(params.staff)
    ]


def invalidate_plates(params, plates):
    '''Invalidate a random set of plates.'''
    selected = [
        (i, p['date']) for (i, p) in enumerate(plates) if random.random() < params.invalid
    ]
    return [
        {
            'plate_id': plate_id,
            'staff_id': random.randint(1, params.staff + 1),
            'date': random_date_interval(exp_date, params.enddate),
        }
        for (plate_id, exp_date) in selected
    ]


def make_random_filename(params):
    '''Create a random filename generator.'''
    filenames = set([''])
    result = ''
    while True:
        while result in filenames:
            stem = ''.join(random.choices(string.hexdigits, k=params.filename_length)).lower()
            result = f'{stem}.csv'
        filenames.add(result)
        yield result


def parse_args():
    '''Parse command-line arguments.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--genomes', type=str, required=True, help='genome file')
    parser.add_argument('--outfile', type=str, default=None, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--samples', type=str, required=True, help='samples file')
    options = parser.parse_args()
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(AssayParams, options.params)
    return options


def random_experiment_duration(params, kind):
    '''Choose random start date and end date for experiment.'''
    start = random.uniform(params.startdate.timestamp(), params.enddate.timestamp())
    start = datetime.fromtimestamp(start)
    duration = timedelta(days=random.randint(*params.experiments[kind]['duration']))
    end = start + duration
    end = None if end > params.enddate else end
    return start, end


def random_plates(params, kind, sample_id, start_id, start_date, random_filename):
    '''Generate random plate data.'''
    return [
        {
            'plate_id': start_id + i + 1,
            'sample_id': sample_id,
            'date': random_date_interval(start_date, params.enddate),
            'filename': next(random_filename),
        }
        for i in range(random.randint(*params.experiments[kind]['plates']))
    ]


def random_date_interval(start_date, end_date):
    '''Choose a random end date (inclusive).'''
    if isinstance(start_date, date):
        start_date = datetime(*start_date.timetuple()[:3])
    choice = random.uniform(start_date.timestamp(), end_date.timestamp())
    choice = datetime.fromtimestamp(choice)
    return round_date(choice)


def round_date(raw):
    '''Round time to whole day.'''
    return None if raw is None else date(*raw.timetuple()[:3])


def save(outfile, result):
    '''Save or show generated data.'''
    as_text = json.dumps(result, indent=4, cls=DateTimeEncoder)
    if outfile:
        Path(outfile).write_text(as_text)
    else:
        print(as_text)


if __name__ == '__main__':
    main()
