import pandas as pd
import pg_conn
eng = pg_conn.get_postgres_connection()
from sqlalchemy import text

from time import time as _t
time = lambda : int(_t())

import datetime
log_today = lambda : str(datetime.datetime.now())[5:16]
print(log_today(),'starting upload of local backup')


from pathlib import Path
p = Path(__file__).absolute().parent.parent.parent / "secrets" / "backup_path.txt"
with open(p,'r') as fi:
    backup_db_path = ( ''.join(fi.readlines()) ).strip('\n').strip(' ')

import os
reddit_dbs = os.listdir(backup_db_path)
reddit_dbs = list(filter(lambda z: ('reddit_' in z) and ('.db' in z),reddit_dbs ))
reddit_db = backup_db_path + '/' + max(reddit_dbs)
print('using reddit db at', reddit_db)

import sqlite3
con = sqlite3.connect(reddit_db)

#all_tables = sorted(list(pd.read_sql("select table_name from information_schema.tables where table_schema = 'public'",eng).table_name.unique()))
all_tables = sorted(list(pd.read_sql("SELECT name table_name FROM sqlite_master WHERE type='table' ORDER BY name;",con).table_name.unique()))

for table in all_tables:
    print('starting', table)
    start_t = time()
    df = pd.read_sql(f"select * from {table}",con)
    df.to_sql(table,eng,if_exists='replace',index=False)
    end_t = time()
    print('took', end_t - start_t, 'seconds')
print(log_today(),'upload of local backup done')