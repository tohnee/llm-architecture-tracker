---
name: llm-architecture-tracker
description: >-
  Continuously research, analyze, and report on the world's leading large
  language models — their architecture, capabilities, and pricing. Use this
  skill whenever the user wants to track, compare, survey, or deep-dive into
  frontier LLMs (OpenAI/GPT, Anthropic/Claude, Google/Gemini, DeepSeek, GLM/Z.ai,
  Kimi/Moonshot, Xiaomi MiMo, Qwen, StepFun, Mistral, Llama, NVIDIA Nemotron,
  MiniMax, and others). Trigger it for requests like "update me on the latest
  models", "compare model X and Y architectures", "generate an LLM landscape
  report", "what changed in DeepSeek V4", "build me a model comparison", "track
  new releases", "what are the top models on OpenRouter", or any request that
  involves collecting model technical reports / HuggingFace cards / ModelScope /
  OpenRouter usage + pricing and turning them into a rigorous architecture-and-
  capability analysis. Also use it to produce the recurring HTML research
  report. Use this even when the user only names one model or asks a seemingly
  simple "what's new" question — the value is in the systematic, sourced,
  architecture-level analysis this skill enforces.
license: For internal research and reporting use.
---

# LLM Architecture & Capability Tracker

This skill turns Claude into a disciplined analyst that tracks the frontier LLM
landscape end-to-end: it collects primary sources, extracts architecture and
capability details rigorously, gathers live pricing and usage data, and emits a
polished, diagram-rich HTML research report on a recurring basis.

The guiding principle is **primary sources over summaries, structure over
vibes**. A benchmark number means little without knowing the architecture,
active-parameter count, attention mechanism, context strategy, and price that
produced it. This skill always reconstructs that full picture.

## When and how to use this skill

Use the skill in one of four modes. Detect the mode from the request, then
follow the matching workflow below.

| Mode | Trigger | Output |
|------|---------|--------|
| **A. Full landscape report** | "generate the report", "survey all models", periodic refresh | Complete HTML report (all tracked models) |
| **B. Single-model deep dive** | "deep dive on DeepSeek V4", "analyze MiMo V2" | HTML section or standalone report for one model |
| **C. Comparison** | "compare Kimi K2.6 vs GLM-5.1" | HTML comparison table + analysis |
| **D. Delta / what's new** | "what changed this month", "track new releases" | HTML changelog vs. the last snapshot |

In all modes: **research first (Step 1), analyze rigorously (Step 2), then
render (Step 3).** Never skip straight to writing prose from memory — model
facts go stale fast and the entire value of this skill is freshness and rigor.

---

## The tracked model roster

These are the priority targets. Always confirm the *current* flagship + newest
release for each lab by searching — the version numbers below are anchors, not
ground truth, and will be out of date.

| Lab / Family | Anchor flagships (verify current) | Why tracked |
|--------------|-----------------------------------|-------------|
| **OpenAI** | GPT-5.x series, gpt-oss (open weight) | Frontier closed + open-weight baseline |
| **Anthropic / Claude** | Claude Opus / Sonnet / Haiku 4.x | Frontier closed, coding/agentic leader |
| **Google / Gemini** | Gemini 3.x Pro / Flash / Flash-Lite, Gemma 4 (open) | Frontier closed + open Gemma line |
| **DeepSeek** | V3 → V3.2 → V4 / V4 Flash | Most-copied open architecture (MLA, MoE, DSA) |
| **GLM / Z.ai (Zhipu)** | GLM-4.5 → 4.7 → 5 → 5.1 | High-cadence open, Prefix-LM + DSA |
| **Kimi / Moonshot** | K2 → K2.5 → K2.6 | Trillion-param MLA MoE, agentic |
| **Xiaomi MiMo** | MiMo-V2-Pro / V2.5-Pro | Top OpenRouter usage, long-horizon agentic |
| **Qwen / Alibaba** | Qwen3 → 3.5 → 3.6/3.7 Plus, Qwen3-Coder-Next | Most complete open family, hybrid attention |
| **StepFun** | Step 3.5 Flash → 3.7 Flash | Efficiency-first, high tok/s, MTP-3 |
| **Mistral** | Mistral 3 Large (adopts DeepSeek arch) | Western open, DeepSeek-template adopter |
| **Meta / Llama** | Llama 4 (Scout/Maverick/Behemoth) | Western open baseline, iRoPE/MoE |
| **NVIDIA Nemotron** | Nemotron 3 Super / Ultra | Hybrid Mamba-Transformer, hardware-co-designed |
| **MiniMax** | M1 → M2.x → M3 | Linear/lightning attention, 1M context |

