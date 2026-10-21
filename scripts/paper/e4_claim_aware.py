"""E4 (rule-based layer): claim-aware numeric faithfulness audit.

For each E1 multi-agent response:
  - extract numeric claims with entity/attribute/unit context
  - search the query's tool-observation trace for a supporting value
  - classify each claim as:
      direct        entity + attribute + value within 5%
      attribute     attribute + value (entity not found)
      any_number    value appears, but attribute/entity context not established
      unsupported   no matching value
This is a heuristic audit, not the human-labeled validation; units are compared
in the claim's canonical value without full observation-unit parsing.

Usage:
    python scripts/paper/e4_claim_aware.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.validation import extract_claims  # noqa: E402

CACHE = PROJECT_ROOT / "logs" / "ablation_architecture_factorial_layer_20261020_181143" / ".ablation_cache.json"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e4_claim_aware.json"

ATTR_RE = {
    "calcium": r"\b(?:calcium|ca)\b",
    "crude_protein": r"\b(?:crude\s+protein|cp)\b",
    "metabolizable_energy": r"\b(?:metabolizable\s+energy|me|kcal)\b",
    "lysine": r"\b(?:lysine|lys)\b",
    "methionine": r"\b(?:methionine|met)\b",
    "phosphorus": r"\b(?:phosphorus|available\s+p|total\s+p|p)\b",
}


def numbers(text: str) -> list[float]:
    return [float(x.replace(",", "")) for x in re.findall(r"[0-9][0-9,]*(?:\.[0-9]+)?", text)]


def close(a: float, b: float, tol: float = 0.05) -> bool:
    return abs(a - b) / max(abs(a), abs(b), 1e-9) <= tol


def classify(claim, observations: str) -> str:
    if not observations:
        return "unsupported"
    obs = observations.lower()
    attr = ATTR_RE.get(claim.attribute)
    attr_present = bool(attr and re.search(attr, obs))
    entity_present = bool(claim.entity and claim.entity.lower() in obs)
    nums = numbers(observations)
    value_match = any(close(claim.canonical, n) for n in nums)
    if entity_present and attr_present and value_match:
        return "direct"
    if attr_present and value_match:
        return "attribute"
    if value_match:
        return "any_number"
    return "unsupported"


def main() -> None:
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    variants = ["Multi-Agent (validation on)", "Multi-Agent (validation off)"]
    out = {}
    for variant in variants:
        entries = cache.get(variant, {})
        counts = {"direct": 0, "attribute": 0, "any_number": 0, "unsupported": 0}
        rows = []
        for query, entry in entries.items():
            resp = entry.get("resp", "") if isinstance(entry, dict) else str(entry)
            trace = entry.get("trace", []) if isinstance(entry, dict) else []
            observations = "\n".join(
                str(s.get("observation", "")) for s in trace if isinstance(s, dict)
            )
            claims = extract_claims(resp, "synthesis")
            local = {"direct": 0, "attribute": 0, "any_number": 0, "unsupported": 0}
            for c in claims:
                label = classify(c, observations)
                counts[label] += 1
                local[label] += 1
            if claims:
                rows.append({"query": query[:120], "n_claims": len(claims), **local})
        total = sum(counts.values())
        out[variant] = {
            "n_claims": total,
            "counts": counts,
            "rates": {k: round(v / total, 3) if total else None for k, v in counts.items()},
            "rows": rows,
        }
        print(variant, total, out[variant]["rates"])

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [
        "# E4 rule-based claim-aware numeric audit",
        "",
        "Claims extracted with entity/attribute/unit context; support searched in the query's tool observations.",
        "",
        "| Variant | Claims | Direct | Attribute | Any number | Unsupported |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for v, d in out.items():
        r = d["rates"]
        md.append(
            f"| {v} | {d['n_claims']} | {r['direct']:.1%} | {r['attribute']:.1%} | "
            f"{r['any_number']:.1%} | {r['unsupported']:.1%} |"
        )
    md += [
        "",
        "**Interpretation and caveat.** `direct` requires the claim's entity and attribute to appear in the",
        "tool observation and a value within 5%; `attribute` drops the entity requirement; `any_number` is",
        "the old permissive criterion. Units are compared in the claim's canonical value without full",
        "observation-unit parsing. This is a rule-based audit, not the human-labeled validation (E4);",
        "it shows how much the permissive 0.444 score overstates claim-level support.",
    ]
    OUT.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
