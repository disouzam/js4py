'''Generate database from data files.'''

import argparse
import json
import pandas as pd
import sqlite3


def main():
    '''Main driver.'''
    options = parse_args()
    con = sqlite3.connect(options.dbfile)

    csv_to_db(con, 'sample', options.samples)
    csv_to_db(con, 'site', options.sites)
    csv_to_db(con, 'survey', options.surveys, 'survey_id', 'site_id', 'date')

    assays = json.load(open(options.assays, 'r'))
    json_to_db(con, assays, 'staff')
    json_to_db(con, assays, 'experiment')
    json_to_db(con, assays, 'performed')
    json_to_db(con, assays, 'plate')
    json_to_db(con, assays, 'invalidated')


def csv_to_db(con, name, source, *columns):
    '''Create table from CSV.'''
    df = pd.read_csv(source)
    if columns:
        df = df[list(columns)]
    df.to_sql(name, con, index=False, if_exists='replace')


def json_to_db(con, data, name):
    '''Create table from JSON.'''
    df = pd.DataFrame(data[name])
    df.to_sql(name, con, index=False, if_exists='replace')


def parse_args():
    '''Parse command-line arguments.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--assays', type=str, required=True, help='assay data file')
    parser.add_argument('--dbfile', type=str, required=True, help='output database file')
    parser.add_argument('--samples', type=str, required=True, help='samples data file')
    parser.add_argument('--sites', type=str, required=True, help='sites parameter file')
    parser.add_argument('--surveys', type=str, required=True, help='surveys parameter file')
    return parser.parse_args()


if __name__ == '__main__':
    main()
