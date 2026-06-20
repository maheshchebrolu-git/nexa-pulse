# Driver Fatigue & Hours-of-Service Policy

**Purpose.** This policy enforces driving-hour limits to reduce fatigue-related risk, consistent with California TNC regulations.

**Driving-time limit.** Consistent with California TNC rules, drivers are allowed to drive a maximum of 10 hours, which resets after an 8-hour rest period. A Nexa Pulse driver may accumulate a maximum of 10 hours of driving time before being required to rest, and the clock resets only after a continuous off-duty period of at least 8 hours (status `offline`).

**Tracking and alerts.** Nexa Pulse tracks cumulative driving time per driver. The driver app warns the driver as they approach the limit and again when the maximum is reached, after which the driver is automatically taken `offline` for trip requests until the required rest period elapses. Time spent `offline` counts toward the rest period; brief toggles do not reset the clock.

**Interaction with incentives.** No incentive, quest, or repositioning request may push a driver past the hours-of-service limit. The system suppresses incentive prompts to drivers nearing the cap. Quests must be achievable within lawful driving hours.

**Multi-app drivers.** Because drivers may use other platforms, the on-platform clock reflects only Nexa Pulse time and may understate total fatigue. Operations should treat the limit as a floor, not a guarantee of alertness, and may act on credible fatigue reports regardless of on-platform hours.

**Operations manager role.** The dashboard shows how many drivers per zone are approaching or have hit the cap, which is a forward-looking supply risk: a wave of drivers timing out during a peak (for example, late-night Mission/Castro demand) can rapidly degrade coverage. Managers should plan replacement supply rather than attempting to extend any individual driver's hours.
