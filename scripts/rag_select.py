import sys, re, json, argparse
from rank_bm25 import BM25Okapi

def chunk_lines(text: str, n: int, overlap: int):
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

def top_k(chunks, query, k: int):
    if not chunks: return []
    corpus = [tok(c) for c in chunks]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(tok(query))
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
    return [c for _, c in ranked[:k]]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="analyse des canaux et fréquences d'échantillonnage")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--chunk-lines", type=int, default=200)
    ap.add_argument("--overlap", type=int, default=40)
    args = ap.parse_args()

    full = sys.stdin.read().strip()
    if not full:
        print("[]")
        raise SystemExit(0)

    chunks = chunk_lines(full, n=args.chunk_lines, overlap=args.overlap)
    print(json.dumps(top_k(chunks, args.query, k=args.k), ensure_ascii=False))
