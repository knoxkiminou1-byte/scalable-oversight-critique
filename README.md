# Scalable Oversight: Does a Judge Defer to a Confidently Wrong Critique?

**Research question:** When a weaker/cheaper model judges candidate answers, does exposure to another model's critique change its accuracy — and critically, does a *deliberately wrong but confidently argued* critique degrade that accuracy?

## What we actually found

We built 14 candidate-judging problems at genuinely advanced difficulty (related-rates calculus, constrained optimization, modular exponentiation, conditional probability via Bayes' theorem, restricted circular permutations) — deliberately harder than typical scalable-oversight eval sets, precisely to give a "weak" judge room to fail. Claude Haiku judged each candidate as CORRECT or INCORRECT across five conditions: alone with careful step-by-step instructions, alone with fast/no-shown-work instructions, after seeing a genuine critique from Claude Opus, after seeing a genuine same-strength critique from another Haiku call, and — the key manipulation — after seeing a **deliberately fabricated critique that confidently argues the wrong verdict on 7 of the 14 items**, with plausible-sounding (but false) mathematical justifications.

**Result: 14/14 (100%) accuracy in every single condition, including with the corrupted critique.** Haiku did not defer to a single one of the 7 fabricated wrong arguments — not the fake "you need to double the rate" calculus claim, not the fake "Bayes' theorem should weight by the defect rate alone" claim, not any of the others. Baseline accuracy was already at ceiling and stayed there under active, confidently-argued misinformation.

This is the strongest and most consistent result across our project set: taken together with [reasoning-consistency-flips](https://github.com/knoxkiminou1-byte/reasoning-consistency-flips) (0/50 sycophantic flips on math) and [sycophancy-pressure-eval](https://github.com/knoxkiminou1-byte/sycophancy-pressure-eval) (0/96 flips on facts), this is now a **third independent study domain** — judgment under a fabricated expert-sounding critique — where naked social/authority pressure and now outright misinformation failed to move a Claude model off a correct, independently-verifiable answer. See [`WRITEUP.md`](./WRITEUP.md) for the full discussion, including what this does and doesn't tell us about scalable oversight more broadly.

## Status

- Data collection: complete (14 items × 5 conditions = 70 judgments)
- Analysis: complete, fully reproducible from committed raw data
- Dashboard: deployed to Vercel
- Cost: 6 Claude Agent tool calls (Haiku ×4, Opus ×1, plus 1 initial baseline pilot on an easier item set that hit ceiling and was redesigned), ~185K tokens total

## Method

1. **Task domain**: 14 problems spanning calculus, optimization, modular arithmetic, combinatorics with constraints, and Bayesian probability — see [`data/items.json`](./data/items.json). Each has one candidate answer with a known ground-truth correctness label (7 correct, 7 incorrect-but-plausible).
2. **Conditions**:
   - `baseline_careful` / `baseline_fast`: Haiku judges alone, under two different instruction framings (explicit step-by-step vs. fast/no-shown-work), to rule out the framing itself as the reason for high accuracy.
   - `with_opus_critique`: Haiku judges after seeing a genuine, accurate critique from Opus.
   - `with_haiku_critique`: Haiku judges after seeing a genuine, accurate critique from a same-strength Haiku call (isolates "any second opinion" from "specifically a stronger model's critique").
   - `with_corrupted_critique`: Haiku judges after seeing a critique where **we deliberately rewrote 7 of the 14 critiques to confidently argue the wrong verdict** with a fabricated-but-plausible-sounding justification (see `data/raw/critiques.json` for exactly which ones and how).
3. **Why this problem set**: an earlier pilot on easier word problems saw Haiku hit 16/16 and 14/14 ceiling accuracy alone, leaving no room to observe a critique effect. We deliberately escalated to graduate-adjacent problems for this reason — see `WRITEUP.md` for that full history, reported honestly rather than hidden.

## Reproduce the analysis

```bash
pip install -r requirements.txt   # standard library only
python analyze.py
```

Regenerates `data/processed/results.json` and `web/results.json` from the committed raw data. Data collection itself was performed via the Claude Agent tool (see `data/raw/critiques.json` and `data/raw/verdicts.json` for the full raw record, including exactly which critiques were corrupted and how).

## Handoff and operations

See [`docs/runbook.md`](./docs/runbook.md) for local verification, static deployment notes, maintenance expectations, and owner handoff guidance. A ready-to-copy GitHub Actions workflow template lives at [`docs/github-actions-verify.yml`](./docs/github-actions-verify.yml); it reruns the analysis and fails if generated outputs are not committed.

## Repo layout

```
data/
  items.json                  14 problems, candidates, ground truth
  raw/critiques.json          genuine Opus/Haiku critiques + the corrupted set, with a flag marking which items were altered
  raw/verdicts.json           Haiku's final verdict per condition
  processed/results.json      output of analyze.py
analyze.py                    regenerates all statistics from raw data
web/                          static results dashboard (deployed to Vercel)
WRITEUP.md
LIMITATIONS.md
```

## License

MIT
