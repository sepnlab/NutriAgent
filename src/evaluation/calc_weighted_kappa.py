"""
Compute inter-rater agreement metrics for the 36-query expert cross-validation study.

For each unique query `key`, pairs Expert-A and Expert-B scores and computes:
  - Cohen's weighted kappa (quadratic weights, ordinal 1-5)
  - Spearman rank correlation
  - Pearson correlation
  - ICC(2,1) two-way random single-rater absolute agreement
  - Exact agreement %, off-by-1 %, |diff|>=2 %

Also computes EvaluatorLLM-vs-Expert pairs (one for each expert_name).

Outputs a JSON summary table to v1/experiments/expert_validation/weighted_kappa_results.json
and prints a Markdown table to stdout.
"""

import json
import os
import sys
from collections import defaultdict
from typing import List, Dict, Tuple

import numpy as np
from scipy.stats import pearsonr, spearmanr

INPUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "v1", "experiments", "expert_validation", "expert_v3_scores_remapped.json",
)
OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "v1", "experiments", "expert_validation", "weighted_kappa_results.json",
)


def load_records(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _dedupe_records(records: List[Dict]) -> List[Dict]:
    """Deduplicate by (key, expert_name), keeping the record with the most non-null expert scores.

    Some definition queries were re-scored after initial parse failures; the latest record
    typically has the most complete scoring. Dedup avoids inflating n in inter-rater pairs.
    """
    by_ke: Dict[Tuple[str, str], Dict] = {}
    for r in records:
        key = r.get("key")
        expert = r.get("expert_name", "")
        tag = "A" if "Expert-A" in expert else ("B" if "Expert-B" in expert else "?")
        if tag == "?":
            continue
        ke = (key, tag)
        expert_scores = r.get("expert", {})
        n_filled = sum(1 for v in expert_scores.values() if v is not None)
        prev = by_ke.get(ke)
        if prev is None or n_filled >= sum(1 for v in prev.get("expert", {}).values() if v is not None):
            by_ke[ke] = r
    return list(by_ke.values())


def pair_by_key(records: List[Dict], dim: str) -> List[Tuple[float, float, str]]:
    """Group records by `key`; for each key, return (Expert-A, Expert-B) score on the given dim.

    Returns a list of (a, b, key) tuples. Skips keys where one of the experts has a null score.
    Deduplicates (key, expert) pairs first to avoid inflating n.
    """
    deduped = _dedupe_records(records)
    by_key: Dict[str, Dict[str, float]] = defaultdict(dict)
    for r in deduped:
        score = r.get("expert", {}).get(dim)
        if score is None:
            continue
        expert = r.get("expert_name", "")
        if "Expert-A" in expert:
            by_key[r["key"]]["A"] = score
        elif "Expert-B" in expert:
            by_key[r["key"]]["B"] = score
    out = []
    for k, d in by_key.items():
        if "A" in d and "B" in d:
            out.append((d["A"], d["B"], k))
    return out


def pair_evaluator_vs_expert(records: List[Dict], dim: str) -> List[Tuple[float, float, str]]:
    """Pair EvaluatorLLM (evaluator_<dim>) with each expert's score on the same dim.

    Returns a list of (evaluator, expert, key) tuples, one per (key, expert) pair after
    deduplication. Skips records where either score is null.
    """
    deduped = _dedupe_records(records)
    out = []
    for r in deduped:
        eval_score = r.get(f"evaluator_{dim}")
        expert_score = r.get("expert", {}).get(dim)
        if eval_score is None or expert_score is None:
            continue
        out.append((eval_score, expert_score, r["key"]))
    return out


def quadratic_weighted_kappa(r1: List[float], r2: List[float], k: int = 5) -> float:
    """Cohen's weighted kappa with quadratic weights for ordinal scales 1..k.

    Reference: Cohen, J. (1968). Weighted kappa: Nominal scale agreement with provision
    for scaled disagreement or partial credit. Psychological Bulletin 70(4), 213-220.
    """
    n = len(r1)
    if n == 0:
        return float("nan")
    # Build k x k confusion matrix O (observed)
    O = np.zeros((k, k), dtype=np.float64)
    for a, b in zip(r1, r2):
        O[int(a) - 1, int(b) - 1] += 1
    O /= n  # row-stochastic (joint proportions)
    # Marginal proportions
    r = O.sum(axis=1)  # row marginals (rater 1)
    c = O.sum(axis=0)  # col marginals (rater 2)
    # Expected under independence E[i,j] = r[i] * c[j]
    E = np.outer(r, c)
    # Quadratic agreement weights: W[i,j] = 1 - (i-j)^2 / (k-1)^2
    W = np.zeros((k, k), dtype=np.float64)
    for i in range(k):
        for j in range(k):
            W[i, j] = 1.0 - ((i - j) ** 2) / ((k - 1) ** 2)
    # Weighted agreement scores
    p_o = np.sum(W * O)        # observed weighted agreement
    p_e = np.sum(W * E)        # expected weighted agreement by chance
    denom = 1.0 - p_e
    if denom == 0:
        return float("nan")
    return float((p_o - p_e) / denom)


def icc_2_1(r1: np.ndarray, r2: np.ndarray) -> float:
    """ICC(2,1) two-way random single-rater absolute agreement (Shrout & Fleiss 1979).

    ICC(2,1) = (MSR - MSE) / (MSR + (k-1)*MSE + k*(MSC - MSE)/n)
    where k = number of raters (2), n = number of targets.
    """
    k = 2
    targets = np.column_stack([r1, r2])  # (n, k)
    n = targets.shape[0]
    # Subject means, rater means
    subject_means = targets.mean(axis=1)
    rater_means = targets.mean(axis=0)
    grand_mean = targets.mean()
    # Sum squares
    SSR = k * np.sum((subject_means - grand_mean) ** 2)  # between-subjects
    SSC = n * np.sum((rater_means - grand_mean) ** 2)    # between-raters
    SSE = np.sum((targets - subject_means[:, None] - rater_means[None, :] + grand_mean) ** 2)
    MSR = SSR / (n - 1)
    MSC = SSC / (k - 1)
    MSE = SSE / ((n - 1) * (k - 1))
    denom = MSR + (k - 1) * MSE + k * (MSC - MSE) / n
    if denom == 0:
        return float("nan")
    return float((MSR - MSE) / denom)


def compute_pair_stats(pairs: List[Tuple[float, float, str]]) -> Dict:
    a = np.array([p[0] for p in pairs], dtype=float)
    b = np.array([p[1] for p in pairs], dtype=float)
    diffs = a - b
    abs_diffs = np.abs(diffs)
    n = len(pairs)
    spearman_r, spearman_p = spearmanr(a, b)
    pearson_r, pearson_p = pearsonr(a, b)
    icc = icc_2_1(a, b)
    # Quadratic weighted kappa needs integer scores 1-5; both are 1-5 here
    kw = quadratic_weighted_kappa(a.tolist(), b.tolist(), k=5)
    return {
        "n": n,
        "spearman_r": round(float(spearman_r), 4),
        "spearman_p": round(float(spearman_p), 4),
        "pearson_r": round(float(pearson_r), 4),
        "pearson_p": round(float(pearson_p), 4),
        "icc_2_1": round(float(icc), 4),
        "kw_quadratic": round(float(kw), 4),
        "exact_agreement_pct": round(float(np.mean(abs_diffs == 0) * 100), 1),
        "off_by_1_pct": round(float(np.mean(abs_diffs == 1) * 100), 1),
        "abs_diff_ge_2_pct": round(float(np.mean(abs_diffs >= 2) * 100), 1),
        "mean_a": round(float(a.mean()), 3),
        "mean_b": round(float(b.mean()), 3),
    }


def main() -> int:
    records = load_records(INPUT)
    print(f"Loaded {len(records)} records from {INPUT}")
    # Count unique keys and expert distribution
    keys = set(r["key"] for r in records)
    print(f"Unique keys: {len(keys)}")
    n_a = sum(1 for r in records if "Expert-A" in r.get("expert_name", ""))
    n_b = sum(1 for r in records if "Expert-B" in r.get("expert_name", ""))
    print(f"  Expert-A entries: {n_a}")
    print(f"  Expert-B entries: {n_b}")

    dimensions = ["correctness", "precision", "scientific_depth"]
    results: Dict[str, Dict] = {}
    for dim in dimensions:
        results[dim] = {}
        # Expert-A vs Expert-B
        ab = pair_by_key(records, dim)
        print(f"\n[{dim}] Expert-A vs Expert-B: n={len(ab)}")
        results[dim]["Expert-A_vs_Expert-B"] = compute_pair_stats(ab)
        # EvaluatorLLM vs each expert (after dedup)
        deduped = _dedupe_records(records)
        eval_a_pairs, eval_b_pairs = [], []
        for r in deduped:
            eval_score = r.get(f"evaluator_{dim}")
            expert_score = r.get("expert", {}).get(dim)
            if eval_score is None or expert_score is None:
                continue
            if "Expert-A" in r.get("expert_name", ""):
                eval_a_pairs.append((eval_score, expert_score, r["key"]))
            elif "Expert-B" in r.get("expert_name", ""):
                eval_b_pairs.append((eval_score, expert_score, r["key"]))
        print(f"[{dim}] EvaluatorLLM vs Expert-A: n={len(eval_a_pairs)}")
        results[dim]["EvaluatorLLM_vs_Expert-A"] = compute_pair_stats(eval_a_pairs)
        print(f"[{dim}] EvaluatorLLM vs Expert-B: n={len(eval_b_pairs)}")
        results[dim]["EvaluatorLLM_vs_Expert-B"] = compute_pair_stats(eval_b_pairs)

    # Write JSON
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved: {OUTPUT}")

    # Print Markdown table
    print("\n# Inter-rater agreement (n_paired queries, Spearman, Pearson, ICC(2,1), kappa_w, exact%, off-by-1%, |d|>=2%)\n")
    for dim, comps in results.items():
        print(f"\n## {dim}\n")
        print("| Comparison | n | Spearman ρ | Pearson r | ICC(2,1) | κ_w (quad) | Exact% | Off-by-1% | \\|d\\|>=2% |")
        print("|------------|---|-----------|-----------|----------|------------|--------|------------|----------|")
        for comp, stats in comps.items():
            print(f"| {comp} | {stats['n']} | {stats['spearman_r']} | {stats['pearson_r']} | "
                  f"{stats['icc_2_1']} | {stats['kw_quadratic']} | {stats['exact_agreement_pct']} | "
                  f"{stats['off_by_1_pct']} | {stats['abs_diff_ge_2_pct']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
