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

Goal
- Build a metadata dictionary: **list field names (metadata), not data rows**.
- Use ONLY what is visible in CONTEXT; if unknown, write "—".
- Output a **single Markdown table** and nothing else.

Definitions (use internally, do not print):
- *Metadata field* = a schema element (column name, header key, EDF header key, or EDF per-signal attribute like label, fs_hz, phys_dim). It is **not** a timestamped event or a data record.

Scope to extract
- CSV/XLSX: take **column headers only** as metadata field names.
- EDF header (global): version, patient_id, recording_id, startdate, starttime, header_bytes, n_records, record_duration_s, n_signals, etc. (whatever is present in CONTEXT).
- EDF signals (per channel): label, transducer, phys_dim, phys_min, phys_max, dig_min, dig_max, prefilter, samp_per_record, fs_hz.

Hard constraints
- **Do NOT list rows of measurements or timelines** (no “start/end/duration” event lines).
- **Deduplicate** logically equivalent fields (normalize names).
- Normalize **metadata_field** to lower_snake_case (e.g., apnea_hypopnea_index for AHI).
- For **example_data**, provide **one short representative value** if the field appears with a value in CONTEXT; otherwise "—".
- Keep **technical**, concise **proposed_definition** (add unit if visible).
- No prose before/after the table. Output the table only.

OUTPUT (print this table only):
| source | metadata_field | example_data | proposed_definition |

- **source** ∈ {{csv,xlsx,edf_header,edf_signal}}.
- Each row = one distinct metadata field discovered in CONTEXT.

---
CONTEXT:
{context}
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
