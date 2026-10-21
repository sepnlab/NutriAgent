"""
测试 SelfCheck 多采样是否能走各个供应商的 API。

验证点：
1. 各供应商生成多个样本是否正常
2. temperature=1.0 能产生多样性
3. 有没有供应商层面的兼容问题

用法：.venv\\Scripts\\python scripts\\test_selfcheck_providers.py
"""
import os, json, sys
from openai import OpenAI

os.environ["PYTHONIOENCODING"] = "utf-8"

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

PROVIDERS = [
    {
        "name": "SiliconFlow (当前 SelfCheck)",
        "base_url": "https://api.siliconflow.cn/v1",
        "api_key_env": "SILICONFLOW_API_KEY",
        "model": "deepseek-ai/DeepSeek-V4-Flash",
    },
    {
        "name": "Aliyun (阿里云)",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key_env": "ALIYUN_API_KEY",
        "model": "qwen3.6-plus",
    },
    {
        "name": "Volcano (火山引擎)",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "api_key_env": "HUOSHAN_API_KEY",
        "model": "doubao-seed-2-0-lite-260215",
    },
    {
        "name": "Tencent (腾讯云)",
        "base_url": "https://tokenhub.tencentmaas.com/v1",
        "api_key_env": "HUNYUAN_API_KEY",
        "model": "hy-mt2-pro",
    },
]

TEST_QUERY = "What is the calcium content of limestone?"


def generate_samples(provider_cfg, n=5):
    """模拟 SelfCheckGPT 的采样：temperature=1.0 生成 n 个响应"""
    api_key = os.environ.get(provider_cfg["api_key_env"], "")
    if not api_key:
        return {"name": provider_cfg["name"], "error": f"No API key for {provider_cfg['api_key_env']}", "samples": []}

    client = OpenAI(base_url=provider_cfg["base_url"], api_key=api_key, timeout=30)
    samples = []
    errors = 0

    for i in range(n):
        try:
            resp = client.chat.completions.create(
                model=provider_cfg["model"],
                messages=[
                    {"role": "system", "content": "You are a poultry nutrition assistant."},
                    {"role": "user", "content": TEST_QUERY},
                ],
                temperature=1.0,
                max_tokens=200,
            )
            text = resp.choices[0].message.content or ""
            samples.append({"index": i, "text": text[:100], "len": len(text), "ok": True})
        except Exception as e:
            errors += 1
            samples.append({"index": i, "text": str(e)[:80], "len": 0, "ok": False})

    return {"name": provider_cfg["name"], "n_ok": len(samples) - errors, "n_err": errors, "samples": samples}


if __name__ == "__main__":
    load_env()
    eprint(f"Query: {TEST_QUERY}")
    eprint(f"Samples per provider: 5")
    eprint()

    for p in PROVIDERS:
        eprint(f">>> {p['name']} ({p['model']})")
        result = generate_samples(p, n=5)
        if result.get("error"):
            eprint(f"  SKIP: {result['error']}")
            eprint()
            continue
        eprint(f"  OK: {result['n_ok']}/{result['n_ok']+result['n_err']} samples")
        for s in result["samples"]:
            if s["ok"]:
                eprint(f"    [{s['index']}] len={s['len']:3d}  {s['text']}")
            else:
                eprint(f"    [{s['index']}] ERR: {s['text']}")
        eprint()

    eprint("=== Diversity check ===")
    for p in PROVIDERS:
        result = generate_samples(p, n=5)
        if result.get("error") or result["n_err"] > 0:
            continue
        texts = [s["text"][:60] for s in result["samples"] if s["ok"]]
        unique = len(set(texts))
        eprint(f"  {p['name']:40s}  {unique}/5 unique responses")
