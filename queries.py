
from models import session, Game
from sqlalchemy import func
import datetime as dt
from models import Team, Player, session, Game, Gamestat




def insert_data(df, table, replace_append='append'):
    #print(df.columns)
    mapped_table = eval(table.capitalize())
    print(mapped_table)
    try:
        session.bulk_insert_mappings(mapped_table, df.to_dict(orient='records'))
        session.commit()
        print(f'Data insterted into: {table}')
    except Exception as ex:
        print(f'Error {ex} when inserting into table: {table}')


def check_last_update(table, is_roster=False):
    if is_roster:
        last_update = session.query(func.max(table.updated)).scalar()
    else:
        last_update = session.query(func.max(table.gamedate)).scalar()
    session.commit()
    return last_update

def get_data(tableAndCol, all=True):
    if all:
        data = session.query(tableAndCol).filter(Game.gamedate == dt.date(2019,7,30)).all()
        #session.commit()
        return data

