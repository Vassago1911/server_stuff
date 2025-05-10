import db_lib.pg_conn as pg_conn
eng = pg_conn.get_postgres_connection()

import pandas as pd
from time import time 
  
def timer_func(func): 
    # This function shows the execution time of  
    # the function object passed 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 
  
@timer_func
def subreddit_compressed():
    subreddit_compression_sql = """select lower(subreddit_url) subreddit_url
                 , max(subscribers) subscribers
                 , max(chosen) chosen
              from subreddits s 
             group by subreddit_url
             order by chosen desc, subscribers desc, subreddit_url""" 
    subreddits = pd.read_sql(subreddit_compression_sql,eng)
    return subreddits

@timer_func
def comments_compressed():
    comment_compression_sql = """select comment_id
                 , submission_id
                 , min(scrape_date) scrape_date
                 , min(comment_created_at_utc) comment_created_at_utc
                 , max(comment_author) comment_author
                 , max(comment_text) comment_text
                 , max(comment_upvote_count) comment_upvote_count   
              from comments
             group by comment_id, submission_id
             order by scrape_date desc, comment_created_at_utc desc"""
    comments = pd.read_sql(comment_compression_sql,eng)
    return comments

@timer_func
def submission_compressed():         
    submission_compression_sql = """select min(scrape_date) scrape_date
                 , min(created_utc) created_utc
                 , subreddit_url 
                 , submission_id
                 , max(submission_comment_count) submission_comment_count 
                 , max(submission_score) submission_score
                 , min(submission_upvote_ratio) submission_upvote_ratio 
                 , max(submission_title) submission_title 
                 , max(submission_text) submission_text 
                 , max(submission_language) submission_language
              from submissions
             group by subreddit_url, submission_id
             order by scrape_date desc, created_utc desc"""
    submissions = pd.read_sql(submission_compression_sql,eng)
    return submissions

@timer_func
def timed_df_save(df,table_name):
    df.to_sql(table_name,eng,if_exists='replace',index=False)

subreddits = subreddit_compressed()
timed_df_save(subreddits,'subreddits')

comments = comments_compressed()
timed_df_save(comments,'comments')

submissions = submission_compressed()
timed_df_save(submissions,'submissions')