Always also pull the **OpenRouter top-usage list** to catch models outside this
roster that have become important (a single high-volume app or a cheap new
preview can vault a model to #1 — note these, but flag usage-rank ≠ quality).

---

## Step 1 — Research & source collection

Collect from primary sources in roughly this priority order. Do not stop at one
source per model; cross-check architecture claims against at least the technical
report **and** the model config when both exist.

### 1.1 Source hierarchy (best → acceptable)

1. **Official technical report / paper** — arXiv, lab GitHub, lab blog. The
   ground truth for architecture and training. Search `"<model> technical
   report"` and `"<model> arxiv"`.
2. **Model config + weights** — HuggingFace `config.json` and model card;
   ModelScope mirror for Chinese labs (often posted there first/only). The
   config is authoritative for layer counts, head counts, hidden dims, expert
   counts, RoPE base, context length. Fetch
   `huggingface.co/<org>/<model>/blob/main/config.json`.
3. **Sebastian Raschka "Ahead of AI" analysis** — the best independent
   architecture explainers, with consistent diagrams. Key URLs to search for
   and fetch (they update over time):
   - `magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison`
   - `magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures`
   - `magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight`
   - `magazine.sebastianraschka.com/p/technical-deepseek`
   - `sebastianraschka.com/llm-architecture-gallery/` (diagrams + fact sheets)
   - `magazine.sebastianraschka.com/p/workflow-for-understanding-llms`
4. **OpenRouter** — live usage rankings (`openrouter.ai/rankings`), the
   programming collection (`openrouter.ai/collections/programming`), per-model
   pages for **pricing incl. effective/cached pricing** and context window.
   This is the single best source for "what developers actually run" + price.
5. **Pricing pages** — official API pricing for closed models (OpenAI,
   Anthropic, Google); OpenRouter or provider pages for open models. Always
   record input / output / cached-input prices per 1M tokens.
6. **Podcasts / talks / interviews** — Raschka on Vanishing Gradients,
   lab founder interviews, conference talks (PyTorch Conf, NeurIPS). Use for
   design rationale and roadmap signals, never as the sole architecture source.
7. **Aggregators (lowest trust)** — Artificial Analysis, llm-stats, secondary
   blogs. Use only for triangulation; never cite as the primary architecture
   source.

### 1.2 Search discipline

- Use the actual current date in queries (e.g. "DeepSeek latest 2026", not a
  stale year). Lab version numbers move monthly.
- For each tracked lab, run at least: `"<lab> latest model"`, `"<flagship>
  technical report"`, and `"<flagship> config.json huggingface"`.
- When a config URL appears in results, **fetch it** — snippets lose the numbers.
- For Chinese labs (DeepSeek, GLM, Kimi, Qwen, MiMo, StepFun, MiniMax) also
  check ModelScope, as weights/cards sometimes land there first.
- Respect copyright: paraphrase technical reports, quote ≤15 words, one quote
  per source max. The numbers and architecture facts are not copyrightable; the
  prose is.

### 1.3 What to extract per model

Capture into the structured schema (see `references/data-schema.md`). At minimum:
release date, total/active params, layer count, attention type & head config,
positional-encoding strategy & context length, MoE config (experts/active/shared),
normalization, training/post-training notes, modality, license, and full pricing.

---

## Step 2 — Rigorous analysis

This is where the skill earns its keep. For background on the technical concepts
referenced below, read `references/architecture-concepts.md` — it explains
MHA/MQA/GQA/MLA, MoE routing, RoPE/YaRN/NoPE, sliding-window/sparse/lightning
attention, MTP, QK-Norm, and the KV-cache math. Read it before writing analysis
so the explanations are correct and consistent.

For each model, produce three analysis layers:

### 2.1 Capabilities (the "what")
- Benchmark posture across reasoning, coding, agentic, long-context, math,
  multilingual, multimodal — but always paired with the cost/active-params that
  produced it. A score without its price and active-param context is noise.
- Reasoning mode: dedicated reasoning, hybrid (toggle), or instruct-only.
- Agentic/tool-use posture and context window (and *effective* usable context).
- Known failure modes / caveats (hallucination rate, context degradation).

### 2.2 Architecture (the "how") — be very detailed
This is the core. For each model, explain not just *what* it uses but *why*,
and how it differs from its nearest neighbor. Cover:
- **Attention**: exact mechanism, head counts, KV-cache strategy, and the
  memory/quality tradeoff it makes. Show the KV-cache size reasoning.
- **MoE**: total vs active params, expert count/granularity, shared-expert
  choice, routing & load-balancing strategy, sparsity ratio.
- **Positional / context**: RoPE base, YaRN/NoPE/DCA, sliding-window ratio,
  sparse-attention (DSA-style) details, claimed vs usable context.
- **Efficiency tricks**: MTP, FP8/quantization, KV-sharing, compressed
  attention, per-layer embeddings, gated attention.
- **Lineage**: what it inherits from (DeepSeek V3 template? Llama? prior gen)
  and the specific deltas.

Use the analysis framing from Raschka's "workflow for understanding LLMs":
isolate *what changed inside the transformer block / residual stream / KV cache /
attention computation* and ignore the marketing.

### 2.3 Cost & economics (the "how much")
- Input / output / cached-input price per 1M tokens; note the growing dominance
  of cached-input pricing and report *effective* price where OpenRouter gives it.
- Price-per-intelligence: position the model on the cost-vs-capability frontier.
- Deployment footprint for open models (VRAM for weights at given precision;
  remember MoE total params ≠ active params for memory).

### 2.4 Cross-model synthesis
After the per-model passes, write the synthesis the report hinges on:
- The KV-cache / long-context efficiency race (who's winning, with what).
- MoE sparsification trend and the shared-expert debate.
- The attention-mechanism fork (MLA vs GQA vs linear/lightning vs sparse).
- Architecture convergence (the "DeepSeek template" spreading) vs divergence
  (linear-attention and Mamba-hybrid bets).
- Geographic / pricing shifts (e.g. Chinese-model share, price compression).

---

## Step 3 — Render the HTML report

Always read `references/report-spec.md` before generating, and base the output
on `assets/report-template.html` (a self-contained, dependency-free template
with the house visual language, diagram components, and dark/light theming).

Key rules (full detail in the spec):
- **Self-contained single `.html` file** — inline CSS/JS, no external build,
  no CDN dependency required for core rendering (charts may use an inlined lib).
- **Diagram-rich** — every architecture section gets at least one inline SVG
  block diagram (transformer-block view, attention-mechanism view, or MoE-routing
  view). Reuse the SVG components in the template; do not ship walls of text.
- **Sourced** — every model card links its primary sources (report, config,
  OpenRouter page).
- **Comparison tables** — roster-wide spec table + per-dimension comparison
  matrices (attention, MoE, context, pricing).
- **Dated & versioned** — header shows generation date and a snapshot version;
  a "what changed since last snapshot" section when prior data exists.

Write the file to the outputs directory and present it. For very large reports,
build section-by-section into the template rather than one giant string.

---

## Recurring / periodic operation

This skill is designed to be re-run on a cadence (e.g. monthly). To support
deltas:
- Persist each run's structured data as `snapshots/<YYYY-MM-DD>.json` (schema in
  `references/data-schema.md`). If the user has a prior snapshot, load it.
- On each run, diff new data against the latest snapshot and surface: new
  releases, version bumps, architecture changes, price changes, and
  usage-rank movements.
- Keep the roster current: if a new lab/model breaks into the OpenRouter top
  list, add it to the tracked set and note it.

If the user wants true automation (scheduled runs), explain that this skill
defines the workflow and templates; the scheduling itself is handled by whatever
runs Claude (a cron-driven Claude Code job, Cowork automation, etc.). Offer to
emit a runnable script (`scripts/collect.py` is a starting point) they can
schedule.

---

## Reference files

Read these as needed; they keep this SKILL.md lean (progressive disclosure):

- `references/architecture-concepts.md` — deep, correct explanations of every
  architecture concept the analysis relies on (read before writing Step 2).
- `references/data-schema.md` — the structured JSON schema for per-model data
  and snapshots (read before Step 1 extraction and before persisting).
- `references/report-spec.md` — exact HTML report structure, sections, diagram
  requirements, and house style (read before Step 3).
- `references/source-directory.md` — concrete URLs and search patterns per lab
  (read during Step 1 to avoid missing sources).
- `scripts/collect.py` — optional helper to fetch OpenRouter rankings/pricing
  and HuggingFace configs into the schema; a scaffold for scheduled runs.
- `assets/report-template.html` — the self-contained report template with SVG
  diagram components and house styling.
