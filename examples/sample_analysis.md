# Worked example

Input: [`sample_transcript.txt`](sample_transcript.txt), a synthetic call between a CSM and a customer.

## Scores against the rubric

| Dimension | Score | Why |
|---|---|---|
| Renewal ownership | 3/3 | Opened the call by proactively naming the 70-day renewal timeline, and later confirmed the budget approver had changed post-acquisition. |
| Risk surfacing | 2/3 | Noticed and named the usage dip before the customer volunteered it, and asked about the backfill timeline -- but the "mitigation plan" stayed informal, no specific owner/date attached to re-onboarding the new hires. |
| Expansion probing | 3/3 | Proactively asked whether the newly acquired entity would use the platform, and turned it into a concrete next step (an onboarding overview, with a date). |
| Stakeholder mapping | 2/3 | Proactively asked whether the budget approver had changed -- surfaced the CFO's new involvement -- but doesn't yet have a full map of who else is involved post-acquisition. |
| Next-step ownership | 3/3 | Closed with two specific, owned, dated next steps (onboarding overview by Friday; follow-up the week of the 14th). |

**Commercial Proactivity Score: 13 of 15 -> Commercial**

This is what "operating commercially, not just relationally" sounds like on an actual call: the CSM drove the renewal conversation, the expansion conversation, and the stakeholder conversation, instead of waiting to be asked.

## Expansion opportunities detected

- *"Are they going to be using our platform too, or is that still being figured out?" / "Still being figured out honestly, nobody's really owned that conversation yet."*
  The recent acquisition means a second entity could onboard onto the platform, and no one at Northwind currently owns that decision internally. An open door, not yet a commitment.

## Risk / churn signals detected

- *"Two of our regional managers who used the dashboards daily left the company. We haven't backfilled yet."*
  Daily active users just left with no replacement yet. Adoption will keep declining until the roles are backfilled and re-onboarded, which is not yet scheduled beyond "probably next month."
- *"I think the CFO wants visibility on anything over six figures now, given the acquisition."*
  A new approval layer has entered the renewal decision process post-acquisition. Not a red flag on its own, but the proposal and timeline need to account for it or the renewal could stall.

Full JSON: [`sample_scorecard.json`](sample_scorecard.json). Chart: [`sample_scorecard.svg`](sample_scorecard.svg).

Reproduce this exact output:

```bash
python3 score.py --renewal 3 --risk 2 --expansion 3 --stakeholder 2 --nextstep 3 \
    --signals sample_signals.json --svg sample_scorecard.svg --json
```
