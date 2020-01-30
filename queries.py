import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from constants import engine
from models import Team, Player, session, Game
from sqlalchemy import func
import datetime as dt
from models import Base
from sqlalchemy.orm import sessionmaker


# Session = sessionmaker(bind=engine)
# session = Session()


# def check_table_exists(table):
#     try:
#         connection = psycopg2.connect(user="andreaserga",
#                                       password="Patrik78",
#                                       host="localhost",
#                                       port="5432",
#                                       dbname="mlb_db")
#
#         cur = connection.cursor()
#
#         query = f'''
#         SELECT EXISTS (
#         SELECT 1
#         FROM   information_schema.tables
#         WHERE  table_schema = 'public'
#         AND    table_name = '{table}');'''
#
#         cur.execute(query)
#         return cur.fetchone()[0]
#
#     except (Exception, psycopg2.Error) as error:
#         print(error)
#         return False
#
#     finally:
#         # closing database connection.
#         if (connection):
#             cur.close()
#             connection.close()

def insert_data(df, table, replace_append='append'):
    #print(df.columns)
    mapped_table = eval(table.capitalize())
    try:
        session.bulk_insert_mappings(mapped_table, df.to_dict(orient='records'))
        session.commit()
        print(f'{table} created')
    except Exception as ex:
        print(f'Error {ex} when inserting table {table}')


def check_last_update(table, is_roster=False):
    if is_roster:
        last_update = session.query(func.max(table.updated)).scalar()
    else:
        last_update = session.query(func.max(table.gamedate)).scalar()
    # print(f'fra check update: {last_update}')
    print(f'{table} last update: {last_update}')
    session.commit()
    return last_update

def get_data(tableAndCol, all=True):
    if all:
        data = session.query(tableAndCol).filter(Game.gamedate == dt.date(2019,7,30)).all()
        session.commit()
        return data

