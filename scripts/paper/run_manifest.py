"""Write a reproducibility manifest for one run.

Captures the environment, model lock, config snapshots, prompt/data hashes and
hardware so that a reported number can be traced to the exact code/data/model
set that produced it (reviewer comments R2.33/R2.34 and R4).

Usage:
    python scripts/paper/run_manifest.py
    python scripts/paper/run_manifest.py --log-dir logs/<run> --command "python main.py --compare"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import socket
import sys
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PACKAGES = [
    "openai",
    "langchain",
    "langchain-core",
    "langchain-openai",
    "langchain-chroma",
    "sentence-transformers",
    "torch",
    "chromadb",
    "pandas",
    "numpy",
    "scipy",
    "PyYAML",
    "textstat",
    "pydantic",
]

PROMPT_SOURCES = [
    "src/agent/router_agent.py",
    "src/agent/synthesis_agent.py",
    "src/agent/validation.py",
    "src/agent/base_agent.py",
    "src/agent/react_agent.py",
    "src/agent/multi_agent_engine.py",
    "src/agent/specialist_feed.py",
    "src/agent/specialist_nutrition.py",
    "src/agent/specialist_performance.py",
    "src/agent/specialist_definitions.py",
    "src/evaluation/evaluator_llm.py",
    "src/evaluation/faithfulness.py",
    "src/evaluation/selfcheck.py",
    "src/evaluation/evaluator.py",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_info() -> dict:
    git_dir = PROJECT_ROOT / ".git"
    if not git_dir.exists():
        return {}
    try:
        head = (git_dir / "HEAD").read_text(encoding="utf-8").strip()
        if head.startswith("ref: "):
            ref = head[5:]
            ref_path = git_dir / ref
            commit = ref_path.read_text(encoding="utf-8").strip() if ref_path.exists() else None
            branch = ref.rsplit("/", 1)[-1]
        else:
            commit, branch = head, None
        return {"branch": branch, "commit": commit}
    except Exception as exc:
        return {"error": str(exc)}


def package_versions() -> dict:
    out = {}
    for name in PACKAGES:
        try:
            out[name] = version(name)
        except PackageNotFoundError:
            out[name] = None
        except Exception:
            out[name] = None
    return out


def gpu_info() -> dict:
    try:
        import torch

        available = bool(torch.cuda.is_available())
        return {
            "cuda_available": available,
            "cuda_version": torch.version.cuda,
            "devices": [
                torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())
            ]
            if available
            else [],
        }
    except Exception as exc:
        return {"error": str(exc)}


def file_hashes() -> dict:
    hashes = {}

    def add(path: Path, label: str) -> None:
        if path.exists():
            hashes[label] = {"path": str(path.relative_to(PROJECT_ROOT)), "sha256": sha256(path)}

    for path in sorted((PROJECT_ROOT / "corpus").glob("**/*.csv")):
        if "_backup" in path.parts:
            continue
        add(path, f"corpus/{path.relative_to(PROJECT_ROOT / 'corpus')}")
    for path in sorted((PROJECT_ROOT / "queries" / "layer").glob("*.json")):
        add(path, f"queries/layer/{path.name}")
    for path in sorted((PROJECT_ROOT / "config").glob("*.yaml")):
        add(path, f"config/{path.name}")
    for rel in PROMPT_SOURCES:
        add(PROJECT_ROOT / rel, rel)
    return hashes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None)
    parser.add_argument("--log-dir", default=None)
    parser.add_argument("--command", default=None)
    args = parser.parse_args()

    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    out = Path(args.out) if args.out else PROJECT_ROOT / "logs" / f"run_manifest_{timestamp}.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    lock_path = PROJECT_ROOT / "config" / "models.lock.yaml"
    model_lock = None
    if lock_path.exists():
        try:
            model_lock = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
        except Exception as exc:
            model_lock = {"error": str(exc)}

    log_config = None
    if args.log_dir:
        config_path = Path(args.log_dir) / "config.yaml"
        if config_path.exists():
            try:
                log_config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            except Exception as exc:
                log_config = {"error": str(exc)}

    manifest = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python": sys.version,
        "cwd": str(Path.cwd()),
        "command": args.command,
        "git": git_info(),
        "packages": package_versions(),
        "gpu": gpu_info(),
        "env_vars_present": sorted(
            k
            for k in os.environ
            if k.endswith("_API_KEY") or k.endswith("_BASE_URL")
        ),
        "model_lock": model_lock,
        "run_config": log_config,
        "files": file_hashes(),
    }

    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print(f"files hashed: {len(manifest['files'])}")
    print(f"git: {manifest['git']}")
    print(f"cuda: {manifest['gpu'].get('cuda_available')}")


if __name__ == "__main__":
    main()
