echo "running full"
# python3 reddit-00-load_submissions.py
python3 reddit-01-load_comments.py
# python3 reddit-02-compress_tables.py
# python3 db_lib/postgres_backup.py