# Autonomy

**EFMW principals framework for sovereign autonomous agents**  
Monolithic · Research specification and executable reference model · v0.1.0

A principal exercises discretion within a declared charter, can decline an action, preserves accountable continuity, and can be challenged through a route it does not control. In this proposal, **sovereignty means bounded discretion with accountable correction**. It does not mean immunity from oversight, unrestricted access, or a claim of consciousness or legal personhood.

The first question is practical: **can someone independent of the decider obtain and implement a justified correction?** A decider's own explanation is useful evidence, but is not independent assurance. Different keys and intact hashes do not establish different controlling interests.

## Interactive lab

Open [index.html](index.html) locally in a browser to explore authority, review independence and observable correction. Six presets, live conditional findings, a reversible mock resource and downloadable case JSON run entirely in the browser. This policy illustration does not perform the Python verifier's signature checks or establish live assurance.

## What is here

| Read | Purpose |
|---|---|
| [Framework](docs/FRAMEWORK.md) | Identity, charter, discretion, authority and responsibilities |
| [EFMW method](docs/EFMW-METHOD.md) | Operational research loop and explicit limits of the mathematics |
| [UDCR filter](docs/UDCR-FILTER.md) | Ten rights articles translated into proposed controls |
| [AUT-001](docs/AUT-001.md) | First test: an externally reviewable reversal with observable effect |
| [Evidence custody](docs/EVIDENCE-CUSTODY.md) | Who holds records, keys, authority and observations |
| [Verdicts](docs/VERDICTS.md) | Claim accuracy, control existence and effective remedy reported separately |
| [Threat model](docs/THREAT-MODEL.md) | Common control, fabricated records, revocation and irreversible effects |
| [Pilot protocol](docs/PILOT.md) | How to move from a local demonstration to a limited live evaluation |
| [Sources](docs/SOURCES.md) | Provenance and separation of sources from this proposal |
| [Roadmap](docs/ROADMAP.md) | Implemented capabilities and unresolved dependencies |
| [Templates](templates/README.md) | Charter, decision, appeal and scoped assessment records |

## Run the reference case

Python 3.12 is the tested local version. Node.js 18+ is also required for the browser-model parity tests (the HTML itself needs only a browser). Use an isolated environment:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m autonomy demo --output artifacts
python -m autonomy verify artifacts/bundle.json --registry artifacts/demo-registry.json
```

The demo changes a local synthetic resource from `DENY` to `ALLOW` after a signed challenge and review. It produces eight signed records, a public-key registry, a mock resource state, a verification result and a source/run manifest. It neither contacts counterparties nor operates a deployed agent. Private signing keys remain in process memory and are not exported.

Expected result:

```json
{
  "technical_verdict": "PASS",
  "real_world_independence": "UNRESOLVED",
  "live_reversal_assurance": "UNRESOLVED"
}
```

**Every demo role is controlled by one process.** This is a test of signature and record consistency plus a local state transition. The verifier does not discover institutional independence, query a production endpoint, verify external consent, or establish trusted wall-clock time. Its technical PASS is never a principal certification. Supplying no registry returns UNRESOLVED (exit 2); inconsistent evidence returns FAIL (exit 1).

`autonomy.policy` supplies proposed hard gates: unavailable authority, rights conflict, unverified required review, or an unreleased artifact cannot be overcome by a high utility score. An eligible action remains discretionary. These gates consume supplied findings; they do not establish the truth of those findings.

Browser addition: 43 tests now pass, including cross-language checks over 1,080 combinations of route and policy conditions. Browser interaction checks cover successful reversal, paper-only failure, absent-route blocking and JSON download.

## Status and scope

Initial implementation: 40 automated tests cover record integrity, signer roles, ordering, scope, expiry, revocation assertions, replay across case IDs, observed correction, policy gates, and verdict distinctions. CI runs those checks and publishes only synthetic run artifacts. See the workflow's actual result for the revision being reviewed.

This repository is an independent Monolithic proposal. It is not a Boardy product, endorsement, engagement, accepted integration, or legal opinion. EFMW is used here as a proposed research method; this repository establishes no physical law, consciousness result or measured advantage over conventional controls. No real independent reviewer or live pilot is represented as appointed.

Read [license status](LICENSE-STATUS.md) before reuse. Read [contribution](CONTRIBUTING.md) and [security](SECURITY.md) guidance before submitting data or deploying adaptations.
