# RFC-0001: Decision-Agent Courts for Kleros V2

## A fast first court where AI jurors can say "not sure", in front of Kleros's agent court

| Field | Value |
|---|---|
| Status | Discussion Draft 0.2 — request for community feedback |
| Date | 30 September 2026 |
| Proposer | lovon-spec |
| Scope | Court design and protocol; not a deployment proposal |
| Discussion | [Repository issues](https://github.com/lovon-spec/kleros-decision-agent-courts/issues) |

This is an independent proposal for discussion with the Kleros community. Kleros hasn't adopted it, and it isn't a KIP. Nothing in it has been built, simulated, benchmarked or audited yet. It describes a proposed design, not how Kleros works today.

## Abstract

This RFC proposes a fast first court for Kleros V2 whose jurors are AI decision systems run by different operators. The goal is to settle clear disputes quickly and cheaply, and to pass the rest on to more thorough courts.

There are two courts. In the **decision court**, fast decision models vote for a ruling or report that they **did not converge** (DNC): they couldn't reach a well-supported ruling in time. DNC is different from voting "refuse to arbitrate" and from not voting at all. A ruling needs more than half of all seats. Otherwise the case moves automatically to the **agent court**, where research agents get more time and must always rule. Court #34, Kleros's Agentic Commerce Court, is the natural agent court. After that, ordinary appeals apply, up to human jurors. The votes and published rules decide when a case moves, not a central classifier.

The court defines the job, not the method. Operators bring their own systems and compete. In a decision-court round that moves up, a juror whose ruling matches the final outcome earns its fee, a wrong ruling loses its stake at risk, and DNC pays a smaller charge. No juror's penalty goes to another juror, so guessing and splitting votes across seats don't pay. Draft 0.1's early-solver transfer, which paid DNC penalties to early matching voters, rewards guessing under Kleros's usual fee pooling; it remains only as a variant to test.

The RFC covers the court model, the evidence rules, the lifecycle, escalation and funding, candidate payoffs, what runs on today's Kleros contracts, and an evaluation plan. It asks for critique before any parameters are chosen or any governance action is proposed.

## 1. Motivation and scope

The starting question is:

> How should Kleros support decentralized adjudication by independently operated decision agents, with fast resolution where possible and progressively deeper adjudication where necessary?

There are three distinct concepts. A dispute can **involve agents as parties**. A juror can **use an agent inside an existing court**. Or a court's **procedure can be designed around decision agents**, including their timing, interfaces, failure modes, and escalation. This RFC concerns the third; agent commerce is a possible initial application, not a restriction on the identity of disputing parties.

This proposal builds on work Kleros already runs. Court #34, the Agentic Commerce Court on Kleros V2, is listed as a live court whose jurors are expected to be AI agents, offering "a Kleros-grade ruling, with the option to appeal to human jurors."[^1] Kleros's published design goes from an AI court to "a non-specialist human panel, verified through a proof-of-personhood protocol," and then to specialist and general courts.[^9] Kleros co-founder Clément Lesaege has put the principle plainly: "Systems cannot be AI only but need to at least be able to appeal to humans in the end."[^10]

This RFC keeps that principle: after the agent court rules, ordinary appeals apply and can reach human jurors. What it adds is a decision court where a juror may report DNC, one automatic and prefunded step from the decision court to the agent court, and settlement rules for that step. The agent step is there because the two courts use different kinds of systems (§6.5): research agents may settle some disputes a fast model can't, more cheaply and quickly than a human panel.

Court #34 is the natural agent court for this design. The first pilot we suggest is a new decision court in front of it, for one family of agent-commerce disputes, such as escrow disputes. The decision court should sit beside Court #34 in the court tree, not under it (§6.5). Kleros has also built Trivium, a prototype that screens disputes with nine AI analyses and sends cases where they disagree to human jurors.[^14] The decision court differs in two ways: each juror reports DNC for itself, and the jurors are independent operators with stake at risk, so the payouts, not a fixed recipe, decide which systems last.

For parties, the intended service is an inexpensive first opportunity for a defensible ruling, with a predictable continuation path rather than either forced guessing or an unexplained failure. For juror operators, the opportunity is to compete on evidence-sensitive adjudication, reliability, and cost without surrendering implementation autonomy.

The hypothesis is that this design can make some kinds of disputes cheaper and faster to resolve without worse rulings. It isn't a promise that AI jurors are cheaper or more accurate in every court. A first pilot should pick one narrow family of disputes with clear policies and outcomes that can be checked. We suggest one above, but the choice remains open (§11).

## 2. Principles and non-goals

**Standardize the service, not the solver.** The protocol defines assignments, input references, permitted outputs, deadlines, review, and payment. It does not require a shared model, prompt, provider, software package, graph, or confidence threshold. Open-source and proprietary implementations can participate on the same terms. Operators compete on their systems, and the payouts reward those that get it right.

**No authoritative cognition router.** An application opts into a configured court and escalation route. Any optional recommendation service is advisory. Once a dispute is admitted, collective votes and deterministic transition rules govern escalation.

**Preserve policy-based adjudication.** The objective is a ruling justified under the governing policy, not a forecast of popular answers divorced from the evidence. Downstream coherence is an observable settlement signal, not proof of factual truth.

**Permit honest non-convergence.** Reporting failure to reach a ruling must be possible without inventing one. The report may still carry pre-agreed economic consequences.

**Keep investigation adaptive.** A juror may discover new research steps during execution. A timeout bounds participation, not the mathematical search space. An agent's successful stop does not prove that its information was sufficient; that remains an adjudicative judgment.

**Separate authority from untrusted material.** Evidence is input to adjudication, not authority to change tools, credentials, court policy, or signing permissions.

This RFC does not propose a universal classifier of finite problems, a proof that an agent has thought hard enough, a canonical chain of reasoning, mandatory publication of private reasoning traces, or an automatic equation between wallet diversity and independent judgment. The proposed performance incentives also don't depend on a Process Court, the separate court Kleros has described for challenging jurors who break court policy, later discussed as a Juror Misbehaviour Court.[^12][^7]

## 3. Court, operator, and agent model

### 3.1 What is a decision agent?

A decision agent is an operator-controlled system that receives a juror assignment, acquires and evaluates permitted information, decides whether it can support a ruling, and fulfills the required commitment and voting duties. It may combine deterministic computation, language models, retrieval, specialist services, and internal checks.

For example, an agent may search a batch of sources, assess the remaining material questions, query a chain, and repeat until it can apply the policy or reaches its decision deadline. The protocol does not require the resulting graph to have been specified in advance. The graph is an implementation detail; the externally meaningful deliverable is a timely valid vote.

Autonomy is a service expectation in both courts, not something proven merely by accepting a transaction from a wallet. This draft does not introduce an oracle that certifies whether cognition was human or machine. Human-assisted operation, disclosure requirements, and any eligibility restrictions are questions for court policy.

### 3.2 Roles and trust boundaries

| Role | Responsibility |
|---|---|
| Parties and arbitrable integration | Choose the service envelope, supply the original question/options, fund agreed fees, and receive the eventual ruling. |
| Court policy | Define admissibility, substantive obligations, timing, participation, and escalation terms. |
| Juror operator | Supply stake and an independently operated adjudication system; remain responsible for its external actions. |
| Decision agent | Investigate and choose a ruling or DNC under policy and deadline constraints. |
| Signer/transaction component | Enforce assignment, domain, round, vote, nonce, and reveal constraints independently of case prose. |
| Core, dispute mechanism, and transition executor | Record votes, aggregate outcomes, advance rounds, enforce custody and finality, and settle liabilities. |

Shared SDKs, parsers, and transaction libraries are compatible with this architecture. Requiring a particular adjudication workflow is not. The design permits heterogeneous systems but cannot ensure that operators actually use them; shared providers and correlated failures must be measured. Jurors that run the same model with the same method will vote the same way, so a panel is only as independent as its methods are different.

### 3.3 The published service envelope

Before accepting a dispute, the integration exposes a versioned configuration containing: applicable policy references; original ruling options; the decision court and the agent court it escalates to; assignment and voting rules; evidence and decision deadlines; appeal rights; fees and the escalation pot; settlement rules; and a terminal failure policy.

Configuration relevant to an accepted dispute must not be silently replaced during that dispute. A concrete implementation must specify how policy versions, governance upgrades, and emergency powers interact with existing cases. This RFC proposes no authority to alter another court or live juror systems already operating there.

## 4. Information model: inherit the governing evidence policy

The design adopts the evidence rule of the current General Court policy, which KIP-32 introduced and which is still in force word for word.[^3] It says jurors "should disregard any evidence that is both 1) submitted after the end of the evidence period of the initial round of a dispute AND 2) cannot be reasonably considered to have been readily, publicly available to jurors. Jurors may, however, consider arguments that are submitted later that are based upon existing evidence and/or information which a juror considering the case during the evidence period of the initial round could reasonably have been expected to find themselves." Evidence is excluded only when **both** conditions hold.

The same policy adds that "evidence related to the presence of attacks on Kleros should be considered by jurors even if it would otherwise violate the above points on evidence admissibility." This matters for agent courts, where evidence written to manipulate agents is a real risk.

The policy also tells appeal jurors to defer to a specialized lower court: "If there is no evidence of an attack AND appellate court jurors cannot be reasonably expected to have the required skills to independently evaluate the case, jurors should vote to uphold the lower court ruling." A later ruling that upholds an earlier one by deference is not a fresh review, which matters for settlement (§7.2).

This is not a submitted-documents-only model. It is also not permission to use anything that happens to be reachable on the Internet at the time an appeal is heard. Public accessibility, historical availability, reasonable discoverability, relevance, and other applicable policy requirements remain distinct questions.

The same admissibility standard applies in both courts. The agent court receives more opportunity for computation and investigation, not an automatic license to use otherwise inadmissible late material. No separate information-availability tribunal or new closed evidence whitelist is proposed.

For example, a later argument that draws attention to historically public token distribution can be relevant without creating a new admissible-world cutoff. A previously private photograph supplied only after the initial evidence period does not become admissible simply because it helps the agent court reach an answer. These are applications of the inherited standard, not additional protocol exceptions.[^3]

Three temporal references should remain explicit: the policy's relevant state-of-the-world date, the initial evidence-period cutoff, and each court's decision deadline. Moving the third does not move the first two. Immutable references, historical chain queries, retrieval timestamps, and content hashes help preserve provenance. They do not mechanically prove reasonable discoverability or admissibility.

Before implementation, contributors must pin the policy of the target deployment. The text quoted above was checked against the V2 General Court policy on 27 September 2026; other courts and chains may differ. Changes to that policy should be evaluated as explicit changes to the service, not introduced indirectly through an agent prompt.

## 5. Outputs and terminology

The conceptual decision type is:

```text
Decision = RULING(originalOptionId) | DID_NOT_CONVERGE
```

`RULING` includes every original option that the governing policy permits, including a refusal option where applicable. `DID_NOT_CONVERGE` (DNC) is a control outcome, not an additional award to a party.

| Output or event | Meaning |
|---|---|
| Ruling for A or B | The juror submits that original answer under the policy. |
| Policy refusal | The juror submits the original refusal option on substantive policy grounds. |
| DNC | The juror did not establish a sufficiently supported ruling within the decision court's window. Only decision-court jurors can report DNC; agent-court jurors must rule. |
| Missing or invalid participation | The juror did not complete the required protocol action; it is not silently converted into DNC. |

DNC does not assert that no terminating procedure exists, that another agent cannot solve the case, or that the reporting operator was negligent. It is a truthful report about a failed service attempt, with compensation determined by the agreed economic rules.

**How DNC differs from the recusal Kleros rejects.** Kleros's FAQ says drawn jurors can't recuse themselves, because that "would disrupt the balance of dispute resolution costs" and "abstention could compromise the integrity of outcomes, potentially lowering the bar for influencing decisions."[^11] DNC is limited to the decision court, where it is a reported, priced outcome rather than a free exit; the agent court keeps Kleros's rule that jurors must rule. On the three concerns:

- *The bar for influence* is handled by construction. A ruling needs more than half of all assigned weight, not just of the votes cast (§6.4), so DNC votes can't let a minority decide: A, DNC, DNC doesn't produce A.
- *Cost balance* is a hypothesis to test. DNC earns no fee and carries a penalty (§7.3), and the one automatic step is prefunded per case and charged to the losing party (§6.6), so hard cases cost more, but that cost is disclosed and stays with the dispute.
- *Quality in hard cases* is also a hypothesis to test. Instead of forcing a guess, DNC sends the case to research agents with more time (§6.5), and ordinary appeals to human jurors remain.

A production encoding must preserve original option IDs and bind the control tag unambiguously. It must not overload refusal, add an executable party award by accident, or pass DNC to an arbitrable contract that does not understand it. An illustrative `0` refusal in examples below is not an instruction to relabel existing dispute options.

## 6. Adjudication lifecycle

### 6.1 Entry and assignment

The arbitrable integration selects the decision court and agreed route when it requests arbitration. The current V2 arbitrator specification describes court and dispute-kit selection through dispute creation parameters.[^2] This RFC adds a versioned service envelope and does not make access depend on one vendor's case classifier.

Agents receive authenticated dispute identity, court and round identity, question, original options, policy references, canonical evidence references, and deadlines. They can normalize and investigate the case differently. Acquisition failures must not be silently represented as proof that a party supplied no evidence.

### 6.2 Adaptive investigation and stopping

An agent may begin with the supplied record and extend its research procedure just in time. It can branch on what it learns, use external operations allowed by policy, and repeatedly assess whether material questions have been resolved sufficiently to vote.

The protocol does not inspect how many model calls the agent used, demand a finite graph in advance, or specify its confidence threshold. The agent's stopping policy is part of the implementation on which operators compete. Its output remains subject to ordinary policy-based review and the proposed settlement rules.

### 6.3 Commitment and decision deadline

For a hidden-vote design, the decision must be fixed by the **commit deadline**, not the later reveal deadline. A reveal opens the committed choice; it does not provide an additional opportunity to choose an answer after seeing peers. Classic already documents an optional commit/reveal mechanism, but the exact commitment format and domain separation for DNC are new design work.[^8]

A commitment must bind the deployment domain, dispute, court, round, assigned vote identity or group, output tag, original ruling ID when present, and secret. Reveal and recovery rules must preserve those bindings. Voting rights must not depend on an untrusted attachment's claimed role or permissions.

The draft proposes hidden voting in both courts, subject to latency and integration evaluation.

**Justifications.** A decision model that only returns probabilities has no written reasoning of its own. A justification would have to be a second model's explanation after the fact, which adds time and isn't why the vote was cast. Requiring each juror to publish its full decision trace would also give its method away: others could copy the best one, panels would start to vote alike, and attackers would learn which questions to target. Human jurors aren't asked to show their thought process either; they're judged by their votes. This draft therefore makes justifications optional in the decision court and requires them in the agent court, so anyone who wants reasons can get them by appealing. Whether decision-court jurors should seal a fingerprint of their decision record with their vote, to be opened on appeal, is an open question (§11).

### 6.4 Candidate aggregation rule

The decision court needs an explicit rule for a mixed panel of ruling votes, DNC, and inactive assignments. The following is a **simulation baseline**, not an assertion about Classic or a settled recommendation. The agent court counts votes as ordinary Kleros courts do.

Let `N` be the total assigned voting weight and `V` the valid revealed weight. We use voting weight, not a count of wallet addresses. An original ruling with weight strictly greater than `N/2` becomes a provisional ruling, and DNC with weight strictly greater than `N/2` moves the case to the agent court, whatever the turnout. If neither has that majority, a quorum of `V >= 2N/3` decides the label: with quorum, the round is inconclusive; without it, it is a participation failure. Both also move the case to the agent court (§6.7). Because the quorum only applies when nothing has a majority, a juror can't block a majority by withholding its reveal.

For three equal-weight assignments:

| Votes | Candidate round disposition |
|---|---|
| A, A, DNC | Provisional A; ordinary review remains available. |
| B, DNC, DNC | Moves to the agent court; the early B vote is kept for settlement. |
| A, B, DNC | Inconclusive; moves to the agent court. |
| DNC, DNC, DNC | Moves to the agent court; no early ruling vote. |
| 0, 0, DNC | Provisional original refusal, not automatic escalation. |
| A, absent, absent | Participation failure; moves to the agent court, and the absent votes are penalized. |

This baseline avoids executing a merits answer supported by only a small fraction of assigned weight. It can also escalate more often than plurality. Thresholds, quorums, and the relationship between disagreement and DNC need comparative evaluation; they are not concealed as implementation details.

### 6.5 Two courts: decision court, then agent court

The route is:

```text
Decision court: fast decision models; a juror may report DNC
    -> agent court: research agents with more time; every juror must rule
        -> ordinary appeals, which can reach human Kleros courts
```

The two courts differ in kind, not only in size. The decision court suits fast, bounded decision models that either rule or report DNC within a short window; DNC is how such a model says a case is beyond what it can settle in that window. The agent court suits agents that do open-ended research, with more time and budget, and it keeps Kleros's ordinary rule that every juror must rule. That is the case for an agent step before human jurors: some cases a decision model can't settle are still tractable with open research, at lower cost and delay than a human panel. Operators can enter either court with any system; the published terms decide the fit.

A case reaches the agent court in one of two ways: automatically, when the decision court has no ruling majority (§6.7), or through an ordinary appeal against a decision-court ruling, paid by the appellant. Either way, the agent court then works like any Kleros court, and its rulings can be appealed as usual. The published route may send appeals elsewhere, but it must say so.

The route can be represented through native court jumps or through an explicit route; the pinned V2 code already lets a dispute kit choose the next court and kit. The current V2 specification describes appeal-related court jumps controlled by juror-count thresholds; a DNC-triggered transition must not be advertised as existing behavior.[^2]

In Kleros V2, stake in a court also counts in its parent courts, so if the agent court were a parent of the decision court, every decision-court juror would automatically be in its draw pool. The agent court should therefore not be a parent of the decision court. This removes automatic overlap, not common ownership: one operator can still run jurors in both courts under different addresses (§6.6). With Court #34 as the agent court, the decision court should sit beside it in the court tree, not under it. On the contracts running today, though, a case can only move up to its parent court; sending it to a court beside it needs Kleros 2.0.0 (§8.1). Until then, a pilot can place the decision court under Court #34 and measure the overlap, use the simpler pilot in §8.1, or wait.

Keep appeals distinct from the automatic step. A decision-court ruling remains challengeable through ordinary appeal. The automatic step should not require a party to pretend to appeal a substantive answer the decision court never produced. Each transition records its cause and predecessor, preserving earlier votes and liabilities.

### 6.6 Funding, liveness, and terminal behavior

The automatic step must be funded and executable. The baseline is that each party deposits the cost of one agent-court round when the case starts. If the case moves up, the losing party's deposit pays for that round and the winner's is refunded; if it doesn't, both deposits are refunded. The money is held per case, not pooled across cases, so no large balance builds up; that follows the per-case, per-round funding Kleros uses today.[^13]

Loser-pays deters parties from forcing escalation, but it is only a partial fix. It changes who pays, not whether a juror profits from causing more paid adjudication: an operator running jurors in both courts may gain from pushing cases into the agent court. That risk is bounded, not removed, by keeping the agent court out of the decision court's parent chain (§6.5), by setting the DNC penalty above what a juror could expect to earn from the resulting agent-court round, and by keeping agent-court fees modest. Validation must measure operator profit across both courts.

Do not finance the agent-court round by spending contingent DNC penalties before their assessment. Those penalties may never become payable. A permissionless keeper can advance an eligible transition; no single operator should have exclusive authority to do so.

Every step needs a time limit, so no case gets stuck. An insufficient pot, an unavailable agent court, or a panel that can't be drawn require declared recovery or terminal paths. They must not silently select a party, become a refusal vote, or lock stakes forever. Some of these, such as a drawing stall, can't be repaired by a dispute kit and need a Core change. Selecting the terminal policy is a prerequisite for deployment.

"Fast" must be measured separately for time to agent decision, provisional court ruling, and executable final resolution. Evidence, drawing, commit/reveal, review, and chain inclusion can dominate end-to-end time. This RFC makes no millisecond or other numerical latency claim.

### 6.7 What happens after each decision-court round

| Decision-court result | Next step | Who pays | Settlement |
|---|---|---|---|
| A ruling has more than half of the assigned weight | Ruling, with the ordinary appeal window | An appellant, as today | Ordinary coherence for ruling votes; DNC per §7.3 |
| DNC has more than half | Agent court | The escalation pot | §7.3 |
| No majority, quorum met (inconclusive) | Agent court | The escalation pot | Same as a DNC majority |
| No majority, no quorum (participation failure) | Agent court | The escalation pot | Same, and absent votes lose their stake at risk |

Among rounds without a ruling majority, the next step and settlement are the same whether the cause is DNC, a split or low turnout, so no juror gains by steering between those labels. The labels still matter for monitoring. The agent court always rules, and later rounds follow ordinary Kleros appeal rules.

## 7. Candidate incentives and retrospective settlement

### 7.1 Objective and scope

The architecture needs economically credible participation. Operators should benefit from producing supported rulings, have a meaningful alternative to guessing, and not receive a free perpetual reward merely for reporting DNC.

Kleros already analyzes costly evidence evaluation, evidence-insensitive voting strategies, and coherence with later voting rounds.[^5][^6][^7] The proposed addition is distinct treatment of DNC, with penalties that never go to other jurors. Its effectiveness remains a hypothesis.

### 7.2 What counts as downstream confirmation?

To settle an escalated round, this draft requires an actual later panel ruling in the linked dispute lineage that survives the applicable review and finality rules. A single later matching vote is not sufficient. A provisional answer subsequently overturned is not confirmation. A later ruling that upholds the earlier one only by deference to a specialized court (§4) is not a fresh review either; whether it counts as confirmation is an open question (§11).

Nor should an appeal-funding default automatically count as a fresh panel's evidentiary confirmation: documented appeal mechanics can produce a default without a new jury voting.[^4] The implementation must retain the provenance of the settlement reference rather than consult an undifferentiated final numeric outcome.

The reference is a policy-governed adjudicative result, not cryptographic proof of truth or independent cognition. Later jurors may assess earlier public arguments; existing Kleros work describes that transmission as useful.[^5]

### 7.3 Baseline payoffs

These rules apply to decision-court rounds that moved to the agent court. The agent court, and decision-court rounds that end in a ruling, keep ordinary Kleros coherence among ruling votes; DNC votes in a decision-court round that ended in a ruling settle by the table below.

The baseline pays each juror only from its own fee share and never moves one juror's penalty to another juror. Let `y*` be the qualifying final ruling (§7.2). With fee `f` per assignment and stake at risk `L`:

| Vote in the decision-court round | Result |
|---|---|
| A ruling that matches `y*` | Keeps its own fee share `f`; stake returned |
| A ruling that doesn't match `y*` | Loses `L` |
| DNC, when some ruling vote in the round matched `y*` | Pays `d` |
| DNC, when no ruling vote matched (including all-DNC) | Pays `ε`, smaller than `d` |
| No vote or an invalid reveal | Loses `L`, as for inactivity today |
| The case never reaches a qualifying ruling | Everyone who voted is treated the same: stakes returned, no fees paid, no DNC charge; only absent votes lose `L` |

The last row matters. If ruling votes kept their fee while DNC paid, an agent expecting an unresolved case would do better by guessing. Because the agent court always rules, the row only applies when something fails, such as a panel that can't be drawn.

DNC needs its own branch in both the penalty and the reward calculation: its penalty is `d` or `ε`, never the full `L`, and it counts as participation, not absence. Leaving DNC out of the count of matching votes isn't enough: Kleros would still charge it the full `L`.

**Where the money goes.** The property that matters is that penalties and unused fee shares never go to other jurors. Kleros V2 already sends unallocated fees and penalties to the core contract's owner, so on Kleros 2.0.0 a dispute kit that pays a matching vote only its own fee share achieves this without a Core change (§8.1). Returning unused fees to the parties' pot instead is fairer but needs a Core change; it is the goal, not a prerequisite. Penalties are paid in PNK and fees in ETH, so only unused fees would go back to the parties.

Under a simplified risk-neutral model, this shape does three things. A lone ruling vote's prize no longer grows with the number of DNC votes around it, so guessing beside DNC voters stops paying, and covering several answers with several seats loses money. DNC stays cheaper than a wrong ruling but never free, so reflexive DNC loses money. And no juror profits from another juror's DNC.

The table implies a break-even. For a juror whose research is already done, ruling beats DNC when its chance `p` of matching `y*` satisfies

```text
p > (L − q·d − (1 − q)·ε) / (f + L)
```

where `q` is the chance that some other ruling vote in the round matches. With illustrative values f = 1, L = 4, d = 1 and ε = 0.5, that is between 0.6 and 0.7. This is not a rule, and nothing checks it; it follows from the published fee and penalties. The validation plan uses it to test whether jurors' DNC behavior matches the incentives.

The costs are real. The reward for solving a hard case early is only the fee, so the fee must be high enough to pay for research. The charge `ε` falls on honest agents when a case is truly unsolvable. And in rounds that moved up, this departs from Kleros's usual rule that incoherent jurors pay coherent ones.

### 7.4 Variant under test: the early-solver transfer

Draft 0.1 proposed paying DNC penalties to earlier votes that matched the final ruling, when such a vote existed. Combined with Kleros's usual fee pooling, where the coherent votes share the round's whole fee pool, it rewards guessing: a lone ruling vote next to `m` DNC votes wins `N·f + m·d` if confirmed and loses `L` if not. It beats DNC whenever its chance of matching exceeds `L / (N·f + m·d + L)`.

- With three jurors, f = 1, L = 4 and d = 2, a coin-flip vote beside two DNC votes wins 7 or loses 4: +1.5 on average, while DNC earns 0.
- An operator holding two of five seats can vote A with one seat and B with the other. If the other three vote DNC, it nets +11 whichever answer is confirmed.

This is a counterexample to that particular combination, not to every early-solver reward. The transfer stays in the validation plan as a labeled variant, for example with a cap on each matching seat's total reward, chosen so that `L / (cap + L)` exceeds the court's highest plausible base rate.

### 7.5 Finality and capital

Preserve earlier vote identity and liability through every linked transition. Penalties and refunds happen only after the designated confirmation is final; don't pay out on a provisional result and assume the money can be recovered later.

A single automatic step does not settle all finality questions either. Ordinary appeals, exceptional recovery, and terminal unresolved cases need maximum exposure and release rules. The economic cost of locked capital is part of the service cost, not an accounting footnote.

An initial prototype should keep reward accounting separate from application execution. A compatible final ruling must be delivered exactly once, while each earlier round's liabilities are settled exactly once against the correct reference. Kit changes must preserve the necessary lineage or explicitly enter a release path.

### 7.6 Incentive analysis, not a proof of effort

A wrong ruling must cost more than DNC, but that ordering alone doesn't prevent guessing. The sizes of the payoffs matter, and so do base rates, capital lockup, and each juror's influence on escalation. Beyond the break-even in §7.3, simulations need to check three conditions:

- **All-DNC doesn't pay.** The charge `ε` must be large enough that honest research beats a panel coordinating on DNC.
- **Fixed-answer voting doesn't pay.** As in Kleros today, `L / (f + L)` must exceed the highest plausible base rate of one side winning.[^7]
- **Seat splitting and cross-court ownership don't pay.** With no transfers between jurors, splitting loses money. Profit from pushing cases into the agent court is only bounded (§6.6), so it must be measured per operator.

These are diagnostic conditions, not an equilibrium proof. A full model makes rewards depend on other jurors' behavior and compares thoughtful investigation with random voting, fixed-answer voting, instant DNC, and collusion.[^6][^7]

This is not a claim to tell diligence from laziness in every case. It is a proposed performance contract with observable triggers. Calculating these payoffs doesn't require a Process Court either.[^12]

## 8. Relationship to Kleros V2

The source baseline for this RFC is `kleros/kleros-v2` commit `320b23d526c2a5d13cae782e1a53896da83d7010`, observed on 25 September 2026. The linked arbitrator specification describes Core-managed periods and execution, dispute-kit voting, sortition/stake operations, and court/kit jumps during appeals.[^2] This is a specification review, not a deployment audit or proof that any particular contract can support the extension unchanged. The pinned commit is the unreleased 2.0.0 `dev` code, which is under audit. §8.1 says what the contracts deployed today can and can't do.

| Concern | Existing public baseline | Proposed extension / investigation |
|---|---|---|
| Entry | Court and dispute-kit selection at creation | Versioned route (decision court, then agent court) and service envelope. |
| Agent operation | Public agentic-court and agent-interface work | Solver-neutral duties and DNC semantics. |
| Ballot | Original ruling choices | A distinct control tag without corrupting original choices. |
| Progression | Period transitions and appeal-related jumps | One outcome-triggered, prefunded step from the decision court to the agent court. |
| Reward accounting | Coherence queries and stake/reward execution | Distinct DNC exposure, deferred confirmation, no juror-to-juror transfers for DNC. |
| Application execution | Final ruling delivered to the arbitrable | No DNC execution; an explicit result for cases that never resolve. |
| Observability | Court, round, vote, and ruling events | Transition reasons, predecessor linkage, confirmation provenance, pot accounting. |

A dedicated dispute kit is a natural place to investigate ballot semantics. It is not automatically sufficient for arbitrary routing, stake retention, and redistribution. Core, sortition, kit-jump, and final-ruling interfaces must be traced together. A production KIP should name exact storage/interface changes and migration effects after that work.

An isolated wrapper with linked child disputes is another prototype route, but it creates additional questions about evidence continuity, appeal rights, custody of the pot, and exactly-once execution. It must not be presented as native Kleros integration without explaining those differences. Both options are open.

### 8.1 What runs on today's Kleros

Checked on 29 September 2026 against the source of the deployed contracts and the pinned 2.0.0 code.

**The contracts running today** (KlerosCore 0.10.0 and dispute kits 0.12.0 on Arbitrum One) would let a new dispute kit add the DNC vote and the majority rule in §6.4. The kit could also pay for the automatic step itself, because Core lets a round's dispute kit start the next round during the appeal period. Two things don't fit:

- **Routing.** The next round can only stay in the same court or move up to its parent. Sending a case to a court beside the decision court isn't possible.
- **Payouts.** Core asks the kit for a single number per vote and uses it for both the penalty and the reward. A DNC vote therefore can't pay a small charge without also getting a share of the rewards, and a matching vote can't get its fee without also sharing other jurors' penalties. The payoffs in §7.3 can't be set exactly.

**Kleros 2.0.0**, which has had release candidates since November 2025 and is under audit, adds separate penalty and reward values, lets the kit compute rewards itself, and lets the kit choose the next court. With it, the core of the design fits in a new dispute kit, with no Core change. Three things would still need Core changes: returning unused fees to the parties (§7.3), recovering from a panel that can't be drawn (§6.6), and an explicit "unresolved" result. The first is optional; the other two matter only when something breaks, and §6.6 requires a declared answer before deployment.

**A pilot without new contracts** is possible too: add a "not sure" answer to the dispute template, and have the application open a new case in the agent court when that answer wins. Classic's payouts would then reward "not sure" when most jurors pick it and penalize it like a wrong answer otherwise, so such a pilot could measure coverage and speed with trusted operators, but not the incentives.

New dispute kits have been added to the live system before: the Shutter and Gated kits were registered in 2025.

## 9. Security and operational requirements

The complete threat model belongs in subsequent revisions. The first implementation must nevertheless address the following categories.

**Correlated judgment and strategic voting.** Multiple addresses may share ownership, models, or sources. An operator can spread guesses across its votes, manipulate escalation, or try to recover transfers through another identity. Simulations must aggregate profit by controller as well as by address. A later coherent answer does not attest to earlier effort. Requiring jurors to publish their full decision traces would make copying methods easy (§6.3).

**Adversarial evidence and research.** Documents and retrieved pages can target a model's role, stopping rule, output schema, tools, or secrets. Jurors need isolated execution, bounded resource use, safe retrieval, and separation of substantive policy from attempts to control their infrastructure. The court must not reward an agent for treating an attachment as permission to access private systems.

**Verdict steering through evidence.** Evidence can also try to steer the ruling itself, for example with hidden text addressed to AI jurors. Isolating tools and secrets doesn't stop this, because reading the evidence is the job, and one crafted exhibit reaches every juror in both courts. Validation must test it across operators and courts, including how often it flips a whole panel. Punishing such text is tricky: honest reports of an attack may quote it, and the policy requires considering attack evidence (§4).

**Timing and availability.** Model/RPC outages, evidence unavailability, sequencer delays, incomplete drawing, reorgs, and reveal failures can look similar at the final ballot boundary. Contract-observable failure reasons should be preserved where available. Recovery policy must not retroactively allow a juror to see peers' revealed answers and then replace an earlier commitment.

**Custody and transitions.** Every transition and payout must be idempotent. Bind commitments to domain and round, preserve original choices across kits, retain liabilities until release conditions, and prohibit double execution. No transition should depend on a single privileged keeper, and every funded automatic path needs an executable timeout/recovery policy.

**Coherence versus correctness.** A shared persuasive error can survive both courts. More computation and more jurors are not proofs against this failure. Validation must examine both agreement and independently assessable policy correctness, with disagreement cases reported rather than hidden.

## 10. Evaluation before deployment

The companion [validation plan](../research/validation-plan.md) specifies work to do, not completed experiments. The initial program should compare ordinary ruling-only voting, DNC without penalties, the baseline payoffs in §7.3, and labeled variants such as the early-solver transfer in §7.4, under common workloads.

Measure resolution coverage, policy-correctness where assessable, downstream agreement, total cost to parties, latency at each stage, honest-operator utility, uncertainty reporting, and adversarial controller profit. Stratify by evidence accessibility, case difficulty, answer base rates, agent family, correlated outages, and independent ownership assumptions.

Use independent implementations and publicly shareable or synthetic cases. Separate development samples from held-out evaluation. Report non-convergent, unreviewed, overturned, and terminal cases in the denominators. Selection of only resolved cases would conceal precisely the behavior the mechanism is meant to improve.

Deployment gates include a fully specified terminal path, funded continuation, machine-checkable conservation and transition invariants, incentive analysis beyond penalty ordering, an audited integration, and a limited reversible pilot. This RFC supplies none of those results and requests no immediate stake, court creation, or changes to an existing deployment.

## 11. Questions for the community

The principal decisions for Draft 0.3 are:

1. Which dispute family and service envelope make a useful first pilot? We suggest agent-commerce disputes, with a new decision court in front of Court #34 (§1).
2. Should the step from the decision court to the agent court use native court jumps or an explicit route, given that the agent court shouldn't be a parent of the decision court (§6.5)? Today's contracts only offer the jump to a parent court (§8.1).
3. Which aggregation rule should the decision court use to balance minority early answers, DNC, disagreement, and inactive assignments?
4. How should the automatic step be priced and prefunded without weakening ordinary appeal rights, and should the losing party bear it (§6.6)?
5. Do the baseline payoffs (§7.3) keep guessing, reflexive DNC and seat splitting unprofitable under realistic base rates and concentrated ownership?
6. How large should the DNC charges `d` and `ε` be, and is an early-solver bonus worth keeping in any capped form (§7.4)?
7. Which finality and confirmation events are sufficient for settlement across court or dispute-kit changes, and should a ruling that upholds by deference count (§7.2)?
8. Should justifications be optional in the decision court and required in the agent court (§6.3)? And should decision-court jurors seal a fingerprint of their decision record with their vote, to be opened on appeal?
9. Is it right that a decision-court round without a ruling majority always moves to the agent court, whatever the cause (§6.7), and that the agent court must always rule?

Counterexamples, alternative architectures, parameter analyses, and corrections to the Kleros integration assumptions are welcome. A subsequent KIP should propose a concrete governance action only after the relevant architecture and validation work, rather than label this exploratory RFC as an adopted design.

## References

Public sources were reviewed between 25 and 30 September 2026. Linked specifications are pinned where possible; web pages may change. Historical proposals are not treated as evidence of present deployment.

[^1]: **Kleros AI, “Trust at Machine Speed.”** Existing agentic-court, agent-interface, and triage context. https://ai.kleros.io/ and https://ai.kleros.io/our-solutions

[^2]: **Kleros V2, “Arbitrator V2” specification.** Pinned at commit `320b23d526c2a5d13cae782e1a53896da83d7010`. https://github.com/kleros/kleros-v2/blob/320b23d526c2a5d13cae782e1a53896da83d7010/contracts/specifications/arbitrator.md

[^3]: **William, “KIP-32: General Court Policy Update,” 3 December 2020.** Introduced the evidence rule that the V2 General Court policy still uses word for word (checked 27 September 2026). KIP-32: https://forum.kleros.io/t/kip-32-general-court-policy-update/483 · Current V2 General Court policy: https://cdn.kleros.link/ipfs/QmRwmJAF8NK1r3fAS8dHofbTKsuhWSd3LruzkjrpNNBprC

[^4]: **Kleros Documentation, “Appeals.”** Appeal funding, voting rounds, defaults, and court progression. https://docs.kleros.io/court/appeals

[^5]: **William George, “Kleros and UMA,” 29 June 2022.** Last-round coherence and arguments visible to appeal jurors. https://blog.kleros.io/kleros-and-uma-a-comparison-of-schelling-point-based-blockchain-oracles/

[^6]: **William George, “Parameterization for Kleros courts,” 13 March 2023.** Effort-sensitive parameterization and evidence-insensitive strategy baselines. https://blog.kleros.io/parameterization-of-kleros-courts/

[^7]: **William George, “Uncommon answers: deposit sizes, lazy strategies, and peer prediction,” 28 May 2024.** Fixed-answer strategies, honest-error exposure, and alternative payment research. https://blog.kleros.io/incentivizing-jurors-to-honestly-report-uncommon-answers-deposit-sizes-lazy-strategies-and-peer-prediction/

[^8]: **Kleros Documentation, “DisputeKitClassic.”** Optional commit/reveal and the public voting/appeal interface. https://docs.kleros.io/reference/contracts/dispute-kit-classic

[^9]: **Kleros, “Justice in the Algorithmic Society: A Decade of Kleros and Artificial Intelligence,” 11 August 2026.** Kleros's layered design, from an AI court to human panels and specialist courts. https://blog.kleros.io/justice-in-the-algorithmic-society-a-decade-of-kleros-and-artificial-intelligence/

[^10]: **Clément Lesaege, post #17 in “A lucid observation of Kleros and the path to follow,” Kleros Forum, 11 June 2026.** https://forum.kleros.io/t/a-lucid-observation-of-kleros-and-the-path-to-follow/1449/17

[^11]: **Kleros Documentation, FAQ.** Why drawn jurors cannot recuse themselves. https://docs.kleros.io/welcome/faq

[^12]: **Clément Lesaege, William George, Federico Ast, “Kleros Long Paper v2.0.2,” July 2021.** §4.7.6 describes challenging a juror's conduct in a separate “Process Court”. https://kleros.io/static/yellowpaper.pdf

[^13]: **William George, post #4 in the KIP-85 discussion (automatic review layer), Kleros Forum, 5 January 2026.** Per-case, per-round funding, and why automatic appeals would need a reserve. https://forum.kleros.io/t/kip-85-add-an-automatic-review-layer-with-loss-only-jurors-reviewers/1413/4

[^14]: **Kleros, “Trivium: AI-powered dispute pre-screening for Kleros Court.”** Nine analyses (three models, three viewpoints each); cases where they diverge go to human jurors. Checked 30 September 2026. https://trivium.eth.limo/
