def get_connection_creds():
    from pathlib import Path
    p = Path(__file__).absolute().parent.parent.parent
    p = p / "dockers" / "databases" / ".env"
    with open(p,'r') as fi:
        s = fi.readlines()
    s = list(map(lambda z: tuple(z.split('=')),s))
    s = list(map(lambda z: (z[0],z[1].strip('\n')),s))
    s = dict(s)
    return s

def get_postgres_connection(port=5432):
    creds = get_connection_creds()
    from sqlalchemy import create_engine
    engine = create_engine(f'postgresql+psycopg2://{creds['POSTGRES_USER']}:{creds['POSTGRES_PASSWORD']}@localhost:{port}/{creds['POSTGRES_DB']}')
    return engine
