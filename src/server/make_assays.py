'''Initialize database with previous experimental data.'''

import argparse
from datetime import date, datetime, timedelta
import json
from pathlib import Path
import random
import string

from faker import Faker

from params import AssayParams, load_params

EXPERIMENTS = {
    'calibration': {'staff': [1, 1], 'duration': [0, 0], 'plates': [1, 1]},
    'trial': {'staff': [1, 2], 'duration': [1, 2], 'plates': [2, 16]},
}
FILENAME_LENGTH = 8


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()


def main():
    '''Main driver.'''
    options = parse_args()
    random.seed(options.params.seed)
    fake = Faker(options.params.locale)
    result = {
        'staff': make_staff(options.params, fake),
        **make_experiments(options.params, fake)
    }
    save(options.outfile, result)


def make_experiments(params, fake):
    '''Create experiments and their data.'''
    kinds = list(EXPERIMENTS.keys())
    staff_ids = list(range(1, params.staff + 1))
    experiments = []
    performed = []
    plates = []

    random_filename = make_random_filename()
    for experiment_id in range(1, params.experiments + 1):
        kind = random.choice(kinds)

        started, ended = random_experiment_duration(params, kind)
        experiments.append(
            {'exp_id': experiment_id, 'kind': kind, 'start': round_date(started), 'end': round_date(ended)}
        )

        num_staff = random.randint(*EXPERIMENTS[kind]['staff'])
        performed.extend(
            [{'staff_id': s, 'exp_id': experiment_id} for s in random.sample(staff_ids, num_staff)]
        )

        if ended is not None:
            plates.extend(
                random_plates(params, kind, experiment_id, started, random_filename)
            )

    invalidated = invalidate_plates(params, plates)

    return {
        'experiments': experiments,
        'performed': performed,
        'plates': plates,
        'invalidated': invalidated
    }


def make_staff(params, fake):
    '''Create people.'''
    return [
        {'staff_id': i, 'personal': fake.first_name(), 'family': fake.last_name()}
        for i in range(params.staff)
    ]


def invalidate_plates(params, plates):
    '''Invalidate a random set of plates.'''
    selected = [
        (i, p['exp_date']) for (i, p) in enumerate(plates) if random.random() < params.invalid
    ]
    return [
        {
            'plate_id': plate_id,
            'staff_id': random.randint(1, params.staff + 1),
            'date': random_date_interval(exp_date, params.enddate),
        }
        for (plate_id, exp_date) in selected
    ]


def make_random_filename():
    '''Create a random filename generator.'''
    filenames = set([''])
    result = ''
    while True:
        while result in filenames:
            stem = ''.join(random.choices(string.hexdigits, k=FILENAME_LENGTH)).lower()
            result = f'{stem}.csv'
        filenames.add(result)
        yield result


def parse_args():
    '''Parse command-line arguments.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--outfile', type=str, default=None, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    options = parser.parse_args()
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(AssayParams, options.params)
    return options


def random_experiment_duration(params, kind):
    '''Choose random start date and end date for experiment.'''
    start = random.uniform(params.startdate.timestamp(), params.enddate.timestamp())
    start = datetime.fromtimestamp(start)
    duration = timedelta(days=random.randint(*EXPERIMENTS[kind]['duration']))
    end = start + duration
    end = None if end > params.enddate else end
    return start, end


def random_plates(params, kind, experiment_id, start_date, random_filename):
    '''Generate random plate data.'''
    return [
        {
            'plate_id': i + 1,
            'exp_id': experiment_id,
            'exp_date': random_date_interval(start_date, params.enddate),
            'filename': next(random_filename),
        }
        for i in range(random.randint(*EXPERIMENTS[kind]['plates']))
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
