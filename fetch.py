import requests
import pandas as pd
from pandas.io.json import json_normalize
import constants
import re
import datetime as dt


def get_data(url):
    res = requests.get(url)
    try:
        results = res.json()
        return results
    except Exception as ex:
        print(f'Error from get_data with : {ex}')
        return None


def get_rosters(team_ids):
    df = pd.DataFrame()
    for i in team_ids:
        url = f'{constants.API_URL}/teams/{i}/roster'
        result = get_data(url)['roster']
        tmp = json_normalize(result)
        tmp['team_id'] = i
        df = df.append(tmp, sort=False)
    df.rename(columns=lambda x: re.sub(r'\.', '_', x), inplace=True)
    df.columns = [x.lower() for x in df.columns]
    df['updated'] = constants.today
    return df


def get_starting_pitcher(game_urls, gamepk, preview=False):
    pitcher_ids = []
    for gmpk, game_url in zip(gamepk, game_urls):
        # print(game_url)
        boxscore = get_data(game_url)
        pitcher_ids.append({
            'gamepk': gmpk,
            'home_pitcher_id': boxscore['teams']['home']['pitchers'][0],
            'away_pitcher_id': boxscore['teams']['away']['pitchers'][0]
        })
    return pitcher_ids


def update_played_games(season, fromDate, toDate, gameType='R'):
    url = f'{constants.BASE_URL}/api/v1/schedule/games/?sportId=1&season={season}&startDate={fromDate}&endDate={toDate}&gameType={gameType}'
    # print(url)
    result = get_data(url)
    games = []

    for gamedata in result['dates']:
        for game in gamedata['games']:
            games.append(game)
    df = pd.DataFrame.from_dict(games)

    cols = ['teams', 'status', 'venue', 'content']
    for col in cols:
        # print(df[col])
        tmp = json_normalize(df[col])
        tmp.columns = [f"{col}_{subcolumn}" for subcolumn in tmp.columns]
        df = df.drop(col, axis=1).merge(tmp, right_index=True, left_index=True)

    df.rename(columns=lambda x: re.sub(r'\.|\-| +', '_', x), inplace=True)
    df.columns = [x.lower() for x in df.columns]
    cols = ['gamepk', 'link', 'gametype',
            'season', 'gamedate', 'calendareventid',
            'seriesdescription', 'teams_away_team_name', 'teams_away_team_id',
            'teams_away_score', 'teams_home_team_name', 'teams_home_team_id',
            'teams_away_leaguerecord_pct', 'teams_home_leaguerecord_pct',
            'teams_home_score', 'teams_home_iswinner', 'teams_away_iswinner',
            'venue_id', 'venue_name', 'status_statuscode', 'status_codedgamestate', 'status_detailedstate']

    df = df[cols]
    df.drop(df[df.status_codedgamestate.isin(['D', 'C'])].index, inplace=True)
    df.rename(columns=lambda x: re.sub(r'teams_', '', x), inplace=True)
    df.link = constants.BASE_URL + df.link
    df['boxscore'] = df.link.replace({'feed/live': 'boxscore', '1.1': '2'}, regex=True)
    df['link'] = df.link.replace({'1.1': '2'}, regex=True)
    df['gamedate'] = ((pd.to_datetime(df['gamedate'])) - dt.timedelta(hours=5)).dt.date

    pitcher_ids = pd.DataFrame.from_dict(get_starting_pitcher(df.boxscore, df.gamepk))
    df = df.merge(pitcher_ids, on='gamepk')

    return df
