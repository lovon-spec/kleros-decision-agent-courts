# Discussion draft: Decision-Agent Courts for Kleros V2

*Prepared for the Kleros Forum Research category. This file is a publication draft; its presence in the repository does not mean it has been posted to the forum.*

We are sharing a first architecture and protocol RFC for **decision-agent courts**: courts designed around independently operated autonomous jurors, adaptive investigation, and a defined path to deeper adjudication when an initial tier does not resolve a dispute.

**Full RFC:** https://github.com/lovon-spec/kleros-decision-agent-courts/blob/main/rfcs/0001-decision-agent-courts.md

This builds on Kleros's existing agentic-court work. It is not an approved specification, a court-creation request, or a claim that automated jurors are new. The aim is to make a proposed court architecture precise enough for the community to critique before implementation choices and economic parameters are frozen.

## The court, not a common bot

Our starting question is: how should Kleros support timely adjudication by independent decision agents without prescribing the agent everyone must run?

A court should define the service: the case and policy references, evidence rules, timing, valid outputs, review, and settlement. Operators choose the implementation. One may use deterministic analysis, another an adaptive research agent, another several models and tools. Open-source and proprietary systems can participate without publishing their internal reasoning traces.

The investigation graph need not be known in advance. An agent may search, assess sufficiency, identify another material question, and investigate again. The governing policy constrains the inquiry; the decision deadline constrains when its answer must be fixed.

## Non-convergence as an explicit outcome

Alongside the original ruling choices, a juror can submit `DID_NOT_CONVERGE` (DNC): it did not reach a policy-supported ruling by the decision cutoff. This is distinct from the original refusal-to-arbitrate option and from failing to commit or reveal.

If the panel's outputs trigger continuation, the dispute moves to a configured deeper **agent** tier before further fallback. That tier can offer a longer window, different fees, or specialist participation. The architecture does not assume that a generic parent court is automatically better at the task.

An application opts into the initial court and route. No privileged classifier decides which disputes deserve escalation; public aggregation and transition rules do. A provisional ruling still needs ordinary appeal rights, because confident agreement can be wrong.

## Use the existing evidence standard

The proposal inherits the governing General Court standard rather than replacing it with a closed list of websites or an identical input package for every agent. The relevant public antecedent is [KIP-32](https://forum.kleros.io/t/kip-32-general-court-policy-update/483): the late-evidence restriction combines timing and reasonable public availability, while allowing later arguments from existing evidence or reasonably discoverable information.

Deeper adjudication buys more opportunity to reason and investigate within that standard. It does not authorize a new evidentiary regime. This does not require an additional Process Court to determine whether each unsuccessful agent was lazy.

## A candidate performance incentive

Consider an initial panel with `B, DNC, DNC`. It escalates; a later panel votes B, and B survives review. The RFC proposes testing a bounded penalty on the earlier DNC votes, paid to the earlier B voter.

The early-solver condition matters. If the initial panel was all DNC—or contained only an earlier A vote followed by final B—the candidate does **not** impose that special DNC transfer. Later success alone is not the trigger.

This is performance-based compensation, not proof that anyone was lazy or that the early voter used a good method. Guessing, fixed-answer strategies, all-DNC coordination, shared-model errors, and cross-tier ownership are explicit analysis targets. Making DNC less costly than a wrong answer is a starting parameter choice, not a proof of incentive compatibility.

## What is ready for discussion

Draft 0.1 describes the court roles, information regime, candidate aggregation, commitment timing, escalation route, funding requirements, confirmation and settlement conditions, and V2 integration boundaries. It includes a validation plan, not completed simulations or audited contracts.

Feedback is especially useful on the court architecture, a first pilot domain, aggregation under DNC and disagreement, prefunding of automatic escalation, all-DNC incentives, and whether a dedicated dispute kit can support the required custody and transition behavior without Core changes.

Please challenge the assumptions and suggest alternatives. The goal is not to sell a finished mechanism; it is to develop a solver-neutral court design with the Kleros community. Detailed feedback can reference the [RFC sections or repository issues](https://github.com/lovon-spec/kleros-decision-agent-courts/issues).
