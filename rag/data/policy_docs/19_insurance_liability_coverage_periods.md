# Insurance & Liability Coverage Periods

**Purpose.** This policy explains the period-based insurance framework that applies to Nexa Pulse trips in California and how operations preserves the evidence needed to determine coverage.

**The period framework.** California TNC insurance coverage (codified at California Public Utilities Code Section 5433) is keyed to the driver's app state, which maps to platform statuses:

- **Period 0** — app off (`offline`): the driver's personal auto policy applies; the platform provides no coverage.
- **Period 1** — app on, `available`, no trip accepted: contingent/excess coverage applies (a state-set minimum, including $200,000 excess liability per occurrence; personal policies typically exclude this period).
- **Period 2** — trip accepted, driver en route to pickup (trip matched, not yet `in_progress`): the TNC must provide $1,000,000 primary commercial liability coverage.
- **Period 3** — passenger in vehicle (`on_trip` / `in_progress` until the rider exits): $1,000,000 primary commercial liability plus uninsured/underinsured-motorist (UM/UIM) coverage.

**Recent statutory change.** Historically, Period 3 UM/UIM coverage was set at $1,000,000. Under SB 371, effective January 1, 2026, the Period 3 UM/UIM requirement was reduced to $60,000 per person / $300,000 per incident. The compliance team maintains the current authoritative figures; operations should not rely on legacy $1,000,000 UM/UIM assumptions when advising on coverage after that date.

**Why it matters.** The coverage available can differ by an order of magnitude depending on whether the driver was merely `available` (Period 1) or had an accepted trip (Periods 2-3). The single most important operational task after a collision is to fix, with precise timestamps, which period applied.

**Evidence preservation.** On any collision report, operations must preserve app timestamps for status transitions (`offline` to `available` to trip accepted to `in_progress` to `completed`/`cancelled`), GPS data, and the trip record. This data must be protected from routine deletion as soon as an incident is known, via a preservation hold.

**Driver obligations.** Drivers must carry compliant personal insurance and provide proof of both personal and commercial coverage after an accident. A driver involved in a collision is typically placed `offline`/on hold pending review and may not return until any required vehicle repairs are verified.
