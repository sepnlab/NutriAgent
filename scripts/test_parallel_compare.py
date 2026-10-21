"""
--compare 并行化可行性测试
直接测试 3 个供应商模型并行执行的效果和限流情况。

用法：.venv\\Scripts\\python scripts\\test_parallel_compare.py
"""
import os
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

os.environ["PYTHONIOENCODING"] = "utf-8"

# ---- config ----
QUERY_IDS = ["CN-LN-005", "CN-BY-006", "FIB-049"]  # 3 queries
N_REPEATS = 1

TEST_MODELS = [
    {
        "name": "DeepSeek-V4-Flash (SiliconFlow)",
        "base_url": "https://api.siliconflow.cn/v1",
        "api_key_env": "SILICONFLOW_API_KEY",
        "model": "deepseek-ai/DeepSeek-V4-Flash",
    },
    {
        "name": "Qwen3.6-Plus (Aliyun)",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key_env": "ALIYUN_API_KEY",
        "model": "qwen3.6-plus",
    },
    {
        "name": "hy-mt2-pro (Tencent)",
        "base_url": "https://tokenhub.tencentmaas.com/v1",
        "api_key_env": "HUNYUAN_API_KEY",
        "model": "hy-mt2-pro",
    },
]


def eprint(*a, **kw):
    print(*a, **kw, flush=True)


def load_env():
    with open(os.path.join(os.path.dirname(__file__), "..", ".env"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, _, v = line.partition("=")
            os.environ[k.strip()] = v.strip()


def load_queries():
    qfile = os.path.join(os.path.dirname(__file__), "..", "queries", "broiler", "evaluation_queries.json")
    with open(qfile, encoding="utf-8") as f:
        data = json.load(f)
    all_q = []
    for cat_list in data.values():
        all_q.extend(cat_list)
    selected = [q for q in all_q if q.get("id") in QUERY_IDS]
    if len(selected) < len(QUERY_IDS):
        selected = all_q[: len(QUERY_IDS)]
    return selected


def call_llm(model_cfg, prompt, timeout=60):
    """通用 LLM 调用，兼容标准 OpenAI 和 Tencent 的非标准格式"""
    api_key = os.environ.get(model_cfg["api_key_env"], "")
    client = OpenAI(base_url=model_cfg["base_url"], api_key=api_key, timeout=timeout)
    resp = client.chat.completions.create(
        model=model_cfg["model"],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0,
    )
    return resp.choices[0].message.content


def run_one_model(model_cfg, queries, run_id):
    """跑一个模型的所有 queries，返回统计"""
    api_key = os.environ.get(model_cfg["api_key_env"], "")
    if not api_key:
        return {"name": model_cfg["name"], "run_id": run_id, "error": "No API key"}

    times = []
    errors = 0
    rate_limited = 0
    results = []

    for q in queries:
        t0 = time.time()
        try:
            text = call_llm(model_cfg, q["query"])
            elapsed = time.time() - t0
            times.append(elapsed)
            results.append({"id": q.get("id", "?"), "ok": True, "elapsed": elapsed})
        except Exception as e:
            elapsed = time.time() - t0
            errors += 1
            times.append(elapsed)
            err = str(e)
            if "429" in err or "rate" in err.lower():
                rate_limited += 1
            results.append({"id": q.get("id", "?"), "ok": False, "elapsed": elapsed, "err": str(e)[:100]})

    return {
        "name": model_cfg["name"],
        "run_id": run_id,
        "total_time": sum(times),
        "avg_time": sum(times) / len(times) if times else 0,
        "max_time": max(times) if times else 0,
        "errors": errors,
        "rate_limited": rate_limited,
        "n_queries": len(times),
        "results": results,
    }


def print_result(r):
    status = "OK" if r["errors"] == 0 else f"ERR({r['errors']})"
    rl = f" RL={r['rate_limited']}" if r["rate_limited"] else ""
    times_detail = ", ".join(f"{x['elapsed']:.1f}s" for x in r["results"])
    eprint(f"  [{r['name']:35s}] run#{r['run_id']}  avg={r['avg_time']:.1f}s  max={r['max_time']:.1f}s  {status}{rl}")
    eprint(f"    times: {times_detail}")


if __name__ == "__main__":
    load_env()
    queries = load_queries()
    n_models = len(TEST_MODELS)
    eprint(f"Queries: {len(queries)} x {n_models} models x {N_REPEATS} rounds = {len(queries)*n_models*N_REPEATS} total calls")
    eprint()

    # === 1. 单模型基线（摸清每个模型独自跑的速度）===
    eprint("=" * 60)
    eprint("  [BASELINE] 每个模型独自串行跑")
    eprint("=" * 60)
    baseline_results = {}
    for model in TEST_MODELS:
        r = run_one_model(model, queries, 0)
        baseline_results[model["name"]] = r
        print_result(r)
    serial_wall_est = sum(r["total_time"] for r in baseline_results.values())
    parallel_ideal = max(r["total_time"] for r in baseline_results.values())
    eprint(f"\n  Baseline serial wall time (sum): {serial_wall_est:.1f}s")
    eprint(f"  Baseline parallel ideal (max):   {parallel_ideal:.1f}s")
    eprint()

    # === 2. 并行执行 ===
    eprint("=" * 60)
    eprint(f"  [PARALLEL] max_workers={n_models} 所有模型同时跑")
    eprint("=" * 60)

    for rnd in range(N_REPEATS):
        eprint(f"\n  --- Round {rnd} ---")
        futures = []
        wall_t0 = time.time()
        with ThreadPoolExecutor(max_workers=n_models) as pool:
            for model in TEST_MODELS:
                futures.append(pool.submit(run_one_model, model, queries, rnd))
            for f in as_completed(futures):
                result = f.result()
                print_result(result)
        wall = time.time() - wall_t0
        eprint(f"  Wall time: {wall:.1f}s")

    eprint()
    eprint("=" * 60)
    eprint("  SUMMARY")
    eprint("=" * 60)
    eprint(f"  Queries per model: {len(queries)}, models: {n_models}, repeats: {N_REPEATS}")
    eprint(f"  Estimated serial wall:   {serial_wall_est:.1f}s")
    eprint(f"  Ideal parallel bound:    {max(baseline_times2.values()):.1f}s")
    eprint()
    eprint("  Per-model baseline (avg/query):")
    for name, r in baseline_results.items():
        eprint(f"    {name:35s}  {r['avg_time']:.1f}s  (total: {r['total_time']:.1f}s)")
