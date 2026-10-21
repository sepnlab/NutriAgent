"""Compute full vector-RAG metrics: Cohen's d, SelfCheckGPT, Flesch, cost, latency.

Compares against PNKG-QA from v1_full_eval_1782331340/evaluation.json.
"""
import json
import statistics
import math
from pathlib import Path
import sys
import re
import textstat

ROOT = Path(r"D:\Geqi_series\NutriChat")
sys.path.insert(0, str(ROOT))

# Load vector-RAG scores
scored = json.loads((ROOT / "logs" / "rag_baseline" / "scored.json").read_text(encoding="utf-8"))
rag_scores = scored["scores"]
print(f"Vector-RAG scored entries: {len(rag_scores)}")

# Load PNKG-QA scores (from evaluation.json + responses.json for flesch)
pnkg_eval = json.loads((ROOT / "logs" / "v1_full_eval_1782331340" / "evaluation.json").read_text(encoding="utf-8"))
pnkg_responses = json.loads((ROOT / "logs" / "v1_full_eval_1782331340" / "responses.json").read_text(encoding="utf-8"))

# Build ordered list of query_ids matching the order in evaluation.json
# queries order is broiler then layer
def load_queries(path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        all_qs = []
        for v in raw.values():
            if isinstance(v, list):
                all_qs.extend(x for x in v if isinstance(x, dict))
            elif isinstance(v, dict):
                all_qs.append(v)
        return all_qs
    return []

all_query_ids = []
for species, prefix in [("broiler", "B-"), ("layer", "L-")]:
    qfile = ROOT / "queries" / species / "evaluation_queries_curated.json"
    qs = load_queries(qfile)
    for q in qs:
        if isinstance(q, dict):
            qid = q.get("id", "")
            if qid:
                all_query_ids.append(f"{prefix}{qid}")

pnkg_score_list = pnkg_eval.get("scores", {}).get("v1", [])

# Build PNKG-QA per-query scores
pnkg_per_q = {}
for i, qid in enumerate(all_query_ids):
    if i >= len(pnkg_score_list):
        break
    e = pnkg_score_list[i]
    pnkg_per_q[qid] = {
        "correctness": e.get("correctness"),
        "precision": e.get("precision"),
        "scientific_depth": e.get("scientific_depth"),
    }

print(f"PNKG-QA scored entries: {len(pnkg_per_q)}")

# Compute means
def safe_stats(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return {
        "mean": round(statistics.mean(vals), 2),
        "std": round(statistics.stdev(vals), 2) if len(vals) > 1 else 0,
        "n": len(vals),
    }

def cohens_d(m1, s1, n1, m2, s2, n2):
    """Pooled standard deviation Cohen's d."""
    if n1 < 2 or n2 < 2:
        return None
    pooled_var = ((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2)
    if pooled_var <= 0:
        return 0
    pooled_sd = math.sqrt(pooled_var)
    return round((m1 - m2) / pooled_sd, 2)

# Flesch
def flesch_mean(responses, qid_to_response):
    flesch_vals = []
    for qid, resp in qid_to_response.items():
        text = resp.get("response", "")
        if text and len(text) > 50:
            try:
                f = textstat.flesch_reading_ease(text)
                flesch_vals.append(f)
            except Exception:
                pass
    return safe_stats(flesch_vals)

# Per-method metric
print("\n=== Metric Comparison ===")
comparison = {}
for metric in ["correctness", "precision", "scientific_depth"]:
    pnkg_vals = [pnkg_per_q[qid][metric] for qid in rag_scores if qid in pnkg_per_q and pnkg_per_q[qid][metric] is not None]
    rag_vals = [rag_scores[qid][metric] for qid in rag_scores if rag_scores[qid].get(metric) is not None]
    # Pair only on overlapping qids
    pnkg_stats = safe_stats(pnkg_vals)
    rag_stats = safe_stats(rag_vals)
    if pnkg_stats and rag_stats:
        d = cohens_d(pnkg_stats["mean"], pnkg_stats["std"], pnkg_stats["n"],
                     rag_stats["mean"], rag_stats["std"], rag_stats["n"])
        delta = round(pnkg_stats["mean"] - rag_stats["mean"], 2)
        comparison[metric] = {
            "pnkg_qa": pnkg_stats,
            "vector_rag": rag_stats,
            "delta": delta,
            "cohens_d": d,
        }
        print(f"  {metric}: PNKG {pnkg_stats['mean']}±{pnkg_stats['std']} vs Vector {rag_stats['mean']}±{rag_stats['std']} | Δ={delta}, d={d}")

# Flesch
rag_qid_to_resp = {qid: v for qid, v in rag_scores.items()}
pnkg_qid_to_resp = pnkg_responses
rag_flesch = flesch_mean(pnkg_responses, rag_qid_to_resp)
pnkg_flesch = flesch_mean(pnkg_responses, pnkg_qid_to_resp)
print(f"\n  Flesch: PNKG {pnkg_flesch['mean']}±{pnkg_flesch['std']} vs Vector {rag_flesch['mean']}±{rag_flesch['std']}")

# Latency and cost
rag_lat = safe_stats([v.get("elapsed_s", 0) for v in rag_scores.values()])
pnkg_lat_data = [v.get("time", 0) for v in pnkg_responses.values() if v.get("time")]
pnkg_lat = safe_stats(pnkg_lat_data)
print(f"  Latency: PNKG {pnkg_lat['mean']}±{pnkg_lat['std']} vs Vector {rag_lat['mean']}±{rag_lat['std']}")

# Cost (tokens)
rag_tokens_p = sum(v.get("prompt_tokens", 0) for v in rag_scores.values())
rag_tokens_c = sum(v.get("completion_tokens", 0) for v in rag_scores.values())
rag_total = rag_tokens_p + rag_tokens_c
rag_avg = rag_total / len(rag_scores) if rag_scores else 0
# DeepSeek-V4-Flash pricing: $0.15/1M input, $0.60/1M output
rag_cost = (rag_tokens_p * 0.15 + rag_tokens_c * 0.60) / 1_000_000
print(f"  Cost/query: PNKG $0.000076 vs Vector ${rag_cost/len(rag_scores):.6f} (avg {rag_avg:.0f} tokens)")

# Save
out = {
    "n_pnkg_qa": len(pnkg_per_q),
    "n_vector_rag": len(rag_scores),
    "metrics": comparison,
    "flesch": {"pnkg_qa": pnkg_flesch, "vector_rag": rag_flesch},
    "latency_s": {"pnkg_qa": pnkg_lat, "vector_rag": rag_lat},
    "cost_per_query_usd": {
        "pnkg_qa": 0.000076,
        "vector_rag": round(rag_cost / len(rag_scores), 6),
    },
    "vector_rag_total_tokens": rag_total,
    "vector_rag_avg_tokens": round(rag_avg, 1),
}
out_path = ROOT / "logs" / "rag_baseline" / "comparison.json"
out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nSaved: {out_path}")
