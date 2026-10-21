"""测试各 LLM 供应商 API 连通性。

遍历 config/models.yaml 中所有供应商，逐个调用 models.list() 探测 API 是否可达。
"""

"""Ping all LLM API providers defined in config/models.yaml.

Usage:
    .venv\Scripts\python scripts\ping_providers.py
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

import yaml

_G = "\033[32m"  # green
_R = "\033[31m"  # red
_Y = "\033[33m"  # yellow
_N = "\033[0m"   # reset
_USE_COLOR = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _c(color: str, text: str) -> str:
    return f"{color}{text}{_N}" if _USE_COLOR else text


def load_providers() -> list[dict]:
    cfg_path = Path(__file__).resolve().parent.parent / "config" / "models.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("providers", [])


def test_provider(p: dict) -> dict:
    name = p["provider"]
    api_key = os.getenv(p.get("api_key_env", ""), "")

    result = {"provider": name, "base_url": p["base_url"], "api_key_set": bool(api_key)}

    if not api_key:
        result["status"] = "SKIP"
        result["detail"] = f"{p['api_key_env']} not set"
        return result

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=p["base_url"], timeout=10)
        models = client.models.list()
        ids = [m.id for m in models]
        result["status"] = "OK"
        result["detail"] = f"{len(ids)} models available"
        result["models"] = ids[:5]
    except Exception as e:
        result["status"] = "FAIL"
        result["detail"] = str(e).split("\n")[0]

    return result


def main():
    providers = load_providers()
    if not providers:
        print("No providers found in config/models.yaml")
        sys.exit(1)

    tags = {"OK": _c(_G, "OK"), "FAIL": _c(_R, "FAIL"), "SKIP": _c(_Y, "SKIP")}

    print(f"{'Provider':<15} {'Status':<6} {'Base URL':<50} {'Detail'}")
    print("-" * 120)

    results = [test_provider(p) for p in providers]
    for r in results:
        print(f"{r['provider']:<15} {tags.get(r['status'], r['status']):<20} {r['base_url']:<50} {r['detail']}")

    print()
    ok = sum(1 for r in results if r["status"] == "OK")
    fail = sum(1 for r in results if r["status"] == "FAIL")
    skip = sum(1 for r in results if r["status"] == "SKIP")
    print(f"Total: {len(results)},  OK: {ok},  FAIL: {fail},  SKIP: {skip}")


if __name__ == "__main__":
    main()
