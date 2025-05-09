import datetime
today = lambda : str(datetime.datetime.now())[:19]

import json
import pandas as pd
from reddit_lib.connection import get_reddit_client

from random import shuffle

def get_uncommented_submissions(connection):
    submission_ids = list(pd.read_sql("""
                    select distinct s.submission_id from submissions s 
                     where submission_id not in ( select distinct submission_id from "comments" c )
                       and s.submission_language = 'de'
                       and s.submission_comment_count >= 32
                       """,connection).submission_id.unique())
    shuffle(submission_ids)
    return submission_ids

def get_submission_comments(submission_id='1il97qd'):
    reddit = get_reddit_client()
    submission = reddit.submission(submission_id)
    for _ in range(8):
        try:
            submission.comments.replace_more(64)
        except:
            break
    submission.comments.replace_more(0)
    comments = submission.comments
    comments = comments.list()
    parsed_comments = list()
    for z in comments:
        try:
            tup = (z.id,z.submission.id,today(),int(z.created_utc),z.author.fullname,z.body,z.ups )
            parsed_comments += [tup]
        except:
            pass
    comments = pd.DataFrame(parsed_comments, columns=['comment_id','submission_id','scrape_date','comment_created_at_utc','comment_author','comment_text','comment_upvote_count'])
    return comments

def load_comments_to_connection(connection):
    submission_ids = get_uncommented_submissions(connection)
    for submission_id in submission_ids:
        print(f"{today()}:  ", 'getting comments for submission: ', submission_id)
        try:
            tmp = get_submission_comments(submission_id)
        except:
            tmp = []
        if len(tmp) > 0:
            tmp.to_sql('comments',connection,if_exists='append',index=False)
            print(f"{today()}:  ",'saved',len(tmp),f"new comments in {submission_id}")
        else:
            print(f"{today()}:  ",f"no comments loaded for {submission_id}")