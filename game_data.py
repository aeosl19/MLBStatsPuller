import queries
import datetime as dt
import pandas as pd
import re
from pandas.io.json import json_normalize
from models import session, Gamestat, Game
from constants import yesterday, today
from fetch import update_played_games, get_data


def get_games():
    last_update = queries.check_last_update(Game)
    print(last_update)
    if last_update == None: last_update = dt.date(2018, 1, 1)
    print(f'Games last_update: {last_update}')
    for i in range(last_update.year, yesterday.year + 1):
        print(i)
        if (i < yesterday.year):
            dfGames = update_played_games(i, f'{i}-01-01', f'{i}-10-15')
            queries.insert_data(df=dfGames, table='game', replace_append='append')

        elif (i == yesterday.year) and (yesterday > dt.date(2020, 3, 26)):
            fromDate = last_update + dt.timedelta(days=1)
            dfGames = update_played_games(i, f'{i}-{fromDate.month}-{fromDate.day}', yesterday)
            queries.insert_data(df=dfGames, table='game', replace_append='append')

        else:
            print('games up to date')
            return


def get_game_stats(game_data):
    df = pd.DataFrame()
    for i in game_data:
        print(i['gamedate'])
        gm = get_data(i['boxscore'])
        gamepk = re.search(r'/game/([^/]+)', i['boxscore']).group(1)
        player_stats = []
        for home_away in gm['teams']:
            for playerID in gm['teams'][home_away]['players']:
                player_info = {
                    'gamepk': gamepk,
                    'gamedate': i['gamedate'],
                    'homegame': True if home_away == 'home' else False,
                    'team_name': gm['teams'][home_away]['team']['name'],
                    'team_id': gm['teams'][home_away]['team']['id'],
                    'player_id': gm['teams'][home_away]['players'][playerID]['person']['id'],
                    'player_fullname': gm['teams'][home_away]['players'][playerID]['person']['fullName'],
                    'player_link': gm['teams'][home_away]['players'][playerID]['person']['link'],
                    'position_code': gm['teams'][home_away]['players'][playerID]['position']['code'],
                    'position_name': gm['teams'][home_away]['players'][playerID]['position']['name'],
                    'position_type': gm['teams'][home_away]['players'][playerID]['position']['type'],
                    'batting': gm['teams'][home_away]['players'][playerID]['stats']['batting'],
                    'fielding': gm['teams'][home_away]['players'][playerID]['stats']['fielding'],
                    'pitching': gm['teams'][home_away]['players'][playerID]['stats']['pitching']
                }
                player_stats.append(player_info)

        stats_df = pd.DataFrame.from_dict(player_stats)
        cols = ['batting', 'fielding', 'pitching']

        for col in cols:
            tmp = json_normalize(stats_df[col])
            tmp.columns = [f"{col}_{subcolumn}" for subcolumn in tmp.columns]
            stats_df = stats_df.drop(col, axis=1).merge(tmp, right_index=True, left_index=True)

        stats_df.fillna(0.0, inplace=True)
        stats_df.columns = [x.lower() for x in stats_df.columns]
        stats_df = stats_df[stats_df.batting_gamesplayed == 1]
        df = df.append(stats_df, sort=False)

    dropCols = ['batting_stolenbasepercentage', 'batting_atbatsperhomerun', 'batting_note',
                'fielding_stolenbasepercentage', 'pitching_note', 'pitching_stolenbasepercentage',
                'pitching_strikepercentage', 'pitching_runsscoredper9', 'pitching_homerunsper9']

    for col in dropCols:
        if col in df.columns:
            df.drop(columns=col, inplace=True)
        else:
            print(f'Columns does not exist {col}')

    # df.drop(columns=dropCols, inplace=True)
    conv_cols = ['gamepk', 'position_code',
                 'fielding_fielding', 'pitching_inningspitched']

    for col in conv_cols:
        df[col] = df[col].astype('float')

    queries.insert_data(df, 'gamestat')

    return True

def update_game_stats():
    last_update = queries.check_last_update(Gamestat)
    print(f'last update: {last_update}')
    if last_update == None:
        last_update = dt.date(2018, 1, 1)

    data = session.query(Game).filter(Game.gamedate > last_update).all()
    session.commit()

    gmdata = []
    for i in data:
        gmdata.append({
            'boxscore': i.boxscore,
            'gamedate': i.gamedate
        })

    return get_game_stats(gmdata)
