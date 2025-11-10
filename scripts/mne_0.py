import sys
from pathlib import Path
import mne

# Usage: python3 scripts/mne_print.py data/raw/ton_fichier.edf

if len(sys.argv) < 2:
    raise SystemExit("Usage: python3 scripts/mne_print.py <edf_path>")

edf_path = Path(sys.argv[1])

if not edf_path.is_file():
    raise SystemExit(f"EDF file not found: {edf_path}")

print(f"Loading EDF: {edf_path}")
raw = mne.io.read_raw_edf(str(edf_path), preload=True, verbose=True)

print("\n=== RAW OBJECT ===")
print(raw)

print("\n=== META INFO ===")
print(f"Channels      : {len(raw.ch_names)}")
print(f"Channel names : {raw.ch_names}")
print(f"Sampling freq : {raw.info['sfreq']} Hz")
print(f"Nb samples    : {raw.n_times}")
print(f"Duration      : {raw.n_times / raw.info['sfreq']:.2f} s")

if raw.annotations:
    print("\n=== ANNOTATIONS ===")
    for ann in raw.annotations:
        print(f"- {ann['onset']:.2f}s / {ann['duration']:.2f}s : {ann['description']}")
