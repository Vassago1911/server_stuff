import datetime
today = lambda : str(datetime.datetime.now())[:19]
log_today = lambda : str(datetime.datetime.now())[5:16]

import json
import pandas as pd
from connection import get_reddit_client

from lingua import Language, LanguageDetectorBuilder

languages = []
languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def lingua_language_name_to_iso2(lg_code):
    match lg_code:
            case "GERMAN":
                lg = 'de'
            case "ENGLISH":
                lg = 'en'
            case "SPANISH":
                lg = 'es'
            case "FRENCH":
                lg = 'fr'
            case _:
                lg = '--'
    return lg

def get_new_submissions(subreddit):
    def url_to_subreddit(url='python',reddit_client=get_reddit_client()):
        return reddit_client.subreddit(url)
    def _submission_to_row(subreddit:str, submission):
        clf = lambda z: lingua_language_name_to_iso2( detector.detect_language_of( z ).name )
        title = submission.title
        text = submission.selftext
        lang = clf( title + " " + text )[0]
        values = (  today(),
                    int(submission.created_utc),
                    subreddit,
                    submission.id,
                    submission.num_comments,
                    submission.score,
                    submission.upvote_ratio,
                    title,
                    text,
                    lang )
        columns = ( 'scrape_date',
                    'created_utc',
                    'subreddit_url',
                    'submission_id',
                    "submission_comment_count",
                    'submission_score',
                    'submission_upvote_ratio',
                    'submission_title',
                    "submission_text",
                    "submission_language" )
        res = dict(zip(columns,values))
        return res
    def get_new_in_subreddit(subreddit='python',count=128):
        if subreddit != 'all':
            tmp = list(url_to_subreddit(subreddit).new(limit=count))
            tmp = list(map( lambda z: _submission_to_row(subreddit,z), tmp))
            return tmp
        tmp = list(url_to_subreddit(subreddit).hot(limit=count))
        tmp = list(map( lambda z: _submission_to_row(subreddit,z), tmp))
        return tmp    
    try:
        tmp = get_new_in_subreddit(subreddit,128)
    except Exception as e:
        tmp = []
        print('Exception thrown', e )
        print('submission request failed for ', subreddit)
    tmp = pd.DataFrame(tmp,columns=['scrape_date',
                                    'created_utc',
                                    'subreddit_url',
                                    'submission_id',
                                    "submission_comment_count",
                                    'submission_score',
                                    'submission_upvote_ratio',
                                    'submission_title',
                                    "submission_text",
                                    "submission_language"])
    return tmp

def get_relevant_subreddits(connection):
    try:
        return tuple(['all'] + sorted(list(pd.read_sql('select * from subreddits where chosen = 1 and subscribers > 100',connection).subreddit_url.unique())))
    except:
        return tuple(['all','de','worldnews','kurrent','mathe','onionlovers','palestine'])

def load_new_submissions_to_connection(connection):
    subreddit_list = get_relevant_subreddits(connection)
    for i,subreddit in enumerate(subreddit_list):
        print("Round",f"{i:02d}",f"- {log_today()} -", 'getting submissions for subreddit: ', subreddit)
        tmp = get_new_submissions(subreddit)
        if len(tmp) > 0:
            tmp.to_sql('submissions',connection,if_exists='append',index=False)
            print("Round",f"{i:02d}",f"- {log_today()} -",'saved',len(tmp),f"new submissions in {subreddit}")
        else:
            print("Round",f"{i:02d}",f"- {log_today()} -",f"no new submissions in {subreddit}")