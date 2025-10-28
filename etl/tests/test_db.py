import os
import pg8000
from urllib.parse import urlparse

DB_DSN = os.getenv("DB_DSN", "postgresql://postgres:postgres@postgres:5432/sleeplab")

def _conn_kwargs(dsn: str):
    u = urlparse(dsn)
    return {
        "user": u.username,
        "password": u.password,
        "host": u.hostname,
        "port": u.port or 5432,
        "database": u.path.lstrip("/"),
    }

def test_tables_exist():
    with pg8000.connect(**_conn_kwargs(DB_DSN)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT count(*) FROM information_schema.tables
            WHERE table_schema='sleeplab'
              AND table_name IN ('patient','session_psg','algo_run','sleep_staging_result')
        """)
        assert cur.fetchone()[0] == 4

def test_seed_has_rows():
    with pg8000.connect(**_conn_kwargs(DB_DSN)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM sleeplab.sleep_staging_result")
        assert cur.fetchone()[0] >= 5
