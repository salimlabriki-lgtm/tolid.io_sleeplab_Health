import os, sys, json, requests

MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
HOST  = os.getenv("OLLAMA_HOST", "127.0.0.1")
PORT  = os.getenv("OLLAMA_PORT", "11434")

# Lis la fenêtre souhaitée depuis l'env, sinon 8192
NUM_CTX = int(os.getenv("NUM_CTX", "8192"))

PROMPT_TMPL = """Tu es un assistant sommeil concis.
Contexte (extraits) :
---
{context}
---
Question: {question}
Réponds en 5-7 phrases, liste claire, sans spéculation médicale.
"""

def ask(model, prompt):
    url = f"http://{HOST}:{PORT}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": NUM_CTX  # tente d'augmenter la fenêtre de contexte
        }
    }
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    return r.json().get("response","").strip()

if __name__ == "__main__":
    raw = sys.stdin.read().strip()
    if not raw:
        print("Aucun contexte reçu."); raise SystemExit(1)
    chunks = json.loads(raw)
    q = sys.argv[1] if len(sys.argv) > 1 else "résume les stades majeurs"
    # ⚠️ on n'applique plus de tranche [:8000]
    context = "\n\n---\n\n".join(chunks)
    prompt = PROMPT_TMPL.format(context=context, question=q)
    print(ask(MODEL, prompt))
