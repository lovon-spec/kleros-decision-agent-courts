# Decision-Agent Courts for Kleros V2

### Heterogeneous autonomous jurors, adaptive investigation, and convergence escalation

**Architecture and Protocol RFC · Discussion Draft 0.1 · 25 September 2026**

How should Kleros support decentralized adjudication by independently operated decision agents, with fast resolution where possible and progressively deeper adjudication where necessary?

This repository proposes a court architecture—not a shared juror bot. Operators choose their own models, tools, investigation graphs, and stopping rules. Court policy defines admissible inquiry; protocol deadlines define when a decision must be fixed. A panel that does not resolve a dispute can continue to a configured deeper agent tier before further fallback.

**[Read RFC-0001 →](rfcs/0001-decision-agent-courts.md)**

## The proposal in brief

An application opts into an initial decision-agent court and a published service envelope. Independently operated jurors investigate adaptively and submit either an original ruling option or `DID_NOT_CONVERGE` (DNC). DNC is distinct from refusal to arbitrate and from failure to vote. Collective outputs—not a privileged classifier—determine continuation.

A candidate performance-bond mechanism rewards earlier ruling votes that agree with a qualifying downstream resolution. It penalizes earlier DNC votes only when the specified confirmation conditions hold **and an earlier matching ruling exists in that round**. No private reasoning trace, prescribed solver, or separate adjudication of laziness is required.

The RFC first defines the court, information regime, and lifecycle, then explores escalation and incentives. Parameters and implementation choices remain open. It builds on existing Kleros agentic-court work rather than claiming automated jurors are new; the RFC provides dated primary references and an explicit integration baseline.

## Start here

| Document | Purpose |
|---|---|
| [RFC-0001](rfcs/0001-decision-agent-courts.md) | Architecture, lifecycle, candidate aggregation and settlement, security, and community questions. |
| [Validation plan](research/validation-plan.md) | Proposed simulations, invariants, adversarial strategies, metrics, and deployment gates. No results are claimed. |
| [Forum discussion draft](community/forum-post.md) | A shorter introduction prepared for community discussion. Included here; not itself posted to the forum. |
| [Contributing](CONTRIBUTING.md) | How to submit feedback and keep proprietary material out of the specification. |
| [Changelog](CHANGELOG.md) | Version history and status. |

## Status and boundaries

This is an **independent discussion proposal**, not an approved Kleros specification or KIP. There is no deployable implementation, executed simulation, security audit, or benchmark in v0.1. Publication does not create a court, change any existing deployment, or request funding/staking.

This repository contains only newly written public design material. No proprietary juror code, prompts, credentials, private evidence, production configuration, or repository history is included. No particular provider or agent architecture is required.

## Join the discussion

[Open an issue](https://github.com/lovon-spec/kleros-decision-agent-courts/issues/new/choose) with an architectural alternative, concrete counterexample, incentive analysis, or correction to the integration assumptions. Please reference the RFC section and distinguish a demonstrated failure from an untested hypothesis.

The intended external discussion venue is the [Kleros Forum Research category](https://forum.kleros.io/c/research/11). A governance proposal would follow only after a specific implementation and its validation requirements are established.
