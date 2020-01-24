import queries
import constants
import fetch
import pandas as pd
from pandas.io.json import json_normalize
import re
import utils
from models import Teams, session, Rosters
import datetime as dt


def get_teams():
    if queries.check_table_exists('teams'):
        print('teams exists')
    else:
        print('Fetching teams')
        data = fetch.get_data(f'{constants.API_URL}/teams')
        list_of_teams = []
        for i in data['teams']:
            if i['sport']['name'] == 'Major League Baseball':
                list_of_teams.append(i)
        teams_df = pd.DataFrame.from_dict(list_of_teams)
        teams_df = utils.clean_teams(teams_df)

        queries.insert_data(teams_df, 'teams', True)
        print('Teams inserted')


def update_roster():
    if queries.check_table_exists('rosters'):
        last_update = queries.check_last_update(Rosters)
        next_update = last_update + dt.timedelta(6)
        if next_update < constants.today:
            team_ids = session.query(Teams.id).all()
            team_ids = [x.id for x in team_ids]
            df = fetch.get_rosters(team_ids)
            queries.insert_data(df, 'rosters')
        else:
            print(f'rosters up to date, next update: {next_update}')
    else:
        print(f'creating table rosters')
        team_ids = session.query(Teams.id).all()
        team_ids = [x.id for x in team_ids]
        df = fetch.get_rosters(team_ids)
        queries.insert_data(df, 'rosters')



    # try:
    #     last_update = queries.check_last_update(Rosters)
    #     next_update = last_update + dt.timedelta(6)
    #     if (last_update == None) or (next_update < constants.today):
    #         team_ids = session.query(Teams.id).all()
    #         team_ids = [x.id for x in team_ids]
    #         df = pd.DataFrame()
    #         for i in team_ids:
    #             url = f'{constants.API_URL}/teams/{i}/roster'
    #             result = fetch.get_data(url)['roster']
    #             tmp = json_normalize(result)
    #             tmp['team_id'] = i
    #             df = df.append(tmp, sort=False)
    #         df.rename(columns=lambda x: re.sub(r'\.', '_', x), inplace=True)
    #         df.columns = [x.lower() for x in df.columns]
    #         df['updated'] = constants.today
    #         queries.insert_data(df, 'rosters')
    #         print(f'rosters updated: {constants.today}')
    # except Exception as ex:
    #     print(ex)
