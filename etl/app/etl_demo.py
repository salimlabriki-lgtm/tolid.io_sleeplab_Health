import os
from datetime import datetime, timedelta
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

def run():
    with pg8000.connect(**_conn_kwargs(DB_DSN)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT session_id FROM sleeplab.session_psg ORDER BY session_id DESC LIMIT 1")
        sid = cur.fetchone()[0]
        cur.execute("SELECT run_id FROM sleeplab.algo_run ORDER BY run_id DESC LIMIT 1")
        rid = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO sleeplab.sleep_staging_result(session_id, run_id, ts, stage_label, confidence)"
            " VALUES (%s, %s, %s, %s, %s)",
            (sid, rid, datetime.utcnow() + timedelta(minutes=5), "W", 0.88),
        )
        conn.commit()
    print("etl_demo: inserted 1 row")

if __name__ == "__main__":
    run()
