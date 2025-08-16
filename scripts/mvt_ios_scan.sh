#!/usr/bin/env bash
# Usage: ./scripts/mvt_ios_scan.sh
set -euo pipefail

BACKUP_SRC=${BACKUP_SRC:-./backup}
BACKUP_PASS=${BACKUP_PASS:-}
DEC=${DEC:-./decrypted}
OUT=${OUT:-./mvt_out}
IOCS=${IOCS:-}

for dir in "$DEC" "$OUT"; do
    if [ -e "$dir" ]; then
        read -r -p "$dir exists. Overwrite? [y/N] " ans
        if [[ ! $ans =~ ^[Yy]$ ]]; then
            echo "Aborting."
            exit 1
        fi
        rm -rf "$dir"
    fi
    mkdir -p "$dir"
done

echo "Downloading latest public IOCs..."
mvt-ios download-iocs

echo "Decrypting backup from $BACKUP_SRC..."
if [ -n "$BACKUP_PASS" ]; then
    mvt-ios decrypt-backup -p "$BACKUP_PASS" -d "$DEC" "$BACKUP_SRC"
else
    mvt-ios decrypt-backup -d "$DEC" "$BACKUP_SRC"
fi

echo "Scanning decrypted backup..."
if [ -n "$IOCS" ]; then
    mvt-ios check-backup --output "$OUT" --iocs "$IOCS" "$DEC"
else
    mvt-ios check-backup --output "$OUT" "$DEC"
fi

echo "Results saved to $OUT"
