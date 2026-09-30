# Changelog

## 0.2 — 2026-09-30

A revision after the review recorded in issues #1–#22.

- Two courts. In the decision court, jurors can vote "did not converge" (DNC). The agent court's jurors must always rule, and ordinary appeals follow. Court #34 is suggested as the agent court, with a new decision court in front of it as a first pilot.
- A ruling needs more than half of all seats, whatever the turnout, so withholding a vote can't block a majority.
- New baseline payoffs. In a round that moved up, a matching ruling earns only its own fee, a wrong ruling loses its stake, DNC pays a small charge, and no penalty goes to another juror. Draft 0.1's early-solver transfer rewarded guessing, so it's now a variant to test.
- The move to the agent court is prepaid per case by both parties and charged to the final loser.
- Also new: an answer to Kleros's FAQ on abstention, the current General Court evidence rule quoted directly, verdict steering through evidence as a threat, Kleros's AI courts and Trivium as context, why justifications are optional in the decision court, and what runs on today's Kleros contracts versus 2.0.0.
- Plain-language README and forum post draft.
- Licensed under CC BY 4.0.

## 0.1 — 2026-09-25

Initial public architecture and protocol discussion draft.

Introduces decision-agent courts before the incentive mechanism; permits heterogeneous solvers and adaptive research; inherits the governing evidence-admissibility standard; separates original rulings, DNC, and inactivity; proposes deeper agent escalation before further fallback; and states a candidate early-solver-conditioned DNC bond mechanism.

Includes worked ballot/settlement examples, implementation boundaries, a validation plan, a forum-post draft, and a feedback template. Public V2 specification references are pinned to commit `320b23d526c2a5d13cae782e1a53896da83d7010`.

No deployed mechanism, executed simulation, benchmark, security audit, approved KIP, or forum publication is claimed by this release of the draft.
