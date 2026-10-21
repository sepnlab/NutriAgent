"""Inspect scored.json structure."""
import json
from pathlib import Path

d = json.loads(Path(r"D:\Geqi_series\NutriChat\logs\rag_baseline\scored.json").read_text(encoding="utf-8"))
s = d["scores"]
print(f"Total entries: {len(s)}")
for k, v in list(s.items())[:3]:
    print(f"\n{k}:")
    print(f"  species: {v.get('species')}")
    print(f"  query: {v.get('query', '')[:80]}")
    print(f"  category: {v.get('category')}")
    print(f"  correctness: {v.get('correctness')}")
print("\n--- Last 3 ---")
for k, v in list(s.items())[-3:]:
    print(f"\n{k}:")
    print(f"  species: {v.get('species')}")
    print(f"  query: {v.get('query', '')[:80]}")
