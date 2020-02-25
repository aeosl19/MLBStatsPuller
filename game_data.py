import queries
import datetime as dt
import pandas as pd
import re
from utils import clean_game_data
from pandas.io.json import json_normalize
from models import session, Playerstat, Game
from constants import yesterday, today
from fetch import update_played_games, get_data


def get_games():
    startDate = dt.date(2018, 1, 1)
    last_update = queries.check_last_update(Game)
    print(last_update)
    if last_update == None: last_update = dt.date(2018, 1, 1)
    print(f'Games last_update: {last_update}')
    for i in range(last_update.year, yesterday.year + 1):
        print(i)
        if last_update > dt.date(i, 9, 28):
            pass
        elif (i < yesterday.year):
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
    team_stats = []
    player_stats = []
    for i in game_data:
        print(i['gamedate'])
        gm = get_data(i['boxscore'])
        gamepk = re.search(r'/game/([^/]+)', i['boxscore']).group(1)

        for home_away in gm['teams']:
            team_stats.append({
                'gamepk': gamepk,
                'gamedate': i['gamedate'],
                'homegame': True if home_away == 'home' else False,
                'team_name': gm['teams'][home_away]['team']['name'],
                'team_id': gm['teams'][home_away]['team']['id'],
                'batting': gm['teams'][home_away]['teamStats']['batting'],
                'pitching': gm['teams'][home_away]['teamStats']['pitching'],
                'fielding': gm['teams'][home_away]['teamStats']['fielding']
            })

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

    df_team_stats = clean_game_data(pd.DataFrame.from_dict(team_stats))
    df_player_stats = clean_game_data(pd.DataFrame.from_dict(player_stats), isPlayer=True)

    queries.insert_data(df_team_stats, 'teamstat')

    queries.insert_data(df_player_stats, 'playerstat')

    return True


def update_game_stats():
    last_update = queries.check_last_update(Playerstat)
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


def game_previews():
    pass
