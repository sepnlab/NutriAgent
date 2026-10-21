"""Recompute human/LLM agreement and paired effect sizes from a comparison log.

This script exists because the submitted manuscript reports EvaluatorLLM–expert
agreement values (rho = 0.83 / 0.67 / 0.37) that cannot be reproduced from the
deposited scores (audit finding F4). It recomputes every statistic with n and
bootstrap confidence intervals, and reports paired method differences with
effect sizes.

Usage:
    python scripts/paper/agreement.py --log-dir logs/comp_layer_20260612_183548
    python scripts/paper/agreement.py --log-dir <rev1_log> --second-rater rater_b.csv

The optional second-rater CSV must contain:
    query_id, metric, rater_a, rater_b
where metric is one of correctness / precision / scientific_depth.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "docs" / "paper" / "audit"

EXPERT_COLS = {
    "correctness_(1-5)": "correctness",
    "precision_(1-5_or_N/A)": "precision",
    "scientific_depth_(1-5)": "scientific_depth",
}
METRICS = ["correctness", "precision", "scientific_depth"]
N_BOOT = 10_000
SEED = 42


# ── helpers ─────────────────────────────────────────────────
def _read_expert(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns=EXPERT_COLS)
    for metric in METRICS:
        if metric in df.columns:
            df[metric] = pd.to_numeric(df[metric], errors="coerce")
    return df


def _boot_ci(values: np.ndarray, stat_fn, n_boot: int = N_BOOT, seed: int = SEED):
    rng = np.random.default_rng(seed)
    stats_ = []
    n = len(values)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        try:
            v = stat_fn(values[idx])
        except Exception:
            continue
        if v is not None and np.isfinite(v):
            stats_.append(v)
    if not stats_:
        return None, None
    return float(np.percentile(stats_, 2.5)), float(np.percentile(stats_, 97.5))


def _spearman_ci(x: np.ndarray, y: np.ndarray):
    if len(x) < 5 or len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        return None, None, None
    rho = float(stats.spearmanr(x, y).statistic)
    pairs = np.column_stack([x, y])

    def _stat(a):
        if len(np.unique(a[:, 0])) < 2 or len(np.unique(a[:, 1])) < 2:
            return np.nan
        return stats.spearmanr(a[:, 0], a[:, 1]).statistic

    lo, hi = _boot_ci(pairs, _stat)
    return rho, lo, hi


def _icc21(matrix: np.ndarray) -> float:
    """ICC(2,1): two-way random effects, absolute agreement, single rater."""
    n, k = matrix.shape
    grand = matrix.mean()
    ms_rows = k * ((matrix.mean(axis=1) - grand) ** 2).sum() / (n - 1)
    ms_cols = n * ((matrix.mean(axis=0) - grand) ** 2).sum() / (k - 1)
    ss_total = ((matrix - grand) ** 2).sum()
    ss_error = ss_total - k * ((matrix.mean(axis=1) - grand) ** 2).sum() - n * (
        (matrix.mean(axis=0) - grand) ** 2
    ).sum()
    ms_error = ss_error / ((n - 1) * (k - 1))
    denom = ms_rows + (k - 1) * ms_error + k * (ms_cols - ms_error) / n
    return float((ms_rows - ms_error) / denom) if denom else float("nan")


def _weighted_kappa(a: np.ndarray, b: np.ndarray, categories=(1, 2, 3, 4, 5)) -> float:
    k = len(categories)
    idx = {c: i for i, c in enumerate(categories)}
    conf = np.zeros((k, k))
    for x, y in zip(a, b):
        if x in idx and y in idx:
            conf[idx[x], idx[y]] += 1
    total = conf.sum()
    if total == 0:
        return float("nan")
    row = conf.sum(axis=1)
    col = conf.sum(axis=0)
    expected = np.outer(row, col) / total
    w = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            w[i, j] = 1 - ((i - j) ** 2) / ((k - 1) ** 2)
    po = (w * conf).sum() / total
    pe = (w * expected).sum() / total
    return float((po - pe) / (1 - pe)) if (1 - pe) else float("nan")


def _paired_diff(nutri: pd.DataFrame, other: pd.DataFrame, metric: str) -> dict:
    a = nutri.set_index("query_id")[metric]
    b = other.set_index("query_id")[metric]
    common = a.index.intersection(b.index)
    d = (a.loc[common] - b.loc[common]).dropna().to_numpy()
    if len(d) < 3:
        return {"n": len(d), "mean_diff": None, "ci_low": None, "ci_high": None}
    mean = float(np.mean(d))
    lo, hi = _boot_ci(d, np.mean)
    dz = float(mean / np.std(d, ddof=1)) if np.std(d, ddof=1) > 0 else float("nan")
    try:
        p = float(stats.wilcoxon(d).pvalue)
    except Exception:
        p = None
    return {
        "n": int(len(d)),
        "mean_diff": round(mean, 4),
        "ci_low": round(lo, 4) if lo is not None else None,
        "ci_high": round(hi, 4) if hi is not None else None,
        "cohen_dz": round(dz, 3),
        "wilcoxon_p": round(p, 5) if p is not None else None,
    }


def _holm(pvals: list[tuple[str, float]]) -> dict[str, float]:
    items = [(k, p) for k, p in pvals if p is not None]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    adjusted = {}
    running = 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, (m - i) * p)
        running = max(running, adj)
        adjusted[k] = running
    return adjusted


# ── main ────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--expert-a", default="expert_eval_nutriagent_scored.csv")
    parser.add_argument("--expert-b", default="expert_eval_baselines_scored.csv")
    parser.add_argument("--second-rater", default=None)
    parser.add_argument("--out-dir", default=str(OUT_DIR))
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = json.loads((log_dir / "report.json").read_text(encoding="utf-8"))
    anon = {}
    anon_path = log_dir / "expert_eval_anon_map.json"
    if anon_path.exists():
        anon = json.loads(anon_path.read_text(encoding="utf-8"))
    # anon: report_key -> model_id ("Model_A" ...)
    name_map = {v: k for k, v in anon.items()}  # model_id -> report_key

    expert_na = _read_expert(log_dir / args.expert_a)
    expert_bl = _read_expert(log_dir / args.expert_b)

    # EvaluatorLLM per-query scores keyed by method display name.
    def evaluator_frame(method_key: str) -> pd.DataFrame:
        rows = report[method_key].get("per_query", [])
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        return df.rename(columns={"id": "query_id"})

    method_keys = [k for k in report if k != "_cost"]
    nutri_key = next((k for k in method_keys if "Nutri" in k or "nutri" in k.lower()), None)
    if nutri_key is None:
        raise SystemExit("could not identify the NutriAgent entry in report.json")

    agreement = {}
    # (a) NutriAgent-only agreement (the manuscript's claim)
    ev = evaluator_frame(nutri_key)
    merged = expert_na.merge(ev, on="query_id", how="inner", suffixes=("_exp", "_ev"))
    for metric in METRICS:
        x = merged[f"{metric}_exp"].to_numpy(dtype=float)
        y = merged[f"{metric}_ev"].to_numpy(dtype=float)
        mask = np.isfinite(x) & np.isfinite(y)
        rho, lo, hi = _spearman_ci(x[mask], y[mask])
        agreement[f"nutriagent_{metric}"] = {
            "n": int(mask.sum()),
            "spearman_rho": round(rho, 3) if rho is not None else None,
            "ci_low": round(lo, 3) if lo is not None else None,
            "ci_high": round(hi, 3) if hi is not None else None,
            "within_1_point": round(float(np.mean(np.abs(x[mask] - y[mask]) <= 1)), 3)
            if mask.sum()
            else None,
        }

    # (b) all-method agreement (pooled)
    pooled = []
    for key in method_keys:
        ev = evaluator_frame(key)
        if ev.empty:
            continue
        if key == nutri_key:
            exp = expert_na.copy()
        else:
            model_id = anon.get(key, key)
            exp = expert_bl[expert_bl["model_id"] == model_id].copy()
        if exp.empty:
            continue
        m = exp.merge(ev, on="query_id", how="inner", suffixes=("_exp", "_ev"))
        m["method"] = key
        pooled.append(m)
    pooled_df = pd.concat(pooled, ignore_index=True) if pooled else pd.DataFrame()
    if not pooled_df.empty:
        for metric in METRICS:
            x = pooled_df[f"{metric}_exp"].to_numpy(dtype=float)
            y = pooled_df[f"{metric}_ev"].to_numpy(dtype=float)
            mask = np.isfinite(x) & np.isfinite(y)
            rho, lo, hi = _spearman_ci(x[mask], y[mask])
            agreement[f"pooled_{metric}"] = {
                "n": int(mask.sum()),
                "spearman_rho": round(rho, 3) if rho is not None else None,
                "ci_low": round(lo, 3) if lo is not None else None,
                "ci_high": round(hi, 3) if hi is not None else None,
            }

    # (c) paired NutriAgent - baseline differences (expert scores)
    diffs = {}
    for model_id, group in expert_bl.groupby("model_id"):
        display = name_map.get(model_id, model_id)
        diffs[display] = {
            metric: _paired_diff(expert_na, group, metric) for metric in METRICS
        }
    # Holm correction within each metric family (across baselines).
    for metric in METRICS:
        pvals = [
            (display, diffs[display][metric]["wilcoxon_p"])
            for display in diffs
            if diffs[display][metric]["wilcoxon_p"] is not None
        ]
        for display, adjusted_p in _holm(pvals).items():
            diffs[display][metric]["holm_p"] = round(adjusted_p, 5)

    # (d) optional second-rater reliability
    rater = None
    if args.second_rater:
        rdf = pd.read_csv(args.second_rater)
        rater = {}
        for metric, group in rdf.groupby("metric"):
            pair = group[["rater_a", "rater_b"]].dropna().to_numpy(dtype=float)
            if len(pair) < 3:
                continue
            icc = _icc21(pair)
            kappa = _weighted_kappa(pair[:, 0], pair[:, 1])
            icc_lo, icc_hi = _boot_ci(pair, lambda a: _icc21(a))
            kappa_lo, kappa_hi = _boot_ci(
                pair, lambda a: _weighted_kappa(a[:, 0], a[:, 1])
            )
            rater[metric] = {
                "n": int(len(pair)),
                "icc_2_1": round(icc, 3),
                "icc_ci": [round(icc_lo, 3), round(icc_hi, 3)]
                if icc_lo is not None
                else None,
                "weighted_kappa": round(kappa, 3),
                "kappa_ci": [round(kappa_lo, 3), round(kappa_hi, 3)]
                if kappa_lo is not None
                else None,
            }

    result = {
        "log_dir": str(log_dir),
        "n_boot": N_BOOT,
        "seed": SEED,
        "agreement": agreement,
        "paired_vs_baselines": diffs,
        "second_rater": rater,
        "note": (
            "The submitted manuscript reported rho=0.83/0.67/0.37 for "
            "correctness/depth/precision. The recomputed NutriAgent-only values "
            "above are the values supported by the deposited scores."
        ),
    }

    json_path = out_dir / "agreement_report.json"
    md_path = out_dir / "agreement_report.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Agreement and paired-difference report (recomputed)",
        "",
        f"> Source: `{log_dir}`  ",
        f"> Bootstrap: {N_BOOT} resamples, seed={SEED}",
        "",
        "## 1. EvaluatorLLM–expert agreement",
        "",
        "| Scope | Metric | n | Spearman ρ | 95% CI | Within 1 point |",
        "|---|---|---:|---:|---|---:|",
    ]
    for key, value in agreement.items():
        scope, metric = key, ""
        for candidate in METRICS:
            if key.endswith("_" + candidate):
                scope = key[: -len(candidate) - 1]
                metric = candidate
                break
        lines.append(
            f"| {scope} | {metric} | {value['n']} | {value['spearman_rho']} | "
            f"[{value['ci_low']}, {value['ci_high']}] | {value.get('within_1_point', '—')} |"
        )
    lines += [
        "",
        "> The submitted values (0.83 / 0.67 / 0.37) are not reproduced by the deposited scores.",
        "",
        "## 2. Paired expert differences (NutriAgent − baseline)",
        "",
        "| Baseline | Metric | n | Δ mean | 95% CI | d_z | Wilcoxon p | Holm p |",
        "|---|---|---:|---:|---|---:|---:|---:|",
    ]
    for display, metrics in diffs.items():
        for metric, value in metrics.items():
            lines.append(
                f"| {display} | {metric} | {value['n']} | {value['mean_diff']} | "
                f"[{value['ci_low']}, {value['ci_high']}] | {value.get('cohen_dz', '—')} | "
                f"{value.get('wilcoxon_p', '—')} | {value.get('holm_p', '—')} |"
            )
    if rater:
        lines += [
            "",
            "## 3. Second-rater reliability",
            "",
            "| Metric | n | ICC(2,1) | ICC 95% CI | Weighted κ | κ 95% CI |",
            "|---|---:|---:|---|---:|---|",
        ]
        for metric, value in rater.items():
            lines.append(
                f"| {metric} | {value['n']} | {value['icc_2_1']} | {value['icc_ci']} | "
                f"{value['weighted_kappa']} | {value['kappa_ci']} |"
            )
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(json.dumps(agreement, indent=2))


if __name__ == "__main__":
    main()
