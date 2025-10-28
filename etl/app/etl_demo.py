import os
from datetime import datetime, timedelta
import psycopg

DB_DSN = os.getenv("DB_DSN", "postgresql://postgres:postgres@postgres:5432/sleeplab")

def run():
    # insère 1 point supplémentaire (W) sur la session la plus récente
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT session_id FROM sleeplab.session_psg ORDER BY session_id DESC LIMIT 1
            """)
            sid = cur.fetchone()[0]
            cur.execute("""
                SELECT run_id FROM sleeplab.algo_run ORDER BY run_id DESC LIMIT 1
            """)
            rid = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO sleeplab.sleep_staging_result(session_id, run_id, ts, stage_label, confidence)
                VALUES (%s, %s, %s, %s, %s)
            """, (sid, rid, datetime.utcnow() + timedelta(minutes=5), "W", 0.88))
        conn.commit()
    print("etl_demo: inserted 1 row")

if __name__ == "__main__":
    run()
