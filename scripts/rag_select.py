import sys, re, json
from rank_bm25 import BM25Okapi
impoty argaparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="stades REM et N3")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--chunk-lines", type=int, default=200)
    parser.add_argument("--overlap", type=int, default=40)
    args = parser.parse_args()

    full = sys.stdin.read().strip()
    if not full:
        print("[]"); raise SystemExit(0)

    # utilise les paramètres
    global CHUNK_LINES, OVERLAP
    CHUNK_LINES, OVERLAP = args.chunk_lines, args.overlap

    chunks = chunk_lines(full)
    print(json.dumps(top_k(chunks, args.query, k=args.k), ensure_ascii=False))
