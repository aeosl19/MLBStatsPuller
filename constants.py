from sqlalchemy import create_engine
import datetime as dt

API_URL = "http://statsapi.mlb.com/api/v1"
BASE_URL = "https://statsapi.mlb.com"

engine = create_engine('postgresql://andreaserga:Patrik78@localhost:5432/mlb_db', echo=True)


today = (dt.datetime.today() - dt.timedelta(hours=9)).date()
yesterday = today - dt.timedelta(1)