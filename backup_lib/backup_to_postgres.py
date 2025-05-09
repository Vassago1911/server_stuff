import pandas as pd
import db_lib.pg_conn as pg_conn
eng = pg_conn.get_postgres_connection()
from sqlalchemy import text

from time import time as _t
time = lambda : int(_t())

import os
bkp_dir = '/media/v/spinDATA/reddit_postgres_backup/'
reddit_dbs = os.listdir(bkp_dir)
reddit_dbs = list(filter(lambda z: ('reddit_' in z) and ('.db' in z),reddit_dbs ))
reddit_db = bkp_dir + max(reddit_dbs)

import sqlite3
con = sqlite3.connect(reddit_db)

all_tables = list(pd.read_sql("select table_name from information_schema.tables where table_schema = 'public'",eng).table_name.unique())

for table in [ t for t in all_tables if t != "submissions" ]:
    print('starting', table)
    start_t = time()
    df = pd.read_sql(f"select * from {table}",con)
    if 'id' in df.columns:
        df = df.drop(columns='id')
    df.to_sql(table,eng,if_exists='replace',index=False)
    end_t = time()
    print('took', end_t - start_t, 'seconds')