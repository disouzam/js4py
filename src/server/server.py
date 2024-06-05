'''Serve experimental data.'''

from flask import Flask, render_template, request
from sqlmodel import Session, SQLModel, create_engine, func, select
import sys

from models import Site, Survey, Sample, Staff, Experiment, Performed, Plate, Invalidated


SITE_TITLE = 'Lab Data'
ENGINE = None
FORMAT = 'fmt'

app = Flask(__name__)

@app.route('/')
def index():
    '''Display data server home page.'''
    with Session(ENGINE) as session:
        page_data = {
            'site_title': SITE_TITLE,
            'num_sites': _db_count(session, Site),
            'num_surveys': _db_count(session, Survey),
            'num_samples': _db_count(session, Sample),
            'num_staff': _db_count(session, Staff),
            'num_experiments': _db_count(session, Experiment),
            'num_performed': _db_count(session, Performed),
            'num_plates': _db_count(session, Plate),
            'num_invalidated': _db_count(session, Invalidated),
        }
        return render_template('index.html', **page_data)


@app.route('/sites/')
def sites_index():
    '''Display site details.'''
    return _details(Site, request.args.get(FORMAT))


@app.route('/surveys/')
def surveys_index():
    '''Display site details.'''
    return _details(Survey, request.args.get(FORMAT))


@app.route('/samples/')
def samples_index():
    '''Display site details.'''
    return _details(Sample, request.args.get(FORMAT))


@app.route('/staff/')
def staff_index():
    '''Display site details.'''
    return _details(Staff, request.args.get(FORMAT))


@app.route('/experiment/')
def experiment_index():
    '''Display site details.'''
    return _details(Experiment, request.args.get(FORMAT))


@app.route('/performed/')
def performed_index():
    '''Display site details.'''
    return _details(Performed, request.args.get(FORMAT))


@app.route('/plate/')
def plate_index():
    '''Display site details.'''
    return _details(Plate, request.args.get(FORMAT))


@app.route('/invalidated/')
def invalidated_index():
    '''Display site details.'''
    return _details(Invalidated, request.args.get(FORMAT))


def _db_count(session, table):
    '''Count rows in table.'''
    return session.exec(select(func.count()).select_from(table)).one()


def _details(table, fmt):
    '''Show details of table.'''
    with Session(ENGINE) as session:
        columns = list(table.__fields__.keys())
        records = list(session.exec(select(table)).all())

        if fmt and (fmt == 'json'):
            return [r.model_dump() for r in records]

        rows = [[getattr(r, c) for c in columns] for r in records]
        page_data = {
            'site_title': SITE_TITLE,
            'page_title': table.__name__,
            'columns': columns,
            'rows': rows,
        }
        return render_template('details.html', **page_data)


if __name__ == '__main__':
    dbfile = sys.argv[1]
    ENGINE = create_engine(f'sqlite:///{dbfile}')
    SQLModel.metadata.create_all(ENGINE)
    app.run()
