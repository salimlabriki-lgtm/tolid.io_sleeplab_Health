import os, ssl
from urllib.parse import urlparse, parse_qs
import pg8000
from dotenv import load_dotenv

load_dotenv()
DSN = os.environ["DB_DSN"]

def kw(dsn: str):
    u=urlparse(dsn); q=parse_qs(u.query or "")
    use_ssl = q.get("sslmode",[""])[0] in ("require","verify-full","verify-ca")
    k={"user":u.username,"password":u.password,"host":u.hostname,"port":u.port or 5432,"database":u.path.lstrip("/")}
    if use_ssl: k["ssl_context"]=ssl.create_default_context()
    return k

def fetch_sessions(limit_sessions=3):
    sql = """
    SELECT s.session_id, ssr.ts, ssr.stage_label, COALESCE(ssr.confidence,0)
    FROM sleeplab.session_psg s
    JOIN sleeplab.sleep_staging_result ssr USING(session_id)
    WHERE s.session_id IN (
      SELECT session_id FROM sleeplab.session_psg ORDER BY session_id DESC LIMIT %s
    )
    ORDER BY s.session_id, ssr.ts;
    """
    with pg8000.connect(**kw(DSN)) as conn, conn.cursor() as cur:
        cur.execute(sql, (limit_sessions,))
        rows = cur.fetchall()
    lines = [f"sid={sid} | ts={ts.isoformat()} | stage={stg} | conf={float(cf):.2f}"
             for (sid, ts, stg, cf) in rows]
    print("\n".join(lines))

if __name__ == "__main__":
    fetch_sessions()
