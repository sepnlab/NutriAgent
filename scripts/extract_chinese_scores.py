"""Extract Chinese subset from PNKG-QA evaluation.json.

PNKG-QA evaluation.json is keyed by query_id with B-/no-prefix. Chinese queries
are filtered by query language.
"""
import json
import statistics
from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
LOG_DIR = ROOT / "logs" / "v1_full_eval_1782331340"

eval_data = json.loads((LOG_DIR / "evaluation.json").read_text(encoding="utf-8"))
responses = json.loads((LOG_DIR / "responses.json").read_text(encoding="utf-8"))

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
for species, prefix in [("broiler", "B-"), ("layer", "")]:
    qs = load_queries(ROOT / "queries" / species / "evaluation_queries_curated.json")
    for q in qs:
        if not isinstance(q, dict):
            continue
        qid = q.get("id", "")
        if qid:
            queries[f"{prefix}{qid}"] = q

# Get scores from evaluation.json
# evaluation.json structure: {method, model, query_count, scores: {v1: [{correctness, precision, scientific_depth, justification}, ...]}}
# The order should match the queries loaded in order
# Build ordered list of (qid, query) and look up scores
all_query_ids = []
for species, prefix in [("broiler", "B-"), ("layer", "")]:
    qs = load_queries(ROOT / "queries" / species / "evaluation_queries_curated.json")
    for q in qs:
        if not isinstance(q, dict):
            continue
        qid = q.get("id", "")
        if qid:
            all_query_ids.append(f"{prefix}{qid}")

scores_list = eval_data.get("scores", {}).get("v1", [])
print(f"Total scores entries: {len(scores_list)}")
print(f"Total query ids: {len(all_query_ids)}")

# Pair them
chinese_scores = {"correctness": [], "precision": [], "scientific_depth": []}
chinese_count = 0
for i, qid in enumerate(all_query_ids):
    if i >= len(scores_list):
        break
    q = queries.get(qid, {})
    lang = q.get("language", "en")
    score_entry = scores_list[i]
    if lang == "zh":
        chinese_count += 1
        for m in ["correctness", "precision", "scientific_depth"]:
            v = score_entry.get(m)
            if v is not None:
                chinese_scores[m].append(v)

print(f"\nChinese queries found: {chinese_count}")
print("\n--- Chinese Subset Performance ---")
for m in ["correctness", "precision", "scientific_depth"]:
    vals = chinese_scores[m]
    if vals:
        m_v = statistics.mean(vals)
        s_v = statistics.stdev(vals) if len(vals) > 1 else 0
        print(f"  {m}: {m_v:.2f} ± {s_v:.2f} (n={len(vals)})")

# Save
out = {
    "n_chinese_queries": chinese_count,
    "chinese_correctness_mean": round(statistics.mean(chinese_scores["correctness"]), 2) if chinese_scores["correctness"] else None,
    "chinese_correctness_std": round(statistics.stdev(chinese_scores["correctness"]), 2) if len(chinese_scores["correctness"]) > 1 else 0,
    "chinese_precision_mean": round(statistics.mean(chinese_scores["precision"]), 2) if chinese_scores["precision"] else None,
    "chinese_precision_std": round(statistics.stdev(chinese_scores["precision"]), 2) if len(chinese_scores["precision"]) > 1 else 0,
    "chinese_sci_depth_mean": round(statistics.mean(chinese_scores["scientific_depth"]), 2) if chinese_scores["scientific_depth"] else None,
    "chinese_sci_depth_std": round(statistics.stdev(chinese_scores["scientific_depth"]), 2) if len(chinese_scores["scientific_depth"]) > 1 else 0,
    "n_correctness": len(chinese_scores["correctness"]),
    "n_precision": len(chinese_scores["precision"]),
    "n_scientific_depth": len(chinese_scores["scientific_depth"]),
}
out_path = ROOT / "logs" / "chinese_subset_scores.json"
out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nSaved: {out_path}")
