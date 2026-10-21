"""Wrap kg_vs_vector_baseline outputs into --score-from compatible format."""
import json, os, sys
from pathlib import Path

species = sys.argv[1]
input_path = f"logs/rag_baseline_{species}_k10.json"
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Load queries to get expected_value
query_file = f"queries/{species}/evaluation_queries_curated.json"
with open(query_file, "r", encoding="utf-8") as f:
    raw = json.load(f)

# Build query lookup by id
query_map = {}
for cat, qs in raw.items():
    for q in qs:
        query_map[q.get("id", q.get("query", ""))] = q

# Build queries list and responses
queries = []
responses = []
for item in data["per_query"]:
    qid = item["query_id"]
    qdata = query_map.get(qid, {})
    queries.append({
        "id": qid,
        "category": qdata.get("category", item.get("category", "")),
        "type": qdata.get("type", item.get("query_type", "")),
        "query": item["query"],
        "expected_value": qdata.get("answer", qdata.get("expected_value")),
    })
    responses.append(item["response"])

log_dir = f"logs/rag_scored_{species}_k10"
os.makedirs(log_dir, exist_ok=True)

out = {
    "timestamp": "2026-06-29T12:15:00",
    "num_queries": len(queries),
    "models": [f"Vector-RAG (k=10, {species})"],
    "queries": queries,
    "responses": {f"Vector-RAG (k=10, {species})": responses},
}
with open(os.path.join(log_dir, "responses.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"Wrapped {len(queries)} queries -> {log_dir}/responses.json")
