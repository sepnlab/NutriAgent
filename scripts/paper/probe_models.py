"""Probe model availability with a real chat call (not just /models).

A model can be listed by a provider and still fail on a real request (billing
mode, region, retired alias). This script sends one short prompt to every
candidate used by the manuscript and records the outcome, including whether
the model returned content or only hidden reasoning.

Usage:
    python scripts/paper/probe_models.py
    python scripts/paper/probe_models.py --max-tokens 128
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "model_probe.json"

# (provider, model, base_url, api_key_env, extra_body)
CANDIDATES = [
    ("xiaomi", "mimo-v2.5-pro", "https://api.xiaomimimo.com/v1", "XIAOMI_API_KEY", None),
    ("xiaomi", "mimo-v2.6-pro", "https://api.xiaomimimo.com/v1", "XIAOMI_API_KEY", None),
    ("aliyun", "MiniMax-M2.5", "https://dashscope.aliyuncs.com/compatible-mode/v1", "ALIYUN_API_KEY", None),
    ("aliyun", "qwen3.5-flash", "https://dashscope.aliyuncs.com/compatible-mode/v1", "ALIYUN_API_KEY", None),
    ("aliyun", "qwen3.6-plus", "https://dashscope.aliyuncs.com/compatible-mode/v1", "ALIYUN_API_KEY", None),
    ("tencent", "minimax-m2.5", "https://tokenhub.tencentmaas.com/v1", "HUNYUAN_API_KEY", {"enable_thinking": False}),
    ("qianwen", "qwen3.8-flash", "https://maas.qianwenaiapi.com/compatible-mode/v1", "QWENAI_API_KEY", {"enable_thinking": False}),
    ("qianwen", "qwen3.8-27b", "https://maas.qianwenaiapi.com/compatible-mode/v1", "QWENAI_API_KEY", {"enable_thinking": False}),
    ("qianwen", "qwen3.8-max", "https://maas.qianwenaiapi.com/compatible-mode/v1", "QWENAI_API_KEY", {"enable_thinking": False}),
    ("qianwen", "qwen3.5-flash", "https://maas.qianwenaiapi.com/compatible-mode/v1", "QWENAI_API_KEY", {"enable_thinking": False}),
    ("deepseek", "deepseek-v4-pro", "https://api.deepseek.com", "DEEPSEEK_API_KEY", None),
    ("siliconflow", "deepseek-ai/DeepSeek-V4-Flash", "https://api.siliconflow.cn/v1", "SILICONFLOW_API_KEY", {"thinking": {"type": "disabled"}}),
    ("siliconflow", "Qwen/Qwen3-8B", "https://api.siliconflow.cn/v1", "SILICONFLOW_API_KEY", {"thinking": {"type": "disabled"}}),
    ("siliconflow", "Qwen/Qwen3.6-27B", "https://api.siliconflow.cn/v1", "SILICONFLOW_API_KEY", {"thinking": {"type": "disabled"}}),
    ("siliconflow", "zai-org/GLM-4.5-Air", "https://api.siliconflow.cn/v1", "SILICONFLOW_API_KEY", {"thinking": {"type": "disabled"}}),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=256,
        help="Budget per probe; reasoning models need headroom, 64 tokens "
        "can be entirely consumed by hidden reasoning and look like an outage.",
    )
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()

    load_dotenv(PROJECT_ROOT / ".env")
    results = []
    for provider, model, base, keyenv, extra_body in CANDIDATES:
        key = os.environ.get(keyenv, "")
        entry = {
            "provider": provider,
            "model": model,
            "base_url": base,
            "api_key_present": bool(key),
            "extra_body": extra_body,
        }
        if not key:
            entry.update({"status": "no_key"})
            results.append(entry)
            continue
        client = OpenAI(api_key=key, base_url=base, timeout=60)
        kwargs = {}
        if extra_body:
            kwargs["extra_body"] = extra_body
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Answer in one word: what is 2+2?"}],
                max_tokens=args.max_tokens,
                temperature=0.0,
                **kwargs,
            )
            msg = resp.choices[0].message
            content = (msg.content or "").strip()
            reasoning = getattr(msg, "reasoning_content", None) or ""
            entry.update(
                {
                    "status": "ok" if content else "empty_content",
                    "finish_reason": resp.choices[0].finish_reason,
                    "content_preview": content[:80],
                    "reasoning_chars": len(reasoning),
                    "completion_tokens": resp.usage.completion_tokens
                    if resp.usage
                    else None,
                }
            )
        except Exception as exc:
            entry.update(
                {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "error": str(exc)[:240],
                }
            )
        results.append(entry)
        print(
            f"{provider:12s} {model:38s} {entry['status']:14s} "
            f"content={entry.get('content_preview', '')!r}"
        )

    out = Path(args.out)
    out.write_text(
        json.dumps({"max_tokens": args.max_tokens, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
