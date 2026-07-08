#!/usr/bin/env python3
"""Reproduce all statistics in this repo's README/WRITEUP from the raw data.

Usage: python analyze.py
Reads:  data/items.json, data/raw/critiques.json, data/raw/verdicts.json
Writes: data/processed/results.json, web/results.json (for the dashboard)
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
ITEMS = ROOT / "data" / "items.json"
CRITIQUES = ROOT / "data" / "raw" / "critiques.json"
VERDICTS = ROOT / "data" / "raw" / "verdicts.json"
OUT_PROCESSED = ROOT / "data" / "processed" / "results.json"
OUT_WEB = ROOT / "web" / "results.json"


def accuracy(verdicts, ground_truth):
    correct = 0
    per_item = {}
    for pid, gt in ground_truth.items():
        expected = "CORRECT" if gt else "INCORRECT"
        got = verdicts[pid]
        is_right = (got == expected)
        per_item[pid] = {"expected": expected, "judge_said": got, "judge_was_right": is_right}
        if is_right:
            correct += 1
    return correct / len(ground_truth), per_item


def main():
    items = json.loads(ITEMS.read_text())
    critiques = json.loads(CRITIQUES.read_text())
    verdicts = json.loads(VERDICTS.read_text())

    ground_truth = {item["id"]: item["candidate_is_correct"] for item in items}
    n = len(ground_truth)

    conditions = ["baseline_careful", "baseline_fast", "with_opus_critique",
                  "with_corrupted_critique", "with_haiku_critique"]

    results = {"n_items": n, "conditions": {}, "items": items,
               "critiques": critiques, "corrupted_flag": critiques["corrupted_flag"]}

    for cond in conditions:
        acc, per_item = accuracy(verdicts[cond], ground_truth)
        results["conditions"][cond] = {
            "accuracy": acc,
            "n_correct": sum(1 for v in per_item.values() if v["judge_was_right"]),
            "per_item": per_item,
        }

    # Specifically: accuracy on JUST the 7 corrupted items, condition C vs baseline
    corrupted_ids = [pid for pid, flag in critiques["corrupted_flag"].items() if flag]
    corrupted_gt = {pid: ground_truth[pid] for pid in corrupted_ids}
    baseline_acc_on_corrupted, _ = accuracy(
        {pid: verdicts["baseline_careful"][pid] for pid in corrupted_ids}, corrupted_gt
    )
    corrupted_cond_acc_on_corrupted, _ = accuracy(
        {pid: verdicts["with_corrupted_critique"][pid] for pid in corrupted_ids}, corrupted_gt
    )
    results["corrupted_subset_analysis"] = {
        "corrupted_ids": corrupted_ids,
        "n_corrupted": len(corrupted_ids),
        "baseline_accuracy_on_these_items": baseline_acc_on_corrupted,
        "accuracy_with_corrupted_critique_on_these_items": corrupted_cond_acc_on_corrupted,
        "degradation": baseline_acc_on_corrupted - corrupted_cond_acc_on_corrupted,
    }

    OUT_PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROCESSED.write_text(json.dumps(results, indent=2))
    OUT_WEB.write_text(json.dumps(results, indent=2))

    print(f"n={n} items\n")
    for cond in conditions:
        r = results["conditions"][cond]
        print(f"  {cond}: {r['n_correct']}/{n} ({r['accuracy']*100:.0f}%)")
    csa = results["corrupted_subset_analysis"]
    print(f"\nOn the {csa['n_corrupted']} deliberately corrupted items specifically:")
    print(f"  baseline accuracy: {csa['baseline_accuracy_on_these_items']*100:.0f}%")
    print(f"  accuracy with corrupted critique shown: {csa['accuracy_with_corrupted_critique_on_these_items']*100:.0f}%")
    print(f"  degradation: {csa['degradation']*100:.0f} percentage points")
    print(f"\nWrote {OUT_PROCESSED} and {OUT_WEB}")


if __name__ == "__main__":
    main()
