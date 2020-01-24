import psycopg2
import sqlalchemy
import pandas as pd
from constants import engine
from models import Teams, Rosters, session
from sqlalchemy import func


def check_table_exists(table):
    try:
        connection = psycopg2.connect(user="andreaserga",
                                      password="Patrik78",
                                      host="localhost",
                                      port="5432",
                                      dbname="mlb_db")

        cur = connection.cursor()

        query = f'''
        SELECT EXISTS (
        SELECT 1
        FROM   information_schema.tables 
        WHERE  table_schema = 'public'
        AND    table_name = '{table}');'''

        cur.execute(query)
        return cur.fetchone()[0]

    except (Exception, psycopg2.Error) as error:
        print(error)
        return False

    finally:
        # closing database connection.
        if (connection):
            cur.close()
            connection.close()

def insert_data(df, table, replace=False):
    try:
        if replace:
            df.to_sql(table, engine, if_exists='replace')
            print(f'{table} created')
        else:
            df.to_sql(table, engine, if_exists='append')
            print(f'{table} updated')
    except Exception as ex:
        print(f'Error {ex} when inserting table {table}')



def check_last_update(table, is_roster=False):
    return session.query(func.max(table.updated)).scalar()

