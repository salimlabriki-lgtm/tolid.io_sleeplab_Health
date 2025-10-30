import os, sys, json, requests

MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
HOST  = os.getenv("OLLAMA_HOST", "127.0.0.1")
PORT  = os.getenv("OLLAMA_PORT", "11434")

# Lis la fenêtre souhaitée depuis l'env, sinon 8192
NUM_CTX = int(os.getenv("NUM_CTX", "8192"))

PROMPT_TMPL = """You are a healthcare sleep data architect.
Use ONLY the CONTEXT. Do not invent anything. If missing, write "—".

Goal: Produce a **comprehensive** metadata catalog table.

OUTPUT (Markdown table only; no preface/no notes):
| source | metadata_field | example_data | proposed_definition |

Coverage rules (strict):
- Extract **every distinct field** you observe across CSV, XLSX and EDF (header + signals).
- For EDF, include: start_datetime, n_records, record_duration_s, n_signals, signal label, fs_hz, phys_dim, phys_min/max, dig_min/max, prefilter, samp_per_record.
- For CSV/XLSX, include all columns (e.g., ahi, odi, ai, hi, plmi, study_type, start_time, nasal_pressure, scorers, etc.).
- Normalize names (lower_snake_case); merge duplicates; add units in definition if visible.
- **Minimum rows required:** 40. If fewer fields are visible, list all available and add “—” where unknown.

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
