import db_lib.pg_conn as pg_conn
eng = pg_conn.get_postgres_connection(port=5432)
import pandas as pd
import time
import datetime
log_today = lambda : str(datetime.datetime.now())[5:16]
print(log_today(),'reading comments with id for language classification')
cmts = pd.read_sql(f'select comment_id, comment_text from comments;',eng)

#import py3langid
import multiprocessing

comments = cmts[['comment_id','comment_text']].to_dict(orient='records')

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

def classify(comment):
    # about 20 minutes for 2.6 mio comments with py3langid, 2 minutes with lingua
    # return { 'comment_id': comment['comment_id'], 'lang': py3langid.classify(comment['comment_text'])[0] }
    try:
        lg = lingua_language_name_to_iso2( detector.detect_language_of(comment['comment_text']).name )
        return { 'comment_id': comment['comment_id'], 'lang': lg }
    except Exception as e:
        return { 'comment_id': comment['comment_id'], 'lang': '--' }

def process_comments(comment_list, num_processes=None):
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()-1
    with multiprocessing.Pool(processes=num_processes) as pool:
        res = pool.map(classify,comments)
    return res

import datetime

log_today = lambda : str(datetime.datetime.now())[5:16]

print(len(cmts))
print(log_today(), '- starting comment language classification')
start_t = int(time.time())
res = process_comments(comments)
end_t = int(time.time())
print(log_today(), '- took',end_t-start_t,'seconds')

res = pd.DataFrame(res)
print(log_today(), '- saving results')
start_t = int(time.time())
res.to_sql('lingua_comment_languages',eng,if_exists='replace',index=False)
end_t = int(time.time())
print(log_today(), '- took',end_t-start_t,'seconds')
