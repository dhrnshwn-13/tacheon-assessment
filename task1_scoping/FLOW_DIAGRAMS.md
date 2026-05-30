# Flow Diagrams: Marketing Performance Assistant (MPA)

---

## 1. User Flow — How a Team Member Uses the Tool

```
 ┌─────────────────────────────────────────────────────────┐
 │                    User opens MPA                        │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │         Selects a client brand from dropdown             │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │     Selects date range (default: last 7 days)            │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │         Reads Top Insight Summary (2–3 lines)            │
 │   "Email CTR dropped 22% vs last week. Paid search       │
 │    is up 11%. No data from Meta since Wednesday."        │
 └──────────────────────────┬──────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              │                            │
              ▼                            ▼
 ┌────────────────────────┐   ┌────────────────────────────┐
 │   All channels look    │   │  A channel is flagged as   │
 │       On Track         │   │     "Needs Attention"      │
 └────────────┬───────────┘   └────────────┬───────────────┘
              │                            │
              ▼                            ▼
 ┌────────────────────────┐   ┌────────────────────────────┐
 │   Session complete.    │   │  User clicks through to    │
 │   No action needed.    │   │  original tool to dig in.  │
 └────────────────────────┘   └────────────────────────────┘
```

**What the user walks away with:**
- A clear answer to "how are we doing right now?"
- Confidence that nothing is being missed
- A starting point if something needs attention

---

## 2. Data Flow — How Data Gets Into MPA

```
 ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
 │   Google Ads API │   │  Meta Ads API    │   │  GA4 / Analytics │
 └────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘
          │                      │                       │
          └──────────────────────┼───────────────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────┐
                  │    Scheduled Data Sync   │
                  │    (runs nightly, 2am)   │
                  └──────────────┬───────────┘
                                 │
                    ┌────────────┴─────────────┐
                    │                          │
                    ▼                          ▼
         ┌──────────────────┐      ┌──────────────────────┐
         │  Sync succeeded  │      │    Sync failed /     │
         │  → store data    │      │    no data returned  │
         └────────┬─────────┘      └──────────┬───────────┘
                  │                           │
                  ▼                           ▼
         ┌──────────────────┐      ┌──────────────────────┐
         │  Mark channel:   │      │  Mark channel:       │
         │  "Last updated:  │      │  "No Data" — show    │
         │   today"         │      │   last known date    │
         └────────┬─────────┘      └──────────┬───────────┘
                  │                           │
                  └─────────────┬─────────────┘
                                │
                                ▼
               ┌────────────────────────────────┐
               │        MPA Dashboard           │
               │  Displays metrics + statuses   │
               │  for selected client + range   │
               └────────────────────────────────┘
```

---

## 3. Channel Health Logic — How "Needs Attention" Is Calculated

```
  For each channel:

  ┌─────────────────────────────────────────┐
  │  Is data available for this channel?    │
  └──────────────┬──────────────────────────┘
                 │
       ┌─────────┴──────────┐
       │ No                 │ Yes
       ▼                    ▼
  ┌──────────────┐   ┌──────────────────────────────────────┐
  │  → No Data   │   │  Compare current period vs previous  │
  └──────────────┘   └──────────────┬───────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │ Drop > 15%    │ Within ±15%   │ Gain > 5%
                    ▼               ▼               ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │   Needs    │  │  On Track  │  │  On Track  │
             │ Attention  │  │            │  │  (upward)  │
             └────────────┘  └────────────┘  └────────────┘
```

---

## Key Design Decisions Reflected in These Flows

1. **No real-time data.** The sync runs nightly. This reduces infrastructure complexity and is sufficient for the "how are we doing" question — which is typically asked at the start of a workday, not mid-second.

2. **Transparency over silence.** If data is stale or missing, the tool says so explicitly rather than hiding the gap or showing an old number without context.

3. **The tool redirects, not replaces.** When something needs attention, the tool points the user back to the original platform. MPA answers "what needs looking at" — not "what should you do about it."
