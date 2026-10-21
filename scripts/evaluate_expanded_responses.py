"""
Run EvaluatorLLM (DeepSeek-V4-Pro) on the 22 new expanded responses.

Output: v1/experiments/expert_validation/evaluator_new_scores.json
"""

import json
import os
import sys
import time
import re
import requests

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

RESPONSES = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                          "expanded_responses.json")
EXPANDED = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                         "expanded_queries.json")
OUTPUT = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                       "evaluator_new_scores.json")
COMBINED = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                         "expert_combined_scores.json")

# DeepSeek config
DEEPSEEK_API_KEY = ""
env_path = os.path.join(PROJECT_ROOT, ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("DEEPSEEK_API_KEY="):
                DEEPSEEK_API_KEY = line.split("=", 1)[1].strip()
                break

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-v4-pro"

SCORING_PROMPT = """You are an expert evaluator of poultry nutrition question-answering systems. Score the system's response on three criteria.

## Rubric

### Correctness (1-5)
5 = All facts accurate, directly answers the query
4 = Mostly accurate with minor imprecision
3 = Partially correct with noticeable errors
2 = Several factual errors or largely off-topic
1 = Completely incorrect or refusal

### Precision (1-5, null if N/A)
5 = Exact point estimate matching reference value
4 = Close estimate with minor rounding
3 = Directionally correct but off
2 = Vague or inaccurate numeric
1 = No numeric when expected, or severe errors
null = Definition/terminology query (no numerical value)

### Scientific Depth (1-5)
5 = Expert-level reasoning with detailed domain knowledge
4 = Good domain knowledge with relevant context
3 = Adequate but surface-level
2 = Superficial, minimal insight
1 = No scientific content

## Query
{query}

## System Response
{response}

## Output Format (JSON ONLY)
{{"correctness": <int>, "precision": <int|null>, "scientific_depth": <int>, "justification": "<string>"}}"""


def call_evaluator(query: str, response: str) -> dict:
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    prompt = SCORING_PROMPT.format(query=query, response=response)
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.0, "max_tokens": 1024}
    resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]

    # Extract JSON
    m = re.search(r'\{\s*"correctness"\s*:\s*\d+\s*,\s*"precision"\s*:\s*[^,]+,\s*"scientific_depth"\s*:\s*\d+[^}]*\}', content, re.DOTALL)
    if m:
        try:
            scores = json.loads(m.group())
            for k in ["correctness", "scientific_depth"]:
                if k in scores and scores[k] is not None:
                    scores[k] = int(scores[k])
            if scores.get("precision") is not None:
                scores["precision"] = int(scores["precision"])
            return scores
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    return {"correctness": None, "precision": None, "scientific_depth": None, "justification": "parse error"}


def main():
    with open(RESPONSES, "r", encoding="utf-8") as f:
        responses = json.load(f)
    with open(EXPANDED, "r", encoding="utf-8") as f:
        expanded = json.load(f)

    # Build lookup for query metadata (to get query text)
    query_by_key = {q["id"]: q["query"] for q in expanded["selected_queries"]}
    resp_by_key = {r["key"]: r for r in responses}

    print(f"Loaded {len(resp_by_key)} responses to evaluate")

    results = {}
    t0 = time.time()
    for i, (key, resp) in enumerate(sorted(resp_by_key.items())):
        query = query_by_key.get(key, resp.get("query", ""))
        response_text = resp.get("response", "")

        if not response_text:
            print(f"  [{i+1}/{len(resp_by_key)}] {key}: empty response, skipping")
            results[key] = {"correctness": None, "precision": None, "scientific_depth": None,
                           "justification": "empty response"}
            continue

        try:
            scores = call_evaluator(query, response_text)
            results[key] = scores
            print(f"  [{i+1}/{len(resp_by_key)}] {key:15s} | C={scores.get('correctness')} "
                  f"P={scores.get('precision')} D={scores.get('scientific_depth')}")
        except Exception as e:
            print(f"  [{i+1}/{len(resp_by_key)}] {key}: ERROR {e}")
            results[key] = {"correctness": None, "precision": None, "scientific_depth": None,
                           "justification": f"error: {e}"}
        time.sleep(0.5)

    elapsed = time.time() - t0
    print(f"\nCompleted {len(results)} evaluations in {elapsed:.1f}s")

    # Save
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {OUTPUT}")

    # Summary
    for dim, dk in [("Correctness", "correctness"), ("Precision", "precision"), ("Scientific Depth", "scientific_depth")]:
        vals = [v[dk] for v in results.values() if v[dk] is not None]
        if vals:
            print(f"  EvaluatorLLM {dim}: {sum(vals)/len(vals):.2f} (n={len(vals)})")

    # Merge into combined scores file
    with open(COMBINED, "r", encoding="utf-8") as f:
        combined = json.load(f)

    # Add evaluator scores to original entries (if not already present)
    added = 0
    for r in combined:
        key = r["key"]
        if key in results and (r.get("evaluator_correctness") is None or r.get("evaluator_correctness") == "null"):
            r["evaluator_correctness"] = results[key].get("correctness")
            r["evaluator_precision"] = results[key].get("precision")
            r["evaluator_scientific_depth"] = results[key].get("scientific_depth")
            added += 1

    with open(COMBINED, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Updated {added} entries in {COMBINED}")


if __name__ == "__main__":
    main()
