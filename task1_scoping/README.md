# Task 1: Product Scoping

## What Is In This Folder

| File | Description |
|------|-------------|
| `PRODUCT_BRIEF.md` | Full product brief: problem, solution, users, features, data, and trade-offs |
| `FLOW_DIAGRAM.md` | User flow and data flow diagrams |

---

## The Decision I Made First

Before thinking about features, I asked: **who is this tool actually for?**

The scenario describes both internal analysts and clients asking the same question. I made the deliberate call to build v1 for **internal users only**. Building for clients before the internal team trusts the tool is risky — you end up showing clients inconsistent or wrong data. Internal adoption first gives a feedback loop.

This one decision shaped everything else in the scope.

---

## What Is In Scope for V1

- Unified performance snapshot across channels for a selected client
- Channel health indicators (On Track / Needs Attention / No Data)
- Plain-English top insight summary
- Data freshness indicators so users know when data was last updated
- CSV upload fallback for tools without APIs

## What Is NOT In Scope for V1 (and Why)

- **Client-facing view** — trust needs to be established internally first
- **Recommendations engine** — risks being confidently wrong without enough context
- **Campaign-level drill down** — adds complexity without solving the core question
- **Real-time data** — daily refresh is sufficient for "how are we doing" and far simpler to build
- **Historical trend charts** — useful but not essential for answering "right now"

---

## What I Would Revisit With More Time

- **User interviews.** I assumed what metrics matter. I would validate with 2–3 actual analysts before building anything.
- **Data refresh frequency.** Daily is a simplification. The real answer depends on how urgently teams need same-day data.
- **The insight summary.** Rule-based in v1. Worth exploring whether AI adds genuine value or just noise.
