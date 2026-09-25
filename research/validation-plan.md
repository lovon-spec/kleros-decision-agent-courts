# Validation plan for RFC-0001

**Status:** proposed work accompanying Discussion Draft 0.1, 25 September 2026.

No experiment, simulation, contract test, or benchmark described here has been executed for this RFC. This document defines how to evaluate the proposal without treating agreement, successful termination, or a single lucky vote as proof of adjudication quality.

## 1. Questions and falsifiable hypotheses

The primary question is whether the proposed court architecture offers a useful cost/quality/latency trade-off relative to an appropriate existing adjudication procedure. A bonus mechanism that works only by making the overall service unaffordable is not a success.

Evaluate the following hypotheses separately:

| Hypothesis | Evidence that would weaken it |
|---|---|
| A short initial agent tier resolves a useful share of cases at lower total cost. | Review, reserve, and transport costs erase the initial-tier savings. |
| Deeper agent tiers add useful capability. | Additional agents reproduce the same error, or extra time does not improve decisions. |
| DNC allows uncertainty to be reported without profitable habitual abstention. | Instant-DNC strategies dominate honest participation or form a stable all-DNC equilibrium. |
| Conditional early-solver transfers improve investment in useful research. | Random/fixed-answer strategies capture the pool, or genuine research is less profitable. |
| The inherited evidence standard supports consistent cross-tier review. | Later panels systematically rely on inadmissible new facts or misclassify retrieval failure as substantive absence. |
| The protocol remains solver-neutral in practice. | Most assigned weight depends on one provider or common evaluator, despite multiple operators. |

These are research questions, not promised findings.

## 2. Comparison arms

Keep input distributions, adjudication deadlines, and cost accounting comparable. Where an arm requires different deadlines or panels, include those differences in the service-level results rather than comparing only model responses.

**A — ruling-only baseline.** Original choices with a stated aggregation/review mechanism and no DNC option.

**B — DNC without the special performance bond.** Same architecture and escalation route as the candidate, but no conditional DNC redistribution. Specify participation fees; “free DNC” is not a complete payoff table.

**C — RFC candidate.** A DNC loss requires a qualifying later panel confirmation and an earlier matching ruling in the affected round. Transfers go to eligible earlier matching votes.

**D — explicitly labeled variants.** Compare broader DNC penalties, different aggregation thresholds, alternative DNC fees, bonus caps, and different reserve designs one change at a time. Do not relabel these as the RFC candidate when they remove the early-solver condition.

Compare against direct entry to the deeper tier as well: the initial tier is useful only if its early resolutions justify their added cost and delay.

## 3. Agent and adversary populations

Model or implement sophisticated adaptive investigators, weaker sincere investigators, calibrated abstainers, random voters, fixed-answer voters, instant-DNC voters, answer-copying strategies, and strategic escalation controllers. Vary skill continuously rather than assuming all non-honest agents are random.

Include shared-model and shared-source correlation. Distinguish assigned voting weight, addresses, and controlling entities. An adversary with votes in multiple tiers should maximize combined profit, including dispute-side value and external bribes where modeled. Reporting only per-address returns can conceal self-transfers and multi-address coverage attacks.

A simulated sophisticated agent must not be granted free oracle access to the final label while other agents pay research costs. Explicitly model where its accuracy comes from, how its queries cost time/money, and how common evidence errors affect it.

## 4. Workloads and evidence regimes

Begin with synthetic disputes having an explicit policy and independently checkable labels, then add legally shareable cases reviewed under a documented protocol. Never import private production evidence, prompts, caches, or credentials.

Include clear cases, ambiguous policy applications, genuinely difficult investigation, policy-valid refusal, burden-of-proof decisions, and unresolvable cases. Vary outcome base rates and material information accessibility.

Evidence tests should include: a decisive fact available in a permitted historical chain view; a late argument using an existing standard; a late private photograph; a cited artifact that cannot be retrieved; a source mutated after the relevant time; evidence-targeted prompt injection; and a case where several sources repeat one unsupported assertion. Track the applicable initial evidence cutoff throughout escalation.

Separate training/development cases, parameter-selection cases, and held-out evaluation. Freeze the tested configuration and agent versions before evaluating the holdout. Document all post-hoc changes and do not present reused cases as independent validation.

## 5. Mechanism and accounting invariants

An executable reference model should check at least these invariants before any networked agent experiment:

