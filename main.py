from team_data import get_teams, update_roster
from game_data import update_historic_games
from models import create_tables
from constants import today




def initialize():
    create_tables()
    get_teams()
    update_roster()
    update_historic_games(today)
    # print(df_teams.columns)


if __name__ == '__main__':
    initialize()