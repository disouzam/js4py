'''Serve experimental data.'''

from datetime import date as date_type
from flask import Flask, render_template
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, func, select
import sys


SITE_TITLE = 'Lab Data'


dbfile = sys.argv[1]
engine = create_engine(f'sqlite:///{dbfile}')
SQLModel.metadata.create_all(engine)


class Sites(SQLModel, table=True):
    '''Survey sites.'''
    site_id: str = Field(primary_key=True)
    lon: float
    lat: float
    surveys: list['Surveys'] = Relationship(back_populates='site_id')


class Surveys(SQLModel, table=True):
    '''Surveys conducted.'''
    survey_id: int = Field(primary_key=True)
    date: date_type
    site_id: str = Field(foreign_key='sites.site_id')
    samples: list['Samples'] = Relationship(back_populates='survey_id')


class Samples(SQLModel, table=True):
    '''Individual samples.'''
    sample_id: int = Field(primary_key=True)
    lon: float
    lat: float
    reading: float
    survey_id: str = Field(foreign_key='surveys.survey_id')


class Staff(SQLModel, table=True):
    '''Lab staff.'''
    staff_id: int = Field(primary_key=True)
    personal: str
    family: str
    performed: list['Performed'] = Relationship(back_populates='staff_id')
    invalidated: list['Invalidated'] = Relationship(back_populates='staff_id')


class Experiments(SQLModel, table=True):
    '''Experiments.'''
    exp_id: int = Field(primary_key=True)
    kind: str
    start: date_type
    start: date_type | None
    performed: list['Performed'] = Relationship(back_populates='exp_id')
    plates: list['Plates'] = Relationship(back_populates='exp_id')


class Performed(SQLModel, table=True):
    '''Who did what experiments?'''
    rowid: int = Field(primary_key=True)
    staff_id: int = Field(foreign_key='staff.staff_id')
    exp_id: int = Field(foreign_key='experiments.exp_id')


class Plates(SQLModel, table=True):
    '''What experimental plates do we have?'''
    plate_id: int = Field(primary_key=True)
    exp_id: int = Field(foreign_key='experiments.exp_id')
    exp_date: date_type
    filename: str
    invalidated: list['Invalidated'] = Relationship(back_populates='plate_id')

class Invalidated(SQLModel, table=True):
    '''Which plates have been invalidated?'''
    rowid: int = Field(primary_key=True)
    plate_id: int = Field(foreign_key='plates.plate_id')
    staff_id: int = Field(foreign_key='staff.staff_id')


app = Flask(__name__)

@app.route('/')
def index():
    '''Display data server home page.'''
    with Session(engine) as session:
        page_data = {
            'site_title': SITE_TITLE,
            'num_sites': _db_count(session, Sites),
            'num_surveys': _db_count(session, Surveys),
            'num_samples': _db_count(session, Samples),
            'num_staff': _db_count(session, Staff),
            'num_performed': _db_count(session, Performed),
            'num_plates': _db_count(session, Plates),
            'num_invalidated': _db_count(session, Invalidated),
        }
        return render_template('index.html', **page_data)


def _db_count(session, table):
    '''Count rows in table.'''
    return session.exec(select(func.count()).select_from(table)).one()


if __name__ == '__main__':
    app.run()
