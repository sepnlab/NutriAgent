"""E11: bilingual breakdown of the Rev.1 NutriAgent auto scores.

Uses the per-query EvaluatorLLM scores in e18_rescored.json and the curated
query metadata. This is an automated-score analysis, not the expert score; the
12 Chinese queries are confounded with breed and data coverage.

Usage:
    python scripts/paper/bilingual_auto.py
"""

from __future__ import annotations

import json
import random
import statistics
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCORES = PROJECT_ROOT / "docs" / "paper" / "audit" / "e18_rescored.json"
QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e11_bilingual_auto.json"


def bootstrap_ci(values: list[float], n_boot: int = 10000, seed: int = 42) -> tuple[float, float]:
    rng = random.Random(seed)
    means = []
    for _ in range(n_boot):
        sample = [rng.choice(values) for _ in values]
        means.append(sum(sample) / len(sample))
    means.sort()
    return means[int(0.025 * n_boot)], means[int(0.975 * n_boot)]


def main() -> None:
    scores = json.loads(SCORES.read_text(encoding="utf-8"))
    model = next(iter(scores))
    per_query = {row["id"]: row for row in scores[model]["per_query"]}

    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    queries = [dict(q, category=cat) for cat, items in data.items() for q in items]
    language = {q["id"]: q.get("language", "en") for q in queries}

    groups: dict[str, dict[str, list[float]]] = {"en": {}, "zh": {}}
    for qid, row in per_query.items():
        lang = language.get(qid, "en")
        for metric in ("correctness", "precision", "scientific_depth"):
            val = row.get(metric)
            if isinstance(val, (int, float)):
                groups[lang].setdefault(metric, []).append(float(val))

    summary = {}
    for lang, metrics in groups.items():
        summary[lang] = {}
        for metric, vals in metrics.items():
            lo, hi = bootstrap_ci(vals)
            summary[lang][metric] = {
                "mean": round(statistics.mean(vals), 3),
                "sd": round(statistics.stdev(vals), 3) if len(vals) > 1 else 0.0,
                "n": len(vals),
                "ci95": [round(lo, 3), round(hi, 3)],
            }

    diffs = {}
    for metric in ("correctness", "precision", "scientific_depth"):
        zh = groups["zh"].get(metric, [])
        en = groups["en"].get(metric, [])
        if zh and en:
            diffs[metric] = round(statistics.mean(zh) - statistics.mean(en), 3)

    outcome = {"summary": summary, "zh_minus_en": diffs}
    OUT.write_text(json.dumps(outcome, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# E11: bilingual breakdown (automated scores)",
        "",
        "NutriAgent, MiMo-V2.5-Pro absolute scores, single run. Chinese n=12, English n=42; language is confounded with breed and data coverage.",
        "",
        "| Language | Metric | Mean | SD | n | 95% bootstrap CI |",
        "|---|---|---:|---:|---:|---|",
    ]
    for lang in ("en", "zh"):
        for metric, s in summary[lang].items():
            md.append(
                f"| {lang} | {metric} | {s['mean']} | {s['sd']} | {s['n']} | "
                f"[{s['ci95'][0]}, {s['ci95'][1]}] |"
            )
    md += ["", "Chinese minus English: " + ", ".join(f"{k} = {v}" for k, v in diffs.items())]
    OUT.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(outcome, indent=2))


if __name__ == "__main__":
    main()
