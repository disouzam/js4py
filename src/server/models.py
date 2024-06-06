'''Lab data models.'''

from datetime import date as date_type
from sqlmodel import Field, Relationship, SQLModel


class ModelWithDate(SQLModel):
    '''Provide uniform date formatting.'''
    class Config:
        json_encoders = {
            date_type: lambda dt: dt.isoformat() if dt is not None else ''
        }


class Site(ModelWithDate, table=True):
    '''Survey sites.'''
    site_id: str = Field(primary_key=True)
    lon: float
    lat: float

    surveys: list['Survey'] = Relationship(back_populates='site')


class Survey(ModelWithDate, table=True):
    '''Surveys conducted.'''
    survey_id: int = Field(primary_key=True)
    site_id: str = Field(foreign_key='site.site_id')
    date: date_type

    site: Site = Relationship(back_populates='surveys')
    samples: list['Sample'] = Relationship(back_populates='survey')


class Sample(ModelWithDate, table=True):
    '''Individual samples.'''
    sample_id: int = Field(primary_key=True)
    survey_id: str = Field(foreign_key='survey.survey_id')
    lon: float
    lat: float
    reading: float

    survey: Survey = Relationship(back_populates='samples')


class Staff(ModelWithDate, table=True):
    '''Lab staff.'''
    staff_id: int = Field(primary_key=True)
    personal: str
    family: str

    performed: list['Performed'] = Relationship(back_populates='staff')
    invalidated: list['Invalidated'] = Relationship(back_populates='staff')


class Experiment(ModelWithDate, table=True):
    '''Experiments.'''
    sample_id: int = Field(primary_key=True)
    kind: str
    start: date_type
    end: date_type | None

    performed: list['Performed'] = Relationship(back_populates='experiment')
    plates: list['Plate'] = Relationship(back_populates='experiment')


class Performed(ModelWithDate, table=True):
    '''Who did what experiments?'''
    staff_id: int = Field(foreign_key='staff.staff_id')
    sample_id: int = Field(foreign_key='experiment.sample_id')

    rowid: int = Field(primary_key=True)
    staff: Staff = Relationship(back_populates='performed')
    experiment: Experiment = Relationship(back_populates='performed')


class Plate(ModelWithDate, table=True):
    '''What experimental plates do we have?'''
    plate_id: int = Field(primary_key=True)
    sample_id: int = Field(foreign_key='experiment.sample_id')
    date: date_type
    filename: str

    experiment: Experiment = Relationship(back_populates='plates')
    invalidated: list['Invalidated'] = Relationship(back_populates='plate')


class Invalidated(ModelWithDate, table=True):
    '''Which plates have been invalidated?'''
    plate_id: int = Field(foreign_key='plate.plate_id')
    staff_id: int = Field(foreign_key='staff.staff_id')
    date: date_type

    rowid: int = Field(primary_key=True)
    plate: Plate = Relationship(back_populates='invalidated')
    staff: Staff = Relationship(back_populates='invalidated')
