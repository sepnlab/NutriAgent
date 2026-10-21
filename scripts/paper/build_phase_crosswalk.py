"""Build an explicit crosswalk from breeder phase labels to the 7 standard phases.

The manuscript (§2.1.2) claims that "seven standard phases are defined". The
corpus does not actually contain those seven labels: it contains the original
breeder labels (55 distinct values in the nutrient table, 59 including the
vitamin/mineral table). This script makes the mapping explicit and records the
mapping type, so the revision can report what was remapped and what was not.

Mapping types:
    exact      same label and age range as the standard phase
    within     same phase family, age range inside the standard phase
    boundary   age range crosses a standard-phase boundary
    semantic   label names the phase but its age range sits elsewhere
    composite  label covers several standard phases (left unmapped)
    ambiguous  label alone does not identify a single phase (left unmapped)

Output: corpus/layer/phase_crosswalk.csv
Usage:
    python scripts/paper/build_phase_crosswalk.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
NUTRIENT = PROJECT_ROOT / "corpus" / "layer" / "nutrient_requirements.csv"
VITAMIN = PROJECT_ROOT / "corpus" / "layer" / "nutrient_vitamin_mineral.csv"
OUT = PROJECT_ROOT / "corpus" / "layer" / "phase_crosswalk.csv"

# (standard_phase, mapping_type, note)
MAPPING: dict[str, tuple[str, str, str]] = {
    # ── Starter ─────────────────────────────────────────────
    "S 0-3w": ("Starter 0-6w", "within", "3-phase Chinese scheme; S = starter"),
    "Starter 0-2w": ("Starter 0-6w", "within", ""),
    "Starter 0-3w": ("Starter 0-6w", "within", ""),
    "Starter 0-4w": ("Starter 0-6w", "within", ""),
    "Starter 0-5w": ("Starter 0-6w", "within", ""),
    "Starter 0-6w": ("Starter 0-6w", "exact", ""),
    "Starter 1 (0-3w)": ("Starter 0-6w", "within", "starter split into 1/2"),
    "Starter 1-3w": ("Starter 0-6w", "within", ""),
    "Starter 2 (4-6w)": ("Starter 0-6w", "within", "starter split into 1/2"),
    # ── Grower ──────────────────────────────────────────────
    "G 4-6w": ("Grower 7-12w", "semantic", "labelled G but 4-6w lies in Starter window"),
    "Grower (7-12w)": ("Grower 7-12w", "exact", ""),
    "Grower 3-6w": ("Grower 7-12w", "semantic", "age lies in Starter window"),
    "Grower 4-6w": ("Grower 7-12w", "semantic", "age lies in Starter window"),
    "Grower 4-8w": ("Grower 7-12w", "boundary", ""),
    "Grower 5-10w": ("Grower 7-12w", "boundary", ""),
    "Grower 6-10w": ("Grower 7-12w", "boundary", ""),
    "Grower 6-12w": ("Grower 7-12w", "boundary", ""),
    "Grower 7-12w": ("Grower 7-12w", "exact", ""),
    # ── Developer ───────────────────────────────────────────
    "D1 6-12w": ("Developer 13-17w", "semantic", "D1 of a 4-phase scheme; age overlaps Grower"),
    "D2 13-16w": ("Developer 13-17w", "within", "D2 of a 4-phase scheme"),
    "Developer (13-16w)": ("Developer 13-17w", "within", ""),
    "Developer 11-16w": ("Developer 13-17w", "boundary", ""),
    "Developer 13-16w": ("Developer 13-17w", "within", ""),
    "Developer 13-17w": ("Developer 13-17w", "exact", ""),
    "Developer 7-10w": ("Developer 13-17w", "semantic", "age lies in Grower window"),
    "Developer 9-16w": ("Developer 13-17w", "boundary", ""),
    "Finisher 11-14w": ("Developer 13-17w", "semantic", "finisher label precedes Pre-Lay 15w-5%"),
    # ── Pre-Lay ─────────────────────────────────────────────
    "PL 17w-5%": ("Pre-Lay 18-20w", "boundary", "PL = pre-lay"),
    "Pre-Lay (17w-5%)": ("Pre-Lay 18-20w", "boundary", ""),
    "Pre-Lay 15w-5%": ("Pre-Lay 18-20w", "boundary", ""),
    "Pre-Lay 17w-2%": ("Pre-Lay 18-20w", "boundary", ""),
    "Pre-Lay 17w-5%": ("Pre-Lay 18-20w", "boundary", ""),
    "Pre-Lay 17w-peak": ("Pre-Lay 18-20w", "composite", "spans pre-lay to peak"),
    "Pre-Lay 18-20w": ("Pre-Lay 18-20w", "exact", ""),
    "Pre-Lay 18w-5%": ("Pre-Lay 18-20w", "boundary", ""),
    # ── Lay I ───────────────────────────────────────────────
    "Lay I 21-40w": ("Lay I 21-40w", "exact", ""),
    "Layer I (5%-90%)": ("Lay I 21-40w", "semantic", "physiological-stage label, not age-based"),
    "Layer I (5%-peak+4w)": ("Lay I 21-40w", "semantic", "physiological-stage label"),
    "Layer I 19-50w": ("Lay I 21-40w", "boundary", "age spans Lay I and Lay II"),
    "Peak 5%-peak": ("Lay I 21-40w", "semantic", "peak lies inside Lay I"),
    "Pk1 5%-88%": ("Lay I 21-40w", "semantic", "peak phase 1"),
    "Pk2 88%-83%": ("Lay II 41-60w", "semantic", "post-peak phase 2"),
    # ── Lay II ──────────────────────────────────────────────
    "Lay II 41-60w": ("Lay II 41-60w", "exact", ""),
    "Layer II (90%-80%)": ("Lay II 41-60w", "semantic", "physiological-stage label"),
    "Layer II (peak+4w-90%)": ("Lay II 41-60w", "semantic", "physiological-stage label"),
    "Layer II (peak-90%)": ("Lay II 41-60w", "semantic", "physiological-stage label"),
    "Layer II 51-70w": ("Lay II 41-60w", "boundary", "age spans Lay II and Lay III"),
    # ── Lay III ─────────────────────────────────────────────
    "Lay III 61w+": ("Lay III 61w+", "exact", ""),
    "Layer III (80%-cull)": ("Lay III 61w+", "semantic", "physiological-stage label"),
    "Layer III (90%-85%)": ("Lay III 61w+", "semantic", "physiological-stage label"),
    "Layer III 71-100w": ("Lay III 61w+", "within", ""),
    "Layer IV (85%-cull)": ("Lay III 61w+", "semantic", "breeder-specific 4th laying phase"),
    "PP <83%": ("Lay III 61w+", "semantic", "post-peak production threshold"),
    # ── unmapped ────────────────────────────────────────────
    "Post-Peak <85%": ("unmapped", "ambiguous", "post-peak may span Lay II and Lay III"),
    "Post-Peak <=85%": ("unmapped", "ambiguous", "post-peak may span Lay II and Lay III"),
    "Layer": ("unmapped", "ambiguous", "vitamin table: laying phase not specified"),
    "Rearing": ("unmapped", "composite", "vitamin table: rearing covers 0-18w"),
    "Rearing 0-18w": ("unmapped", "composite", "covers Starter-Grower-Developer-PreLay"),
    "Starter-Grower": ("unmapped", "composite", "covers Starter and Grower"),
}


def main() -> None:
    nut = pd.read_csv(NUTRIENT)
    vit = pd.read_csv(VITAMIN)

    nut_labels = set(nut["Phase"].unique())
    vit_labels = set(vit["Phase"].unique())
    all_labels = nut_labels | vit_labels

    missing = sorted(all_labels - set(MAPPING))
    if missing:
        raise SystemExit(f"phase labels missing from MAPPING: {missing}")
    unused = sorted(set(MAPPING) - all_labels)
    if unused:
        print(f"[warn] MAPPING contains labels not present in the corpus: {unused}")

    nut_breeds = nut.groupby("Phase")["Breed"].apply(lambda s: sorted(set(s))).to_dict()
    vit_breeds = vit.groupby("Phase")["Breed"].apply(lambda s: sorted(set(s))).to_dict()

    rows = []
    for label in sorted(all_labels):
        standard, mtype, note = MAPPING[label]
        nb = nut_breeds.get(label, [])
        vb = vit_breeds.get(label, [])
        rows.append(
            {
                "phase_label": label,
                "standard_phase": standard,
                "mapping_type": mtype,
                "used_by_nutrition": "; ".join(nb),
                "used_by_vitamin": "; ".join(vb),
                "n_breeds_nutrition": len(nb),
                "n_breeds_vitamin": len(vb),
                "note": note,
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False, encoding="utf-8")
    print(f"wrote {OUT} ({len(out)} labels)")
    print(out["mapping_type"].value_counts().to_string())
    print("\nby standard phase:")
    print(out.groupby(["standard_phase", "mapping_type"]).size().to_string())


if __name__ == "__main__":
    main()
