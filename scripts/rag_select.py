import sys, re, json
from rank_bm25 import BM25Okapi

CHUNK_LINES = 200
OVERLAP = 40

def chunk_lines(text: str, n=CHUNK_LINES, overlap=OVERLAP):
    lines = text.strip().splitlines()
    if not lines: return []
    chunks=[]; i=0
    step = max(1, n - overlap)
    while i < len(lines):
        chunks.append("\n".join(lines[i:i+n]))
        i += step
    return chunks

def tok(s: str):
    return re.findall(r"[a-zA-Z0-9]+", s.lower())

def top_k(chunks, query, k=3):
    if not chunks: return []
    corpus = [tok(c) for c in chunks]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(tok(query))
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
    return [c for _, c in ranked[:k]]

if __name__ == "__main__":
    full = sys.stdin.read().strip()
    if not full:
        print("[]"); raise SystemExit(0)
    user_q = sys.argv[1] if len(sys.argv) > 1 else "stades REM et N3"
    chunks = chunk_lines(full)
    print(json.dumps(top_k(chunks, user_q, k=3), ensure_ascii=False))
