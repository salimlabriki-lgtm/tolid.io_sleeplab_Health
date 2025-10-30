#!/usr/bin/env python
import os, sys, json, requests
from pathlib import Path
from rag_fetch_files import read_csv, read_xlsx, read_edf  # réutilise tes helpers

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
HOST  = os.getenv("OLLAMA_HOST", "127.0.0.1")
PORT  = os.getenv("OLLAMA_PORT", "11434")
NUM_CTX = int(os.getenv("NUM_CTX", "16384"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "900"))

PROMPT_TMPL = """You are a healthcare sleep **data catalog** assistant.
Use ONLY the CONTEXT. Do not invent. If unknown, write "—".

Output **one Markdown table only** with **exactly** these columns:
| source | metadata_field | example_data | proposed_definition |

Rules:
- **source** ∈ {{csv,xlsx,edf_header,edf_signal}}. Use `edf_header` for global EDF header fields, `edf_signal` for per-channel fields.
- **metadata_field**: normalized lower_snake_case (e.g., ahi, odi, start_datetime, n_records, record_duration_s, n_signals, signal_label, fs_hz, phys_dim, phys_min, phys_max, dig_min, dig_max, prefilter, samp_per_record, study_type, scorers, nasal_pressure, etc.).
- **example_data**: one short value you saw in CONTEXT (e.g., "200.0", "uV", "PSG", "18.12").
- **proposed_definition**: 1 short sentence, include unit when relevant.
- No event timelines. No clinical interpretation. No extra text before/after the table.

---
CONTEXT:
{context}
---
QUESTION:
Build ONLY the required Markdown table (no other text).
"""

def ask(prompt: str) -> str:
    url = f"http://{HOST}:{PORT}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": NUM_CTX,
            "num_predict": int(os.getenv("NUM_PREDICT", "2048")),
            "temperature": 0.1,
            "top_p": 0.9,
            "repeat_penalty": 1.15,
        },
    }
    r = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json().get("response","").strip()

def file_to_context(p: Path, max_rows: int = 300) -> str:
    ext = p.suffix.lower()
    lines = []
    if ext == ".csv":
        lines = read_csv(p, max_rows)
    elif ext == ".xlsx":
        lines = read_xlsx(p, max_rows)
    elif ext == ".edf":
        lines = read_edf(p, max_rows)
    return "\n".join(lines)

def main(root="data/raw", out_path="outputs/metadata_catalog.md", max_rows=300):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    wrote_header = False

    with open(out_path, "w", encoding="utf-8") as fout:
        for p in sorted(Path(root).rglob("*.*")):
            if p.suffix.lower() not in (".csv",".xlsx",".edf"):
                continue
            ctx = file_to_context(p, max_rows)
            if not ctx.strip():
                continue
            prompt = PROMPT_TMPL.format(context=ctx)
            try:
                resp = ask(prompt)
            except Exception as e:
                print(f"# skip {p}: {e}", file=sys.stderr); continue

            # garde uniquement le tableau (skip texte parasite)
            lines = [ln for ln in resp.splitlines() if ln.strip()]
            # détecte le header du tableau
            try:
                start = next(i for i,l in enumerate(lines) if l.strip().startswith("| source |"))
            except StopIteration:
                # rien d'exploitable
                continue

            table = lines[start:]
            # écrit le header une seule fois
            if not wrote_header:
                fout.write("\n".join(table) + "\n")
                wrote_header = True
            else:
                # saute les 2 premières lignes du tableau (header + séparateur) pour éviter la redite
                fout.write("\n".join(table[2:]) + "\n")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
    out  = sys.argv[2] if len(sys.argv) > 2 else "outputs/metadata_catalog.md"
    maxr = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    main(root, out, maxr)
