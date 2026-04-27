## Part XVII — Harness Health Metrics

A harness without metrics becomes opinion. Without indicators, discussions stay at *"I think it's helping"*. Define 3–5 indicators and review quarterly.

### 1. Quantitative indicators

| Metric | How to measure | Healthy target |
|---|---|---|
| **Bug recurrence** | % of fixed bugs that return within 90 days | < 5% |
| **Time-to-first-gate** | From item entering the backlog to spec approved | < 3 days (medium), < 1 day (small) |
| **Spec rework** | % of specs that go back to "draft" after "approved" | < 15% |
| **Skill coverage** | % of PRs that consulted/applied at least one relevant skill | > 70% |
| **Context file churn** | Changes per month in the main context file | 1–5 (neither unstable nor forgotten) |
| **Validation pass rate (1st try)** | % of PRs that pass `verify.sh` on first push | > 60% |
| **Mean review cycles** | Average rounds of review until merge | < 2.5 |
| **PR open time** | Median time from PR open to merge | < 2 working days |
| **Fast-path adoption** | % of trivial changes that used fast-path correctly | > 80% |

### 2. Qualitative indicators

Not everything is a number. Quarterly survey with the team (5–10 questions):

- *"Does the harness accelerate or hinder my work?"* (1–5 scale);
- *"Do I know where to find rule X?"* (yes / no / sort of);
- *"Code generated with AI has the same quality as mine?"* (better / same / worse);
- *"Can a new dev operate within 2 weeks?"* (yes / no);
- *"What's the most annoying thing about the harness today?"* (open);
- *"What's missing?"* (open).

The quantitative + qualitative combination avoids two errors:

- **Quantitative only**: good metrics, everyone hating it;
- **Qualitative only**: everyone happy, bugs in prod.

### 3. Periodic review

Quarterly, in 1–2 hours:

1. Look at indicators → which got worse?;
2. Read qualitative survey → recurring theme?;
3. List 1–3 actions for next quarter;
4. Update harness backlog with these actions.

### 4. When to reorganize

If in two consecutive quarters:

- Recurrence rises;
- Validation pass rate drops;
- Qualitative plummets;

It's time to revisit structure. Don't keep stacking: **stop and clean**.

---
