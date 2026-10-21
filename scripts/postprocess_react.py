"""Post-process ReAct baseline responses: extract cleaner final answers.

Two issues to fix:
1. Some responses contain "Thought: ..." / "Action: ..." prefixes (LLM didn't follow
   the "Final Answer:" format). Strip these prefixes to expose the actual answer.
2. Re-count "context does not contain sufficient data" rate to report.

Usage:
    python scripts/postprocess_react.py
"""
import json
import re

INSUFFICIENT_PATTERNS = [
    r"the provided context does not contain sufficient data",
    r"the provided data does not contain",
    r"insufficient data",
    r"insufficient information",
    r"not enough (?:data|information)",
]


def clean_response(text: str) -> str:
    if not text:
        return text
    m = re.search(r"Final Answer\s*:\s*(.+?)(?:\n\s*\n|\Z)", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    stripped = re.sub(r"^(Thought|Action|Observation)\s*:.*?\n", "", text, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)
    stripped = re.sub(r"\n(Thought|Action|Observation)\s*:.*?(?=\n|$)", "", stripped, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)
    stripped = stripped.strip()
    return stripped if stripped else text


def is_insufficient(text: str) -> bool:
    if not text:
        return True
    lower = text.lower()
    return any(re.search(p, lower) for p in INSUFFICIENT_PATTERNS)


def process_file(in_path: str, out_path: str) -> dict:
    with open(in_path, encoding="utf-8") as f:
        data = json.load(f)

    n = len(data["per_query"])
    n_insufficient = 0
    n_cleaned = 0
    for r in data["per_query"]:
        orig = r["response"]
        cleaned = clean_response(orig)
        if cleaned != orig:
            n_cleaned += 1
            r["response"] = cleaned
        if is_insufficient(cleaned):
            n_insufficient += 1

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "file": in_path,
        "n_queries": n,
        "n_cleaned": n_cleaned,
        "n_insufficient": n_insufficient,
        "pct_insufficient": round(100.0 * n_insufficient / max(n, 1), 1),
    }


if __name__ == "__main__":
    import os
    for species in ("broiler", "layer"):
        in_p = f"logs/react_{species}.json"
        out_p = f"logs/react_{species}_clean.json"
        if not os.path.exists(in_p):
            print(f"SKIP {in_p} (not found)")
            continue
        result = process_file(in_p, out_p)
        print(result)
    print("\nDone. Use *_clean.json for downstream scoring.")
