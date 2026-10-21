"""从已有 responses.json 跑评分（不含 SelfCheck）。

Usage:  .venv/Scripts/python scripts/score_from.py <log_dir>

分两步运行以避免 Bash 工具超时：
  1. 先跑 EvaluatorLLM 评分（每条查询 ~20s，分步执行）
  2. 写入 report.json
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

log_dir = sys.argv[1] if len(sys.argv) > 1 else "logs/log_20260522_144831"

with open(os.path.join(log_dir, "responses.json"), encoding="utf-8") as f:
    data = json.load(f)

queries = data["queries"]
all_responses = data["responses"]
print(f"Loaded {len(queries)} queries, models: {list(all_responses.keys())}")

from src.evaluation.evaluator import EvalReport, compute_flesch, evaluate_tolerance, save_report
from src.evaluation.evaluator_llm import EvaluatorLLM

ev_llm = EvaluatorLLM()

# Build EvalReports step by step
methods = list(all_responses.keys())
reports = {m: EvalReport(m) for m in methods}
all_resp_dict = {"NutriCHAT": all_responses.get("NutriCHAT", all_responses[methods[0]]),
                 **{m: all_responses[m] for m in methods if m != "NutriCHAT"}}

# 1. Flesch
for method in methods:
    for resp in all_resp_dict[method]:
        reports[method].add(flesch=compute_flesch(resp))

# 2. Tolerance
for i, q in enumerate(queries):
    gt = q.get("expected_value")
    if gt is None:
        continue
    for method in methods:
        resp = all_resp_dict[method][i]
        reports[method].add(tol2=evaluate_tolerance(resp, gt, 0.02),
                           tol5=evaluate_tolerance(resp, gt, 0.05))

# 3. EvaluatorLLM — 逐条评分，每条约 20s
print("--- EvaluatorLLM Scoring ---")
for i, q in enumerate(queries):
    batch = {m: all_resp_dict[m][i] for m in methods}
    t0 = time.time()
    scores = ev_llm.score_responses(q["query"], batch)
    elapsed = time.time() - t0
    status = "OK" if scores else "FAIL"
    print(f"  [{i+1}/{len(queries)}] {q.get('id', f'q{i}')} ({elapsed:.0f}s) {status}")
    if scores:
        for method in methods:
            s = scores.get(method, {})
            reports[method].add(c=s.get("correctness"), p=s.get("precision"), d=s.get("scientific_depth"))

# Save
save_report(reports, log_dir)

# Print table
from src.evaluation.evaluator import format_report_table
print(format_report_table(reports))
print(f"\nSaved to {log_dir}/")
