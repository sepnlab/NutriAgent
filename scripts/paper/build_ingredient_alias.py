"""Build a controlled ingredient alias table.

The manuscript's entity-resolution description ("progressively truncated to
its first word or first four characters", §2.1.1) is not a robust identifier
scheme (R2.23). This script creates an explicit alias table:

    canonical_name, alias, alias_type, language, source, note

Only curated aliases are included; the table is meant to be reviewed and
extended by a domain expert before it is used by the resolver.

Output: corpus/shared/ingredient_alias.csv
Usage:
    python scripts/paper/build_ingredient_alias.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BANK = PROJECT_ROOT / "corpus" / "shared" / "feed_ingredient_bank.csv"
OUT = PROJECT_ROOT / "corpus" / "shared" / "ingredient_alias.csv"

# canonical name -> [(alias, alias_type, language), ...]
# alias_type: zh_name | en_variant | abbreviation | misspelling
ALIASES: dict[str, list[tuple[str, str, str]]] = {
    # ── Cereals and by-products ─────────────────────────────
    "Maize": [
        ("玉米", "zh_name", "zh"),
        ("corn", "en_variant", "en"),
        ("maiz", "misspelling", "en"),
    ],
    "Maize, extruded": [("膨化玉米", "zh_name", "zh")],
    "Maize, flaked": [("玉米片", "zh_name", "zh")],
    "Maize, high moisture": [("高水分玉米", "zh_name", "zh")],
    "Maize germ meal, oil < 5%": [("玉米胚芽粕", "zh_name", "zh")],
    "Maize distillers grains with solubles, ethanol production, dried": [
        ("玉米DDGS", "zh_name", "zh"),
        ("maize DDGS", "en_variant", "en"),
        ("DDGS", "abbreviation", "en"),
    ],
    "Corn gluten feed": [("玉米蛋白饲料", "zh_name", "zh")],
    "Corn gluten meal": [("玉米蛋白粉", "zh_name", "zh")],
    "Wheat, soft": [("软小麦", "zh_name", "zh"), ("soft wheat", "en_variant", "en")],
    "Wheat, durum": [("硬粒小麦", "zh_name", "zh"), ("durum wheat", "en_variant", "en")],
    "Wheat bran": [("麸皮", "zh_name", "zh"), ("wheat bran", "en_variant", "en")],
    "Wheat middlings (average)": [("次粉", "zh_name", "zh"), ("wheat middlings", "en_variant", "en")],
    "Wheat feed flour": [("小麦饲料粉", "zh_name", "zh")],
    "Wheat gluten": [("谷朊粉", "zh_name", "zh")],
    "Wheat distillers grains, starch < 7%, dried": [("小麦DDGS", "zh_name", "zh")],
    "Wheat distillers grains, starch > 7%, dried": [("小麦DDGS", "zh_name", "zh")],
    "Barley": [("大麦", "zh_name", "zh")],
    "Barley distillers grains, dried": [("大麦DDGS", "zh_name", "zh")],
    "Barley rootlets, dried": [("大麦胚芽", "zh_name", "zh")],
    "Oats": [("燕麦", "zh_name", "zh")],
    "Rye": [("黑麦", "zh_name", "zh")],
    "Triticale": [("小黑麦", "zh_name", "zh")],
    "Sorghum": [("高粱", "zh_name", "zh")],
    "Millet, pearl": [("珍珠粟", "zh_name", "zh")],
    "Millet, proso": [("糜子", "zh_name", "zh")],
    # ── Protein meals ───────────────────────────────────────
    "Soybean meal, oil < 5%, 46% protein + oil": [
        ("豆粕46%", "zh_name", "zh"),
        ("豆粕46", "zh_name", "zh"),
        ("豆粕", "zh_name", "zh"),          # ambiguous across variants
        ("SBM46", "abbreviation", "en"),
        ("SBM", "abbreviation", "en"),      # ambiguous across variants
        ("soybean meal 46%", "en_variant", "en"),
    ],
    "Soybean meal, oil < 5%, 48% protein + oil": [
        ("豆粕48%", "zh_name", "zh"),
        ("豆粕48", "zh_name", "zh"),
        ("豆粕", "zh_name", "zh"),
        ("SBM48", "abbreviation", "en"),
        ("SBM", "abbreviation", "en"),
        ("soybean meal 48%", "en_variant", "en"),
    ],
    "Soybean meal, oil < 5%, 50% protein + oil": [
        ("豆粕50%", "zh_name", "zh"),
        ("豆粕50", "zh_name", "zh"),
        ("豆粕", "zh_name", "zh"),          # ambiguous across variants
        ("SBM50", "abbreviation", "en"),
        ("SBM", "abbreviation", "en"),      # ambiguous across variants
    ],
    "Soybean, whole, extruded": [("膨化全脂大豆", "zh_name", "zh")],
    "Soybean, whole, toasted": [("烘焙全脂大豆", "zh_name", "zh")],
    "Soybean hulls": [("豆皮", "zh_name", "zh")],
    "Soybean protein concentrate, protein 60-70%": [("大豆浓缩蛋白", "zh_name", "zh")],
    "Cottonseed meal, oil < 5%, crude fibre 15-20%": [("棉粕", "zh_name", "zh"), ("棉籽粕", "zh_name", "zh")],
    "Cottonseed meal, oil < 5%, crude fibre < 15%": [("棉粕", "zh_name", "zh"), ("棉籽粕", "zh_name", "zh")],
    "Cottonseed, whole": [("棉籽", "zh_name", "zh")],
    "Rapeseed meal, oil < 5%": [("菜粕", "zh_name", "zh"), ("菜籽粕", "zh_name", "zh")],
    "Canola meal, oil < 5%": [("双低菜粕", "zh_name", "zh"), ("canola meal", "en_variant", "en")],
    "Rapeseed, whole": [("油菜籽", "zh_name", "zh")],
    "Rapeseed, whole, extruded": [("膨化油菜籽", "zh_name", "zh")],
    "Groundnut meal, oil < 5%, crude fibre < 9%": [("花生粕", "zh_name", "zh")],
    "Groundnut meal, oil < 5%, crude fibre > 9%": [("花生粕", "zh_name", "zh")],
    "Sunflower meal, oil < 5%, dehulled": [("葵花粕", "zh_name", "zh"), ("葵花籽粕", "zh_name", "zh")],
    "Sunflower meal, oil < 5%, non dehulled": [("葵花粕", "zh_name", "zh")],
    "Linseed meal, oil < 5%": [("亚麻粕", "zh_name", "zh"), ("胡麻粕", "zh_name", "zh")],
    "Linseed meal, oil > 5%": [("亚麻粕", "zh_name", "zh")],
    "Sesame meal, oil > 5%": [("芝麻粕", "zh_name", "zh")],
    "Copra meal, oil < 5%": [("椰子粕", "zh_name", "zh")],
    "Palm kernel meal, oil < 5%": [("棕榈仁粕", "zh_name", "zh")],
    "Palm kernel meal, oil 5-20%": [("棕榈仁粕", "zh_name", "zh")],
    "Pea": [("豌豆", "zh_name", "zh")],
    "Pea protein concentrate": [("豌豆蛋白", "zh_name", "zh")],
    "Faba bean, coloured flowers": [("蚕豆", "zh_name", "zh")],
    "Faba bean, white flowers": [("蚕豆", "zh_name", "zh")],
    "Chickpea, kabuli type": [("鹰嘴豆", "zh_name", "zh")],
    "Lupin, blue": [("蓝羽扇豆", "zh_name", "zh")],
    "Lupin, white": [("白羽扇豆", "zh_name", "zh")],
    "Potato protein concentrate": [("马铃薯蛋白", "zh_name", "zh")],
    # ── Animal proteins and fats ────────────────────────────
    "Fish meal, protein 62%": [("鱼粉62%", "zh_name", "zh"), ("鱼粉", "zh_name", "zh"), ("FM", "abbreviation", "en")],
    "Fish meal, protein 65%": [("鱼粉65%", "zh_name", "zh"), ("鱼粉", "zh_name", "zh"), ("FM", "abbreviation", "en")],
    "Fish meal, protein 70%": [("鱼粉70%", "zh_name", "zh"), ("鱼粉", "zh_name", "zh"), ("FM", "abbreviation", "en")],
    "Feather meal": [("羽毛粉", "zh_name", "zh")],
    "Blood meal": [("血粉", "zh_name", "zh")],
    "Processed animal proteins, poultry, protein 60-70%": [("禽类加工蛋白", "zh_name", "zh")],
    "Poultry fat": [("禽脂", "zh_name", "zh")],
    "Lard": [("猪油", "zh_name", "zh")],
    "Tallow": [("牛羊脂", "zh_name", "zh")],
    "Milk powder, skimmed": [("脱脂奶粉", "zh_name", "zh")],
    "Whey powder, acid": [("酸性乳清粉", "zh_name", "zh")],
    "Whey powder, sweet": [("甜乳清粉", "zh_name", "zh")],
    # ── Minerals and additives ──────────────────────────────
    "Limestone": [("石粉", "zh_name", "zh"), ("石灰石", "zh_name", "zh"), ("limesone", "misspelling", "en")],
    "Calcium carbonate": [("碳酸钙", "zh_name", "zh")],
    "Dicalcium phosphate dihydrate": [("磷酸氢钙", "zh_name", "zh"), ("DCP", "abbreviation", "en")],
    "Monocalcium phosphate": [("磷酸二氢钙", "zh_name", "zh"), ("MCP", "abbreviation", "en")],
    "Monodicalcium phosphate": [("磷酸一二钙", "zh_name", "zh")],
    "Sodium chloride": [("食盐", "zh_name", "zh"), ("salt", "en_variant", "en")],
    "Sodium bicarbonate": [("小苏打", "zh_name", "zh"), ("碳酸氢钠", "zh_name", "zh")],
    # ── Energy / fibrous by-products ────────────────────────
    "Alfalfa, dehydrated, protein 17-19% dry matter": [("苜蓿粉", "zh_name", "zh")],
    "Beet pulp, dried": [("甜菜粕", "zh_name", "zh")],
    "Citrus pulp, dried": [("柑橘渣", "zh_name", "zh")],
    "Apple pomace, dried": [("苹果渣", "zh_name", "zh")],
    "Bakery byproduct": [("面包副产物", "zh_name", "zh")],
    "Biscuit byproduct": [("饼干副产物", "zh_name", "zh")],
    "Cassava, starch 66-70%": [("木薯", "zh_name", "zh")],
    "Cassava, starch 70-74%": [("木薯", "zh_name", "zh")],
    "Sweet potato, dried": [("甘薯", "zh_name", "zh"), ("红薯", "zh_name", "zh")],
    "Potato tuber, dried": [("马铃薯", "zh_name", "zh")],
    "Rice, paddy": [("稻谷", "zh_name", "zh")],
    "Rice, brown": [("糙米", "zh_name", "zh")],
    "Rice, polished, broken": [("碎米", "zh_name", "zh")],
    "Rice bran, oil < 5%, crude fibre 5-11%": [("米糠", "zh_name", "zh")],
    "Rice bran, oil < 5%, crude fibre 11-20%": [("米糠", "zh_name", "zh")],
    "Rice bran, oil > 5%, crude fibre 5-11%": [("米糠", "zh_name", "zh")],
    "Rice bran, oil > 5%, crude fibre 11-20%": [("米糠", "zh_name", "zh")],
    "Rice hulls": [("稻壳", "zh_name", "zh")],
    "Brewers grains, dried": [("啤酒糟", "zh_name", "zh")],
    "Brewers yeast, dried": [("啤酒酵母", "zh_name", "zh")],
    "Vinasse, from yeast production, protein 48%": [("酒糟", "zh_name", "zh")],
    "Molasses, beet": [("甜菜糖蜜", "zh_name", "zh")],
    "Molasses, sugarcane": [("甘蔗糖蜜", "zh_name", "zh")],
    # ── Oils ────────────────────────────────────────────────
    "Soybean oil": [("豆油", "zh_name", "zh")],
    "Rapeseed oil": [("菜籽油", "zh_name", "zh")],
    "Sunflower oil": [("葵花籽油", "zh_name", "zh")],
    "Palm oil": [("棕榈油", "zh_name", "zh")],
    # ── Insects ─────────────────────────────────────────────
    "Black soldier fly larvae, fat < 20%, dried": [("黑水虻幼虫", "zh_name", "zh")],
    "Black soldier fly larvae, fat > 20%, dried": [("黑水虻幼虫", "zh_name", "zh")],
    "Mealworm larvae, dried": [("黄粉虫幼虫", "zh_name", "zh")],
}


def main() -> None:
    bank = pd.read_csv(BANK)
    canonical = bank["Ingredient"].astype(str).tolist()

    unknown = sorted(set(ALIASES) - set(canonical))
    if unknown:
        raise SystemExit(f"aliases reference names not in the bank: {unknown}")

    rows = []
    for name in canonical:
        rows.append(
            {
                "canonical_name": name,
                "alias": name,
                "alias_type": "canonical",
                "language": "en",
                "source": "corpus",
                "note": "",
            }
        )
        for alias, alias_type, language in ALIASES.get(name, []):
            rows.append(
                {
                    "canonical_name": name,
                    "alias": alias,
                    "alias_type": alias_type,
                    "language": language,
                    "source": "curated",
                    "note": "",
                }
            )

    out = pd.DataFrame(rows)
    # Generic aliases such as "豆粕" or "鱼粉" necessarily map to several
    # variant rows (46/48/50%; 62/65/70% protein). Keep them but flag them so
    # the resolver can require a more specific variant before matching.
    alias_counts = (
        out[out["alias_type"] != "canonical"]
        .groupby("alias")["canonical_name"]
        .nunique()
    )
    out["ambiguous"] = [
        bool(alias_counts.get(alias, 0) > 1) if alias_type != "canonical" else False
        for alias, alias_type in zip(out["alias"], out["alias_type"])
    ]

    out.to_csv(OUT, index=False, encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"canonical={len(canonical)} aliases={len(out) - len(canonical)}")
    print(out["alias_type"].value_counts().to_string())
    print(out["language"].value_counts().to_string())
    ambiguous = out[out["ambiguous"]][["alias", "canonical_name"]]
    if not ambiguous.empty:
        print("\nambiguous aliases (require a specific variant):")
        print(ambiguous.to_string(index=False))


if __name__ == "__main__":
    main()
