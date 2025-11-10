#!/usr/bin/env python3
import sys
from pathlib import Path
import mne


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/edf_info.py <path_to_edf>")
        sys.exit(1)

    edf_path = Path(sys.argv[1])

    if not edf_path.is_file():
        print(f"Error: EDF file not found: {edf_path}")
        sys.exit(1)

    print(f"Loading EDF file: {edf_path}")
    # preload=False suffit pour lire les métadonnées rapidement
    raw = mne.io.read_raw_edf(str(edf_path), preload=False, verbose="ERROR")

    # Meta de base
    sfreq = raw.info["sfreq"]
    n_channels = raw.info["nchan"]
    n_samples = raw.n_times
    duration_sec = n_samples / sfreq if sfreq else 0

    print("\n=== META INFO (synthèse) ===")
    print(f"Channels count : {n_channels}")
    print(f"Channels names : {raw.ch_names}")
    print(f"Sampling freq  : {sfreq} Hz")
    print(f"Samples count  : {n_samples}")
    print(f"Duration       : {duration_sec:.2f} s")

    print("\n=== RAW.INFO (complet) ===")
    print(raw.info)


if __name__ == "__main__":
    main()
