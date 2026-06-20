# Demand Zone Management & Rebalancing

**Purpose.** This policy defines how Nexa Pulse measures, interprets, and acts on demand across the seven San Francisco zones, and how the operations manager rebalances supply.

**The seven zones.** Each zone has a distinct demand profile: Financial District (commercial, weekday-peaked), SOMA (commercial, event-influenced), Mission (residential/nightlife), Marina / Fisherman's Wharf (tourist), Inner Sunset (residential), Castro (residential/commercial), and West Portal (residential). Demand is tracked per zone via `request_count`, the count of open `requested` trips.

**Health metrics.** For each zone the dashboard displays `request_count`, the number of `available` drivers, the request-to-driver ratio, average pickup ETA, and short-term trend. A zone is "balanced" when the ratio sits near 1:1 with acceptable ETAs; "under-supplied" when requests outpace drivers; and "over-supplied" when many drivers sit `available` with low `request_count`.

**Rebalancing levers.** When a zone is under-supplied, the manager may, in order of preference: (1) issue repositioning guidance drawing from adjacent over-supplied zones; (2) authorize zone bonuses; (3) allow dynamic surge to engage. Over-supplied zones should have incentives wound down to avoid wasteful spend.

**Adjacency logic.** Rebalancing should favor short repositioning hops — for example, pulling drivers from a quiet West Portal or Inner Sunset toward a busy Castro or Mission, rather than long cross-city moves that strand supply and increase dead miles.

**Forecasting.** The system blends historical patterns by hour and day with live signals. Recurring patterns (Financial District morning inflow, Mission/Castro late-night outflow, Marina weekend tourist peaks) should be pre-planned rather than handled reactively.

**Operations manager role.** The manager validates that recommended moves reflect real conditions, avoids over-correcting (which causes oscillation between under- and over-supply), and records the outcomes of rebalancing actions for review.
