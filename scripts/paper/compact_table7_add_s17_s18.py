"""Compact Table 7 and move the full claim matrix to Supplementary S17.

Also adds the model-transition table S18 used by the model-set note.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
MS = ROOT / "docs" / "paper" / "NutriAgent_paper.md"
SUP = ROOT / "docs" / "paper" / "supplementary_material.md"

t = MS.read_text(encoding="utf-8")
start = t.index("**Table 7.**")
end = t.index("#### 3.6.2", start)
full = t[start:end].rstrip()

compact = """**Table 7.** Summary of claim calibration under the Rev.1 model set. Full 14-row matrix in Supplementary S17. "Not supported" means the Rev.1 evidence does not reproduce the direction or magnitude; "withdrawn" means the condition did not execute as described.

| Submitted claim | Rev.1 evidence | Status |
|---|---|---|
| NutriAgent 4.42 vs 3.80 (+0.62); DeepSeek-V4-Flash strongest | Rev.1 expert: 4.34 vs 4.05 (DeepSeek-V4-Pro strongest); ΔC +0.20 (95% CI −0.09 to +0.50; Holm p = 0.146); ΔP +0.50 (p = 0.037) | **Not replicated; precision-led, not a correctness gain** |
| Synthesis / cross-validation is the dominant driver (+24.2% C, −29.7% inconsistency) | E2: validation-off 4.91 = correct warnings 4.91; shuffled 4.87; query-only 4.85; concatenation 4.28 | **Not supported; extra synthesis pass, not validation content** |
| Multi-agent beats single agent by +5.3% C / −48.3% inconsistency | No-ReAct row was a duplicate full-pipeline run and is withdrawn; E1 tools-only 4.31 < standalone 4.63; multi-agent 4.74/4.83 | **Withdrawn** |
| Each specialist contributes; Feed data are necessary | D2 removal does not reduce quality; E7 Feed hard removal 4.70 vs full 4.40 (single run) | **Not replicated; no positive specialist effect** |
| RAG improves correctness and precision | D4 n=54: +RAG 4.52 vs no-RAG 4.52; C 0.00, P +0.04, D −0.22; see ITT in S19 | **Null on C/P** |
| Hallucination −70%; 56% parametric; evaluator ρ = 0.83/0.67/0.37 | Inconsistency metric renamed; claim-aware support 10.9–16.7%; evaluator ρ = 0.55/0.34/0.71 against Rev.1 expert | **Reframed/corrected** |

"""

MS.write_text(t[:start] + compact + t[end:], encoding="utf-8")

sup = SUP.read_text(encoding="utf-8")
s17 = "\n## S17. Full claim-calibration matrix\n\n" + full.replace("**Table 7.**", "**Table S17.**", 1) + "\n"

s18 = """
## S18. Model-set transition

The submitted model set included endpoints that are no longer available. Rev.1 uses one frozen current set; absolute scores are not comparable across versions.

| Role | Submitted | Rev.1 | Availability note |
|---|---|---|---|
| NutriAgent backbone | DeepSeek-V4-Flash | DeepSeek-V4-Flash | current endpoint |
| Strong baseline | DeepSeek-V4-Pro | DeepSeek-V4-Pro | current endpoint/version |
| Strong baseline | DeepSeek-V4-Flash | DeepSeek-V4-Flash | current endpoint/version |
| Qwen baseline | Qwen3.5-Flash | Qwen3.8-Flash | Qwen3.5 endpoint retired |
| GLM baseline | GLM-4.5-Air | GLM-4.5-Air | current endpoint |
| Small baseline | Qwen3-8B | Qwen3-8B | current endpoint |
| Small baseline | MiniMax-M2.5 | MiniMax-M2.5 | current provider |

| Method | Submitted overall | Rev.1 overall | Direction |
|---|---:|---:|---|
| NutriAgent | 4.42 | 4.34 | −0.08 |
| DeepSeek-V4-Pro | 3.77 | 4.05 | +0.28 |
| DeepSeek-V4-Flash | 3.80 | 4.04 | +0.24 |
| GLM-4.5-Air | 3.59 | 3.55 | −0.04 |
| Qwen (3.5 → 3.8) | 3.44 | 4.01 | +0.57 |
| Qwen3-8B | 3.11 | 3.04 | −0.07 |
| MiniMax-M2.5 | 3.71 | 2.63 | −1.08 |

The strongest submitted baseline improved from 3.80 to 4.05; the NutriAgent point estimate moved by −0.08. Thus much of the smaller margin reflects stronger current baselines, not only a change in NutriAgent. The submitted and Rev.1 scores also use different expert/rubric passes, so the table is descriptive and is not used for causal attribution.
"""

marker = "\n## Closing note"
if marker in sup:
    sup = sup.replace(marker, s17 + s18 + marker, 1)
else:
    sup = sup.rstrip() + "\n" + s17 + s18
SUP.write_text(sup, encoding="utf-8")
print("compacted Table 7; appended S17/S18")
