from team_data import get_teams, update_player_table
from game_data import get_games, update_game_stats
from models import create_tables


def initialize():
    create_tables()
    get_teams()
    update_player_table()
    get_games()
    update_game_stats()
    # game_previews()
#     # print(df_teams.columns)


if __name__ == '__main__':
    initialize()