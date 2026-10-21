"""从日志目录的 responses.json 导出响应表格 CSV，支持中英文。

每行一条查询，每列一个模型的响应，方便人工评分或对比。

用法:
  python scripts/export_responses.py                          # 默认最新日志，英文
  python scripts/export_responses.py --lang zh                # 中文翻译版（本地模型）
  python scripts/export_responses.py logs/eval_xxx/           # 指定日志目录
  python scripts/export_responses.py logs/eval_xxx/ --lang zh
"""
import argparse
import csv
import hashlib
import json
import os
import sys
from typing import List

_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_DEFAULT_MODEL = os.path.join(_PROJECT_ROOT, "models", "Hy-MT1.5-1.8B")
_CACHE_PATH = os.path.join(_PROJECT_ROOT, ".cache", "translations.json")
_BATCH_SIZE = 4


class Translator:
    """Local translation model with batch inference and disk cache."""

    def __init__(self, model_path: str):
        self.model_path = model_path
        self._tokenizer = None
        self._model = None
        self._cache: dict[str, str] = {}
        self._load_cache()

    # ── cache ────────────────────────────────────────────────

    def _load_cache(self):
        os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
        if os.path.exists(_CACHE_PATH):
            try:
                with open(_CACHE_PATH, encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception:
                self._cache = {}

    def _save_cache(self):
        try:
            with open(_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    # ── model loading ────────────────────────────────────────

    def _load_model(self):
        if self._model is not None:
            return
        print(f"  Loading translation model from {self.model_path}...")
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_path, trust_remote_code=True, padding_side="left"
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path, trust_remote_code=True, device_map="auto"
        )
        if self._tokenizer.pad_token_id is None:
            self._tokenizer.pad_token_id = self._tokenizer.eos_token_id
        print(f"  Model loaded (batch_size={_BATCH_SIZE}, cached={len(self._cache)}).")

    # ── translate one ────────────────────────────────────────

    def translate_one(self, text: str) -> str:
        if not text or len(text.strip()) <= 5:
            return text
        key = self._cache_key(text)
        if key in self._cache:
            return self._cache[key]
        self._load_model()
        result = self._translate_batch([text])[0]
        self._cache[key] = result
        self._save_cache()
        return result

    # ── translate many (batched + cached) ────────────────────

    def translate_many(self, items: List[tuple]) -> List[str]:
        """Translate a list of (label, text) pairs, returns translated texts.

        - label: display label for progress (e.g. "DEF-008 / model name")
        - text:  the text to translate
        """
        # Skip trivial and cached
        pending_texts: List[str] = []
        pending_indices: List[int] = []
        results: List[str] = [""] * len(items)

        for i, (label, text) in enumerate(items):
            if not text or len(text.strip()) <= 5:
                results[i] = text
                continue
            key = self._cache_key(text)
            if key in self._cache:
                results[i] = self._cache[key]
                continue
            pending_texts.append(text)
            pending_indices.append(i)

        if not pending_texts:
            return results

        self._load_model()
        total = len(items)
        done = total - len(pending_texts)

        # Translate in batches
        for start in range(0, len(pending_texts), _BATCH_SIZE):
            batch = pending_texts[start:start + _BATCH_SIZE]
            batch_results = self._translate_batch(batch)
            for j, result in enumerate(batch_results):
                idx = pending_indices[start + j]
                results[idx] = result
                key = self._cache_key(pending_texts[start + j])
                self._cache[key] = result
                done += 1
                lbl = items[idx][0]
                print(f"  Translating [{done}/{total}]: {lbl[:60]}...")

        self._save_cache()
        return results

    # ── batch inference ──────────────────────────────────────

    def _translate_batch(self, texts: List[str]) -> List[str]:
        """Run model.generate on a batch of texts with padding."""
        import torch
        prompts = [
            f"Translate from English to Chinese. Output ONLY the Chinese translation, no explanations.\n\n{t}"
            for t in texts
        ]
        inputs = self._tokenizer(
            prompts, padding=True, return_tensors="pt", truncation=True, max_length=512,
            padding_side="left",
        )
        input_ids = inputs.input_ids.to(self._model.device)
        attn_mask = inputs.attention_mask.to(self._model.device)

        outputs = self._model.generate(
            input_ids, attention_mask=attn_mask,
            max_new_tokens=512,
            top_k=20, top_p=0.6, repetition_penalty=1.05, temperature=0.7,
        )
        results = []
        for i, out in enumerate(outputs):
            prompt_len = (input_ids[i] != self._tokenizer.pad_token_id).sum().item()
            decoded = self._tokenizer.decode(out[prompt_len:], skip_special_tokens=True)
            # Strip any trailing repetition (model sometimes loops)
            lines = decoded.strip().split("\n")
            clean = []
            for line in lines:
                if line not in clean:
                    clean.append(line)
            results.append("\n".join(clean))
        return results


# ═══════════════════════════════════════════════════════════════
# ApiTranslator: online API (via OpenAI-compatible endpoint)
# ═══════════════════════════════════════════════════════════════

class ApiTranslator:
    """Translate via OpenAI-compatible API (e.g. SiliconFlow / DeepSeek)."""

    @staticmethod
    def _load_settings():
        """Load translation config from config/translation.yaml."""
        import yaml
        path = os.path.join(_PROJECT_ROOT, "config", "translation.yaml")
        try:
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def __init__(self, model: str = None):
        import os as _os
        from openai import OpenAI
        settings = self._load_settings()
        api_model = settings.get("api_model") or "Qwen/Qwen3.5-9B"
        self._model = model or api_model

        # Resolve API key and base_url
        tr_base_url = settings.get("base_url")
        tr_key_env = settings.get("api_key_env")
        if tr_key_env:
            api_key = _os.getenv(tr_key_env, "")
        else:
            from src.config import Config
            api_key = Config.LLM_API_KEY

        if tr_base_url:
            self._client = OpenAI(api_key=api_key, base_url=tr_base_url)
        else:
            from src.config import Config
            self._client = OpenAI(api_key=api_key, base_url=Config.LLM_BASE_URL)

        self._timeout = settings.get("timeout", 30)
        self._concurrency = settings.get("concurrency", 4)
        self._cache: dict[str, str] = {}
        self._load_cache()

    def _load_cache(self):
        os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
        if os.path.exists(_CACHE_PATH):
            try:
                with open(_CACHE_PATH, encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception:
                self._cache = {}

    def _save_cache(self):
        try:
            with open(_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    def translate_many(self, items: List[tuple]) -> List[str]:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results: List[str] = [""] * len(items)
        pending = []
        for i, (label, text) in enumerate(items):
            if not text or len(text.strip()) <= 5:
                results[i] = text
                continue
            key = self._cache_key(text)
            if key in self._cache:
                results[i] = self._cache[key]
                continue
            pending.append((i, label, text))

        if not pending:
            return results

        total = len(items)
        done = total - len(pending)

        def _translate_one(idx, label, text):
            from src.retry import llm_retry
            @llm_retry
            def _call():
                return self._client.chat.completions.create(
                    model=self._model,
                    messages=[
                        {"role": "user", "content": f"Translate the following English text to Simplified Chinese. Output ONLY the Chinese translation, no explanations or extra text:\n\n{text}"},
                    ],
                    temperature=0.0,
                    max_tokens=512,
                    timeout=self._timeout,
                    extra_body={"thinking": {"type": "disabled"}},
                )
            try:
                resp = _call()
                translated = resp.choices[0].message.content.strip()
                if translated:
                    return idx, translated
            except Exception as e:
                print(f"  [WARN] Translation failed: {e}", file=sys.stderr)
            return idx, text

        # Build index→text lookup for cache key resolution
        _idx_to_text = {i: text for i, label, text in pending}

        max_workers = min(self._concurrency, len(pending))
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(_translate_one, i, label, text): (i, label)
                       for i, label, text in pending}
            for f in as_completed(futures):
                idx, translated = f.result()
                results[idx] = translated
                key = self._cache_key(_idx_to_text[idx])
                self._cache[key] = translated
                done += 1
                lbl = futures[f][1]
                print(f"  Translating [{done}/{total}]: {lbl[:60]}...")

        self._save_cache()
        return results


# ═══════════════════════════════════════════════════════════════
# Translator: local model (via transformers)
# ═══════════════════════════════════════════════════════════════


def find_latest_log() -> str:
    logs_dir = os.path.join(_PROJECT_ROOT, "logs")
    candidates = []
    for d in os.listdir(logs_dir):
        rp = os.path.join(logs_dir, d, "responses.json")
        if os.path.isfile(rp):
            candidates.append((os.path.getmtime(rp), os.path.join(logs_dir, d)))
    if not candidates:
        print("Error: no log directories with responses.json found")
        sys.exit(1)
    return max(candidates, key=lambda x: x[0])[1]


def export(log_dir: str, lang: str = "en", model_path: str = _DEFAULT_MODEL, use_api: bool = False, api_model: str = None):
    responses_path = os.path.join(log_dir, "responses.json")
    if not os.path.exists(responses_path):
        print(f"Error: {responses_path} not found")
        sys.exit(1)

    with open(responses_path, encoding="utf-8") as f:
        data = json.load(f)

    models = data["models"]
    queries = data["queries"]
    responses = data["responses"]

    is_zh = lang == "zh"
    suffix = "_zh" if is_zh else ""
    out_path = os.path.join(log_dir, f"responses_table{suffix}.csv")

    if is_zh and use_api:
        translator = ApiTranslator(model=api_model)
    elif is_zh:
        translator = Translator(model_path)
    else:
        translator = None

    # Collect all texts for batch translation: (label, text) pairs
    to_translate = []
    if is_zh:
        for i, q in enumerate(queries):
            if q["query"]:
                to_translate.append((f"query {q.get('id','')}", q["query"]))
            for m in models:
                resp_list = responses.get(m, [])
                text = resp_list[i] if i < len(resp_list) else ""
                if text:
                    to_translate.append((f"{q.get('id','')} / {m[:30]}", text))

    # Translate all at once
    translated = translator.translate_many(to_translate) if is_zh else []
    ti = iter(translated)

    # Write CSV
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "category", "type", "query", "expected_value"] + models)

        for i, q in enumerate(queries):
            query_text = next(ti, "") if is_zh and q["query"] else q["query"]

            row = [
                q.get("id", f"Q{i+1:03d}"),
                q.get("category", ""),
                q.get("type", ""),
                query_text,
                q.get("expected_value", ""),
            ]
            for m in models:
                resp_list = responses.get(m, [])
                text = resp_list[i] if i < len(resp_list) else ""
                if is_zh and text:
                    text = next(ti, text)  # fallback to original if iterator exhausted
                row.append(text)
            w.writerow(row)

    print(f"\nExported {len(queries)} queries × {len(models)} models → {out_path}")
    if is_zh:
        print(f"  ({len(to_translate)} items translated, cache: {len(translator._cache)})")


def parse_args():
    parser = argparse.ArgumentParser(description="Export response table from log directory")
    parser.add_argument("log_dir", nargs="?", default=None, help="Path to log directory")
    parser.add_argument("--lang", choices=["en", "zh"], default="en",
                        help="Language: en (original) or zh (translated)")
    parser.add_argument("--model-path", default=_DEFAULT_MODEL,
                        help=f"Path to local translation model (default: {_DEFAULT_MODEL})")
    parser.add_argument("--api", action="store_true",
                        help="Use online API (SiliconFlow) instead of local model")
    parser.add_argument("--api-model", default=None,
                        help="API model name (default: same as NutriCHAT base model)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_dir = args.log_dir or find_latest_log()
    export(log_dir, lang=args.lang, model_path=args.model_path,
           use_api=args.api, api_model=args.api_model)