| Invariant | Required property |
|---|---|
| Option identity | DNC never changes an original option ID or leaks into an arbitrable ruling. |
| Commitment integrity | A valid reveal has exactly the committed tag, option, round, and authorized vote domain. |
| Missing participation | Absent, invalid, and unrevealed votes do not become DNC. |
| Escalation eligibility | Partial tallies and duplicate transition calls cannot create unauthorized successor rounds. |
| Route termination | The tier route is acyclic; exhaustion selects only a predeclared terminal/recovery path. |
| Funding separation | Future conditional penalties are not spent as if they already funded a successor round. |
| Bonus conservation | Special payouts plus explicitly handled dust equal collected eligible DNC penalties. |
| Exposure limit | Combined losses never exceed the disclosed locked liability, including any ordinary coherence penalty. |
| Early-solver condition | No special DNC pool is collected without an earlier matching ruling in the affected round. |
| Confirmation provenance | One later vote, an overturned provisional ruling, or an unqualified funding default cannot trigger confirmation. |
| Exactly-once settlement | Repeated calls cannot duplicate a penalty, reward, stake release, or application execution. |
| Finality and release | Unconfirmed and terminal paths have explicit release rules; provisional recipients need not be trusted to return funds. |
| Lineage preservation | Court/kit transitions retain the binding between earlier assignments and the appropriate settlement reference. |

Enumerate small panels exhaustively. Include weights rather than just wallet counts, every output category, invalid reveals, ties, quorum boundaries, repeated transitions, and multiple review rounds. Use property-based testing for larger sequences once the reference model exists.

## 6. Adversarial and boundary scenarios

At minimum, test the following paths:

- All-DNC panels with later successful resolution, both honest difficulty and coordinated low effort.
- A single early matching answer produced by research, by random choice, or by a controller spreading its assigned votes across options.
- No early matching vote despite later resolution; this must not acquire a special penalty merely because the test author expected one.
- Cross-tier ownership, deliberate early DNC, and attempts to capture later fees or early-solver transfers through another address.
- DNC near the threshold, deliberate non-reveal, and strategic disagreement intended to force an expensive successor.
- A provisional downstream result that reverses, a funding default without fresh voting, a kit change, and a terminal unresolved case.
- Exhausted reserves, unavailable successor jurors, keeper outages, reorgs, delayed transactions, and restart during reveal or settlement.
- Late inadmissible evidence that creates a tempting but procedurally invalid answer, and persuasive common-source errors that all tiers reproduce.

Distinguish an architectural failure from a bad parameter choice. Conversely, do not dismiss an exploit solely because one chosen parameter sample did not exhibit it.

## 7. Metrics and reporting

Report total cost to parties, operator research costs, locked-capital cost, convergence coverage, policy-correctness where assessable, agreement with the final panel, and the distribution of escalation depth. Separate decision latency, provisional ruling latency, and executable-finality latency.

Report utility by both assignment and controlling entity. Include fee income, penalties, bonuses, capital duration, failed transactions, and costs of unsuccessful investigation. Sensitivity analysis should vary answer base rates, correlations, ownership concentration, available evidence, DNC fees, penalty sizes, quorum rules, and reserve assumptions.

Use all eligible cases in denominators. Include inactive, non-convergent, unreviewed, overturned, and terminal cases. Do not compare only the candidate's resolved subset against a baseline's full sample.

Where correctness cannot be independently established, label the metric agreement or expert-panel assessment rather than accuracy. Public justifications may improve review, but their availability must be identical across comparison arms or reported as an intervention.

## 8. Staged acceptance gates

**Model gate:** a complete state machine, payoff table, and terminal policy; exhaustive small-state tests; no unexplained accounting gaps.

**Economic gate:** useful strategies outperform the modeled evidence-insensitive alternatives in a published parameter region, with documented limits. No claim of universal equilibrium security follows from this result.

**Agent gate:** at least two independently built solver implementations, fixed evaluation sets, evidence-policy tests, and fully accounted costs. Architectural difference alone is not proof of independent errors.

**Integration gate:** audited contract changes, original-option preservation across kits, bounded custody, reorg/restart tests, ordinary appeal interoperability, and permissionless transition execution.

**Pilot gate:** explicit scope, economic limits, monitoring, shutdown/recovery procedure, and the governance authorization actually required for the selected deployment.

Passing a gate means publishing the evidence for it, not changing the status label in this document. Thresholds for success should be preregistered before collecting the corresponding evaluation results.

Return to [RFC-0001](../rfcs/0001-decision-agent-courts.md).
