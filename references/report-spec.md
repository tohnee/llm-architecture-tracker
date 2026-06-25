# Report Spec

The exact structure, content, and house style for the HTML research report.
Read before Step 3. Base the output on `assets/report-template.html`, which
already encodes the visual language and reusable SVG diagram components.

## Output rules

- **One self-contained `.html` file.** All CSS and JS inline. Core rendering
  (layout, tables, SVG diagrams, theme toggle) must work with no network. If you
  use a chart library, inline it; never hard-depend on a CDN for content the
  reader must see.
- **No `localStorage`/`sessionStorage`** if this will ever render in an Artifacts
  sandbox — keep state in JS variables. (Standalone file in a browser is fine,
  but defaulting to in-memory keeps it portable.)
- Write to the outputs directory; for large reports, build section-by-section
  into the template rather than assembling one giant string.
- Filename: `llm-landscape-report_<YYYY-MM-DD>.html`.

## House visual language

The template defines CSS variables — use them, don't hardcode colors. Default
direction: a clean technical-editorial look with a dark/light toggle.

- **Type**: a distinctive display face for headers + a readable text face for
  body + a mono face for specs/code. (Template sets these; don't fall back to
  Arial/Inter system defaults.)
- **Color**: one dominant ink color + one sharp accent for emphasis + per-lab
  accent chips. Restraint over rainbow.
- **Density**: generous whitespace around sections; dense, scannable tables.
- **Diagrams over walls of text** — this is the defining rule.

## Required sections (Mode A — full landscape report)

1. **Header** — title, generation date, snapshot version, one-line thesis.
2. **Executive summary** — 4–6 bullets: the headline shifts since last snapshot
   (architecture, pricing, usage). Lead with what changed.
3. **The landscape at a glance** — the roster spec table (all tracked models):
   columns = model, lab, release, total/active params, attention, MoE,
   context, license, input/output price. Sortable if JS is included.
4. **OpenRouter reality check** — top-usage list with the caveat that usage rank
   ≠ quality; note any single-app or cheap-preview distortions.
5. **Architecture deep dives** — one subsection per lab/flagship. Each MUST have:
   - a spec strip (params, attention, MoE, context, price),
   - **≥1 inline SVG diagram** (block view, attention view, or MoE-routing view),
   - prose explaining *what changed and what constraint it buys down*,
   - lineage + deltas, and source links.
6. **Cross-cutting analysis** (the synthesis) — dedicated subsections with at
   least one comparison diagram/chart each:
   - KV-cache & long-context efficiency race,
   - MoE sparsification & the shared-expert debate,
   - the attention fork (MLA vs GQA vs linear vs sparse),
   - convergence (DeepSeek template) vs divergence (linear/Mamba bets),
   - economics: cost-vs-capability frontier, cached-pricing dominance,
     geographic share shift.
7. **What changed since last snapshot** (delta) — table of new releases, version
   bumps, arch changes, price moves, usage-rank moves. Omit if no prior snapshot.
8. **Methodology & sources** — source hierarchy used, snapshot date, confidence
   notes, and the full source link list.
9. **Footer** — generation metadata, "usage≠quality / verify on your own evals"
   disclaimer.

For Mode B (single deep dive): sections 1, 5 (expanded), 6 (relevant slices), 8.
For Mode C (comparison): sections 1, 3 (the two/few models), a side-by-side
diagram, per-dimension matrices, 6 (relevant), 8.
For Mode D (delta): sections 1, 2, 7 (expanded), 8.

## Diagram requirements

Reuse the SVG components in the template. Provide, as relevant:

- **Transformer-block diagram** — show Norm placement, attention sub-layer, FFN
  (or MoE) sub-layer, residual paths; annotate the model-specific twist.
- **Attention-mechanism diagram** — Q/K/V flow for the model's attention type;
  for MLA show the latent compress→cache→up-project path; for GQA show head
  grouping; for linear show the running-state; for sparse show indexer→selector.
- **MoE-routing diagram** — tokens → router → top-K experts (+ shared expert),
  with total/active counts annotated.
- **KV-cache comparison chart** — bar chart of cache size vs context length
  across MHA/GQA/MLA/linear for the headline models.
- **Cost-vs-capability scatter** — price per 1M input (x) vs a capability proxy
  (y), bubble size = usage; label the frontier.

Keep diagrams legible: clear labels, the house palette, captions stating the
takeaway (not just "Figure N").

## Tone & integrity

- Rigorous and sourced. Every nontrivial claim traces to a source link.
- Paraphrase technical reports; obey copyright (≤15-word quotes, one per source).
- Distinguish *measured* facts (config numbers) from *claimed* (vendor benchmarks)
  from *analyst inference*. Label inference as such.
- Pair every benchmark with its cost/active-params context.
- Don't overstate: where the architecture is undisclosed (closed models), say so
  and analyze what *is* observable (capabilities, pricing, behavior).
