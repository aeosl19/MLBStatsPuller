from pandas.io.json import json_normalize

def clean_teams(df):
    cols = ['division', 'league', 'sport', 'springLeague', 'venue']
    for col in cols:
        tmp = json_normalize(df[col])
        tmp.columns = [f"{col}_{subcolumn}" for subcolumn in tmp.columns]
        df = df.drop(col, axis=1).merge(tmp, right_index=True, left_index=True)
    df.columns = [x.lower() for x in df.columns]

    return df