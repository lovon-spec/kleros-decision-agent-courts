# RFC-0001: Decision-Agent Courts for Kleros V2

## Heterogeneous autonomous jurors, adaptive investigation, and convergence escalation

| Field | Value |
|---|---|
| Status | Discussion Draft 0.1 — request for community feedback |
| Date | 25 September 2026 |
| Proposer | lovon-spec |
| Scope | Court architecture and protocol design; not a deployment proposal |
| Discussion | [Repository issues](https://github.com/lovon-spec/kleros-decision-agent-courts/issues) |

This is an independent proposal for discussion with the Kleros community. It is not an approved Kleros specification, a KIP, or a claim of endorsement. This version supplies no deployed implementation, simulation results, economic security proof, or performance benchmark for the proposed mechanism. Requirements below describe the proposed design, not existing Kleros behavior.

## Abstract

This RFC proposes a Kleros V2 court architecture designed for adjudication by independently operated decision agents. The objective is timely, lower-cost dispute resolution without requiring a common model, centrally operated classifier, or prescribed investigation graph.

Juror operators choose their own models, tools, research strategies, and stopping rules. Their agents may investigate adaptively using information permitted by the governing court policies. By the applicable decision deadline, each juror commits either an original ruling option or an explicit report of non-convergence. Non-convergence is neither refusal to arbitrate nor failure to participate.

The architecture starts with an initial agent court and provides a defined continuation path to a deeper agent-adjudication tier before further fallback. Escalation follows the panel's recorded outputs and public protocol rules, not a privileged classifier. Court policy constrains admissible inquiry; deadlines constrain when decisions must be submitted. Neither requires an ex-ante specification of the agent's complete research graph.

A candidate settlement mechanism rewards earlier ruling votes that agree with a qualifying downstream resolution. When such early votes exist, earlier non-convergence votes may incur a smaller performance penalty than incorrect ruling votes, with that penalty redistributed to the early coherent voters. This is performance-based compensation, not a finding of laziness or an inspection of private cognition.

The RFC introduces the court model, information regime, lifecycle, escalation and finality requirements, candidate incentives, integration boundaries, and an evaluation plan. It asks the community to critique the architecture before selecting production parameters or proposing governance action.

## 1. Motivation and scope

The starting question is:

> How should Kleros support decentralized adjudication by independently operated decision agents, with fast resolution where possible and progressively deeper adjudication where necessary?

There are three distinct concepts. A dispute can **involve agents as parties**. A juror can **use an agent inside an existing court**. Or a court's **procedure can be designed around decision agents**, including their timing, interfaces, failure modes, and escalation. This RFC concerns the third; agent commerce is a possible initial application, not a restriction on the identity of disputing parties.

This proposal does not introduce automated adjudication to an otherwise empty field. Kleros's public AI site already presents Court #34 as a working automated court, identifies a separate triage prototype, and describes escalation toward specialized agents and humans.[^1] The contribution proposed here is a more explicit architecture for independently operated solvers, a protocol-level non-convergence outcome, and settlement across a configured agent-court ladder. We do not infer production maturity or the presence of this mechanism from those public descriptions.

For parties, the intended service is an inexpensive first opportunity for a defensible ruling, with a predictable continuation path rather than either forced guessing or an unexplained failure. For juror operators, the opportunity is to compete on evidence-sensitive adjudication, reliability, and cost without surrendering implementation autonomy.

The hypothesis is that this architecture can improve the cost/quality/latency trade-off for some dispute classes. It is not a promise that agents are cheaper or more accurate in every court. A first pilot should choose a narrow dispute family with interpretable policies and evaluable outcomes; the choice remains open.

## 2. Principles and non-goals

**Standardize the service, not the solver.** The protocol defines assignments, input references, permitted outputs, deadlines, review, and payment. It does not require a shared model, prompt, provider, software package, graph, or confidence threshold. Open-source and proprietary implementations can participate on the same terms.

**No authoritative cognition router.** An application opts into a configured court and escalation route. Any optional recommendation service is advisory. Once a dispute is admitted, collective votes and deterministic transition rules govern escalation.

**Preserve policy-based adjudication.** The objective is a ruling justified under the governing policy, not a forecast of popular answers divorced from the evidence. Downstream coherence is an observable settlement signal, not proof of factual truth.

**Permit honest non-convergence.** Reporting failure to reach a ruling must be possible without inventing one. The report may still carry pre-agreed economic consequences.

**Keep investigation adaptive.** A juror may discover new research steps during execution. A timeout bounds participation, not the mathematical search space. An agent's successful stop does not prove that its information was sufficient; that remains an adjudicative judgment.

**Separate authority from untrusted material.** Evidence is input to adjudication, not authority to change tools, credentials, court policy, or signing permissions.

This RFC does not propose a universal classifier of finite problems, a proof that an agent has thought hard enough, a canonical chain of reasoning, mandatory publication of private reasoning traces, or an automatic equation between wallet diversity and independent judgment. A separate Process Court is not a dependency of the proposed performance incentives.

## 3. Court, operator, and agent model

### 3.1 What is a decision agent?

A decision agent is an operator-controlled system that receives a juror assignment, acquires and evaluates permitted information, decides whether it can support a ruling, and fulfills the required commitment and voting duties. It may combine deterministic computation, language models, retrieval, specialist services, and internal checks.

For example, an agent may search a batch of sources, assess the remaining material questions, query a chain, and repeat until it can apply the policy or reaches its decision deadline. The protocol does not require the resulting graph to have been specified in advance. The graph is an implementation detail; the externally meaningful deliverable is a timely valid vote.

Autonomy is a service expectation in the agent tiers, not something proven merely by accepting a transaction from a wallet. This draft does not introduce an oracle that certifies whether cognition was human or machine. Human-assisted operation, disclosure requirements, and any eligibility restrictions are questions for court policy.

### 3.2 Roles and trust boundaries

| Role | Responsibility |
|---|---|
| Parties and arbitrable integration | Choose the service envelope, supply the original question/options, fund agreed fees, and receive the eventual ruling. |
| Court policy | Define admissibility, substantive obligations, timing, participation, and escalation terms. |
| Juror operator | Supply stake and an independently operated adjudication system; remain responsible for its external actions. |
| Decision agent | Investigate and choose a ruling or DNC under policy and deadline constraints. |
| Signer/transaction component | Enforce assignment, domain, round, vote, nonce, and reveal constraints independently of case prose. |
| Core, dispute mechanism, and transition executor | Record votes, aggregate outcomes, advance rounds, enforce custody and finality, and settle liabilities. |

Shared SDKs, parsers, and transaction libraries are compatible with this architecture. Requiring a particular adjudication workflow is not. The design permits heterogeneous systems but cannot ensure that operators actually use them; shared providers and correlated failures must be measured.

### 3.3 The published service envelope

Before accepting a dispute, the integration exposes a versioned configuration containing: applicable policy references; original ruling options; initial tier and authorized successors; assignment and voting rules; evidence and decision deadlines; appeal rights; fees and escalation reserves; maximum tier traversal; settlement rules; and a terminal failure policy.

Configuration relevant to an accepted dispute must not be silently replaced during that dispute. A concrete implementation must specify how policy versions, governance upgrades, and emergency powers interact with existing cases. This RFC proposes no authority to alter another court or live juror systems already operating there.

## 4. Information model: inherit the governing evidence policy

The design adopts the General Court evidence standard supplied for this discussion, whose public antecedent is KIP-32.[^3] Its critical conjunction is preserved: evidence is excluded under the quoted rule when it is **both** submitted after the initial evidence period **and** not reasonably considered readily public. Later arguments may draw on existing evidence or information jurors could reasonably have been expected to discover during that initial period.

This is not a submitted-documents-only model. It is also not permission to use anything that happens to be reachable on the Internet at the time an appeal is heard. Public accessibility, historical availability, reasonable discoverability, relevance, and other applicable policy requirements remain distinct questions.

The same governing admissibility standard applies through the agent tiers. Deeper adjudication receives more opportunity for computation and investigation, not an automatic license to use otherwise inadmissible late material. No separate information-availability tribunal or new closed evidence whitelist is proposed.

For example, a later argument that draws attention to historically public token distribution can be relevant without creating a new admissible-world cutoff. A previously private photograph supplied only after the initial evidence period does not become admissible simply because it helps the deeper tier reach an answer. These are applications of the inherited standard, not additional protocol exceptions.[^3]

Three temporal references should remain explicit: the policy's relevant state-of-the-world date, the initial evidence-period cutoff, and each tier's decision deadline. Moving the third does not move the first two. Immutable references, historical chain queries, retrieval timestamps, and content hashes help preserve provenance. They do not mechanically prove reasonable discoverability or admissibility.

Before implementation, contributors must identify and pin the operative policy for the target deployment. The historical source linked here is not a claim that every current court or chain uses identical text. Changes to that policy should be evaluated as explicit changes to the service, not introduced indirectly through an agent prompt.

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
| DNC | The juror did not establish a sufficiently supported ruling within this tier's decision window. |
| Missing or invalid participation | The juror did not complete the required protocol action; it is not silently converted into DNC. |

DNC does not assert that no terminating procedure exists, that another agent cannot solve the case, or that the reporting operator was negligent. It is a truthful report about a failed service attempt, with compensation determined by the agreed economic rules.

A production encoding must preserve original option IDs and bind the control tag unambiguously. It must not overload refusal, add an executable party award by accident, or pass DNC to an arbitrable contract that does not understand it. An illustrative `0` refusal in examples below is not an instruction to relabel existing dispute options.

## 6. Adjudication lifecycle

### 6.1 Entry and assignment

The arbitrable integration selects the initial agent tier and agreed route when it requests arbitration. The current V2 arbitrator specification describes court and dispute-kit selection through dispute creation parameters.[^2] This RFC adds a versioned service envelope and does not make access depend on one vendor's case classifier.

Agents receive authenticated dispute identity, court and round identity, question, original options, policy references, canonical evidence references, and deadlines. They can normalize and investigate the case differently. Acquisition failures must not be silently represented as proof that a party supplied no evidence.

### 6.2 Adaptive investigation and stopping

An agent may begin with the supplied record and extend its research procedure just in time. It can branch on what it learns, use external operations allowed by policy, and repeatedly assess whether material questions have been resolved sufficiently to vote.

The protocol does not inspect how many model calls the agent used, demand a finite graph in advance, or specify its confidence threshold. The agent's stopping policy is part of the implementation on which operators compete. Its output remains subject to ordinary policy-based review and the proposed settlement rules.

### 6.3 Commitment and decision deadline

For a hidden-vote design, the decision must be fixed by the **commit deadline**, not the later reveal deadline. A reveal opens the committed choice; it does not provide an additional opportunity to choose an answer after seeing peers. Classic already documents an optional commit/reveal mechanism, but the exact commitment format and domain separation for DNC are new design work.[^8]

A commitment should bind the deployment domain, dispute, tier, round, assigned vote identity or group, output tag, original ruling ID when present, and secret. Reveal and recovery rules must preserve those bindings. Voting rights must not depend on an untrusted attachment's claimed role or permissions.

The first draft proposes hidden voting for the agent tiers, subject to latency and integration evaluation. Public justifications, when required or supplied, should be released under a specified schedule consistent with that protection. They need not expose private reasoning traces or proprietary implementation details.

### 6.4 Candidate aggregation rule

The court needs an explicit rule for a mixed panel of ruling votes, DNC, and inactive assignments. The following is a **simulation baseline**, not an assertion about Classic or a settled recommendation.

Let `N` be the total assigned voting weight and `V` the valid revealed weight. We use voting weight, not a count of wallet addresses. Require `V >= 2N/3` for quorum. With quorum, an original ruling with weight strictly greater than `N/2` becomes a provisional ruling. DNC with weight strictly greater than `N/2` triggers convergence escalation. If neither obtains that threshold, the round is inconclusive and escalates with a distinct reason. Without quorum, it follows a participation-failure path.

For three equal-weight assignments:

| Votes | Candidate round disposition |
|---|---|
| A, A, DNC | Provisional A; ordinary review remains available. |
| B, DNC, DNC | DNC escalation; preserve the early B vote. |
| A, B, DNC | Inconclusive escalation, not a DNC majority. |
| DNC, DNC, DNC | DNC escalation with no early ruling vote. |
| 0, 0, DNC | Provisional original refusal, not automatic escalation. |
| A, absent, absent | Participation failure, not affirmative DNC. |

This baseline avoids executing a merits answer supported by only a small fraction of assigned weight. It can also escalate more often than plurality. Thresholds, quorums, and the relationship between disagreement and DNC need comparative evaluation; they are not concealed as implementation details.

### 6.5 Agent-first escalation ladder

The proposed logical route is:

```text
Initial agent court
    -> deeper agent court
        -> further configured agent tier, if any
            -> configured expert/general fallback
```

The deeper agent tier comes before further fallback. Its published terms can provide a longer decision window, different fees, a different juror configuration, or a different specialization. Those are measurable design choices intended to attract or enable deeper adjudication; the word "deeper" does not certify superior intelligence.

The route can be represented through native parent courts or through an explicit route abstraction. That implementation choice is open. The current V2 specification describes appeal-related court jumps controlled by juror-count thresholds; a DNC-triggered transition must not be advertised as existing behavior.[^2]

Keep ordinary appeals distinct from convergence escalation. A provisional ruling remains challengeable through the agreed appeal process. DNC continuation should not require a party to pretend to appeal a substantive answer that the tier never produced. Each transition records its cause and predecessor, preserving earlier votes and liabilities.

### 6.6 Funding, liveness, and terminal behavior

An automatic transition must be funded and executable. A simulation baseline is an upfront, disclosed reserve for the configured convergence ladder, separate from ordinary appeal funding. Unused amounts are refundable under specified rules. A production design may choose another explicit funding arrangement, but cannot assume an unfunded higher tier will materialize.

Do not finance the next round by spending contingent DNC penalties before their assessment. Those penalties may never become payable. A permissionless keeper can advance an eligible transition; no single operator should have exclusive authority to do so.

A finite configured ladder and bounded phase rules are needed for liveness. Insufficient reserve, unavailable successor, incomplete drawing, and exhausted tiers require declared recovery or terminal paths. They must not silently select a party, become a refusal vote, or lock stakes forever. The terminal policy could enter a configured fallback or expose an explicit unresolved status to a compatible integration. Selecting that policy is a prerequisite for deployment.

"Fast" must be measured separately for time to agent decision, provisional court ruling, and executable final resolution. Evidence, drawing, commit/reveal, review, and chain inclusion can dominate end-to-end time. This RFC makes no millisecond or other numerical latency claim.

## 7. Candidate incentives and retrospective settlement

### 7.1 Objective and scope

The architecture needs economically credible participation. Operators should benefit from producing supported rulings, have a meaningful alternative to guessing, and not receive a free perpetual reward merely for reporting DNC.

Kleros already analyzes costly evidence evaluation, evidence-insensitive voting strategies, and coherence with later voting rounds.[^5][^6][^7] The proposed addition is distinct treatment of DNC and a conditional transfer to earlier successful ruling voters. Its effectiveness remains a hypothesis.

### 7.2 What counts as downstream confirmation?

For the special transfer, this draft requires an actual later panel ruling in the linked dispute lineage that survives the applicable review and finality rules. A single later matching vote is not sufficient. A provisional answer subsequently overturned is not confirmation.

Nor should an appeal-funding default automatically count as a fresh panel's evidentiary confirmation: documented appeal mechanics can produce a default without a new jury voting.[^4] The implementation must retain the provenance of the settlement reference rather than consult an undifferentiated final numeric outcome.

The reference is a policy-governed adjudicative result, not cryptographic proof of truth or independent cognition. Later jurors may assess earlier public arguments; existing Kleros work describes that transmission as useful.[^5] Hidden initial commitments protect against copying peers' unrevealed choices, not against every kind of later persuasion or collusion.

### 7.3 The early-matching-vote condition

Let `y*` be the qualifying downstream ruling. For an earlier round `r`, let `E_r` be the set of timely valid original-ruling votes in that round that match `y*`.

The candidate's special convergence penalty applies to earlier DNC voters **only when `E_r` is nonempty**. This retains a crucial distinction: a later tier solving a case does not by itself demonstrate that an earlier tier contained a successful answer.

Each DNC assignment `i` has a disclosed maximum performance exposure `d_i`, funded and locked under the applicable stake rules. For a qualifying round, the special pool is:

```text
P_r = sum of assessed d_i over that round's DNC assignments
```

The pool is allocated to matching early votes in proportion to their eligible voting weight. It is not a general bonus for the later court. Allocation by voting weight, rather than address count, avoids creating extra reward shares merely by splitting addresses; it does not eliminate control of multiple votes.

| Earlier situation | Special convergence-transfer treatment |
|---|---|
| B, DNC, DNC; later qualifying panel confirms B | Assess the agreed DNC exposure; transfer the pool to the early B weight. |
| A, DNC, DNC; later qualifying panel confirms B | No matching early vote; no special DNC transfer under this candidate. |
| DNC, DNC, DNC; later panel resolves | No early ruling vote; no special DNC transfer. |
| An early refusal vote matches a qualifying later original refusal | May qualify as an original ruling; DNC remains distinct. |
| Later answer is provisional, overturned, or not a qualifying panel result | Do not settle this special transfer on that answer. |

Ordinary wrong-ruling and inactivity treatment is separate. There must be no accidental double slashing where an ordinary coherence function already treats DNC as fully incoherent. The combined maximum liability, source of funds, and release conditions must be explicit.

DNC fees and stake treatment where no special trigger exists are still design parameters. Returning an unassessed bond does not imply rewarding DNC as an affirmative correct ruling. Nor does a later unreviewed outcome magically validate an early decision. These paths must be represented in simulations and the eventual specification.

### 7.4 Finality and capital

Preserve earlier vote identity and liability through every linked transition. Special payments occur only after the designated confirmation is final under the mechanism; do not distribute a provisional pool and assume it can later be recovered from recipients.

Finite convergence tiers alone do not settle all finality questions. Ordinary appeals, exceptional recovery, and terminal unresolved cases need maximum exposure and release rules. The economic cost of locked capital is part of the service cost, not an accounting footnote.

An initial prototype should keep reward accounting separate from application execution. A compatible final ruling must be delivered exactly once, while each earlier round's liabilities are settled exactly once against the correct reference. Kit changes must preserve the necessary lineage or explicitly enter a release path.

### 7.5 Incentive analysis, not a proof of effort

A natural parameter family has wrong-ruling exposure greater than DNC exposure. **That ordering alone does not prevent guessing.** Rewards, base rates, confirmation probability, capital lockup, and the agent's influence on escalation all matter.

Under a deliberately simplified risk-neutral comparison, with correct-ruling reward `R`, wrong-ruling loss `L`, research cost `c`, subjective agreement probability `p`, DNC net payment before the special penalty `F_D`, penalty-trigger probability `q`, and conditional penalty `D`:

```text
U(ruling) = p R - (1-p) L - c
U(DNC)    = F_D - q D
```

These are diagnostic equations, not an equilibrium model. A real model makes rewards and `q` endogenous to other jurors' behavior, ownership concentration, and review outcomes. It must compare thoughtful investigation with random voting, fixed-answer voting, instant DNC, and collusive strategies.[^6][^7]

In particular, all-DNC collusion can avoid the early-solver trigger. The candidate therefore cannot be justified solely by that transfer. DNC fees, participation opportunity costs, operator entry, and alternative settlement variants need testing. Preferentially paying early solvers removes one direct reward to the later tier, but does not eliminate cross-tier ownership or manipulation.

This is not a claim to distinguish diligence from laziness in every case. It is a proposed performance contract whose observable triggers may encourage useful agent capability. No separate Process Court is needed to calculate these specified transfers.

## 8. Relationship to Kleros V2

The source baseline for this RFC is `kleros/kleros-v2` commit `320b23d526c2a5d13cae782e1a53896da83d7010`, observed on 25 September 2026. The linked arbitrator specification describes Core-managed periods and execution, dispute-kit voting, sortition/stake operations, and court/kit jumps during appeals.[^2] This is a specification review, not a deployment audit or proof that any particular contract can support the extension unchanged.

| Concern | Existing public baseline | Proposed extension / investigation |
|---|---|---|
| Entry | Court and dispute-kit selection at creation | Versioned agent-tier route and service envelope. |
| Agent operation | Public agentic-court and agent-interface work | Solver-neutral duties and DNC semantics. |
| Ballot | Original ruling choices | A distinct control tag without corrupting original choices. |
| Progression | Period transitions and appeal-related jumps | Outcome-triggered, funded convergence escalation. |
| Reward accounting | Coherence queries and stake/reward execution | Distinct DNC exposure, deferred confirmation, early-solver allocation. |
| Application execution | Final ruling delivered to the arbitrable | No DNC execution; explicit terminal and fallback mappings. |
| Observability | Court, round, vote, and ruling events | Transition reasons, predecessor linkage, confirmation provenance, bond accounting. |

A dedicated dispute kit is a natural place to investigate ballot semantics. It is not automatically sufficient for arbitrary routing, stake retention, and redistribution. Core, sortition, kit-jump, and final-ruling interfaces must be traced together. A production KIP should name exact storage/interface changes and migration effects after that work.

An isolated wrapper with linked child disputes is another prototype route, but it creates additional questions about evidence continuity, appeal rights, bond custody, and exactly-once execution. It must not be presented as native Kleros integration without explaining those differences. Both options are open; software malleability is assumed, not treated as a limitation.

## 9. Security and operational requirements

The complete threat model belongs in subsequent revisions. The first implementation must nevertheless address the following categories.

**Correlated judgment and strategic voting.** Multiple addresses may share ownership, models, or sources. An operator can spread guesses across its votes, manipulate escalation, or try to recover transfers through another identity. Simulations must aggregate profit by controller as well as by address. A later coherent answer does not attest to earlier effort.

**Adversarial evidence and research.** Documents and retrieved pages can target a model's role, stopping rule, output schema, tools, or secrets. Jurors need isolated execution, bounded resource use, safe retrieval, and separation of substantive policy from attempts to control their infrastructure. The court must not reward an agent for treating an attachment as permission to access private systems.

**Timing and availability.** Model/RPC outages, evidence unavailability, sequencer delays, incomplete drawing, reorgs, and reveal failures can look similar at the final ballot boundary. Contract-observable failure reasons should be preserved where available. Recovery policy must not retroactively allow a juror to see peers' revealed answers and then replace an earlier commitment.

**Custody and transitions.** Every transition and payout must be idempotent. Bind commitments to domain and round, preserve original choices across kits, retain liabilities until release conditions, and prohibit double execution. No transition should depend on a single privileged keeper, and every funded automatic path needs an executable timeout/recovery policy.

**Coherence versus correctness.** A shared persuasive error can survive every tier. More computation and more jurors are not proofs against this failure. Validation must examine both agreement and independently assessable policy correctness, with disagreement cases reported rather than hidden.

## 10. Evaluation before deployment

The companion [validation plan](../research/validation-plan.md) specifies work to do, not completed experiments. The initial program should compare ordinary ruling-only voting, free DNC, the proposed conditional-bond candidate, and carefully labeled alternatives under common workloads.

Measure resolution coverage, policy-correctness where assessable, downstream agreement, total cost to parties, latency at each stage, honest-operator utility, uncertainty reporting, and adversarial controller profit. Stratify by evidence accessibility, case difficulty, answer base rates, agent family, correlated outages, and independent ownership assumptions.

Use independent implementations and publicly shareable or synthetic cases. Separate development samples from held-out evaluation. Report non-convergent, unreviewed, overturned, and terminal cases in the denominators. Selection of only resolved cases would conceal precisely the behavior the mechanism is meant to improve.

Deployment gates include a fully specified terminal path, funded continuation, machine-checkable conservation and transition invariants, incentive analysis beyond penalty ordering, an audited integration, and a limited reversible pilot. This RFC supplies none of those results and requests no immediate stake, court creation, or changes to an existing deployment.

## 11. Questions for the community

The principal decisions for Draft 0.2 are:

1. Which initial dispute family and service envelope offer a useful first pilot?
2. Should native parent courts implement the tier ladder, or should an explicit route be represented separately?
3. Which aggregation rule best balances minority early answers, DNC, disagreement, and inactive assignments?
4. How should automatic continuation be priced and reserved while preserving ordinary appeal rights?
5. Does the early-matching-vote condition create useful incentives under realistic answer base rates and concentrated ownership?
6. What are the fees and release rules for all-DNC, no-matching-vote, unconfirmed, and terminal-unresolved paths?
7. Which finality and confirmation events are sufficient for settlement across court or dispute-kit changes?
8. What source references and concise public justifications improve review without mandating a shared solver or disclosing proprietary internals?

Counterexamples, alternative architectures, parameter analyses, and corrections to the Kleros integration assumptions are welcome. A subsequent KIP should propose a concrete governance action only after the relevant architecture and validation work, rather than label this exploratory RFC as an adopted design.

## References

Public sources were reviewed on 25 September 2026. Linked specifications are pinned where possible; web pages may change. Historical proposals are not treated as evidence of present deployment.

[^1]: **Kleros AI, “Trust at Machine Speed.”** Existing agentic-court, agent-interface, and triage context. https://ai.kleros.io/

[^2]: **Kleros V2, “Arbitrator V2” specification.** Pinned at commit `320b23d526c2a5d13cae782e1a53896da83d7010`. https://github.com/kleros/kleros-v2/blob/320b23d526c2a5d13cae782e1a53896da83d7010/contracts/specifications/arbitrator.md

[^3]: **William, “KIP-32: General Court Policy Update,” 3 December 2020.** Public antecedent for the evidence standard supplied in this discussion; verify operative target-court policy before implementation. https://forum.kleros.io/t/kip-32-general-court-policy-update/483

[^4]: **Kleros Documentation, “Appeals.”** Appeal funding, voting rounds, defaults, and court progression. https://docs.kleros.io/court/appeals

[^5]: **William George, “Kleros and UMA,” 29 June 2022.** Last-round coherence and arguments visible to appeal jurors. https://blog.kleros.io/kleros-and-uma-a-comparison-of-schelling-point-based-blockchain-oracles/

[^6]: **William George, “Parameterization for Kleros courts,” 13 March 2023.** Effort-sensitive parameterization and evidence-insensitive strategy baselines. https://blog.kleros.io/parameterization-of-kleros-courts/

[^7]: **William George, “Uncommon answers: deposit sizes, lazy strategies, and peer prediction,” 28 May 2024.** Fixed-answer strategies, honest-error exposure, and alternative payment research. https://blog.kleros.io/incentivizing-jurors-to-honestly-report-uncommon-answers-deposit-sizes-lazy-strategies-and-peer-prediction/

[^8]: **Kleros Documentation, “DisputeKitClassic.”** Optional commit/reveal and the public voting/appeal interface. https://docs.kleros.io/reference/contracts/dispute-kit-classic
