"""导出匿名化的评估 CSV，供人工评分。

用法：
  1. 先跑 python main.py --compare 生成 responses.json
  2. 再跑本脚本生成评分表：
     python scripts/export_for_expert_eval.py [log_dir]
     （不指定 log_dir 则使用最新日志）
  3. 评分人给 correctness / precision / scientific_depth 分别打分（1-5）
  4. 将填好的 CSV 放回 logs/ 目录

输出文件：
  - expert_eval_nutriagent.csv  — NutriAgent 响应评分表（54 条）
  - expert_eval_baselines.csv   — 基线模型响应评分表（54×6 条）
"""
import csv
import json
import os
import glob
import random

LOGS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "logs"))


def find_latest_log():
    """找到最新的 --compare 日志目录。"""
    dirs = sorted(glob.glob(os.path.join(LOGS_DIR, "comp_*")), reverse=True)
    if not dirs:
        raise FileNotFoundError("No comp_* log directories found")
    return dirs[0]


def load_curated_queries():
    """加载 curated 查询集（54 条）。"""
    queries_file = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "..", "queries", "layer",
        "evaluation_queries_curated.json"
    ))
    with open(queries_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    queries = []
    for cat, cat_queries in data.items():
        for q in cat_queries:
            queries.append(q)
    return queries


def load_responses(log_dir):
    """加载 responses.json。"""
    resp_file = os.path.join(log_dir, "responses.json")
    with open(resp_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def export_nutriagent(log_dir, queries, responses):
    """导出 NutriAgent 响应评分表。"""
    # 找到 NutriAgent 的响应
    models = responses.get("models", [])
    resp_dict = responses.get("responses", {})

    nutri_key = None
    for key in resp_dict:
        if "nutrichat" in key.lower() or "nutriagent" in key.lower() or "nutri" in key.lower():
            nutri_key = key
            break

    if not nutri_key:
        print("Error: No NutriAgent responses found")
        return

    nutri_responses = resp_dict[nutri_key]
    print(f"Found NutriAgent responses: {nutri_key} ({len(nutri_responses)} queries)")

    out_path = os.path.join(log_dir, "expert_eval_nutriagent.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([
            "query_id", "category", "query_type", "language",
            "query",
            "response",
            "correctness_(1-5)", "precision_(1-5_or_N/A)", "scientific_depth_(1-5)",
            "notes",
        ])

        for i, q in enumerate(queries):
            resp = nutri_responses[i] if i < len(nutri_responses) else ""
            lang = q.get("language", "en")

            w.writerow([
                q.get("id", f"Q{i+1}"),
                q.get("category", ""),
                q.get("type", ""),
                lang,
                q.get("query", ""),
                resp,
                "", "", "",  # 评分留空
                "",
            ])

    print(f"Exported {len(queries)} NutriAgent responses to {out_path}")
    return out_path


def export_baselines(log_dir, queries, responses):
    """导出基线模型响应评分表（匿名化）。"""
    resp_dict = responses.get("responses", {})

    # 找到所有基线模型
    baseline_keys = []
    for key in resp_dict:
        if "nutrichat" in key.lower() or "nutriagent" in key.lower():
            continue
        baseline_keys.append(key)

    if not baseline_keys:
        print("No baseline responses found")
        return

    print(f"Found {len(baseline_keys)} baselines: {baseline_keys}")

    # 匿名化模型名
    random.seed(42)
    anon_names = [f"Model_{chr(65+i)}" for i in range(len(baseline_keys))]
    random.shuffle(anon_names)
    anon_map = dict(zip(baseline_keys, anon_names))

    out_path = os.path.join(log_dir, "expert_eval_baselines.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([
            "query_id", "category", "query_type", "language",
            "query",
            "model_id",  # 匿名 ID
            "response",
            "correctness_(1-5)", "precision_(1-5_or_N/A)", "scientific_depth_(1-5)",
            "notes",
        ])

        for i, q in enumerate(queries):
            lang = q.get("language", "en")

            for key in baseline_keys:
                model_responses = resp_dict[key]
                resp = model_responses[i] if i < len(model_responses) else ""
                w.writerow([
                    q.get("id", f"Q{i+1}"),
                    q.get("category", ""),
                    q.get("type", ""),
                    lang,
                    q.get("query", ""),
                    anon_map[key],
                    resp,
                    "", "", "",
                    "",
                ])

    # 保存匿名映射（仅研究者可见）
    map_path = os.path.join(log_dir, "expert_eval_anon_map.json")
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(anon_map, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(queries) * len(baseline_keys)} baseline responses to {out_path}")
    print(f"Anonymous mapping saved to {map_path}")
    return out_path


def main():
    import sys
    log_dir = sys.argv[1] if len(sys.argv) > 1 else find_latest_log()
    print(f"Using log directory: {log_dir}")

    queries = load_curated_queries()
    print(f"Loaded {len(queries)} curated queries")

    responses = load_responses(log_dir)
    resp_dict = responses.get("responses", {})
    print(f"Loaded responses for {len(resp_dict)} methods")

    export_nutriagent(log_dir, queries, responses)
    export_baselines(log_dir, queries, responses)

    print("\nDone! Files are ready for expert evaluation.")
    print("Scoring rubric (same as EvaluatorLLM):")
    print("  Correctness: 1=incorrect, 2=partial, 3=adequate, 4=mostly accurate, 5=fully accurate")
    print("  Precision:   1=wrong value, 2=vague, 3=close, 4=near-exact, 5=exact (N/A for definitions)")
    print("  Depth:       1=no science, 2=superficial, 3=adequate, 4=good context, 5=mechanistic")


if __name__ == "__main__":
    main()
