import os, sys, json, requests

MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
HOST  = os.getenv("OLLAMA_HOST", "127.0.0.1")
PORT  = os.getenv("OLLAMA_PORT", "11434")

PROMPT_TMPL = """Tu es un assistant sommeil concis.
Contexte (extraits, horodatés et étiquetés) :
---
{context}
---
Question: {question}
Réponds en 5-7 phrases, liste claire, sans spéculation médicale.
"""

def ask(model, prompt):
    url = f"http://{HOST}:{PORT}/api/generate"
    r = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=120)
    r.raise_for_status()
    return r.json().get("response","").strip()

if __name__ == "__main__":
    raw = sys.stdin.read()
    chunks = json.loads(raw)
    q = sys.argv[1] if len(sys.argv) > 1 else "résume les stades majeurs"
    context = "\n\n---\n\n".join(chunks)
    prompt = PROMPT_TMPL.format(context=context[:8000], question=q)
    print(ask(MODEL, prompt))

raw = sys.stdin.read().strip()
if not raw:
    print("Aucun contexte reçu (stdin vide)."); raise SystemExit(1)

