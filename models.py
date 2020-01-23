import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://andreaserga:Patrik78@localhost:5432/mlb_db')
Session = sessionmaker(bind=engine)
session = Session()




Base = declarative_base()

class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    teamcode = Column(String)
    abbreviation = Column(String)
    shortname = Column(String)
    division_id = Column(Integer)
    division_name = Column(String)
    league_id = Column(Integer)
    league_name = Column(String)
    sport_id = Column(Integer)
    sport_name = Column(String)
    springleague_id = Column(Integer)
    springleague_name = Column(String)
    venue_id = Column(Integer)
    venue_name = Column(String)
    venue_link = Column(String)

class Rosters(Base):
    __tablename__ = 'rosters'
    id = Column(Integer, primary_key=True)
    jerseynumber = Column(Integer)
    parentteamid = Column(Integer)
    person_id = Column(Integer)
    person_fullname = Column(String)
    person_link = Column(String)
    position_code = Column(Integer)
    position_name = Column(String)
    position_type = Column(String)
    position_abbreviation = Column(String)
    status_code = Column(String)
    status_description = Column(String)
    team_id = Column(Integer)
    updated = Column(DateTime)






