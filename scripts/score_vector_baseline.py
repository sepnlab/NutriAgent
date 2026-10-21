"""Score vector baseline responses using EvaluatorLLM (one response at a time)."""
import json
import sys
import time
from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
sys.path.insert(0, str(ROOT))

from src.evaluation.evaluator_llm import EvaluatorLLM

evaluator = EvaluatorLLM()

# Load queries
def load_queries(path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if "queries" in raw and isinstance(raw["queries"], list):
            return raw["queries"]
        out = []
        for v in raw.values():
            if isinstance(v, dict):
                out.append(v)
            elif isinstance(v, list):
                out.extend(x for x in v if isinstance(x, dict))
        return out
    return []

queries = {}
for species, prefix in [("broiler", "B-"), ("layer", "L-")]:
    qs = load_queries(ROOT / "queries" / species / "evaluation_queries_curated.json")
    for q in qs:
        if not isinstance(q, dict):
            continue
        qid = q.get("id", "")
        if qid:
            queries[f"{prefix}{qid}"] = q

print(f"Loaded {len(queries)} queries")

# Load vector baseline results
all_baseline = {}
for species in ["broiler", "layer"]:
    rfile = ROOT / "logs" / "rag_baseline" / f"{species}_k3.json"
    if not rfile.exists():
        print(f"Missing: {rfile}")
        continue
    data = json.loads(rfile.read_text(encoding="utf-8"))
    prefix = "B-" if species == "broiler" else "L-"
    for entry in data.get("per_query", []):
        qid = entry.get("query_id", "")
        # Always prefix with species
        if not qid.startswith(("B-", "L-")):
            qid = f"{prefix}{qid}"
        all_baseline[qid] = entry

print(f"Loaded {len(all_baseline)} baseline responses")

# Score each
scores = {}
start = time.time()
n_done = 0
for qid, query_data in queries.items():
    if qid not in all_baseline:
        continue
    response_text = all_baseline[qid].get("response", "")
    if not response_text:
        continue
    query_text = query_data.get("query", "")

    result = evaluator.score_responses(query_text, {"Vector-RAG": response_text})
    if result and "Vector-RAG" in result:
        scores[qid] = {
            "query": query_text,
            "response": response_text,
            "category": query_data.get("category", ""),
            "query_type": query_data.get("type", "single-value"),
            "species": query_data.get("species", species),
            "language": query_data.get("language", "en"),
            "correctness": result["Vector-RAG"].get("correctness"),
            "precision": result["Vector-RAG"].get("precision"),
            "scientific_depth": result["Vector-RAG"].get("scientific_depth"),
            "justification": result["Vector-RAG"].get("justification", ""),
            "prompt_tokens": all_baseline[qid].get("prompt_tokens", 0),
            "completion_tokens": all_baseline[qid].get("completion_tokens", 0),
            "elapsed_s": all_baseline[qid].get("elapsed_s", 0),
        }
    n_done += 1
    if n_done % 10 == 0:
        elapsed = time.time() - start
        rate = n_done / elapsed if elapsed > 0 else 0
        eta = (len(queries) - n_done) / rate if rate > 0 else 0
        print(f"  {n_done}/{len(queries)} scored ({rate:.1f}/s, ETA {eta:.0f}s)")

# Save
out_path = ROOT / "logs" / "rag_baseline" / "scored.json"
out_path.write_text(json.dumps({"scores": scores}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nScored {len(scores)} responses")
print(f"Saved: {out_path}")

# Summary
import statistics
def stats(metric):
    vals = [s[metric] for s in scores.values() if s[metric] is not None]
    if not vals:
        return None
    return {"mean": round(statistics.mean(vals), 2), "std": round(statistics.stdev(vals), 2) if len(vals) > 1 else 0, "n": len(vals)}

print("\n=== Vector-RAG Baseline Summary ===")
for m in ["correctness", "precision", "scientific_depth"]:
    s = stats(m)
    if s:
        print(f"  {m}: {s['mean']} ± {s['std']} (n={s['n']})")
