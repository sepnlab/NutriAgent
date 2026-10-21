"""
Generate PNKG-QA responses for expanded expert evaluation queries.

Most responses already exist in logs/v1_full_eval_1782309578/responses.json.
Only generates for queries not found there.

Usage:
    python scripts/run_expanded_expert_queries.py

Output:
    v1/experiments/expert_validation/expanded_responses.json
"""

import json
import os
import sys
import time
import logging

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ── Paths ────────────────────────────────────────────────────────────────
QUERIES_FILE = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expanded_queries.json",
)
EXISTING_RESPONSES = os.path.join(
    PROJECT_ROOT, "logs", "v1_full_eval_1782309578", "responses.json",
)
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expanded_responses.json",
)


def main():
    # ── 1. Load expanded queries ──
    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    selected = data["selected_queries"]
    logger.info(f"Loaded {len(selected)} queries to process")

    # ── 2. Load existing responses ──
    existing = {}
    if os.path.exists(EXISTING_RESPONSES):
        with open(EXISTING_RESPONSES, "r", encoding="utf-8") as f:
            existing = json.load(f)
        logger.info(f"Loaded {len(existing)} existing responses from {EXISTING_RESPONSES}")

    # ── 3. Separate cached and new queries ──
    cached = []
    new_queries = []
    for q in selected:
        qid = q["id"]
        if qid in existing:
            cached.append(q)
        else:
            new_queries.append(q)

    logger.info(f"Cached: {len(cached)} queries (can extract responses)")
    logger.info(f"Need to generate: {len(new_queries)} queries")

    # ── 4. Generate responses for new queries ──
    new_responses = {}
    if new_queries:
        from v1.src.knowledge_graph.graph_store import PNKGStore
        from v1.src.agent.kg_multi_agent import KGMultiAgentEngine

        kg_path = os.path.join(PROJECT_ROOT, "v1", "data", "pnkg.json")
        if os.path.exists(kg_path):
            logger.info(f"Loading PNKG from {kg_path}")
            store = PNKGStore()
            store.load(kg_path)
        else:
            logger.info("Building PNKG from CSV data...")
            store = PNKGStore()

        engine = KGMultiAgentEngine(pnkg=store, verbose=False)
        logger.info("Engine initialized")

        query_texts = [q["query"] for q in new_queries]
        logger.info(f"Running {len(query_texts)} new queries through PNKG-QA...")
        t0 = time.time()
        responses = engine.answer_batch(query_texts, n_workers=2)
        elapsed = time.time() - t0
        logger.info(f"Completed in {elapsed:.1f}s ({elapsed/len(query_texts):.1f}s/query avg)")

        for q, resp in zip(new_queries, responses):
            new_responses[q["id"]] = {
                "query": q["query"],
                "response": resp.get("response", resp.get("text", "")),
                "steps": resp.get("steps", []),
                "tools_used": resp.get("tools_used", []),
                "latency_s": resp.get("latency_s", None),
            }

    # ── 5. Assemble final output ──
    output = []
    for q in selected:
        qid = q["id"]
        # Prefer existing, fall back to newly generated, else empty
        if qid in existing:
            raw = existing[qid]
            resp_text = raw.get("response", raw.get("text", "")) if isinstance(raw, dict) else str(raw)
            entry = {
                "key": qid,
                "category": q.get("category", ""),
                "query": q["query"],
                "species": q["species"],
                "language": q.get("language", "en"),
                "response": resp_text,
                "latency_s": raw.get("latency_s") if isinstance(raw, dict) else None,
            }
        elif qid in new_responses:
            nr = new_responses[qid]
            entry = {
                "key": qid,
                "category": q.get("category", ""),
                "query": q["query"],
                "species": q["species"],
                "language": q.get("language", "en"),
                "response": nr["response"],
                "latency_s": nr["latency_s"],
            }
        else:
            entry = {
                "key": qid,
                "category": q.get("category", ""),
                "query": q["query"],
                "species": q["species"],
                "language": q.get("language", "en"),
                "response": "",
                "warning": "no response available",
            }
        output.append(entry)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(output)} responses to {OUTPUT_FILE}")

    # Quality check
    empty = [r for r in output if not r.get("response", "").strip()]
    if empty:
        logger.warning(f"{len(empty)}/{len(output)} responses are empty: {[r['key'] for r in empty]}")
    else:
        logger.info("All responses non-empty!")


if __name__ == "__main__":
    main()
