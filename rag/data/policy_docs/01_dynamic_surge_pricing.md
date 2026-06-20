# Dynamic Surge Pricing Policy

**Purpose.** This policy governs how Nexa Pulse applies dynamic (surge) pricing in response to short-term imbalances between rider demand and available driver supply across the seven San Francisco demand zones: Financial District, SOMA, Mission, Marina / Fisherman's Wharf, Inner Sunset, Castro, and West Portal.

**Trigger conditions.** Surge is evaluated continuously at the zone level. The primary signal is the ratio of `request_count` (open `requested` trips) to the number of drivers with status `available` inside the zone. When the ratio exceeds 1.5 open requests per available driver for more than three consecutive minutes, the zone enters a surge state. The system computes a multiplier between 1.1x and 3.0x applied to the base fare estimate. Surge multipliers update on a rolling clock as supply and demand change.

**Operations manager role.** Nexa Pulse surfaces a recommended multiplier; the operations manager reviews and confirms. The dashboard displays the contributing factors — current `request_count`, available-driver count, average pickup ETA, and trend direction — so the manager can validate the recommendation against live conditions before applying it. Managers may override the recommended multiplier downward at any time and should document the rationale.

**Rider transparency.** Whenever surge is in effect, riders must be shown the multiplier or the surge-inclusive upfront fare before confirming. No rider may be charged a surge fare without explicit pre-trip acknowledgment.

**Limits and guardrails.** Standard surge is capped at 3.0x in routine operations. Surge must never be applied in a way that violates California Penal Code Section 396 price-gouging protections during a declared emergency; emergency surge handling is governed by the separate Weather and Major-Event policies. Surge is a supply-balancing tool, not a revenue tool: its purpose is to attract `available` drivers toward under-supplied zones and to moderate demand so the marketplace clears.

**Monitoring.** Operations managers should watch for "surge chasing" — drivers repositioning toward an expiring surge zone — which can create over-supply and a sudden multiplier collapse. The dashboard flags zones where available-driver count is climbing faster than `request_count`, indicating surge should be wound down.
