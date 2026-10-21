"""Reposition the Rev.1 manuscript: title, abstract, highlights, contributions,
and query-selection provenance. Text-only; no numbers changed.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
P = ROOT / "docs" / "paper" / "NutriAgent_paper.md"
lines = P.read_text(encoding="utf-8").splitlines()

TITLE = ("# NutriAgent: a controlled evaluation of specialist routing for "
         "layer-hen nutrition question answering")

ABSTRACT = (
    "Layer-hen nutrition advisory requires breed-, phase-, and ingredient-specific "
    "numerical answers, yet general-purpose LLMs can produce plausible values that are "
    "not traceable to a reference. We present NutriAgent, a specialist-routed multi-agent "
    "system that assigns four nutrition domains to isolated tool-using specialists and "
    "integrates their outputs through a synthesis stage. The system covers 17 layer "
    "breeds, including 10 Chinese domestic strains, and supports English and Chinese "
    "queries. We evaluate it on 54 purposefully selected queries with a primary expert "
    "(378 responses), an independent 120-response reliability rater, and controlled "
    "factorial and ablation experiments. NutriAgent achieved the numerically highest "
    "overall score (4.34 vs 4.05 for the strongest baseline, DeepSeek-V4-Pro) and "
    "significantly higher numeric precision (4.47 vs 3.97; +0.50, Holm p = 0.037). "
    "Correctness was comparable rather than superior (4.46 vs 4.26; +0.20, 95% CI "
    "−0.09 to +0.50; p = 0.146), and performance was strongest on single-value, "
    "comparison, multi-hop, and constraint queries but weaker on open-ended synthesis "
    "(C 3.29). Controlled comparisons separate the contributions of tool access, "
    "retrieval, specialist routing, and synthesis; the reproducible benefit is "
    "precision-focused routing on structured queries, whereas retrieval augmentation "
    "and validation show no measurable correctness gain once the extra synthesis pass "
    "is controlled. The automated judge agrees moderately with the expert on correctness "
    "(ρ = 0.55) and depth (ρ = 0.34) and better on precision (ρ = 0.71), while scoring "
    "more leniently. We report the boundaries explicitly: one primary expert, 54 queries, "
    "a changed current model set, and incomplete human-labeled faithfulness validation."
)

HIGHLIGHTS = [
    "- A specialist-routed, tool-grounded layer-hen system covering 17 breeds, including 10 Chinese domestic strains, with bilingual queries.",
    "- A controlled evaluation separates tool/data access, retrieval, specialist routing, synthesis, and validation across 54 queries and 378 expert-scored responses.",
    "- NutriAgent achieves the numerically highest overall score (4.34) and a significant numeric-precision advantage over the strongest baseline (4.47 vs 3.97; p = 0.037), with comparable correctness.",
    "- Gains concentrate in structured query types; open-ended synthesis is weaker, and component ablations show that retrieval and validation do not add measurable correctness once the extra synthesis pass is controlled.",
    "- Numeric grounding remains limited (0.444); we report the metric's limits, a claim-aware audit, and a reproducible evaluation package rather than treating consistency as provenance.",
]

CONTRIB = (
    "This work makes four contributions. First, it provides a layer-hen nutrition "
    "resource covering 17 breeds — including 10 Chinese domestic strains — with "
    "breed-level provenance and bilingual queries, extending a domain previously "
    "dominated by broiler systems. Second, it presents a precision-focused "
    "specialist-routed architecture with isolated tool access and a separate synthesis "
    "stage, designed for numerical layer-hen questions rather than open-domain chat. "
    "Third, it provides a controlled evaluation that separates tool access, retrieval, "
    "specialist routing, synthesis, validation, backbone, and query type, using expert "
    "scoring for the main comparison and automated scoring only for within-dimension "
    "ablations; this identifies precision-focused routing on structured queries as the "
    "reproducible benefit and shows where the architecture does not add measurable "
    "quality. Fourth, it releases the query sets, prompts, de-identified scores, audit "
    "artifacts, and reproduction commands, with reliability checks (independent rater "
    "ICC 0.85/0.88/0.76; same-expert repeat ICC 0.995/0.996/0.932) that make the "
    "boundaries auditable. NutriAgent is therefore not a new domain ontology; it is a "
    "layer-hen extension plus a controlled test of specialist routing."
)

QUERY = (
    "The 54-query evaluation set was selected by purposeful stratified selection from "
    "the 195-query candidate pool (120 English, 28 Chinese, 30 English advanced, and "
    "17 Chinese advanced), ensuring representation of all seven query types and six "
    "knowledge domains while prioritizing queries that test distinct system "
    "capabilities. The 54-query set was fixed before Rev.1 scoring. Two domain experts "
    "on the study team independently reviewed the selected queries before Rev.1; "
    "external independent query validation was not obtained. Because selection was "
    "criterion-based rather than random, no random seed is reported, and we do not "
    "describe the set as a random sample. The full 195-query pool and the selection "
    "criteria are provided in the repository; the reported results use the 54-query "
    "set. The approach is consistent with established practice in LLM evaluation, where "
    "purposefully curated, stratified sets provide more diagnostic signal per query "
    "than larger, undifferentiated sets (Zheng et al., 2023)."
)

new: list[str] = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("# NutriAgent:"):
        new.append(TITLE)
    elif line.startswith("Poultry nutrition advisory") and "general-purpose LLMs" in line:
        new.append(ABSTRACT)
    elif line.strip() == "## Highlights":
        new.append(line)
        # skip until the next horizontal rule
        i += 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        new.extend(HIGHLIGHTS)
        continue
    elif line.startswith("This work addresses the gaps identified above through four contributions."):
        new.append(CONTRIB)
    elif line.startswith("The curated set was constructed through stratified sampling"):
        new.append(QUERY)
    else:
        new.append(line)
    i += 1

P.write_text("\n".join(new) + "\n", encoding="utf-8")
print("updated", P)
