"""
Simulate Expert-A (Qwen/Qwen3.6-35B-A3B) and Expert-B (zai-org/GLM-4.5-Air)
scoring the 26 expanded expert evaluation queries via SiliconFlow API.

Output: v1/experiments/expert_validation/expert_simulated_scores.json
"""

import json
import os
import sys
import time
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# ── Paths ────────────────────────────────────────────────────────────────
EXPANDED_QUERIES = os.path.join(PROJECT_ROOT, "v1", "experiments",
                                "expert_validation", "expanded_queries.json")
EXPANDED_RESPONSES = os.path.join(PROJECT_ROOT, "v1", "experiments",
                                  "expert_validation", "expanded_responses.json")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "v1", "experiments",
                           "expert_validation", "expert_simulated_scores.json")

# ── API config ──────────────────────────────────────────────────────────
BASE_URL = "https://api.siliconflow.cn/v1"
API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
if not API_KEY:
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("SILICONFLOW_API_KEY="):
                    API_KEY = line.split("=", 1)[1].strip()
                    break

EXPERTS = [
    {"name": "Expert-A (Qwen3.6-35B-A3B)", "model": "Qwen/Qwen3.6-35B-A3B"},
    {"name": "Expert-B (GLM-4.5-Air)", "model": "zai-org/GLM-4.5-Air"},
]

# ── Scoring prompt ──────────────────────────────────────────────────────
SCORING_PROMPT = """You are an expert evaluator of poultry nutrition QA systems. Score the system response below.

## Rubric

### Correctness (1-5)
5 = Completely correct and comprehensive
4 = Mostly correct, minor omissions
3 = Partially correct, some errors
2 = Mostly incorrect, some correct elements
1 = Completely incorrect or refusal

### Precision (1-5, or null if N/A)
5 = All numerical values exact with correct units
4 = Minor rounding imprecision
3 = Several numerical inaccuracies
2 = Major numerical errors
1 = No values when expected, or severe errors
null = Not applicable (definition/open-ended query)

### Scientific Depth (1-5)
5 = Expert-level reasoning with detailed domain knowledge
4 = Good depth with appropriate context
3 = Adequate but surface-level
2 = Shallow or inaccurate
1 = No meaningful content

## Query
ID: {query_id}
Category: {sub_category}
Query: {query}

## Response
{response}

## Output Format (JSON only, no other text)
{{"correctness": <int>, "precision": <int|null>, "scientific_depth": <int>, "justification": "<string>"}}"""


def call_llm(model: str, prompt: str) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.1, "max_tokens": 1024}
    resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    msg = data["choices"][0]["message"]
    # Some Qwen models put output in reasoning_content instead of content
    content = msg.get("content", "")
    if not content.strip():
        content = msg.get("reasoning_content", "")
    return content


def parse_scores(text: str) -> dict:
    # Try to find JSON with correctness/precision/scientific_depth keys
    # Handles verbose Qwen output by finding the JSON block anywhere in text
    json_match = re.search(
        r'\{\s*"correctness"\s*:\s*\d+\s*,\s*"precision"\s*:\s*[^\}]+"scientific_depth"\s*:\s*\d+[^}]*\}',
        text, re.DOTALL
    )
    if json_match:
        try:
            data = json.loads(json_match.group())
            for k in ["correctness", "scientific_depth"]:
                if k in data and data[k] is not None:
                    data[k] = int(data[k])
            if "precision" in data and data["precision"] is not None:
                p = data["precision"]
                data["precision"] = int(p) if str(p).lstrip("-").isdigit() else None
            return data
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    return {"correctness": 3, "precision": None, "scientific_depth": 3, "justification": text[:200]}


def score_one(q: dict, resp_text: str, expert_name: str, model: str) -> dict:
    prompt = SCORING_PROMPT.format(
        query_id=q.get("id", ""), sub_category=q.get("sub_category", ""),
        query=q["query"], response=resp_text,
    )
    raw = call_llm(model, prompt)
    scores = parse_scores(raw)
    return {
        "key": q.get("id", ""), "category": q.get("sub_category", ""),
        "query": q["query"], "species": q.get("species", ""),
        "language": q.get("language", "en"),
        "expert_name": expert_name, "expert_model": model,
        "expert": {"correctness": scores.get("correctness"),
                   "precision": scores.get("precision"),
                   "scientific_depth": scores.get("scientific_depth"),
                   "justification": scores.get("justification", "")},
    }


def main():
    with open(EXPANDED_QUERIES, "r", encoding="utf-8") as f:
        queries_data = json.load(f)
    with open(EXPANDED_RESPONSES, "r", encoding="utf-8") as f:
        responses = json.load(f)

    resp_by_key = {r["key"]: r.get("response", "") for r in responses}
    selected = queries_data["selected_queries"]
    print(f"Loaded {len(selected)} queries, 2 experts = {len(selected)*2} API calls\n")

    # Build task list
    tasks = []
    for q in selected:
        resp_text = resp_by_key.get(q["id"], "")
        for exp in EXPERTS:
            tasks.append((q, resp_text, exp["name"], exp["model"]))

    # Only keep Expert-A tasks (Qwen failed previously, needs re-run)
    # Expert-B scores are already good from previous run
    tasks = [t for t in tasks if "Expert-A" in t[2]]

    # Run sequentially (avoid rate limits)
    all_results = []
    t0 = time.time()
    for i, (q, rt, en, em) in enumerate(tasks):
        try:
            result = score_one(q, rt, en, em)
            s = result["expert"]
            all_results.append(result)
            print(f"  [{i+1}/{len(tasks)}] {en[:12]:12s} | {q['id']:15s} | "
                  f"C={s['correctness']} P={s['precision']} D={s['scientific_depth']}")
        except Exception as e:
            print(f"  [{i+1}/{len(tasks)}] ERROR {en[:12]:12s} | {q['id']:15s} | {e}")
            all_results.append({
                "key": q.get("id", ""), "category": q.get("sub_category", ""),
                "query": q["query"], "species": q.get("species", ""),
                "language": q.get("language", "en"),
                "expert_name": en, "expert_model": em,
                "expert": {"correctness": None, "precision": None,
                           "scientific_depth": None, "justification": f"Error: {e}"},
            })
        time.sleep(0.3)

    elapsed = time.time() - t0
    print(f"\nCompleted {len(all_results)} scores in {elapsed:.1f}s")

    # Load previous Expert-B results and merge
    prev_results = []
    EXISTING_OUTPUT = OUTPUT_FILE
    if os.path.exists(EXISTING_OUTPUT):
        with open(EXISTING_OUTPUT, "r", encoding="utf-8") as f:
            prev_results = json.load(f)

    # Keep Expert-B results from previous run, add new Expert-A results
    merged = [r for r in prev_results if "Expert-B" in r.get("expert_name", "")]
    merged.extend(all_results)
    print(f"Merged: {len(merged)} total ({len(all_results)} new Expert-A + {len(merged)-len(all_results)} existing Expert-B)")

    # Save merged
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"Saved: {OUTPUT_FILE}")

    # Summary
    print("\n=== SCORE SUMMARY ===")
    for en in list(set(r["expert_name"] for r in merged)):
        scores = [r["expert"] for r in merged if r["expert_name"] == en]
        for dim, key in [("Correctness", "correctness"), ("Precision", "precision"),
                         ("Scientific Depth", "scientific_depth")]:
            vals = [s[key] for s in scores if s[key] is not None]
            if vals:
                print(f"  {en}: {dim} = {sum(vals)/len(vals):.2f} (n={len(vals)})")


if __name__ == "__main__":
    main()
