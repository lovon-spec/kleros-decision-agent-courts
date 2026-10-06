# Changelog

## 0.3 — 2026-10-06

A revision after a second review, checked against Court #34's on-chain record.

- New lead. The proposal now rests on two promises: no forced guesses in the first round, and any fast ruling can be sent to the agent court at a price paid in advance. Speed and price come second.
- The objection. Each side's deposit is tied to the answer it backs. After a decision-court ruling, the losing side can object within a short window, and the case moves to the agent court with no new money and no funding race. The side that loses in the end pays.
- One seat per juror in the decision court.
- One flat DNC charge. Draft 0.2's two-level charge is now a variant, and the charge is no longer used to deter pushing cases up.
- New example values (f = 1, L = 9, d = 0.25) and a list of the limits a court's settings must meet. The old values put the bar for ruling at 0.60 to 0.70, and a juror that ruled on 40% of its cases at 95% accuracy could at best break even.
- One payoff table for every decision-court round: no money moves between jurors. Kleros's usual sharing in settled rounds, which Draft 0.2 kept, is now a variant, because it makes a speculative vote against the likely answer pay.
- What a settled round pays for, and why that depends on wrong rulings being challenged.
- A new section on why a separate court and not a feature inside each juror, with a "not sure" dispute kit inside Court #34 as a middle option.
- Court #34's numbers as it runs today: cases, fees, time to a first and a final ruling, and the cost of appeals.
- A path of small steps toward a pilot, starting with a shadow run that needs no contracts.
- Validation plan: three more comparison arms, a shadow gate, pass marks and sample sizes, and reporting on objections and spot checks.
- A short script that reproduces the payoff numbers (`research/payoff_checks.py`).
- Eight hard sentences rewritten.

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
