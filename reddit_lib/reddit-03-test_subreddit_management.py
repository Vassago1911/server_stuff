from subreddits import add_subreddit, choose_subreddit, unchoose_subreddit

import db_lib.pg_conn as pg_conn
eng = pg_conn.get_postgres_connection()

adders = ['studium'
            ,'autismus'
            ,'psychologiestudium'
            ,'medizinstudium'
            ,'fragreddit'
            ,'de_iama'
            ,'medizin'
            ,'goetheuni'
            ,'ratschlag'
            ,'biologie'
            ,'lehrerzimmer'
            ,'einfach_posten'
            ,'informatikkarriere'
            ,'blaulicht'
            ,'pflege'
            ,'abitur'
            ,'physik'
            ,'rwth'
            ,'nachrichten'
            ,'legaladvicegerman'
            ,'tuhh'
            ,'uni_hamburg'
            ,'uniwien'
            ,'studentenkueche'
            ,'heutelernteich'
            ,'musik'
            ,'germanmetal'
            ,'germanrap'
            ,'musizierende'
            ,'coronavirusdach'
            ,'immobilieninvestments'
            ,'wallstreetbetsger'
            ,'eltern'
            ,'naturfreunde'
            ,'pcgamingde'
            ,'ki_welt']

choosers = ['studium'
            ,'autismus'
            ,'psychologiestudium'
            ,'medizinstudium'
            ,'fragreddit'
            ,'de_iama'
            ,'medizin'
            ,'goetheuni'
            ,'ratschlag'
            ,'biologie'
            ,'lehrerzimmer'
            ,'einfach_posten'
            ,'informatikkarriere'
            ,'blaulicht'
            ,'pflege'
            ,'abitur'
            ,'physik'
            ,'rwth'
            ,'nachrichten'
            ,'legaladvicegerman'
            ,'tuhh'
            ,'uni_hamburg'
            ,'uniwien'
            ,'studentenkueche'
            ,'heutelernteich'
            ,'musik'
            ,'germanmetal'
            ,'germanrap'
            ,'musizierende'
            ,'coronavirusdach'
            ,'immobilieninvestments'
            ,'wallstreetbetsger'
            ,'eltern'
            ,'naturfreunde'
            ,'pcgamingde'
            ,'ki_welt']

unchoosers = [ 'pferdesindkacke'
             , 'bundesliga' ]

for subreddit in sorted(adders):
    add_subreddit(subreddit,connection=eng,chosen=1)

for subreddit in sorted(choosers):
    choose_subreddit(subreddit,eng)

for subreddit in sorted(unchoosers):
    unchoose_subreddit(subreddit,eng)