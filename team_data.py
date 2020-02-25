import queries
import constants
import fetch
import pandas as pd
import utils
from models import Team, session, Player, Teamstat
import datetime as dt


def get_teams():
    num_ids = session.query(Team.id).count()
    session.commit()
    if num_ids > 0:
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
        print('Inserting Teams')
        queries.insert_data(teams_df, 'team', 'replace')
        print('Teams inserted')


def update_player_table():
    last_update = queries.check_last_update(Player, is_roster=True)

    if last_update == None: last_update = dt.date(2018, 1, 1)
    next_update = last_update + dt.timedelta(6)
    print(type(last_update))

    if next_update < constants.today:
        print(f'updating, last update: {last_update}')
        team_ids = session.query(Team.id).all()
        session.commit()
        team_ids = [x.id for x in team_ids]
        # print(team_ids)
        df = fetch.get_rosters(team_ids)
        df.reset_index(drop=True, inplace=True)
        df.jerseynumber.replace("", -1, inplace=True)
        df.position_code.replace('O', 9, inplace=True)
        #print(df.shape)
        queries.insert_data(df, 'player')
    else:
        print(f'rosters up to date, next update: {next_update}')
