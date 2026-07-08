# Runbook: Scalable Oversight Critique

## Purpose

This repo preserves a small reproducible AI safety pilot testing whether a weaker model judge defers to expert-sounding critiques, including deliberately corrupted critiques that argue for the wrong verdict.

## Current Status

- Status: complete research pilot
- Primary artifact: `WRITEUP.md`
- Reproducible analysis: `python3 analyze.py`
- Public dashboard source: `web/`
- Production deployment: Vercel deployment is referenced in the README, but the public deployment URL is not recorded in repository metadata
- Last verified locally: 2026-07-08

## System Overview

- `data/items.json`: evaluation items and ground truth
- `data/raw/critiques.json`: genuine and corrupted critique records
- `data/raw/verdicts.json`: final judge verdicts
- `analyze.py`: regenerates processed statistics
- `data/processed/results.json`: processed output
- `web/results.json`: dashboard data source
- `web/index.html`: static dashboard

No secrets or live API calls are required to reproduce the committed analysis. The model calls used for data collection were performed before publication and are preserved as raw records.

## Local Development

```bash
python3 analyze.py
```

Optional isolated setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 analyze.py
```

`requirements.txt` is intentionally minimal; the analysis uses the Python standard library.

## Verification

Run:

```bash
python3 analyze.py
git diff -- data/processed/results.json web/results.json
```

Expected result: no diff after regeneration.

## Deployment

This is a static dashboard. Any static host can serve the `web/` directory.

Vercel deployment checklist:

1. Set the project root to the repository root.
2. Set output/static directory to `web` if the host asks for one.
3. There are no required environment variables.
4. After deploying, add the production URL to the GitHub repository homepage.

Rollback is host-level: redeploy a previous static deployment or revert the commit that changed `web/`.

## Maintenance Checklist

- Re-run `python3 analyze.py` before any release or README result update.
- Update `WRITEUP.md` and `LIMITATIONS.md` together if the methodology changes.
- Do not edit processed JSON by hand; regenerate it from raw data.
- If new model calls are added, commit the raw records and note collection conditions.
- Keep safety framing defensive and avoid turning fixtures into an attack catalog.

## Handoff Notes

The most important owner responsibility is preserving the distinction between raw data, processed results, and interpretation. A future maintainer should be able to re-run the analysis, inspect the raw critique manipulation, and understand the result without needing credentials or private logs.
