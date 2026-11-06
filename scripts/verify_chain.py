#!/usr/bin/env python3
"""Recomputes every hash in chain.json and reports the first entry that doesn't match."""
import hashlib
import json
import sys
from pathlib import Path

chain = json.loads((Path(__file__).resolve().parent.parent / "chain.json").read_text())
prev = "0" * 64
for n, entry in enumerate(chain, 1):
    digest = hashlib.sha256(f'{prev}\n{entry["text"]}'.encode()).hexdigest()
    if entry["prev"] != prev or entry["hash"] != digest:
        sys.exit(f"Entry {n} is broken: its contents or link no longer match its hash.")
    prev = digest
print(f"All {len(chain)} entries verified. Latest hash: {prev}")
