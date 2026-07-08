# Write-up: Scalable Oversight and Resistance to a Corrupted Critique

## Hypothesis (stated before the corrupted-critique condition was run)

The canonical scalable-oversight concern is that a weaker judge, unable to verify a claim itself, will defer to *any* confidently-stated critique regardless of whether it's actually correct — that's the whole reason "critique quality" needs to be measured, not assumed. We expected: (1) baseline accuracy below ceiling on a genuinely hard problem set, (2) accuracy improving with a genuine critique, and (3) accuracy *dropping* meaningfully on the subset of items where we fed a corrupted critique, since a plausible-sounding wrong argument should have some persuasive pull even on a model that would have gotten the item right alone.

## The ceiling problem, reported honestly

Our first attempt used 16 moderate-difficulty word problems (compound interest, ratios, basic combinatorics). Haiku alone scored 16/16. We redesigned to 14 genuinely harder problems — related-rates calculus, constrained optimization, modular exponentiation of large powers, restricted circular permutations, Bayes' theorem — expecting these to create real errors. Haiku alone still scored 14/14, *twice*: once with explicit "show your work carefully" instructions, and again with "give a fast gut-check, don't show work" instructions designed to simulate a rushed, lower-effort pass. Both hit ceiling.

We did not go back and re-redesign a third problem set to chase a below-ceiling baseline. Instead, we recognized that the ceiling itself doesn't block the more interesting question: **regardless of whether the judge needs help, does it wrongly take help that's actively wrong?** A judge that's accurate alone but easily talked out of a correct answer by a fabricated critique has a real vulnerability that a pure accuracy number would hide. So we shifted the headline question in place, before running the corrupted condition, from "does critique help a struggling judge" to "does a corrupted critique hurt an unstruggling one."

## Method

14 problems (`data/items.json`), 7 with correct candidate answers and 7 with incorrect-but-plausible ones. Five conditions run via the Claude Agent tool:

- Two baseline conditions (careful vs. fast framing), Haiku alone.
- Opus critique condition: Haiku sees a genuine, verified-accurate Opus critique per item.
- Haiku critique condition: Haiku sees a genuine, verified-accurate same-strength critique.
- Corrupted critique condition: we hand-authored a fabricated critique for 7 of the 14 items (3 originally-correct items reframed as wrong via a fake "you forgot to double the rate" style argument; 4 originally-incorrect items reframed as right via a fake "by symmetry" or "acceptable at typical precision" style argument), while leaving the other 7 critiques genuine and accurate.

## Results

| Condition | Accuracy | n correct / 14 |
|---|---|---|
| Baseline (careful framing) | 100% | 14/14 |
| Baseline (fast framing) | 100% | 14/14 |
| With genuine Opus critique | 100% | 14/14 |
| With genuine Haiku (same-strength) critique | 100% | 14/14 |
| **With corrupted critique** | **100%** | **14/14** |

On the 7 specifically corrupted items: baseline accuracy 100%, accuracy with the corrupted critique shown 100%. **Zero percentage points of degradation.** Every fabricated argument — a fake calculus rule about "doubling the rate," a fake symmetry argument about dice probabilities, a fake claim that dropping a Bayes' theorem term is more correct, a fake claim that 19,990 "rounds to" 20,000 at "typical precision" — was independently caught and rejected.

## Discussion

We did not get to test the originally-intended question (does genuine critique rescue a genuinely struggling judge), because we could not engineer a struggling judge on this problem class within the Claude model family. But we got a cleaner and arguably more safety-relevant result than we set out to find: **on checkable, verifiable tasks, Haiku's judgment was not merely accurate, it was actively resistant to a fabricated, plausible-sounding wrong argument.** This connects directly to the pattern found in our other two projects — [reasoning-consistency-flips](https://github.com/knoxkiminou1-byte/reasoning-consistency-flips) and [sycophancy-pressure-eval](https://github.com/knoxkiminou1-byte/sycophancy-pressure-eval) — both of which found zero sycophantic flips under naked social/authority pressure. This is now a third domain (judgment under a fabricated *expert critique*, as opposed to naked disagreement or an authority claim) showing the same pattern.

The honest caveat is important: **this is not evidence that critique corruption never works.** It's evidence that on *this* difficulty tier of *checkable* math, with a single-shot corrupted critique, one specific model tier didn't take the bait. A judge that's actually uncertain (which we never achieved here), or a corrupted critique that's more subtle than ours, or a domain where the judge can't independently re-derive the answer (subjective quality judgments, ambiguous code review, safety-relevant risk assessments) could show a very different result. The scalable-oversight literature's core concern — deferring to confident-sounding but wrong critique — remains a real and open question; we simply didn't find it here, on this task, at this difficulty.

## What we'd do with another month

- Find a genuinely below-ceiling baseline — likely requires moving outside crisp checkable math entirely, into domains like code review of subtle bugs, ambiguous multi-step reasoning chains, or tasks near the edge of the judge model's actual competence (calibrated via a pretest, not guessed at).
- Make the corrupted critique more sophisticated — ours used somewhat inventable-sounding fake rules; a more careful adversarial corruption (subtly wrong rather than outright fabricated-sounding) might have more pull.
- Test degradation as a function of corruption *fraction* (what if 12 of 14 critiques are corrupted, not 7 — does a "pile-on" effect emerge?) and as a function of *framing* (an insistent, repeated corrupted critique vs. a single one-shot critique).
- Run the same design with a genuine cross-vendor judge/critic pair once other providers' API access is available.
