from submissions import load_new_submissions_to_connection
import db_lib.pg_conn as pg_conn
eng = pg_conn.get_postgres_connection()

load_new_submissions_to_connection(eng)