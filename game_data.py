import queries
import datetime as dt
from models import Game
import pandas as pd
from constants import yesterday, today
from fetch import update_played_games


def get_games():
    last_update = queries.check_last_update(Game) if not None else dt.date(2018,1,1)
    print('heheh', last_update)
    for i in range(last_update.year, yesterday.year+1):
        if (i < yesterday.year) and (last_update < dt.date(2019,9,29)):
            print(i)
            dfGames = update_played_games(i, f'{i}-03-15', f'{i}-10-15')
            queries.insert_data(df=dfGames, table='game', replace_append='append')
        elif (i == yesterday.year) and (yesterday > dt.date(2020,3,26)):
            print(i)
            dfGames = update_played_games(i, f'{i}-{last_update.month}-{last_update.day}', yesterday)
            queries.insert_data(df=dfGames, table='game', replace_append='append')
        else:
            print('games up to date')
            return

def update_game_stats():
    last_update = queries.check_last_update(Game) if not None else dt.date(2018, 1, 1)
    print(last_update)
    gamepks = queries.get_data()
    print(gamepks)
    # for url, gamedate in gamepks:
    #     print (url[0])