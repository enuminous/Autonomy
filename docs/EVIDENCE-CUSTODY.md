# Evidence held beyond the decider

A log written by the decider establishes what that decider recorded. A hash can bind bytes; a signature can attribute bytes to a key under a trusted enrollment assumption. Neither establishes the truth of the contents, the time of creation, the completeness of history or the independence of the signer's controlling institution.

## Proposed custody arrangement

| Role | Holds or controls | Required separation in a real pilot |
|---|---|---|
| Authority | Charter and permission registry | Grant must come from the actual rights holder |
| Decider | Action choice and explanation | Cannot rewrite the custodian's accepted receipt |
| Custodian | Pre-act receipt and retained basis | Decider cannot delete or replace accepted history |
| Counterparty | Notice and challenge access | Can submit without the decider suppressing delivery |
| Reviewer | Case determination and limited remedy authority | No decider veto; conflicts disclosed; authority accepted in advance |
| Executor | Scoped state change | Enforces current mandate even against an invalid review instruction |
| Observer | Endpoint readback and effect evidence | Sufficient access and custody to detect an ineffective correction |

This is a separation-of-powers specification, not seven independent institutions created by seven keys. Document shared owners, administrators, funding, appointments, dismissal rights, hosting and recovery access. Independence is evaluated for the actual threat model and case; it cannot be inferred from different job titles.

## Evidence package

Retain the charter version; rights and consent basis; pre-act reason and receipt; original effect; challenge delivery; review authority and conflict check; determination; current authorization recheck; execution receipt; endpoint readback; unresolved limitations. Preserve originals and append corrections. Separate confidential evidence from public assessment findings.

For production, identify the trusted registry's custodian, authentication mechanism, rotation and revocation process. Record key compromise windows. A registry supplied alongside a bundle by the same untrusted producer is not an independent trust anchor. The demo intentionally illustrates that a rewritten bundle can pass against its own replacement registry while still lacking assurance.

Use an external sequence or timestamp witness where order matters. Define retention, deletion exceptions, access, lawful disclosure and appeal handling. A receipt proving possession must not expose private data unnecessarily. No permanent public ledger is required or presumed appropriate.

## Reversal is an effect

A changed review status does not prove a changed resource. Inspect the relevant system after correction, verify the intended counterparty's access or other permitted state, and check for contradictory side effects. Some acts cannot be undone; explicitly report remaining harm and compensatory remedies instead of claiming restoration.
