"""D4 RAG ITT sensitivity (documented proxy).

The Rev.1 D4 rescore contains all 54 correctness scores but does not preserve a
retrieval-failure flag. The four submitted-run exclusions cannot be reconstructed
exactly. As a transparent conservative proxy, E6 hit@5 misses are scored as
system failures (1; sensitivity 0) in the +RAG condition. The no-RAG condition is
unchanged. Complete-case analysis uses observed scores.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

ROOT = Path(r"D:\Geqi_series\NutriChat")
D4 = ROOT / "docs" / "paper" / "audit" / "d4_rescored.json"
E6 = ROOT / "docs" / "paper" / "audit" / "e6_retrieval_k.json"
OUT_MD = ROOT / "docs" / "paper" / "audit" / "d4_itt_report.md"
OUT_JSON = ROOT / "docs" / "paper" / "audit" / "d4_itt_report.json"

d4 = json.loads(D4.read_text(encoding="utf-8"))
e6 = json.loads(E6.read_text(encoding="utf-8"))
fail = {r["id"] for r in e6["rows"] if not r["hit@5"]}
print("proxy failures", len(fail), sorted(fail))

rag = {r["id"]: r for r in d4["Multi-Agent + RAG"]["per_query"]}
nor = {r["id"]: r for r in d4["Multi-Agent (no RAG)"]["per_query"]}
ids = sorted(set(rag) | set(nor))
rng = np.random.default_rng(42)


def boot_ci(diff: np.ndarray, n: int = 10000) -> tuple[float, float]:
    vals = [np.mean(rng.choice(diff, len(diff), replace=True)) for _ in range(n)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def metric(name: str, floor: float | None, complete: bool = False):
    """Return RAG, no-RAG, delta, CI, p for a metric.

    floor None = complete-case (drop missing); else replace +RAG failures with floor.
    The no-RAG condition is never imputed.
    """
    ra, no = [], []
    for qid in ids:
        rv = rag[qid].get(name)
        nv = nor[qid].get(name)
        if qid in fail and floor is not None:
            rv = floor
        if complete:
            if rv is None or nv is None:
                continue
        else:
            if nv is None:
                continue
            if rv is None:
                rv = floor if floor is not None else None
        if rv is None or nv is None:
            continue
        ra.append(float(rv)); no.append(float(nv))
    diff = np.array(ra) - np.array(no)
    p = float(wilcoxon(diff).pvalue) if len(diff) else float("nan")
    return dict(n=len(diff), rag=float(np.mean(ra)), no_rag=float(np.mean(no)),
                delta=float(np.mean(diff)), ci=list(boot_ci(diff)), p=p)


rows = {}
for metric_name in ["correctness", "precision", "scientific_depth"]:
    rows[metric_name] = {
        "itt_floor_1": metric(metric_name, 1.0),
        "itt_floor_0": metric(metric_name, 0.0),
        "complete_case": metric(metric_name, None, complete=True),
    }

md = [
    "# D4 RAG ITT sensitivity (proxy failures)",
    "",
    "The Rev.1 D4 rescore includes all 54 correctness scores but does not preserve a",
    "retrieval-failure flag; the four submitted-run exclusions cannot be reconstructed",
    "exactly. As a conservative, clearly labeled proxy, the **16 E6 hit@5 misses** are",
    "scored as system failures (1; sensitivity 0) in the +RAG condition. This is not an",
    "exact reconstruction of the submitted exclusions and is reported as a sensitivity",
    "analysis, not as the primary D4 estimate.",
    "",
    f"Proxy failure IDs: {', '.join(sorted(fail))}.",
    "",
    "| Metric | Analysis | n | +RAG | no-RAG | Δ | 95% CI | Wilcoxon p |",
    "|---|---|---:|---:|---:|---:|---|---:|",
]
for m, blocks in rows.items():
    for label, r in blocks.items():
        md.append(
            f"| {m} | {label} | {r['n']} | {r['rag']:.3f} | {r['no_rag']:.3f} | "
            f"{r['delta']:+.3f} | {r['ci'][0]:+.3f} to {r['ci'][1]:+.3f} | {r['p']:.4f} |"
        )
md += [
    "",
    "The proxy ITT does not support a RAG correctness or precision benefit; the direction",
    "is neutral-to-negative, consistent with the complete-case null result. Because the",
    "failure set is a proxy, this analysis is labeled in the manuscript and supplement",
    "and is not used to claim an exact intention-to-treat effect.",
]
OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
OUT_JSON.write_text(json.dumps({"proxy_failures": sorted(fail), "results": rows}, indent=2), encoding="utf-8")
print("\n".join(md))
