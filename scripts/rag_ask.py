import os, sys, json, requests

MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
HOST  = os.getenv("OLLAMA_HOST", "127.0.0.1")
PORT  = os.getenv("OLLAMA_PORT", "11434")

# Lis la fenêtre souhaitée depuis l'env, sinon 8192
NUM_CTX = int(os.getenv("NUM_CTX", "8192"))

PROMPT_TMPL = """You are a Data Architect specialized in healthcare and sleep analysis.
The text below contains factual extracts from CSV, XLSX, and EDF files.
You must rely **only** on the visible content in the CONTEXT.
Do not invent or infer anything that is not explicitly present. 
If a piece of information is missing, write "—".

Your task:
Extract metadata in a clear and structured table format.

EXPECTED OUTPUT (Markdown table):
| source | metadata_field | example_data | proposed_definition |

Rules:
- Do NOT generate medical diagnostics or mention imaging (CT, MRI, etc.).
- Each table row must correspond to a field or data element actually observed in the CONTEXT.
- Group similar fields and normalize naming (e.g., “ahi” = “apnea-hypopnea index”).
- Include units in the definition when present.
- Keep the tone technical and descriptive, suitable for data catalog documentation.

---
CONTEXT:
{context}
---
QUESTION:
{question}
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
