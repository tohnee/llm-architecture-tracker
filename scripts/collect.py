#!/usr/bin/env python3
"""
collect.py — optional data-collection helper for the llm-architecture-tracker skill.

This is a SCAFFOLD for scheduled / repeatable runs. It pulls machine-readable
data (OpenRouter model list + pricing, HuggingFace configs) into the snapshot
schema so the human/Claude analysis step starts from structured data instead of
hand-copied numbers. It does NOT replace the qualitative architecture analysis —
it feeds it.

Network notes:
- OpenRouter exposes a public models endpoint: https://openrouter.ai/api/v1/models
  (no key required for the public list; pricing is included per model).
- HuggingFace config: https://huggingface.co/<org>/<model>/raw/main/config.json
- Some Chinese-lab weights live on ModelScope; configs there are at
  https://modelscope.cn/models/<org>/<model>/resolve/master/config.json

Usage:
    python collect.py --out snapshots/$(date +%F).json
    python collect.py --out snapshots/2026-06-25.json --hf deepseek-ai/DeepSeek-V3.2 Qwen/Qwen3-235B-A22B

Dependencies: only the standard library (urllib). If `requests` is available it
will be used, otherwise urllib.
"""

import argparse
import datetime as dt
import json
import sys
import urllib.request
import urllib.error

OPENROUTER_MODELS = "https://openrouter.ai/api/v1/models"
HF_CONFIG = "https://huggingface.co/{repo}/raw/main/config.json"
MODELSCOPE_CONFIG = "https://modelscope.cn/models/{repo}/resolve/master/config.json"

# Labs we care about, used to tag/filter the OpenRouter list.
TRACKED_LABS = [
    "openai", "anthropic", "google", "deepseek", "z-ai", "glm", "zhipu",
    "moonshot", "kimi", "xiaomi", "mimo", "qwen", "alibaba", "stepfun", "step",
    "mistral", "meta", "llama", "nvidia", "nemotron", "minimax",
]


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "llm-arch-tracker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"[warn] HTTP {e.code} for {url}", file=sys.stderr)
    except Exception as e:  # noqa: BLE001
        print(f"[warn] failed {url}: {e}", file=sys.stderr)
    return None


def get_openrouter_models():
    """Return a list of normalized model dicts with pricing from OpenRouter."""
    raw = fetch(OPENROUTER_MODELS)
    if not raw:
        return []
    data = json.loads(raw).get("data", [])
    out = []
    for m in data:
        pricing = m.get("pricing", {}) or {}
        # OpenRouter prices are per-token strings; convert to per-1M for readability.
        def per_m(key):
            v = pricing.get(key)
            try:
                return round(float(v) * 1_000_000, 4) if v not in (None, "") else None
            except (TypeError, ValueError):
                return None

        out.append({
            "id": m.get("id"),
            "display_name": m.get("name"),
            "context_max": m.get("context_length"),
            "pricing": {
                "currency": "USD",
                "per_1m_input": per_m("prompt"),
                "per_1m_output": per_m("completion"),
                "per_1m_cached_input": per_m("input_cache_read"),
            },
            "modality": (m.get("architecture", {}) or {}).get("modality"),
            "source_url": f"https://openrouter.ai/{m.get('id', '')}",
        })
    return out


def tag_tracked(models):
    """Mark models that belong to a tracked lab so the analyst can prioritize."""
    for m in models:
        mid = (m.get("id") or "").lower()
        m["tracked"] = any(lab in mid for lab in TRACKED_LABS)
    return models


def get_hf_config(repo):
    """Fetch a HuggingFace config.json, falling back to ModelScope."""
    raw = fetch(HF_CONFIG.format(repo=repo))
    if not raw:
        raw = fetch(MODELSCOPE_CONFIG.format(repo=repo))
    if not raw:
        return None
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError:
        return None
    # Pull the architecture-relevant fields the analysis cares about.
    keep = {
        "model_type", "architectures", "num_hidden_layers", "hidden_size",
        "num_attention_heads", "num_key_value_heads", "head_dim",
        "vocab_size", "max_position_embeddings", "rope_theta",
        "intermediate_size", "n_routed_experts", "num_experts",
        "num_experts_per_tok", "n_shared_experts", "moe_intermediate_size",
        "kv_lora_rank", "q_lora_rank", "qk_rope_head_dim", "v_head_dim",
        "sliding_window", "attention_dropout", "torch_dtype",
    }
    extracted = {k: cfg.get(k) for k in keep if k in cfg}
    return {"repo": repo, "config_url": HF_CONFIG.format(repo=repo),
            "config_excerpt": extracted}


def main():
    ap = argparse.ArgumentParser(description="Collect LLM landscape data into a snapshot.")
    ap.add_argument("--out", default=f"snapshots/{dt.date.today().isoformat()}.json")
    ap.add_argument("--hf", nargs="*", default=[],
                    help="HuggingFace repos to pull configs for, e.g. deepseek-ai/DeepSeek-V3.2")
    ap.add_argument("--no-openrouter", action="store_true")
    args = ap.parse_args()

    snapshot = {
        "snapshot_date": dt.date.today().isoformat(),
        "snapshot_version": dt.date.today().strftime("%Y.%m"),
        "generated_by": "llm-architecture-tracker/collect.py",
        "openrouter_models": [],
        "hf_configs": [],
        "models": [],   # left for the analyst/Claude to fill with full Model objects
        "synthesis": {},
        "notes": "Machine-collected scaffold. Architecture/capability analysis is "
                 "done by Claude using the skill's reference files; this file only "
                 "seeds pricing/context/config numbers.",
    }

    if not args.no_openrouter:
        print("[info] fetching OpenRouter model list…", file=sys.stderr)
        snapshot["openrouter_models"] = tag_tracked(get_openrouter_models())
        print(f"[info] got {len(snapshot['openrouter_models'])} models", file=sys.stderr)

    for repo in args.hf:
        print(f"[info] fetching config for {repo}…", file=sys.stderr)
        cfg = get_hf_config(repo)
        if cfg:
            snapshot["hf_configs"].append(cfg)

    import os
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"[done] wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
