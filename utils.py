from pandas.io.json import json_normalize
import pandas as pd

def clean_teams(df):
    cols = ['division', 'league', 'sport', 'springLeague', 'venue']
    for col in cols:
        tmp = json_normalize(df[col])
        tmp.columns = [f"{col}_{subcolumn}" for subcolumn in tmp.columns]
        df = df.drop(col, axis=1).merge(tmp, right_index=True, left_index=True)
    df.columns = [x.lower() for x in df.columns]

    return df


def clean_game_data(df, isPlayer=False):
    cols = ['batting', 'fielding', 'pitching']

    for col in cols:
        tmp = json_normalize(df[col])
        tmp.columns = [f"{col}_{subcolumn}" for subcolumn in tmp.columns]
        df = df.drop(col, axis=1).merge(tmp, right_index=True, left_index=True)

    # df.fillna(0.0, inplace=True)
    df.columns = [x.lower() for x in df.columns]
    if isPlayer:
        df = df[(df.batting_gamesplayed >= 1) | (df.pitching_battersfaced >= 1)]
        dropCols = ['batting_stolenbasepercentage', 'batting_atbatsperhomerun',
                    'batting_note', 'fielding_stolenbasepercentage',
                    'pitching_note', 'pitching_stolenbasepercentage',
                    'pitching_strikepercentage', 'pitching_runsscoredper9',
                    'pitching_homerunsper9']
        df.drop(columns=dropCols, inplace=True)

        conv_cols = ['gamepk', 'position_code',
                     'fielding_fielding', 'pitching_inningspitched']

        for col in conv_cols:
            df[col] = df[col].astype('float')

        df.fillna(0.0, inplace=True)
    else:
        conv_cols = ['batting_avg',
                     'batting_obp',
                     'batting_slg',
                     'batting_ops',
                     'batting_stolenbasepercentage',
                     'batting_atbatsperhomerun',
                     'fielding_stolenbasepercentage',
                     'pitching_obp',
                     'pitching_stolenbasepercentage',
                     'pitching_era',
                     'pitching_inningspitched',
                     'pitching_whip',
                     'pitching_groundoutstoairouts',
                     'pitching_runsscoredper9',
                     'pitching_homerunsper9']

        for col in conv_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(0, inplace=True)
    return df
