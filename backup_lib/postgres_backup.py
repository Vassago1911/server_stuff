import pandas as pd
import db_lib.pg_conn as pg_conn
eng = pg_conn.get_postgres_connection()

from time import time as _t
time = lambda : int(_t())

import sqlite3
con = sqlite3.connect(f'/media/v/spinDATA/reddit_postgres_backup/reddit_{time()}.db')

all_tables = list(pd.read_sql("select table_name from information_schema.tables where table_schema = 'public'",eng).table_name.unique())
all_tables = sorted(all_tables)

for table in all_tables:
    print('starting', table)
    start_t = time()
    df = pd.read_sql(f"select * from {table}",eng)
    if 'id' in df.columns:
        df = df.drop(columns='id')
    df.to_sql(table,con,if_exists='replace',index=False)
    end_t = time()
    print('took', end_t - start_t, 'seconds')