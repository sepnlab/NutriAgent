"""Provider-equivalence check (E17).

Switching a model to another provider is only acceptable if the served model
behaves the same. This script runs the same queries through two provider/model
pairs and reports response similarity, token counts and latency. If the
similarity falls below the threshold in `config/models.lock.yaml`, treat the
switch as a new model vintage and re-run the whole comparison grid.

Usage:
    python scripts/paper/provider_equivalence.py \
        --provider-a siliconflow --model-a deepseek-ai/DeepSeek-V4-Flash \
        --provider-b aliyun --model-b deepseek-v4-flash-0731

    python scripts/paper/provider_equivalence.py --dry-run
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import random
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_YAML = PROJECT_ROOT / "config" / "models.yaml"
QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
OUT_DIR = PROJECT_ROOT / "docs" / "paper" / "audit"


def load_providers() -> dict:
    cfg = yaml.safe_load(MODELS_YAML.read_text(encoding="utf-8"))
    return {p["provider"]: p for p in cfg.get("providers", [])}


def provider_extra_body(provider: str):
    """Match the pipeline's thinking-disabled settings (src/config.py)."""
    p = provider.lower()
    if p in ("deepseek", "volcano", "siliconflow"):
        return {"thinking": {"type": "disabled"}}
    if p in ("aliyun", "tencent"):
        return {"enable_thinking": False}
    return None


def select_queries(n: int, seed: int = 42) -> list[dict]:
    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    rows = [q for items in data.values() for q in items if q.get("language") == "en"]
    rng = random.Random(seed)
    return rng.sample(rows, min(n, len(rows)))


def call(
    client: OpenAI, model: str, query: str, max_tokens: int, extra_body=None
) -> dict:
    t0 = time.perf_counter()
    try:
        kwargs = {}
        if extra_body:
            kwargs["extra_body"] = extra_body
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": query}],
            temperature=0.0,
            max_tokens=max_tokens,
            **kwargs,
        )
        elapsed = time.perf_counter() - t0
        usage = resp.usage
        return {
            "text": (resp.choices[0].message.content or "").strip(),
            "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
            "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
            "elapsed_s": round(elapsed, 3),
            "error": None,
        }
    except Exception as exc:
        return {
            "text": "",
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "elapsed_s": round(time.perf_counter() - t0, 3),
            "error": f"{type(exc).__name__}: {str(exc)[:200]}",
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider-a", default="siliconflow")
    parser.add_argument("--model-a", default="deepseek-ai/DeepSeek-V4-Flash")
    parser.add_argument("--provider-b", default="aliyun")
    parser.add_argument("--model-b", default="deepseek-v4-flash-0731")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--max-tokens", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--out-dir", default=str(OUT_DIR))
    args = parser.parse_args()

    load_dotenv(PROJECT_ROOT / ".env")
    providers = load_providers()
    pairs = [(args.provider_a, args.model_a), (args.provider_b, args.model_b)]
    configs = []
    for provider, model in pairs:
        meta = providers.get(provider, {})
        key = os.getenv(meta.get("api_key_env", ""), "")
        configs.append(
            {
                "provider": provider,
                "model": model,
                "base_url": meta.get("base_url"),
                "api_key_present": bool(key),
            }
        )

    print("configs:")
    for cfg in configs:
        print(
            f"  {cfg['provider']}/{cfg['model']} base={cfg['base_url']} "
            f"key={'yes' if cfg['api_key_present'] else 'NO'}"
        )
    if args.dry_run:
        return

    clients = {}
    for provider, model in pairs:
        meta = providers[provider]
        clients[(provider, model)] = OpenAI(
            api_key=os.getenv(meta["api_key_env"], ""),
            base_url=meta["base_url"],
            timeout=60,
        )

    queries = select_queries(args.n, args.seed)
    extra_bodies = {
        provider: provider_extra_body(provider) for provider, _ in pairs
    }
    rows = []
    for q in queries:
        for repeat in range(args.repeats):
            a = call(
                clients[pairs[0]],
                pairs[0][1],
                q["query"],
                args.max_tokens,
                extra_bodies.get(pairs[0][0]),
            )
            b = call(
                clients[pairs[1]],
                pairs[1][1],
                q["query"],
                args.max_tokens,
                extra_bodies.get(pairs[1][0]),
            )
            sim = (
                difflib.SequenceMatcher(None, a["text"], b["text"]).ratio()
                if a["text"] and b["text"]
                else 0.0
            )
            rows.append(
                {
                    "id": q["id"],
                    "repeat": repeat,
                    "similarity": round(sim, 3),
                    "a_len": len(a["text"]),
                    "b_len": len(b["text"]),
                    "a_tokens": a["prompt_tokens"] + a["completion_tokens"],
                    "b_tokens": b["prompt_tokens"] + b["completion_tokens"],
                    "a_s": a["elapsed_s"],
                    "b_s": b["elapsed_s"],
                    "a_error": a["error"],
                    "b_error": b["error"],
                }
            )
            print(
                f"{q['id']} rep{repeat}: sim={sim:.2f} "
                f"tok {a['prompt_tokens'] + a['completion_tokens']}/"
                f"{b['prompt_tokens'] + b['completion_tokens']}"
            )

    ok = [r for r in rows if not r["a_error"] and not r["b_error"]]
    sims = [r["similarity"] for r in ok]
    summary = {
        "config_a": configs[0],
        "config_b": configs[1],
        "extra_body": {p: extra_bodies.get(p) for p, _ in pairs},
        "n_queries": len(queries),
        "repeats": args.repeats,
        "n_successful_pairs": len(ok),
        "mean_similarity": round(sum(sims) / len(sims), 3) if sims else None,
        "median_similarity": round(sorted(sims)[len(sims) // 2], 3) if sims else None,
        "fraction_similarity_ge_0_8": round(
            sum(1 for s in sims if s >= 0.8) / len(sims), 3
        )
        if sims
        else None,
        "errors": [r for r in rows if r["a_error"] or r["b_error"]],
        "rows": rows,
        "thresholds": {
            "min_response_similarity": 0.80,
            "on_fail": "treat_as_new_vintage_and_rerun_all",
        },
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "provider_equivalence.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print(
        f"successful={len(ok)}/{len(rows)} mean_sim={summary['mean_similarity']} "
        f">=0.8={summary['fraction_similarity_ge_0_8']}"
    )


if __name__ == "__main__":
    main()
