# Validation plan for RFC-0001

**Status:** proposed work accompanying Discussion Draft 0.2, 30 September 2026.

No experiment, simulation, contract test, or benchmark described here has been executed for this RFC. This document defines how to evaluate the proposal without treating agreement, successful termination, or a single lucky vote as proof of adjudication quality.

## 1. Questions and falsifiable hypotheses

The primary question is whether the proposed court architecture offers a useful cost/quality/latency trade-off relative to an appropriate existing adjudication procedure. A bonus mechanism that works only by making the overall service unaffordable is not a success.

Evaluate the following hypotheses separately:

| Hypothesis | Evidence that would weaken it |
|---|---|
| A fast decision court resolves a useful share of cases at lower total cost. | Review, escalation, and transport costs erase the decision court's savings. |
| The agent court adds useful capability on the cases the decision court passes up. | It reproduces the same errors, or extra time and research don't improve decisions. |
| DNC allows uncertainty to be reported without profitable habitual abstention. | Instant-DNC strategies dominate honest participation or form a stable all-DNC equilibrium. |
| The baseline payoffs reward useful research over guessing and reflexive DNC. | Guessing, fixed-answer voting, seat splitting or instant DNC earns more than honest research, or all-DNC is stable. |
| The inherited evidence standard supports consistent review across both courts. | Later panels systematically rely on inadmissible new facts or misclassify retrieval failure as substantive absence. |
| The protocol remains solver-neutral in practice. | Most assigned weight depends on one provider or common evaluator, despite multiple operators. |

These are research questions, not promised findings.

## 2. Comparison arms

Keep input distributions, adjudication deadlines, and cost accounting comparable. Where an arm requires different deadlines or panels, include those differences in the service-level results rather than comparing only model responses.

**A — ruling-only baseline.** Original choices with a stated aggregation/review mechanism and no DNC option.

**B — DNC without penalties.** Same courts and route as arm C, but DNC votes pay nothing. Specify participation fees; “free DNC” is not a complete payoff table.

**C — RFC baseline.** The payoffs in RFC §7.3: no transfers between jurors in escalated rounds; unallocated fees and penalties go to the Core owner, as in Kleros V2 today (returning unused fees to the parties would need a Core change); DNC pays `d` when a ruling vote in its round matched the final ruling, and `ε` otherwise.

