import requests
import pandas as pd
from pandas.io.json import json_normalize
import constants
import re

def get_data(url):
    res = requests.get(url)
    try:
        results = res.json()
        return results
    except Exception as ex:
        print (f'Error from get_data with : {ex}')
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
