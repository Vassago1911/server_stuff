import pandas as pd
import sqlite3 
import db_lib.pg_conn as pg_conn

eng = pg_conn.get_postgres_connection()
con = sqlite3.connect('reddit.db')

local_submissions = pd.read_sql('select * from submissions', con)
#pg_submission = pd.read_sql('select * from submissions', eng)
local_submissions.reset_index().drop(columns='index').reset_index().rename(columns={'index':'id'}).to_sql('submissions',con=eng,if_exists='replace',index=False)