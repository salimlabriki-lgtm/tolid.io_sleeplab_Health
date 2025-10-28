import os
import psycopg

DB_DSN = os.getenv("DB_DSN", "postgresql://postgres:postgres@postgres:5432/sleeplab")

def test_tables_exist():
    with psycopg.connect(DB_DSN) as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT count(*) FROM information_schema.tables
            WHERE table_schema='sleeplab'
              AND table_name IN ('patient','session_psg','algo_run','sleep_staging_result')
        """)
        assert cur.fetchone()[0] == 4

def test_seed_has_rows():
    with psycopg.connect(DB_DSN) as conn, conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM sleeplab.sleep_staging_result")
        assert cur.fetchone()[0] >= 5
