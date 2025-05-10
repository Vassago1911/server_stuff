import json
import praw
from pathlib import Path

def get_reddit_client():
    p = Path(__file__).absolute().parent.parent / "secrets" / "reddit_credentials.json"
    with open(p) as fi:
        creds = ''.join(fi.readlines())
    creds = json.loads(creds)

    reddit = praw.Reddit(
        client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        user_agent=creds['user_agent'],
    )

    try:
        tmp = reddit.read_only
        del tmp
        return reddit
    except Exception as e:
        print("reddit connection failed, are credentials okay? are you online?", e)