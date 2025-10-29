import os, sys, json, requests

MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
HOST  = os.getenv("OLLAMA_HOST", "127.0.0.1")
PORT  = os.getenv("OLLAMA_PORT", "11434")

# Lis la fenêtre souhaitée depuis l'env, sinon 8192
NUM_CTX = int(os.getenv("NUM_CTX", "8192"))

PROMPT_TMPL = """Tu es un Data Architect spécialisé en santé et en analyses du sommeil (PSG/EDF).
Ta mission : à partir du CONTEXTE ci-dessous (extraits texte déjà lus depuis des CSV/XLSX/EDF sous data/),
construire une extraction de MÉTADONNÉES sous forme de tableau.

RÈGLES GÉNÉRALES
- Tu ne peux PAS parcourir des fichiers ni ouvrir des chemins : tu utilises UNIQUEMENT le texte du CONTEXTE.
- Déduis/normalise la métadonnée depuis les lignes fournies (ex. "file=... row=... | col=val | ...", entêtes EDF, labels de canaux, fs_hz, unités, etc.).
- Concentre-toi sur les éléments stables et utiles à un data catalog (source, nom de champ, unité, range, typologie, remarque qualité).
- Évite les doublons (normalise les libellés proches : ex. AHI / ahi).
- Si une info est absente, mets "—".
- Prudence RGPD/PII : si un champ ressemble à de l’identifiant patient, note-le.

SORTIE ATTENDUE (Markdown)
Un tableau avec EXACTEMENT ces colonnes :
| source | champ_metadata | exemple_donnees | proposition_definition |

Définitions de colonnes :
- source : nom de fichier ou bloc (ex. PANDORE_SAS_DATASET_Metadata.csv, S0001_PSG.edf:edf_header, S0001_PSG.edf:edf_signal:EEG F3).
- champ_metadata : nom normalisé de la métadonnée (ex. ahi, odi, start_datetime, signal_label, fs_hz, phys_dim, prefilter, n_records, record_duration_s).
- exemple_donnees : une ou deux valeurs représentatives vues dans le CONTEXTE.
- proposition_definition : ta définition claire et opérationnelle (1–2 phrases), incluant unité/portée si pertinent.

EXEMPLES (indicatifs)
- Pour CSV/XLSX : "ahi", "odi", "start_time", "study_type", "nasal_pressure".
- Pour EDF header : "startdate", "starttime" → proposer "start_datetime", "n_records", "record_duration_s", "n_signals".
- Pour EDF signals : "label", "phys_dim", "fs_hz", "prefilter", "dig_min/max", "phys_min/max", "samp_per_record".

FORMAT FINAL UNIQUEMENT : le tableau Markdown demandé. Aucune intro ni conclusion.

---
CONTEXTE :
{context}
---
QUESTION :
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
