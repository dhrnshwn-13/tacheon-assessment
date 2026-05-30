# Product Brief: Marketing Performance Assistant (MPA)

## The Problem

The team at a marketing technology company is constantly asked one question:

> *"How is our marketing performing across channels right now, and where should we be focusing?"*

Today, answering this question means one person manually logging into multiple tools, pulling numbers, and stitching together a response. The result:

- The answer looks different every time depending on who does it
- It takes 30–60 minutes of skilled analyst time per request
- If that person is busy, the question goes unanswered
- There is no shared, consistent view of performance across the team

---

## The Solution: Marketing Performance Assistant (MPA)

A lightweight internal tool that gives any team member — analyst or account manager — a single, consistent answer to the performance question in under 60 seconds, without needing to touch any of the underlying tools.

**One sentence:** MPA is an internal dashboard that aggregates marketing performance data from the tools the team already uses, surfaces the key numbers in one place, and flags where attention is needed.

---

## Who Is It For?

**Primary user: Internal analysts and account managers**

The tool is built for the people who are *asked* the performance question, not the clients asking it. A client-facing version is a future possibility, but v1 is internal only.

Why internal first:
- Internal users understand the data context and can validate it
- Building for clients before the internal team trusts it is risky
- Internal adoption gives us a feedback loop before any external exposure

**Secondary user: Team leads and managers**

They need a quick overview across multiple client brands without digging into individual tool dashboards.

---

## What Does V1 Do?

### Core Features

**1. Unified Performance Snapshot**
A single view showing key metrics across all active marketing channels for a selected client brand:
- Impressions, clicks, spend (paid channels)
- Open rate, click rate (email)
- Sessions, conversions (web/analytics)

The user selects a client and a date range. The tool pulls the numbers and displays them in one place.

**2. Channel Health Indicators**
Each channel gets a simple status: **On Track / Needs Attention / No Data**
- Calculated by comparing current performance against the previous period
- A channel that has dropped more than 15% week-on-week is flagged as "Needs Attention"
- This replaces the need to mentally compare numbers across multiple tools

**3. Top Insight Summary**
A short, plain-English summary (2–3 lines) at the top of the page:
- Best performing channel this week
- Biggest drop compared to last week
- Any channel with missing or stale data

This is what a user reads first. It answers the question directly.

---

## What Does V1 NOT Do?

These are deliberate exclusions, not future roadmap items that got cut:

| Excluded | Why |
|----------|-----|
| Client-facing view | Trust needs to be established internally first |
| Recommendations engine | Requires more context than v1 has; risks being wrong |
| Campaign-level drill down | Adds complexity without solving the core question |
| Automated reporting/exports | Out of scope for an internal query tool |
| Historical trend charts | Useful but not essential for answering "right now" |
| Multi-brand comparison | Different brands have different channel mixes; confusing in v1 |

---

## Data: Where Does It Come From?

The tool does not replace existing tools. It reads from them.

**Principle: No new data entry. No workflow changes.**

The team connects their existing tools via APIs or scheduled data exports:

| Source Type | Examples | Method |
|-------------|----------|--------|
| Paid media | Google Ads, Meta Ads | API integration |
| Email marketing | Mailchimp, Klaviyo | API integration |
| Web analytics | Google Analytics | API integration |
| Manual/other | Any tool without an API | CSV upload fallback |

Data is refreshed once daily (overnight). The tool shows data as of yesterday — not real-time. This is a deliberate v1 constraint to reduce complexity.

**Data reliability is displayed transparently.** If a data source failed to refresh, the tool shows a "Last updated: 3 days ago" warning rather than silently showing stale data.

---

## What Makes a User Trust It?

Trust is the hardest problem for this kind of tool. We address it in three ways:

1. **Show the source.** Every metric links back to the original tool it came from. Users can click through to verify.
2. **Show data freshness.** Every number shows when it was last updated. Stale data is clearly labelled.
3. **Never hide problems.** If data is missing or a connection broke, it says so plainly. A tool that silently shows wrong data is worse than one that shows nothing.

---

## How Does a User Interact With It?

**Entry point:** Internal web app (browser-based, no install)

**Typical interaction:**
1. User opens MPA
2. Selects a client brand from a dropdown
3. Selects a date range (default: last 7 days)
4. Sees the performance snapshot and health indicators immediately
5. Reads the top insight summary
6. If something is flagged, clicks through to the source tool for details

**Total time: under 60 seconds for a routine check**

---

## What Would I Revisit With More Time?

- **User interviews first.** I made assumptions about what "performance" means to an analyst. In reality, different roles care about different metrics. I would validate the metric set with 2–3 actual users before building.
- **Data refresh frequency.** Daily refresh is a v1 simplification. Some teams need same-day data. I would understand the actual use case before locking this in.
- **The insight summary.** I scoped this as a rule-based calculation (biggest drop, best performer). With more time, I would explore whether a lightweight AI layer adds genuine value here or just adds noise.