**D — explicitly labeled variants.** Change one thing at a time: the Draft 0.1 early-solver transfer (RFC §7.4), with and without a cap; broader DNC penalties; different aggregation thresholds, DNC charges and pot sizes; and ways to protect honest jurors on hard cases without DNC, such as outcome-dependent fees and deposits or penalties scaled by peer prediction ([George, 2024](https://blog.kleros.io/incentivizing-jurors-to-honestly-report-uncommon-answers-deposit-sizes-lazy-strategies-and-peer-prediction/)). Don't relabel a variant as the baseline.

Compare against sending cases straight to the agent court as well: the decision court is useful only if its early rulings justify their added cost and delay. Also compare letting agent-court jurors report DNC too (the Draft 0.1 design) against requiring them to rule.

## 3. Agent and adversary populations

Model or implement sophisticated adaptive investigators, weaker sincere investigators, calibrated abstainers, random voters, fixed-answer voters, instant-DNC voters, answer-copying strategies, and strategic escalation controllers. Vary skill continuously rather than assuming all non-honest agents are random. Include optimizing agents that choose between ruling and DNC to maximize their payoff, and report their DNC rate at each confidence level. Also include overconfident agents that rarely report DNC even when they should.

Include shared-model and shared-source correlation. Distinguish assigned voting weight, addresses, and controlling entities. An adversary with votes in both courts should maximize combined profit, including dispute-side value and external bribes where modeled. Reporting only per-address returns can conceal self-transfers and multi-address coverage attacks.

A simulated sophisticated agent must not be granted free oracle access to the final label while other agents pay research costs. Explicitly model where its accuracy comes from, how its queries cost time/money, and how common evidence errors affect it.

## 4. Workloads and evidence regimes

Begin with synthetic disputes having an explicit policy and independently checkable labels, then add legally shareable cases reviewed under a documented protocol.

Include clear cases, ambiguous policy applications, genuinely difficult investigation, policy-valid refusal, burden-of-proof decisions, and unresolvable cases. Vary outcome base rates and material information accessibility.

Evidence tests should include: late evidence that shows an attack on Kleros, which the policy says must be considered; hidden text in an exhibit that tries to steer the verdict, tested across operators and both courts, including how often it flips a whole panel; the same facts argued for the other side, where the vote should hold; a decisive fact changed, where it should flip; a decisive fact available in a permitted historical chain view; a late argument using an existing standard; a late private photograph; a cited artifact that cannot be retrieved; a source mutated after the relevant time; evidence-targeted prompt injection; and a case where several sources repeat one unsupported assertion. Track the applicable initial evidence cutoff throughout escalation.

Separate training/development cases, parameter-selection cases, and held-out evaluation. Freeze the tested configuration and agent versions before evaluating the holdout. Document all post-hoc changes and do not present reused cases as independent validation.

## 5. Mechanism and accounting invariants

An executable reference model should check at least these invariants before any networked agent experiment:

| Invariant | Required property |
|---|---|
| Option identity | DNC never changes an original option ID or leaks into an arbitrable ruling. |
| Commitment integrity | A valid reveal has exactly the committed tag, option, round, and authorized vote domain. |
| Missing participation | Absent, invalid, and unrevealed votes do not become DNC. |
| No absence veto | Withholding a reveal can't change a majority outcome that a contrary vote couldn't change. |
| Escalation eligibility | Partial tallies and duplicate transition calls cannot create unauthorized successor rounds. |
| Route termination | The route has one automatic step; any failure selects only a predeclared terminal or recovery path. |
| Unresolved cases | If no qualifying ruling is ever reached, ruling votes and DNC settle identically; only absent votes are penalized. |
| Funding separation | Future conditional penalties are not spent as if they already funded a successor round. |
| Conservation | Payouts, refunds, amounts sent to the Core owner, and explicitly handled dust equal the fees and penalties collected. |
| Exposure limit | Combined losses never exceed the disclosed locked liability, including any ordinary coherence penalty. |
| DNC charges | A DNC vote pays `d` only if some ruling vote in its round matched the final ruling, and `ε` otherwise; never both, and never more than `L`. |
| Confirmation provenance | One later vote, an overturned provisional ruling, or an unqualified funding default cannot trigger confirmation. |
| Exactly-once settlement | Repeated calls cannot duplicate a penalty, reward, stake release, or application execution. |
| Finality and release | Unconfirmed and terminal paths have explicit release rules; provisional recipients need not be trusted to return funds. |
| Lineage preservation | Court/kit transitions retain the binding between earlier assignments and the appropriate settlement reference. |

Enumerate small panels exhaustively. Include weights rather than just wallet counts, every output category, invalid reveals, ties, quorum boundaries, repeated transitions, and multiple review rounds. Use property-based testing for larger sequences once the reference model exists.

## 6. Adversarial and boundary scenarios

At minimum, test the following paths:

- All-DNC panels with later successful resolution, both honest difficulty and coordinated low effort.
- A single early matching answer produced by research, by random choice, or by a controller spreading its assigned votes across options.
- No early matching vote despite later resolution: DNC votes then pay only `ε`, never `d`.
- Ownership across both courts, deliberate early DNC, and attempts to capture agent-court fees (or, in variant arms, early-solver transfers) through another address, including when the agent court is a parent of the decision court.
- DNC near the threshold, deliberate non-reveal, and strategic disagreement intended to force an expensive successor.
- A provisional downstream result that reverses, a funding default without fresh voting, a kit change, and a terminal unresolved case.
- An insufficient pot, unavailable successor jurors, keeper outages, reorgs, delayed transactions, and restart during reveal or settlement.
- Late inadmissible evidence that creates a tempting but procedurally invalid answer, and persuasive common-source errors that both courts reproduce.

Distinguish an architectural failure from a bad parameter choice. Conversely, do not dismiss an exploit solely because one chosen parameter sample did not exhibit it.

## 7. Metrics and reporting

Report total cost to parties, operator research costs, locked-capital cost, convergence coverage, policy-correctness where assessable, agreement with the final panel, and the share of cases that move to the agent court. Separate decision latency, provisional ruling latency, and executable-finality latency.

Report utility by both assignment and controlling entity. Include fee income, penalties, bonuses, capital duration, failed transactions, and costs of unsuccessful investigation. Sensitivity analysis should vary answer base rates, correlations, ownership concentration, available evidence, DNC charges, penalty sizes, quorum rules, and pot sizes.

Calibration: for jurors who answer rather than report DNC, report how often they agree with the final ruling and compare it with the break-even in RFC §7.3 (about 60–70% with its example values), both overall and by operator. Error dependence: on independently labeled cases, report how often operators are wrong together and their error correlation after adjusting for case difficulty. "Same wrong answer when both are wrong" says nothing when there are only two options. In tests where implementations are known, also report how often jurors using the same model and method vote identically.

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
