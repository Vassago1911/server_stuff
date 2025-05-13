import pandas as pd
import pg_conn
eng = pg_conn.get_postgres_connection(port=5432)
pg_con = eng.connect().execution_options(stream_results=True)

from time import time as _t
time = lambda : int(_t())

import datetime
log_today = lambda : str(datetime.datetime.now())[5:16]
print(log_today(),'starting local backup')

from pathlib import Path
p = Path(__file__).absolute().parent.parent.parent / "secrets" / "backup_path.txt"
with open(p,'r') as fi:
    backup_db_path = ''.join(fi.readlines())

import sqlite3
con = sqlite3.connect(backup_db_path + '/' + f'reddit_{time()}.db')

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
print(log_today(),'local backup done')