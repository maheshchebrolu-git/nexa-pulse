# Incident Response Protocol

**Purpose.** This policy defines how Nexa Pulse detects, triages, and responds to safety incidents involving drivers or riders during any trip in San Francisco.

**Detection.** Incidents may be surfaced by automated trip-anomaly detection (an `in_progress` trip that goes substantially off the computed route, an unexpected long stop, or a possible crash signal), by an in-app emergency button, or by a post-trip report. Any of these creates an incident record on the operations dashboard.

**Severity triage.** Incidents are classified into tiers:

- **Tier 1 (critical)**: crash with injury, alleged assault, weapon, medical emergency, or any threat to life. Immediate instruction: call 911. The operations team supports emergency responders with live location and trip details and does not delay emergency contact for internal process.
- **Tier 2 (serious)**: minor collision with no injury, verbal altercation, intoxicated rider, allegation of unsafe driving. Requires same-shift follow-up by the safety team.
- **Tier 3 (standard)**: cleanliness disputes, minor service complaints, property left behind (routed to Lost and Found procedures).

**Immediate actions.** For Tier 1, the operations manager confirms emergency services are engaged, preserves all trip data (driver and rider identities, vehicle make/model/color, license plate, GPS route, timestamps for trip status transitions `requested` to `in_progress` to `completed`/`cancelled`), and may place the driver's account on hold pending review under the Driver Deactivation & Account Standards policy.

**Communication.** Affected parties receive a callback from the safety team within minutes for Tier 1 and within 24 hours for Tier 2. All communications follow the Communication & Notification Standards.

**Escalation.** Incidents that involve regulatory reporting obligations, media exposure, or potential litigation are escalated under the Operations Escalation Procedures. Law-enforcement data requests are handled only through the verified secure portal and the designated public-safety liaison.
