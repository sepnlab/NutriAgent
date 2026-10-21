"""Analyze the completed Rev.1 expert scores.

Primary: 378 responses (54 queries x 7 methods).
Second/third: two independent 120-response subsets covering all 54 queries.

Outputs:
  docs/paper/audit/expert_analysis.json
  docs/paper/audit/expert_analysis.md
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from difflib import SequenceMatcher

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"D:\Geqi_series\NutriChat")
AUDIT = ROOT / "docs" / "paper" / "audit"

MODEL_NAMES = {
    "Model_G": "NutriAgent",
    "Model_D": "DeepSeek-V4-Pro",
    "Model_F": "DeepSeek-V4-Flash",
    "Model_E": "Qwen3.8-Flash",
    "Model_B": "GLM-4.5-Air",
    "Model_C": "Qwen3-8B",
    "Model_A": "MiniMax-M2.5",
}
ORDER = ["NutriAgent", "DeepSeek-V4-Pro", "DeepSeek-V4-Flash", "Qwen3.8-Flash",
         "GLM-4.5-Air", "Qwen3-8B", "MiniMax-M2.5"]


def load(role: str) -> pd.DataFrame:
    df = pd.read_csv(AUDIT / f"expert_scores_{role}.csv")
    df["precision_num"] = pd.to_numeric(df["precision"], errors="coerce")
    df["method"] = df["model_id"].map(MODEL_NAMES)
    df["overall_row"] = df[["correctness", "precision_num", "scientific_depth"]].mean(axis=1)
    return df


def boot_ci(values: np.ndarray, n_boot: int = 10000, seed: int = 42):
    rng = np.random.default_rng(seed)
    values = np.asarray(values, dtype=float)
    idx = rng.integers(0, len(values), size=(n_boot, len(values)))
    means = values[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def boot_overall_ci(sub: pd.DataFrame, n_boot: int = 10000, seed: int = 42):
    """Bootstrap CI for O = (mean C + mean P + mean D)/3."""
    arr = sub[["correctness", "precision_num", "scientific_depth"]].to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(n_boot, len(arr)))
    out = np.empty(n_boot)
    for i in range(n_boot):
        block = arr[idx[i]]
        out[i] = (np.nanmean(block[:, 0]) + np.nanmean(block[:, 1]) + np.nanmean(block[:, 2])) / 3
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def icc21(x: np.ndarray, y: np.ndarray) -> float:
    """Two-way random-effects, absolute agreement, single rater ICC(2,1)."""
    data = np.column_stack([x, y]).astype(float)
    n, k = data.shape
    grand = data.mean()
    subj = data.mean(axis=1)
    rater = data.mean(axis=0)
    ssr = k * ((subj - grand) ** 2).sum()
    ssc = n * ((rater - grand) ** 2).sum()
    sst = ((data - grand) ** 2).sum()
    sse = sst - ssr - ssc
    df_r, df_c, df_e = n - 1, k - 1, (n - 1) * (k - 1)
    msr, msc, mse = ssr / df_r, ssc / df_c, sse / df_e
    denom = msr + (k - 1) * mse + k * (msc - mse) / n
    return float((msr - mse) / denom) if denom else float("nan")


def quadratic_kappa(a: np.ndarray, b: np.ndarray) -> float:
    labels = [1, 2, 3, 4, 5]
    k = len(labels)
    mat = np.zeros((k, k), dtype=float)
    for x, y in zip(a, b):
        if isinstance(x, (int, np.integer)) and isinstance(y, (int, np.integer)) and 1 <= x <= 5 and 1 <= y <= 5:
            mat[int(x) - 1, int(y) - 1] += 1
    total = mat.sum()
    if total == 0:
        return float("nan")
    mat /= total
    weights = np.array([[1 - ((i - j) / (k - 1)) ** 2 for j in range(k)] for i in range(k)])
    po = (weights * mat).sum()
    row, col = mat.sum(axis=1), mat.sum(axis=0)
    pe = (weights * np.outer(row, col)).sum()
    return float((po - pe) / (1 - pe)) if pe != 1 else float("nan")


def bland_altman(a: np.ndarray, b: np.ndarray):
    diff = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    mean = float(diff.mean())
    sd = float(diff.std(ddof=1))
    return {"mean_diff": round(mean, 3), "sd": round(sd, 3),
            "lower": round(mean - 1.96 * sd, 3), "upper": round(mean + 1.96 * sd, 3)}


def agreement(df_a: pd.DataFrame, df_b: pd.DataFrame, metric: str, label: str):
    key = ["query_id", "model_id"]
    merged = df_a[key + [metric]].merge(df_b[key + [metric]], on=key, suffixes=("_a", "_b"))
    merged = merged.dropna(subset=[f"{metric}_a", f"{metric}_b"])
    if metric == "precision":
        merged = merged[pd.to_numeric(merged[f"{metric}_a"], errors="coerce").notna()]
        merged = merged[pd.to_numeric(merged[f"{metric}_b"], errors="coerce").notna()]
        a = pd.to_numeric(merged[f"{metric}_a"]).astype(int).to_numpy()
        b = pd.to_numeric(merged[f"{metric}_b"]).astype(int).to_numpy()
    else:
        a = merged[f"{metric}_a"].astype(int).to_numpy()
        b = merged[f"{metric}_b"].astype(int).to_numpy()
    if len(a) < 3:
        return {"pair": label, "metric": metric, "n": len(a)}
    rho = stats.spearmanr(a, b).statistic
    return {
        "pair": label,
        "metric": metric,
        "n": len(a),
        "icc21": round(icc21(a, b), 3),
        "weighted_kappa": round(quadratic_kappa(a, b), 3),
        "spearman": round(float(rho), 3),
        "bland_altman": bland_altman(a, b),
        "exact_agreement": round(float((a == b).mean()), 3),
        "mean_abs_diff": round(float(np.abs(a - b).mean()), 3),
    }


def note_similarity(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    """Character-level similarity of notes for the same (query, model)."""
    key = ["query_id", "model_id"]
    merged = df_a[key + ["notes"]].merge(df_b[key + ["notes"]], on=key, suffixes=("_a", "_b")).dropna()
    sims = []
    exact = 0
    for a, b in zip(merged["notes_a"].astype(str), merged["notes_b"].astype(str)):
        a, b = a.strip(), b.strip()
        if not a or not b:
            continue
        sims.append(SequenceMatcher(None, a, b).ratio())
        exact += int(a == b)
    return {
        "n": len(sims),
        "median_similarity": round(float(np.median(sims)), 3) if sims else None,
        "n_ge_0_8": int(sum(s >= 0.8 for s in sims)),
        "n_exact": exact,
    }


def main() -> None:
    primary = load("primary")
    second = load("second")
    third = load("third")

    # ---------- primary model table
    rows = []
    for method in ORDER:
        sub = primary[primary["method"] == method]
        c, p, d = sub["correctness"].to_numpy(), sub["precision_num"].dropna().to_numpy(), sub["scientific_depth"].to_numpy()
        ci_c, ci_p, ci_d = boot_ci(c), boot_ci(p), boot_ci(d)
        ci_o = boot_overall_ci(sub)
        rows.append({
            "method": method,
            "n_C": len(c), "n_P": len(p), "n_D": len(d),
            "C": round(float(c.mean()), 3),
            "C_ci": [round(ci_c[0], 3), round(ci_c[1], 3)],
            "P": round(float(p.mean()), 3),
            "P_ci": [round(ci_p[0], 3), round(ci_p[1], 3)],
            "D": round(float(d.mean()), 3),
            "D_ci": [round(ci_d[0], 3), round(ci_d[1], 3)],
            "O": round(float((c.mean() + p.mean() + d.mean()) / 3), 3),
            "O_ci": [round(ci_o[0], 3), round(ci_o[1], 3)],
            "provenance": round(float(sub["provenance"].dropna().mean()), 3) if sub["provenance"].notna().any() else None,
        })
    table = pd.DataFrame(rows).sort_values("O", ascending=False).reset_index(drop=True)
    print(table.to_string(index=False))

    # ---------- paired comparisons vs NutriAgent
    wide = primary.pivot_table(index="query_id", columns="method", values=["correctness", "precision_num", "scientific_depth", "overall_row"], aggfunc="mean")
    baseline_order = [m for m in table["method"] if m != "NutriAgent"]
    comparisons = []
    pvals = []
    for method in baseline_order:
        rec = {"baseline": method}
        for metric, col in [("C", "correctness"), ("P", "precision_num"), ("D", "scientific_depth"), ("O", "overall_row")]:
            g = wide[(col, "NutriAgent")]
            b = wide[(col, method)]
            mask = g.notna() & b.notna()
            diff = (g[mask] - b[mask]).to_numpy()
            if len(diff) == 0:
                continue
            lo, hi = boot_ci(diff)
            dz = float(diff.mean() / diff.std(ddof=1)) if len(diff) > 1 and diff.std(ddof=1) > 0 else float("nan")
            try:
                pval = float(stats.wilcoxon(diff, zero_method="wilcox").pvalue)
            except ValueError:
                pval = 1.0
            rec[metric] = {
                "n": len(diff),
                "diff": round(float(diff.mean()), 3),
                "ci": [round(lo, 3), round(hi, 3)],
                "dz": round(dz, 3),
                "p": pval,
            }
        comparisons.append(rec)
        pvals.append(rec["C"]["p"])

    # Holm across C comparisons
    order = np.argsort(pvals)
    holm = np.ones(len(pvals))
    running = 0.0
    for rank, idx in enumerate(order):
        adjusted = min(1.0, (len(pvals) - rank) * pvals[idx])
        running = max(running, adjusted)
        holm[idx] = running
    for rec, h in zip(comparisons, holm):
        rec["C"]["p_holm"] = round(float(h), 5)

    # ---------- second/third model table (120 subset)
    subset_rows = []
    for method in ORDER:
        s2 = second[second["method"] == method]
        s3 = third[third["method"] == method]
        subset_rows.append({
            "method": method,
            "n2": len(s2), "n3": len(s3),
            "C2": round(float(s2["correctness"].mean()), 3),
            "C3": round(float(s3["correctness"].mean()), 3),
            "P2": round(float(s2["precision_num"].mean()), 3),
            "P3": round(float(s3["precision_num"].mean()), 3),
            "D2": round(float(s2["scientific_depth"].mean()), 3),
            "D3": round(float(s3["scientific_depth"].mean()), 3),
        })

    # ---------- agreement
    agreements = []
    pair_defs = [
        ("second", second, "third", third, "Repeat sheet vs Third (120)"),
        ("primary", primary, "second", second, "Primary vs repeat sheet (120, intra-rater)"),
        ("primary", primary, "third", third, "Primary vs Third (120)"),
    ]
    for _, a, _, b, label in pair_defs:
        for metric in ("correctness", "precision", "scientific_depth", "provenance"):
            agreements.append(agreement(a, b, metric, label))

    # ---------- score distributions / notes
    dist = {}
    for role, df in [("primary", primary), ("second", second), ("third", third)]:
        dist[role] = {}
        for metric in ("correctness", "precision", "scientific_depth", "provenance"):
            sub = df[metric].dropna()
            if sub.empty:
                continue
            counts = sub.value_counts().sort_index()
            dist[role][metric] = {str(k): int(v) for k, v in counts.items()}

    notes = {}
    for role, df in [("primary", primary), ("second", second), ("third", third)]:
        note_df = df[df["notes"].notna()]
        notes[role] = {
            "n_with_notes": int(len(note_df)),
            "examples": note_df["notes"].astype(str).head(20).tolist(),
        }

    result = {
        "primary_table": table.to_dict(orient="records"),
        "comparisons": comparisons,
        "subset_table": subset_rows,
        "agreement": agreements,
        "distributions": dist,
        "notes": notes,
        "note_similarity": {
            "primary_second": note_similarity(primary, second),
            "primary_third": note_similarity(primary, third),
            "second_third": note_similarity(second, third),
        },
        "n_primary": len(primary),
        "n_second": len(second),
        "n_third": len(third),
    }
    (AUDIT / "expert_analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------- markdown
    md = ["# Rev.1 expert-score analysis", "",
          f"Primary: {len(primary)} responses; second: {len(second)}; third: {len(third)}.", "",
          "## Primary model means (378 responses)", "",
          "| Method | C | 95% CI | P | 95% CI | D | 95% CI | Overall | 95% CI | Provenance | n (C/P/D) |",
          "|---|---:|---|---:|---|---:|---|---:|---|---:|---:|"]
    for r in table.to_dict(orient="records"):
        md.append(
            f"| {r['method']} | {r['C']:.2f} | {r['C_ci'][0]:.2f}–{r['C_ci'][1]:.2f} | "
            f"{r['P']:.2f} | {r['P_ci'][0]:.2f}–{r['P_ci'][1]:.2f} | "
            f"{r['D']:.2f} | {r['D_ci'][0]:.2f}–{r['D_ci'][1]:.2f} | "
            f"{r['O']:.2f} | {r['O_ci'][0]:.2f}–{r['O_ci'][1]:.2f} | "
            f"{r['provenance'] if r['provenance'] is not None else '—'} | {r['n_C']}/{r['n_P']}/{r['n_D']} |"
        )

    md += ["", "## Paired comparisons vs NutriAgent", "",
           "| Baseline | ΔC [95% CI] | p (Holm) | d_z | ΔP | ΔD | ΔO |", "|---|---:|---:|---:|---:|---:|---:|"]
    for r in comparisons:
        c = r["C"]
        md.append(
            f"| {r['baseline']} | {c['diff']:+.2f} [{c['ci'][0]:+.2f}, {c['ci'][1]:+.2f}] | "
            f"{c['p_holm']:.4f} | {c['dz']:+.2f} | {r['P']['diff']:+.2f} | {r['D']['diff']:+.2f} | {r['O']['diff']:+.2f} |"
        )

    md += ["", "## Second/third subset means (120 responses)", "",
           "| Method | C2 | C3 | P2 | P3 | D2 | D3 |", "|---|---:|---:|---:|---:|---:|---:|"]
    for r in subset_rows:
        md.append(f"| {r['method']} | {r['C2']:.2f} | {r['C3']:.2f} | {r['P2']:.2f} | {r['P3']:.2f} | {r['D2']:.2f} | {r['D3']:.2f} |")

    md += ["", "## Inter-rater agreement", "",
           "| Pair | Metric | n | ICC(2,1) | weighted κ | Spearman ρ | BA mean (LoA) | exact | MAD |",
           "|---|---|---:|---:|---:|---:|---|---:|---:|"]
    for a in agreements:
        if "icc21" not in a:
            continue
        ba = a["bland_altman"]
        md.append(
            f"| {a['pair']} | {a['metric']} | {a['n']} | {a['icc21']:.3f} | {a['weighted_kappa']:.3f} | "
            f"{a['spearman']:.3f} | {ba['mean_diff']:+.2f} ({ba['lower']:+.2f}, {ba['upper']:+.2f}) | "
            f"{a['exact_agreement']:.2f} | {a['mean_abs_diff']:.2f} |"
        )

    md += ["", "## Data-integrity note", "",
           "- The primary repeat 120-response sheet is a same-expert repeat/copy pass "
           "(user-confirmed; 118/120 exact correctness, 79/80 precision, 106/120 depth; "
           "ICC 0.995/0.996/0.932; notes median similarity 0.70, 38/109 ≥0.80). It is "
           "reported as intra-rater consistency, not independent inter-rater.",
           "- The independent third rater vs primary gives ICC 0.847/0.876/0.760; weighted "
           "kappa 0.846/0.874/0.758; notes median similarity 0.30. The 120 subset does not "
           "reproduce the full top rank (third-rater overall: DeepSeek-V4-Flash 4.28, "
           "DeepSeek-V4-Pro 4.14, NutriAgent 4.12).",
           "- The primary 378-response table (Table 9) remains the main analysis; the subset "
           "is a reliability check, not a ranking replication."]

    (AUDIT / "expert_analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\nwrote", AUDIT / "expert_analysis.md")


if __name__ == "__main__":
    main()
