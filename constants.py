from sqlalchemy import create_engine
import datetime as dt

API_URL = "http://statsapi.mlb.com/api/v1"
engine = create_engine('postgresql://andreaserga:Patrik78@localhost:5432/mlb_db')


today = (dt.datetime.today() - dt.timedelta(hours=9)).date()