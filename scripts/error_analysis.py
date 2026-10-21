"""Error analysis for NutriCHAT evaluation results.

Loads saved responses from a log directory and identifies:
1. Queries with largest score gap between methods (best/worst for Multi-Agent)
2. High-hallucination queries (lowest faithfulness / highest SelfCheck)
3. Query types / categories where each method systematically underperforms
4. Representative examples for paper discussion section

Usage:
    python scripts/error_analysis.py logs/log_20260522_144831/
    python scripts/error_analysis.py logs/log_20260522_144831/ --top-k 20 --output analysis.md
    python scripts/error_analysis.py logs/log_20260522_144831/ --compare NutriCHAT vs Hunyuan-A13B
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def load_log_data(log_dir: str) -> dict:
    """Load responses.json and optional step traces from a log directory."""
    responses_path = os.path.join(log_dir, "responses.json")
    if not os.path.exists(responses_path):
        raise FileNotFoundError(f"No responses.json found at {responses_path}")

    with open(responses_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Load step traces if available
    step_traces = {}
    for suffix in ["", "_single", "_multi"]:
        path = os.path.join(log_dir, f"step_traces{suffix}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                step_traces[suffix or "default"] = json.load(f)

    # Load report if available
    report_path = os.path.join(log_dir, "report.json")
    report = {}
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)

    return {
        "queries": data.get("queries", []),
        "responses": data.get("responses", {}),
        "models": data.get("models", list(data.get("responses", {}).keys())),
        "step_traces": step_traces,
        "report": report,
        "log_dir": log_dir,
    }


def compute_flesch(text: str) -> float:
    """Flesch Reading Ease Score (0-100). Delegates to evaluator module."""
    from src.evaluation.evaluator import compute_flesch as _compute_flesch
    result = _compute_flesch(text)
    return result if result is not None else 0.0


def compute_faithfulness(response: str, steps: list) -> Optional[float]:
    """Quick faithfulness estimate: fraction of numeric claims supported by tool data."""
    from src.evaluation.faithfulness import compute_faithfulness_from_steps
    return compute_faithfulness_from_steps(response, steps)


def check_tolerance_prediction(response: str, ground_truth: float) -> Tuple[bool, bool]:
    """Check ±2% and ±5% tolerance. Returns (pass_2pct, pass_5pct)."""
    values = _parse_numeric(response)
    if not values:
        return False, False
    best = min(values, key=lambda x: abs(x[0] - ground_truth))
    return _within_tolerance(best[0], ground_truth, 0.02), _within_tolerance(best[0], ground_truth, 0.05)


def _parse_numeric(text: str) -> List[Tuple[float, bool]]:
    """Extract numeric values from text. Delegates to evaluator module."""
    from src.evaluation.evaluator import parse_numeric
    return parse_numeric(text)


def _within_tolerance(predicted: float, ground_truth: float, tol: float) -> bool:
    lower = predicted * (1 - tol)
    upper = predicted * (1 + tol)
    return lower <= ground_truth <= upper


def compute_per_query_metrics(data: dict) -> List[dict]:
    """Compute per-query metrics (Flesch, tolerance, faithfulness, response length)."""
    queries = data["queries"]
    responses = data["responses"]
    models = data["models"]
    step_traces = data.get("step_traces", {})

    # Build step traces lookup: trace_id -> steps list
    trace_map = {}
    for suffix, traces in step_traces.items():
        for t in traces:
            trace_map[t.get("id", "")] = t.get("steps", [])

    per_query = []
    for i, q in enumerate(queries):
        entry = {
            "id": q.get("id", f"q{i}"),
            "query": q.get("query", ""),
            "category": q.get("category", ""),
            "type": q.get("type", ""),
            "expected_value": q.get("expected_value"),
            "metrics": {},
        }
        for m in models:
            resp = responses.get(m, [""] * len(queries))[i] if i < len(responses.get(m, [])) else ""
            flesch = compute_flesch(resp)
            tol2, tol5 = False, False
            if q.get("expected_value") is not None:
                tol2, tol5 = check_tolerance_prediction(resp, q["expected_value"])

            faithfulness = None
            semantic_faithfulness = None
            if step_traces:
                steps = trace_map.get(q.get("id", f"q{i}"), [])
                if steps:
                    try:
                        faithfulness = compute_faithfulness(resp, steps)
                    except Exception:
                        pass
                    try:
                        from src.evaluation.faithfulness import compute_semantic_faithfulness
                        sem_score = compute_semantic_faithfulness(resp, steps)
                        if sem_score is not None:
                            semantic_faithfulness = sem_score
                    except Exception:
                        pass

            entry["metrics"][m] = {
                "text": resp,
                "length": len(resp),
                "word_count": len(resp.split()),
                "flesch": flesch,
                "tolerance_p2": tol2,
                "tolerance_p5": tol5,
                "faithfulness": faithfulness,
                "faithfulness_semantic": semantic_faithfulness,
                "has_numeric": len(_parse_numeric(resp)) > 0,
            }
        per_query.append(entry)
    return per_query


def find_top_disagreements(
    per_query: List[dict],
    method_a: str,
    method_b: str,
    metric: str = "flesch",
    top_k: int = 10,
) -> List[dict]:
    """Find queries where method_a and method_b differ most on a metric.

    Returns top_k entries sorted by absolute difference, with method_a's
    metrics as the reference (positive diff = method_a wins).
    """
    scored = []
    for pq in per_query:
        a_val = pq["metrics"].get(method_a, {}).get(metric)
        b_val = pq["metrics"].get(method_b, {}).get(metric)
        if a_val is not None and b_val is not None:
            scored.append({
                "id": pq["id"],
                "query": pq["query"],
                "category": pq["category"],
                "type": pq["type"],
                "a_value": a_val,
                "b_value": b_val,
                "diff": a_val - b_val,
                "abs_diff": abs(a_val - b_val),
            })
    scored.sort(key=lambda x: x["abs_diff"], reverse=True)
    return scored[:top_k]


def find_lowest_performers(
    per_query: List[dict],
    method: str,
    metric: str = "faithfulness",
    top_k: int = 10,
) -> List[dict]:
    """Find queries where a method scores lowest on a metric."""
    scored = []
    for pq in per_query:
        val = pq["metrics"].get(method, {}).get(metric)
        if val is not None:
            scored.append({
                "id": pq["id"],
                "query": pq["query"],
                "category": pq["category"],
                "type": pq["type"],
                "value": val,
            })
    scored.sort(key=lambda x: x["value"])
    return scored[:top_k]


def group_by_category(per_query: List[dict], models: List[str]) -> dict:
    """Compute average metrics grouped by query category and type."""
    groups = {
        "by_category": defaultdict(lambda: defaultdict(list)),
        "by_type": defaultdict(lambda: defaultdict(list)),
    }

    for pq in per_query:
        cat = pq.get("category", "Unknown")
        typ = pq.get("type", "Unknown")
        for m in models:
            m_metrics = pq["metrics"].get(m, {})
            for key in ("flesch", "faithfulness", "faithfulness_semantic"):
                val = m_metrics.get(key)
                if val is not None:
                    groups["by_category"][cat][m].append(val)
                    groups["by_type"][typ][m].append(val)

    # Average
    result = {}
    for group_name, group_data in groups.items():
        result[group_name] = {}
        for key, method_data in group_data.items():
            result[group_name][key] = {}
            for m, vals in method_data.items():
                result[group_name][key][m] = sum(vals) / len(vals) if vals else None
    return result


def format_example(entry: dict, method_a: str, method_b: str) -> str:
    """Format a single comparison entry for markdown output."""
    lines = []
    lines.append(f"### {entry['id']}: {entry['query'][:80]}")
    lines.append("")
    lines.append(f"- **Category:** {entry['category']} | **Type:** {entry['type']}")
    lines.append(f"- **Diff ({method_a} - {method_b}):** {entry['diff']:+.3f}")
    lines.append("")
    lines.append(f"**{method_a}** ({entry['a_value']:.3f}):")
    a_text = entry.get('a_text', '')[:300]
    lines.append(f"  > {a_text}")
    lines.append("")
    lines.append(f"**{method_b}** ({entry['b_value']:.3f}):")
    b_text = entry.get('b_text', '')[:300]
    lines.append(f"  > {b_text}")
    lines.append("")
    return "\n".join(lines)


def generate_report(
    data: dict,
    top_k: int = 15,
    compare: Optional[Tuple[str, str]] = None,
    output_path: Optional[str] = None,
) -> str:
    """Generate a complete error analysis markdown report."""
    models = data["models"]
    queries = data["queries"]
    report_data = data["report"]
    log_dir = data["log_dir"]

    # If only one model, compare categories instead
    if len(models) < 2 and compare is None:
        compare = None  # Just do per-category analysis

    per_query = compute_per_query_metrics(data)

    lines = []
    lines.append("# Error Analysis Report")
    lines.append("")
    lines.append(f"- **Log directory:** `{log_dir}`")
    lines.append(f"- **Models:** {', '.join(models)}")
    lines.append(f"- **Queries:** {len(queries)}")
    lines.append(f"- **Generated:** {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # ── 1. Summary statistics from report.json ──
    if report_data:
        lines.append("## 1. Overall Summary")
        lines.append("")
        lines.append("| Method | Correctness | Precision | Depth | FRES | Halluc. | Faith(Num) | Faith(Sem) | Tol±2% | Tol±5% |")
        lines.append("|--------|-------------|-----------|-------|------|---------|------------|------------|--------|--------|")
        model_entries = [m for m in models if m in report_data and m != "_cost"]
        for m in model_entries:
            s = report_data[m]
            def _v(key, fmt="{:.2f}"):
                v = s.get(key, {}).get("mean") if isinstance(s.get(key), dict) else None
                return fmt.format(v) if v is not None else "N/A"
            def _vpct(key):
                v = s.get(key, {}).get("mean") if isinstance(s.get(key), dict) else None
                return f"{v*100:.1f}%" if v is not None else "N/A"
            lines.append(
                f"| {m} | {_v('correctness')} | {_v('precision')} | {_v('scientific_depth')} "
                f"| {_v('flesch_reading_ease')} | {_v('hallucination', '{:.4f}')} "
                f"| {_vpct('faithfulness')} | {_vpct('faithfulness_semantic')} | {_vpct('tolerance_p2')} | {_vpct('tolerance_p5')} |"
            )
        lines.append("")

    # ── 2. Category-level breakdown ──
    lines.append("## 2. Category-Level Breakdown")
    lines.append("")
    by_cat = group_by_category(per_query, models)
    for group_key, group_label in [("by_category", "Category"), ("by_type", "Type")]:
        group_data = by_cat.get(group_key, {})
        if group_data:
            lines.append(f"### By {group_label}")
            lines.append("")
            for key in sorted(group_data):
                lines.append(f"**{key}**")
                lines.append("")
                lines.append(f"| {'Metric':<15} | {' | '.join(f'{m:<20}' for m in models)} |")
                lines.append(f"| {'-'*15} | {' | '.join('-'*20 for _ in models)} |")
                for metric_name, metric_label in [("flesch", "FRES"), ("faithfulness", "Faith(Num)"), ("faithfulness_semantic", "Faith(Sem)")]:
                    row = f"| {metric_label:<15} "
                    for m in models:
                        v = group_data[key].get(m)
                        row += f"| {v:.2f}" if v is not None else "| N/A"
                    row += " |"
                    lines.append(row)
                lines.append("")

    # ── 3. Model comparison (Top-K disagreements) ──
    if compare:
        method_a, method_b = compare
        lines.append(f"## 3. Model Comparison: {method_a} vs {method_b}")
        lines.append("")

        # Find disagreements on various metrics
        for metric_name, metric_label, fmt in [
            ("flesch", "Flesch Reading Ease", "{:.2f}"),
            ("faithfulness", "Faithfulness (Numeric)", "{:.2%}"),
            ("faithfulness_semantic", "Faithfulness (Semantic)", "{:.2%}"),
        ]:
            disagreements = find_top_disagreements(per_query, method_a, method_b, metric=metric_name, top_k=top_k)
            if not disagreements:
                continue

            # Separate into A-wins (diff > 0) and B-wins (diff < 0)
            a_wins = [d for d in disagreements if d["diff"] > 0]
            b_wins = [d for d in disagreements if d["diff"] < 0][:top_k // 2]

            lines.append(f"### 3.{list(['flesch', 'faithfulness']).index(metric_name) + 1} {metric_label} Gap (Top {top_k})")
            lines.append("")

            if a_wins:
                lines.append(f"#### {method_a} wins (higher {metric_label})")
                lines.append("")
                for d in a_wins[:5]:
                    d["a_text"] = next((pq["metrics"][method_a]["text"][:300]
                                        for pq in per_query if pq["id"] == d["id"]), "")
                    d["b_text"] = next((pq["metrics"][method_b]["text"][:300]
                                        for pq in per_query if pq["id"] == d["id"]), "")
                    lines.append(format_example(d, method_a, method_b))
                    lines.append("---")
                    lines.append("")

            if b_wins:
                lines.append(f"#### {method_b} wins (higher {metric_label})")
                lines.append("")
                for d in b_wins[:5]:
                    d["a_text"] = next((pq["metrics"][method_a]["text"][:300]
                                        for pq in per_query if pq["id"] == d["id"]), "")
                    d["b_text"] = next((pq["metrics"][method_b]["text"][:300]
                                        for pq in per_query if pq["id"] == d["id"]), "")
                    lines.append(format_example(d, method_a, method_b))
                    lines.append("---")
                    lines.append("")

    # ── 4. Failure mode analysis ──
    lines.append("## 4. Failure Mode Analysis")
    lines.append("")

    for m in models:
        # Lowest numeric faithfulness
        worst_faith = find_lowest_performers(per_query, m, "faithfulness", top_k=5)
        if worst_faith and worst_faith[0]["value"] is not None:
            lines.append(f"### {m}: Lowest Numeric Faithfulness")
            lines.append("")
            for d in worst_faith:
                lines.append(f"- **{d['id']}** ({d['category']}/{d['type']}): "
                             f"faithfulness={d['value']:.2%} — *{d['query'][:100]}*")
            lines.append("")

        # Lowest semantic faithfulness
        worst_sem = find_lowest_performers(per_query, m, "faithfulness_semantic", top_k=5)
        if worst_sem and worst_sem[0]["value"] is not None:
            lines.append(f"### {m}: Lowest Semantic Faithfulness")
            lines.append("")
            for d in worst_sem:
                lines.append(f"- **{d['id']}** ({d['category']}/{d['type']}): "
                             f"semantic_faithfulness={d['value']:.2%} — *{d['query'][:100]}*")
            lines.append("")

        # No tool data (faithfulness=None)
        no_tool = [pq for pq in per_query if pq["metrics"].get(m, {}).get("faithfulness") is None]
        if no_tool:
            lines.append(f"### {m}: Missing Tool Observations ({len(no_tool)} queries)")
            lines.append("")
            for d in no_tool[:5]:
                lines.append(f"- **{d['id']}** ({d['category']}/{d['type']}): *{d['query'][:100]}*")
            lines.append("")

        # Empty/short responses
        short = [pq for pq in per_query if pq["metrics"].get(m, {}).get("length", 0) < 20]
        if short:
            lines.append(f"### {m}: Empty/Short Responses ({len(short)} queries)")
            lines.append("")
            for d in short[:5]:
                lines.append(f"- **{d['id']}** ({d['category']}/{d['type']}): "
                             f"'{d['metrics'].get(m, {}).get('text', '')[:80]}'")
            lines.append("")

    # ── 5. Pattern summary ──
    lines.append("## 5. Pattern Summary")
    lines.append("")

    # Tolerance failures by category
    lines.append("### Tolerance Failure Rate by Category")
    lines.append("")
    lines.append(f"| {'Category':<35} | {' | '.join(f'{m:<12}' for m in models)} |")
    lines.append(f"| {'-'*35} | {' | '.join('-'*12 for _ in models)} |")
    cats = sorted(set(pq["category"] for pq in per_query if pq["category"]))
    for cat in cats:
        row = f"| {cat:<35} "
        for m in models:
            cat_qs = [pq for pq in per_query if pq["category"] == cat]
            tol5_ok = sum(1 for pq in cat_qs if pq["metrics"].get(m, {}).get("tolerance_p5"))
            tol5_total = sum(1 for pq in cat_qs if pq["expected_value"] is not None and m in pq["metrics"])
            row += f"| {tol5_ok}/{tol5_total}" if tol5_total > 0 else f"| N/A"
        row += " |"
        lines.append(row)
    lines.append("")

    # Faithfulness by category
    for metric_name, metric_label in [("faithfulness", "Faith(Num)"), ("faithfulness_semantic", "Faith(Sem)")]:
        lines.append(f"### Average {metric_label} by Category")
        lines.append("")
        lines.append(f"| {'Category':<35} | {' | '.join(f'{m:<12}' for m in models)} |")
        lines.append(f"| {'-'*35} | {' | '.join('-'*12 for _ in models)} |")
        for cat in cats:
            row = f"| {cat:<35} "
            for m in models:
                vals = [pq["metrics"][m][metric_name] for pq in per_query
                        if pq["category"] == cat and pq["metrics"].get(m, {}).get(metric_name) is not None]
                avg = sum(vals) / len(vals) if vals else None
                row += f"| {avg:.2%}" if avg is not None else "| N/A"
            row += " |"
            lines.append(row)
        lines.append("")

    # Response length comparison
    lines.append("### Average Response Length")
    lines.append("")
    lines.append(f"| {'Method':<30} | {'Avg Words':<12} | {'Avg Chars':<12} |")
    lines.append(f"| {'-'*30} | {'-'*12} | {'-'*12} |")
    for m in models:
        lengths = [pq["metrics"][m]["word_count"] for pq in per_query if m in pq["metrics"]]
        char_lens = [pq["metrics"][m]["length"] for pq in per_query if m in pq["metrics"]]
        avg_words = sum(lengths) / len(lengths) if lengths else 0
        avg_chars = sum(char_lens) / len(char_lens) if char_lens else 0
        lines.append(f"| {m:<30} | {avg_words:<12.1f} | {avg_chars:<12.1f} |")
    lines.append("")

    report = "\n".join(lines)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {output_path}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Error analysis for NutriCHAT evaluation results.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("log_dir", type=str, help="Path to evaluation log directory")
    parser.add_argument("--top-k", type=int, default=15, help="Number of top disagreements to report")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output markdown file path")
    parser.add_argument("--compare", type=str, nargs=2, metavar=("METHOD_A", "METHOD_B"),
                        help="Compare two specific methods (default: first two methods in log)")
    args = parser.parse_args()

    data = load_log_data(args.log_dir)
    models = data["models"]

    compare = args.compare
    if compare is None and len(models) >= 2:
        compare = (models[0], models[1])
        print(f"Auto-selected comparison: {compare[0]} vs {compare[1]}")
    elif compare is not None:
        a, b = compare
        if a not in models or b not in models:
            print(f"Warning: one or both methods not found in log. Available: {models}")
            compare = None

    report = generate_report(data, top_k=args.top_k, compare=compare, output_path=args.output)

    if not args.output:
        print(report)
    print(f"\nAnalysis complete. {len(data['queries'])} queries, {len(models)} models.")


if __name__ == "__main__":
    main()
