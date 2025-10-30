import os, sys, json, requests

MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
HOST  = os.getenv("OLLAMA_HOST", "127.0.0.1")
PORT  = os.getenv("OLLAMA_PORT", "11434")

# Lis la fenêtre souhaitée depuis l'env, sinon 8192
NUM_CTX = int(os.getenv("NUM_CTX", "8192"))

PROMPT_TMPL = """You are a healthcare sleep **data catalog** assistant.
Use ONLY the CONTEXT. Do not invent. If unknown, write "—".

Output **one Markdown table only** with **exactly** these columns:
| source | metadata_field | example_data | proposed_definition |

Rules:
- **source** ∈ {csv,xlsx,edf_header,edf_signal}. Use `edf_header` for global EDF header fields, `edf_signal` for per-channel fields.
- **metadata_field**: normalized lower_snake_case (e.g., ahi, odi, start_datetime, n_records, record_duration_s, n_signals, signal_label, fs_hz, phys_dim, phys_min, phys_max, dig_min, dig_max, prefilter, samp_per_record, study_type, scorers, nasal_pressure, etc.).
- **example_data**: one short value you saw in CONTEXT (e.g., "200.0", "uV", "PSG", "18.12").
- **proposed_definition**: 1 short sentence, include unit when relevant.
- No event timelines. No clinical interpretation. No extra text before/after the table.

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
             "num_ctx": NUM_CTX,
             "num_predict": int(os.getenv("NUM_PREDICT", "2048")),
             "temperature": 0.1,
             "top_p": 0.9,
            "repeat_penalty": 1.15
        }        
    }
    r = requests.post(url, json=payload, timeout=int(os.getenv("REQUEST_TIMEOUT", "900")))
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
