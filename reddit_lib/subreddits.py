import datetime
today = lambda : str(datetime.datetime.now())[:19]
log_today = lambda : str(datetime.datetime.now())[5:16]

import json
import pandas as pd
from connection import get_reddit_client

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

def add_subreddit(name:str,connection,chosen:int=1):
    tmp = list()
    known_subreddits = list(pd.read_sql('select distinct subreddit_url from subreddits',connection).subreddit_url.apply(str.lower).unique())
    if name in known_subreddits:
        print('known subreddit', name)
        return
    try:
        reddit = get_reddit_client()
        subr = reddit.subreddit(name)
        sub_count = subr.subscribers
        tmp = list(subr.new(limit=6))
    except:
        print('subreddit probably does not exist?', name)
        pass
    if len(tmp) > 0:
        row = { 'subreddit_url':str.lower(name)
              , 'subscribers': sub_count
              , 'chosen': chosen }
        rows = pd.DataFrame([row])
        rows.to_sql('subreddits',connection,index=False,if_exists='append')
        print(log_today(),f'- added subreddit {name}')
        return
    else:
        print('subreddit returned no posts or subscribers', name)
        return

def unchoose_subreddit(name:str,connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    ud = f"""
    update subreddits
       set chosen = 0
     where subreddit_url = '{name}';"""
    session.execute(text(ud)); session.commit(); session.close()
    print(name, 'unchosen')

def choose_subreddit(name:str,connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    ud = f"""
    update subreddits
       set chosen = 1
     where subreddit_url = '{name}';"""
    session.execute(text(ud)); session.commit(); session.close()
    print(name, 'chosen')    