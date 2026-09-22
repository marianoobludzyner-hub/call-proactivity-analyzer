# Call Proactivity & Expansion Signal Analyzer (open-source edition)

Reads a customer call transcript and scores how commercially proactive the CSM/AM was, against a transparent 5-dimension rubric, then separately surfaces expansion opportunities and risk signals with direct quotes.

Part of the same open-source series as [nrr-leak-diagnostic](https://github.com/marianoobludzyner-hub/nrr-leak-diagnostic) (company-level leak estimate) and [renewal-risk-rollup](https://github.com/marianoobludzyner-hub/renewal-risk-rollup) (account-level ARR at risk). This one is the "T" piece: AI automation applied to a single call instead of a spreadsheet.

## Why this project

"Great call, good relationship" is not a data point a leader can act on. This tool exists to turn a transcript into two things a leader *can* act on: a consistent score for whether the CSM drove the conversation commercially (renewal, risk, expansion, stakeholders, next steps) or just responded to it, and a short list of the specific expansion and risk signals that were said out loud and might otherwise get lost between the call and the CRM note.

## What it does

Given a call transcript, it:

1. Scores the call across 5 dimensions, 0-3 each, against the rubric in [`rubric.md`](rubric.md): renewal ownership, risk surfacing, expansion probing, stakeholder mapping, next-step ownership
2. Sums to a Commercial Proactivity Score (0-15) and a band: Commercial / Developing / Reactive / Order-taking
3. Extracts expansion opportunities and risk/churn signals mentioned in the call, each with the direct quote and a one-line reason
4. Renders a chart of the 5 scores

**Reading the transcript and applying the rubric is a judgment call, not arithmetic** -- that part is done by an LLM (Claude or GPT), following the rubric exactly. `score.py` handles the deterministic part: taking the 5 scores once assigned, applying the banding logic, and rendering a consistent report and chart, the same division of labor the other two tools in this series use for their own math.

## How to run it

No installation required -- pure Python standard library, once you have the 5 scores.

```bash
python3 score.py --renewal 3 --risk 2 --expansion 3 --stakeholder 2 --nextstep 3 \
    --signals my_signals.json --svg scorecard.svg --json
```

`--signals` points to a JSON file shaped like [`examples/sample_signals.json`](examples/sample_signals.json): `{"expansion": [{"quote": "...", "why": "..."}], "risk": [...]}`.

You will not usually run `score.py` by hand against a real transcript -- see below for the two ways this is actually meant to be used.

Worked example: [`examples/sample_transcript.txt`](examples/sample_transcript.txt) in, full scoring walkthrough in [`examples/sample_analysis.md`](examples/sample_analysis.md), scoring 13/15 (Commercial).

## Run it as a Claude Skill

See [`skill/SKILL.md`](skill/SKILL.md). Paste in a transcript (or point Claude at a recording/notes file) and ask it to run the proactivity scorecard. Claude reads it, applies the rubric, calls `score.py`, and walks you through the result.

## Run it as your own GPT

See [`gpt/CUSTOM_GPT_INSTRUCTIONS.md`](gpt/CUSTOM_GPT_INSTRUCTIONS.md) -- paste it into a Custom GPT's instructions field (Code Interpreter enabled), then paste or upload a transcript directly in the chat.

## Method

The full rubric, with the exact scoring anchors for every dimension, is in [`rubric.md`](rubric.md) -- not hidden in a prompt, not a black box. It encodes one idea five ways: did the CSM drive the conversation forward, or only respond to it. That is the "F: from reactive to commercial" mindset shift at the center of the SHIFT Method, applied to one call instead of a whole team.

## What this is not

A single call is one data point, not a performance review. A CSM can score low on a hard call for reasons that have nothing to do with skill (an angry customer, a compressed agenda, a first meeting with no context yet). Use this to spot patterns across many calls and as coaching input, not to grade a person off one transcript.

---

**Obludzyner & Co.** -- Post-sales advisory for B2B SaaS. We install a commercial operating system that protects ARR and generates expansion in 90 days, without replacing your team or making you the bottleneck. [obludzyner.com](https://obludzyner.com) | [Start the diagnostic](https://obludzyner.com/diagnostic) | [Book a conversation](https://obludzyner.com/#contact)
