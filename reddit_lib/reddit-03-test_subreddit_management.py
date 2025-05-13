from subreddits import add_subreddit, choose_subreddit, unchoose_subreddit

import db_lib.pg_conn as pg_conn
eng = pg_conn.get_postgres_connection()

adders = ['ltb_iel','die_linke','diegruenen']

choosers = ['ltb_iel','die_linke']

unchoosers = [ 'ukrainemt' ]

for subreddit in sorted(adders):
    add_subreddit(subreddit,connection=eng,chosen=1)

for subreddit in sorted(choosers):
    choose_subreddit(subreddit,eng)

for subreddit in sorted(unchoosers):
    unchoose_subreddit(subreddit,eng)