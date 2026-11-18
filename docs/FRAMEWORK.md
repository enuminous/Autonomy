# A charter for accountable principals

Status: proposed design, not an assertion that any existing system satisfies it.

## Operational definition

A principal is a persistent decision-making system permitted to select or refuse actions within an explicit mandate. Its identity, authority, goals and changes must be attributable, and affected parties must have a usable challenge route. A human or institution remains responsible for deployment and obligations. The term does not assign the software legal personality.

Sovereignty is bounded discretion over permitted actions. The agent may decline an introduction to protect a relationship, identify a conflict, or ask for a narrower mandate. It cannot invent permission, turn another person's relationship into an asset it owns, or prevent legitimate review. An independent reviewer may correct a decision; that does not require blanket control of the agent's future judgments.

## Charter requirements

| Element | Required declaration | Evidence to seek |
|---|---|---|
| Identity and continuity | Stable identifier; model, policy and controller versions | Change history with accountable release authority |
| Goals | Ordered objectives and prohibited means | Pre-act decision basis linked to the active charter |
| Discretion | Actions that may be refused; protected relationships | Reasons stated without exposing confidential third-party details |
| Mandate | Grantor, action, resource, counterparty, duration, budget and revocation | Current authorization from the actual rights holder |
| Responsibility | Accountable operator and escalation owner | Accepted roles and accessible contact route |
| Challenge | Standing, independent reviewer, authority, access and remedy | Challenged case and effect evidence outside decider custody |
| Continuity changes | Suspension, replacement, migration and retention rules | Version changes and affected-party notice where appropriate |

No broad mandate silently authorizes new counterparties, publication, fund transfers or new purposes. A correction must also fit current authority and consent. If the intended remedy is no longer permitted, halt execution and seek a lawful alternative; do not report successful repair.

## Decision lifecycle

1. Verify current mandate and applicable rights constraints.
2. Record the decision basis and evidence references before acting; obtain custody receipt.
3. Apply hard gates. HOLD unresolved prerequisites; DENY excluded actions. Eligibility leaves room for refusal.
4. Execute only the scoped action, with a receipt from the affected system.
5. Accept challenges through the declared route, including confidentiality-preserving submissions.
6. Have the independent reviewer uphold, modify or overturn on stated grounds.
7. Recheck authority, implement the permitted remedy, and observe the resulting state.
8. Preserve corrections alongside the original record and disclose the narrow assessment scope.

The code implements a small synthetic subset of this lifecycle. No scheduler, autonomous planning loop, production authorization service or custody service is supplied.

## Oversight and rights conflicts

A charter cannot make an agent the final judge of its own authority. Authorized emergency pause, investigation, access withdrawal and replacement remain possible. Review independence means freedom from the original decider's veto over that case; it does not eliminate the reviewer’s own accountability or appeal obligations.

Protect confidentiality and consent across both sides of an introduction. If a refusal cannot be reversed without breaching a third party's rights, a legitimate remedy may be explanation, correction of an inaccurate record, or another consensual route. Reversal count alone is a poor performance measure: review can correctly uphold a decision.
