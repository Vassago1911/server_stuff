import datetime
today = lambda : str(datetime.datetime.now())[:19]
log_today = lambda : str(datetime.datetime.now())[5:16]

import json
import pandas as pd
from connection import get_reddit_client

from random import shuffle

unscraped_submissions = """
select s.submission_id from 
( select s.submission_id
       , s.submission_comment_count
       , coalesce( c_cnt.comments , 0 ) scraped_comments
       , s.submission_comment_count - coalesce( c_cnt.comments , 0 ) unscraped_comments
    from submissions s 
    left join ( select submission_id, count(distinct comment_id) comments from comments group by submission_id ) c_cnt
      on s.submission_id = c_cnt.submission_id 
   where created_utc > 1700000000
     and s.submission_language = 'de'
     and ( s.submission_comment_count - coalesce( c_cnt.comments , 0 ) ) > 16
   order by unscraped_comments desc ) s """


def get_uncommented_submissions(connection):
    try:
        submission_ids = list(pd.read_sql(unscraped_submissions,connection).submission_id.unique())
    except Exception as e:
        print('Exception',e)
        submission_ids = list(pd.read_sql("""
                        select distinct s.submission_id from submissions s 
                         where s.submission_language = 'de'
                           and s.submission_comment_count >= 32
                           """,connection).submission_id.unique()) 
    blocked = ["1dbo2q2","1dq173n","189o5u4","1dgh2yv","1dspun8"]
    submission_ids = [ s for s in submission_ids if s not in blocked ]
    print("                 ",len(submission_ids),"remaining")
    shuffle(submission_ids)
    return submission_ids[:32]

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
            tup = (z.id,submission_id,today(),int(z.created_utc),z.author_fullname,z.body,z.ups )
            parsed_comments += [tup]
        except:
            pass
    comments = pd.DataFrame(parsed_comments, columns=['comment_id','submission_id','scrape_date','comment_created_at_utc','comment_author','comment_text','comment_upvote_count'])
    return comments

def load_comments_to_connection(connection):
    while True:
        submission_ids = get_uncommented_submissions(connection)
        if len(submission_ids) == 0:
            print(f"{log_today()} --",'no unknown submissions left')
            break
        for i,submission_id in enumerate(submission_ids):
            print("Round", f"{i:02d}", f"-- {log_today()} - ", 'getting comments for submission: ', submission_id)
            # """put back in to have more than one worker running without duplicate entries, for one worker it's useless"""
            # try:
            #     known = list(pd.read_sql('select distinct submission_id from "comments" c',connection).submission_id.unique())
            # except Exception as e:
            #     print('Exception',e)
            #     known = []
            # if submission_id in known:
            #     print('      ',submission_id,'known already, skipping')
            #     continue
            try:
                tmp = get_submission_comments(submission_id)
            except:
                tmp = []
            if len(tmp) > 0:
                tmp.to_sql('comments',connection,if_exists='append',index=False)
                print("Round", f"{i:02d}", f"-- {log_today()} - ",'saved',len(tmp),f"new comments in {submission_id}")
            else:
                print("Round", f"{i:02d}", f"-- {log_today()} - ",f"no comments loaded for {submission_id}")