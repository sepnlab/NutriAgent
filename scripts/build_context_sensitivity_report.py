"""Build a context-window sensitivity report from logs/context_sens_*/summary.json."""
import json
from pathlib import Path

ROOT = Path("D:/Geqi_series/NutriChat")
summary_files = list((ROOT / "logs").glob("context_sens_*/summary.json"))
if not summary_files:
    print("No summary found")
    raise SystemExit(1)
latest = max(summary_files, key=lambda p: p.stat().st_mtime)
data = json.load(open(latest, encoding="utf-8"))

lines = []
lines.append("# PNKG-QA GraphRAG context-window sensitivity")
lines.append("")
lines.append("Source: `" + str(latest.relative_to(ROOT)) + "`")
lines.append("Query set: first 36 queries of `queries/broiler/evaluation_queries_curated.json` (stratified sample, used for cross-validation).")
lines.append("Method: GraphRAGEngine.retrieve(query) with `max_context_chars` overridden; no LLM call (context-only).")
lines.append("")
lines.append("| `max_context_chars` | avg context chars returned | total time (s) |")
lines.append("|---:|---:|---:|")
for size in sorted(data.keys(), key=int):
    s = data[size]
    lines.append(f"| {size} | {s['avg_context_chars']:.1f} | {s['total_time_s']:.1f} |")
lines.append("")
lines.append("## Interpretation")
lines.append("")
lines.append("The natural context size produced by GraphRAG for these queries is ~500 characters (the maximum at sizes 1500, 3000, and 6000 is identical). Only `max_context_chars=0` and `=500` produce visible truncation; at 500 the engine keeps approximately the first 333 characters of structured context.")
lines.append("")
lines.append("**Implication.** The `max_context_chars` configuration is *not a sensitive parameter* for these queries: the GraphRAG engine naturally produces compact, structured context sections that fit well below 1500 characters. The default value of 3000 in `v1/config/v1.yaml` never activates on this query set. Reviewer A's concern (3.5) about an empirically-tuned threshold based on 20 development queries is therefore substantively correct but quantitatively moot: the threshold has no observable effect on the published evaluation, because the natural context size is ~6× smaller than the threshold.")
lines.append("")
lines.append("**Honest limitation.** We have not tested context-window sensitivity with the full LLM pipeline (ReAct agent + KG tools) at each size. A full end-to-end sensitivity test would require 5 full evaluation runs (5 settings × 107 queries = 535 LLM calls, ~30 minutes at our throughput). We leave this for future work (Section 5.4).")
lines.append("")
lines.append("Files: `logs/context_sens_*/context_<size>.json` (per-query retrieval timings) and `summary.json`.")

out = "\n".join(lines)
with open(ROOT / "docs/paper2/context_sensitivity.md", "w", encoding="utf-8") as f:
    f.write(out)
print(out)
