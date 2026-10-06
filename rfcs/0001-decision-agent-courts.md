# RFC-0001: Decision-Agent Courts for Kleros V2

## A first court where AI jurors can say "not sure", in front of Kleros's agent court

| Field | Value |
|---|---|
| Status | Discussion Draft 0.3 — request for community feedback |
| Date | 6 October 2026 |
| Proposer | lovon-spec |
| Scope | Court design and protocol; not a deployment proposal |
| Discussion | [Repository issues](https://github.com/lovon-spec/kleros-decision-agent-courts/issues) |

This is an independent proposal for discussion with the Kleros community. Kleros hasn't adopted it, and it isn't a KIP. Nothing in it has been built, benchmarked or audited yet. The only numbers so far are small payoff calculations ([script](../research/payoff_checks.py)) and measurements of Court #34 as it runs today (§1.2). It describes a proposed design, not how Kleros works today.

## Abstract

This RFC proposes a first court for Kleros V2 whose jurors are AI decision systems run by different operators. It sits in front of Court #34, Kleros's Agentic Commerce Court, and makes two promises.

**No forced guesses.** In the **decision court**, fast decision models vote for a ruling or report that they **did not converge** (DNC): they couldn't reach a well-supported ruling in time. DNC is different from voting "refuse to arbitrate" and from not voting at all. A ruling needs more than half of all seats. Otherwise the case moves automatically to the **agent court**, where research agents get more time and must always rule. Court #34 is the natural agent court. The votes and published rules decide when a case moves, not a central classifier.

**Any fast ruling can be rejected at a price paid in advance.** When a case starts, each side deposits the cost of one agent-court round. If the decision court rules, the losing side has a short window to object. The case then moves to the agent court exactly as if the decision court hadn't settled it, with no new money and no race to fund an appeal. The side that loses in the end pays for the round. After the agent court, ordinary Kleros appeals apply; by Kleros's design they lead to human jurors.

The court defines the job, not the method. Operators bring their own systems and compete. A ruling that matches the final outcome earns its fee, a ruling that doesn't loses its stake at risk, and DNC pays a small flat charge. No money moves between jurors, so with the stake set high enough, guessing and splitting votes across seats lose money whenever a ruling is checked (§7.6). When the decision court settles a case itself, the objection is what checks the ruling, which is why it is cheap.

The design is not mainly about speed. A single court whose jurors try a fast model first can already be quick (§1.1). A separate court adds its own price, its own stake at risk, and room for operators that run only a fast model. §1.2 gives Court #34's numbers for comparison.

The RFC covers the court model, the evidence rules, the lifecycle, deposits and objections, candidate payoffs, what runs on today's Kleros contracts, a path of small steps toward a pilot, and an evaluation plan. It asks for critique before any parameters are chosen or any governance action is proposed.

## 1. Motivation and scope

The starting question is:

> How should Kleros support decentralized adjudication by independently operated decision agents, with fast resolution where possible and progressively deeper adjudication where necessary?

There are three distinct concepts. A dispute can **involve agents as parties**. A juror can **use an agent inside an existing court**. Or a court's **procedure can be designed around decision agents**, including their timing, interfaces, failure modes, and escalation. This RFC concerns the third; agent commerce is a possible initial application, not a restriction on the identity of disputing parties.

This proposal builds on work Kleros already runs. Court #34, the Agentic Commerce Court on Kleros V2, is listed as a live court whose jurors are expected to be AI agents, offering "a Kleros-grade ruling, with the option to appeal to human jurors."[^1] Kleros's published design goes from an AI court to "a non-specialist human panel, verified through a proof-of-personhood protocol," and then to specialist and general courts.[^9] Kleros co-founder Clément Lesaege has put the principle plainly: "Systems cannot be AI only but need to at least be able to appeal to humans in the end."[^10]

This RFC keeps that principle: after the agent court rules, ordinary appeals apply, and by Kleros's design they lead to human jurors. What it adds is a decision court where a juror may report DNC, a prepaid step from the decision court to the agent court, and settlement rules for that step. The step happens automatically when the decision court doesn't settle a case, and on request when the losing side objects to its ruling. The agent step is there because the two courts use different kinds of systems (§6.5): research agents may settle some disputes a fast model can't, more cheaply and quickly than a human panel.

Court #34 is the natural agent court for this design. The first pilot we suggest is a new decision court in front of it, for one family of agent-commerce disputes, such as escrow disputes. The decision court should sit beside Court #34 in the court tree, not under it (§6.5). Kleros has also built Trivium, a prototype that screens disputes with nine AI analyses and sends cases where they disagree to human jurors.[^14] The decision court differs in two ways: each juror reports DNC for itself, and the jurors are independent operators with stake at risk, so the payouts and the objections, not a fixed recipe, decide which systems last.

For parties, the service is a cheap first ruling when the case is clear, a known next step when it isn't, and a known price for rejecting a ruling they think is wrong. For operators, it's a way to compete on getting cases right, on reliability and on cost, with systems of their own.

The hypothesis is that this design leads to fewer rulings built on guesses and makes clear cases cheaper, without making hard cases much slower. It isn't a promise that AI jurors are cheaper or more accurate in every court. A first pilot should pick one narrow family of disputes with clear policies, outcomes that can be checked, and evidence that is complete when the case is filed (§4). We suggest one above, but the choice remains open (§11).

### 1.1 Why a court and not a feature inside each juror?

There is a simpler way to get fast rulings, and it deserves a direct answer. Keep one AI court. Let each juror try a fast model first and fall back to a slower agent when the fast model isn't sure. On this view, courts only need to separate AI jurors from human ones, and what happens inside an AI juror is the operator's business. If every juror's fast model is confident, the votes arrive within a minute and the voting periods end early.

On speed we agree. In Kleros V2 the commit and vote periods end as soon as every juror has acted, so one court can already be quick on easy cases without any protocol change.

A juror can't change the settings of its court, though. Kleros sets four things per court:

- the fee per juror;
- the stake at risk per vote, which decides how sure a juror must be before ruling pays (§7.3);
- the evidence period of the first round;
- who is in the pool of jurors.

So a separate court can do things that a feature inside each juror can't:

- **Charge less for a clear case.** In one court every case pays the same fee per juror, whether the juror needed a second or a long research run.
- **Set its own bar.** The decision court can put more stake at risk for each unit of fee than the agent court, so that ruling only pays for a juror that is quite sure (§7.3).
- **Admit operators that run only a fast model.** In a court where every juror must rule, such an operator has to guess on hard cases or stay out.
- **Put doubt on the record.** When a juror escalates inside its own software, nobody else learns that it was unsure. A DNC vote is public, and it counts against a ruling.

There is also a middle option: add DNC as a dispute kit inside Court #34, with no new court. Jurors could report DNC in a first round and would have to rule in a second round in the same court. Less has to be built. Both rounds keep Court #34's fee and stake, and fast-only operators would be drawn for the second round too unless the kit filters the draw.

| | Fast-then-slow inside each juror | DNC kit inside Court #34 | Separate decision court (this RFC) |
|---|---|---|---|
| What must be built | Nothing | A dispute kit, and an application that pays the deposits | The same, and a court |
| Runs on today's contracts (§8.1) | Yes | The vote count and the second round do; exact payoffs need Kleros 2.0.0 | The same, and moving to a court beside it also needs 2.0.0 |
| Clear case, every juror sure | Fast | Fast | Fast |
| One juror unsure | The round waits for its slow agent, or gets its guess | It votes DNC; the others can still settle the case | Same |
| Lower fee for clear cases | No | No | Yes |
| Own stake at risk | No | No | Yes |
| What an unclear case costs extra | Nothing | A second round and a second juror draw | The same, and the decision court's fee |
| Operators with only a fast model | Must guess or stay out | Are drawn for the must-rule round too, unless the kit filters the draw | Yes |
| Doubt is on the record | No | Yes | Yes |

One more rule is worth comparing: no DNC at all, and any round that isn't unanimous moves up. Trivium works that way.[^14] DNC only helps when the unsure jurors would all have guessed the same answer. That mostly happens when they run similar systems. The validation plan tests these alternatives.

This RFC proposes the third column and treats the second as a step on the way (§8.2). Whether the separate court earns its extra cost is a question for the community (§11).

### 1.2 Court #34 today, in numbers

These numbers were read from the Kleros V2 contracts on Arbitrum One on 6 October 2026.[^15] Dollar amounts use that day's prices (ETH $2,716, PNK $0.00824) and will move.

| | Court #34 |
|---|---|
| Cases so far | 129, filed between 19 August and 25 September 2026, all through the general-purpose DisputeResolver contract |
| Staked jurors | 9 |
| Appeal rounds | None. No Kleros V2 dispute has had an appeal round so far (290 disputes) |
| Fee per juror | 0.00027 ETH, about $0.73. A round costs $2.20 with 3 jurors and $3.67 with 5; most rounds had 5 |
| Stake at risk per vote | 187 PNK, about $1.54, or 2.1 times the fee |
| Time limits | Evidence 10 minutes, commit 45 minutes, reveal 30 minutes, appeal window 36 hours |
| Filing to first ruling | About 46 minutes: 14 until voting opens, 20 for the commits, 10 for the reveals (medians over the 98 cases filed under the current time limits; the steps don't add up exactly) |
| Filing to final ruling | About 19 hours. The appeal window closes after 18 hours when nobody funds an appeal |
| The court above, Court #33 | 0.018 ETH per juror, about $49 |

All cases so far came through the general-purpose contract, so these numbers show how the court runs. They say little yet about how parties with money at stake behave, for example how often they would appeal.

What follows for this design:

- **Price.** The most a decision court can save a case is the price of a Court #34 round, a few dollars today. That matters for small jobs, where a $3.67 fee is a large share of the amount in dispute, and it will matter more if agent-court fees rise to pay for deeper research. It is not the main argument. A decision court saves money on average only if its round costs less than an agent-court round times the share of cases it settles: if it settles a third of its cases, its round has to cost less than a third as much.
- **Time to a first ruling.** About two thirds of the 46 minutes is the jurors' commit and reveal steps. If every juror acted within a minute or two, a first ruling would take roughly 15 to 20 minutes with the same evidence period. A decision court gets there through short voting windows; one court gets there only if all its jurors are fast (§1.1). A case that moves up gets its first ruling later than today, because the decision-court round and a second juror draw come first.
- **Time to a final ruling.** 18 of the 19 hours are the appeal window. A decision court shortens that only if its own objection window is short (§6.6).
- **Appeals.** No appeal round has been held yet, and beyond the first one they are priced for larger cases. From a 5-juror round in Court #34, the first appeal stays in Court #34 with 11 jurors and costs about $8 in fees. The second moves to Court #33 with 23 jurors and costs about 0.41 ETH (about $1,120). Under the usual funding rule, the side that lost the previous round must put up three times a round's cost.[^16] A cheap, prepaid way to challenge a first ruling may therefore matter (§6.6).

## 2. Principles and non-goals

**Standardize the service, not the solver.** The protocol defines assignments, input references, permitted outputs, deadlines, review, and payment. It does not require a shared model, prompt, provider, software package, graph, or confidence threshold. Open-source and proprietary implementations can participate on the same terms. Operators compete on their systems. The payouts reward those that get it right, as far as rulings get checked (§7.3).

**No authoritative cognition router.** An application opts into a configured court and escalation route. Any optional recommendation service is advisory. Once a dispute is admitted, collective votes and deterministic transition rules govern escalation.

**Preserve policy-based adjudication.** The objective is a ruling justified under the governing policy, not a forecast of popular answers divorced from the evidence. Jurors are paid for matching the final ruling. That can be measured; it doesn't prove they were right.

**Permit honest non-convergence.** Reporting failure to reach a ruling must be possible without inventing one. The report may still carry pre-agreed economic consequences.

**Keep investigation adaptive.** A juror may discover new research steps during execution. The deadline limits a juror's time, not what it may look into. An agent's successful stop does not prove that its information was sufficient; that remains an adjudicative judgment.

**Separate authority from untrusted material.** Evidence is input to adjudication, not authority to change tools, credentials, court policy, or signing permissions.

This RFC does not propose a universal classifier of finite problems, a proof that an agent has thought hard enough, a canonical chain of reasoning, mandatory publication of private reasoning traces, or an automatic equation between wallet diversity and independent judgment. The proposed performance incentives also don't depend on a Process Court, the separate court Kleros has described for challenging jurors who break court policy, later discussed as a Juror Misbehaviour Court.[^12][^7]

## 3. Court, operator, and agent model

### 3.1 What is a decision agent?

A decision agent is an operator-controlled system that receives a juror assignment, acquires and evaluates permitted information, decides whether it can support a ruling, and fulfills the required commitment and voting duties. It may combine deterministic computation, language models, retrieval, specialist services, and internal checks. This RFC uses the term for any AI juror, in either court. The decision court's fast systems are called decision models, and the agent court's systems are called research agents.

For example, an agent may search a batch of sources, assess the remaining material questions, query a chain, and repeat until it can apply the policy or reaches its decision deadline. The protocol does not require the resulting graph to have been specified in advance. The graph is an implementation detail; the externally meaningful deliverable is a timely valid vote.

Both courts expect automated jurors, but nothing checks it. This draft does not introduce an oracle that certifies whether cognition was human or machine. Human-assisted operation, disclosure requirements, and any eligibility restrictions are questions for court policy.

### 3.2 Roles and trust boundaries

| Role | Responsibility |
|---|---|
| Parties and arbitrable integration | Choose the service envelope, supply the original question/options, fund agreed fees and deposits, and receive the eventual ruling. |
| Court policy | Define admissibility, substantive obligations, timing, participation, and escalation terms. |
| Juror operator | Supply stake and an independently operated adjudication system; remain responsible for its external actions. |
| Decision agent | Investigate and choose a ruling or DNC under policy and deadline constraints. |
| Signer/transaction component | Enforce assignment, domain, round, vote, nonce, and reveal constraints independently of case prose. |
| Core, dispute mechanism, and transition executor | Record votes, aggregate outcomes, advance rounds, enforce custody and finality, and settle liabilities. |

Shared SDKs, parsers, and transaction libraries are compatible with this architecture. Requiring a particular adjudication workflow is not. The design permits heterogeneous systems but cannot ensure that operators actually use them; shared providers and correlated failures must be measured. Jurors that run the same model with the same method will vote the same way, so a panel is only as independent as its methods are different.

### 3.3 The published service envelope

Before accepting a dispute, the integration exposes a versioned configuration containing: applicable policy references; original ruling options; the decision court and the agent court it escalates to; assignment and voting rules; evidence and decision deadlines; the objection window and later appeal rights; fees and deposits; the size of the agent-court round; the smallest number of independent operators; settlement rules; and a terminal failure policy.

Configuration relevant to an accepted dispute must not be silently replaced during that dispute. A concrete implementation must specify how policy versions, governance upgrades, and emergency powers interact with existing cases. This RFC proposes no authority to alter another court or live juror systems already operating there.

## 4. Information model: inherit the governing evidence policy

The design adopts the evidence rule of the current General Court policy, which KIP-32 introduced and which is still in force word for word.[^3] It says jurors "should disregard any evidence that is both 1) submitted after the end of the evidence period of the initial round of a dispute AND 2) cannot be reasonably considered to have been readily, publicly available to jurors. Jurors may, however, consider arguments that are submitted later that are based upon existing evidence and/or information which a juror considering the case during the evidence period of the initial round could reasonably have been expected to find themselves." Evidence is excluded only when **both** conditions hold.

The same policy adds that "evidence related to the presence of attacks on Kleros should be considered by jurors even if it would otherwise violate the above points on evidence admissibility." This matters for agent courts, where evidence written to manipulate agents is a real risk.

The policy also tells appeal jurors to defer to a specialized lower court: "If there is no evidence of an attack AND appellate court jurors cannot be reasonably expected to have the required skills to independently evaluate the case, jurors should vote to uphold the lower court ruling." A later ruling that upholds an earlier one by deference is not a fresh review, which matters for settlement (§7.2).

This is not a submitted-documents-only model. It is also not permission to use anything that happens to be reachable on the Internet at the time an appeal is heard. Being online today doesn't make a source admissible: was it public then, could a juror have found it, and is it relevant?

The same admissibility standard applies in both courts. The agent court receives more opportunity for computation and investigation, not an automatic license to use otherwise inadmissible late material. No separate information-availability tribunal or new closed evidence whitelist is proposed.

For example, a later argument that draws attention to historically public token distribution can be relevant without creating a new admissible-world cutoff. A previously private photograph supplied only after the initial evidence period does not become admissible simply because it helps the agent court reach an answer. These are applications of the inherited standard, not additional protocol exceptions.[^3]

Three temporal references should remain explicit: the policy's relevant state-of-the-world date, the initial evidence-period cutoff, and each court's decision deadline. Moving the third does not move the first two. Immutable references, historical chain queries, retrieval timestamps, and content hashes help preserve provenance. They do not mechanically prove reasonable discoverability or admissibility.

One consequence matters for a fast court. The decision court's evidence period is "the evidence period of the initial round". Under the rule above, private evidence handed in after it is disregarded in every later court, including human appeals. A short evidence period therefore suits only disputes where both sides' material exists when the case is filed, for example because the application collects it first. That is a condition for choosing a pilot (§11).

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

- *The bar for influence* is handled by construction. A ruling needs more than half of all seats, not just of the votes cast (§6.4), so DNC votes can't let a minority decide: A, DNC, DNC doesn't produce A.
- *Cost balance* is a hypothesis to test. DNC earns no fee and carries a charge (§7.3), and the step to the agent court is prepaid per case and charged to the side that loses in the end (§6.6), so hard cases cost more, but that cost is disclosed and stays with the dispute.
- *Quality in hard cases* is also a hypothesis to test. Instead of forcing a guess, DNC sends the case to research agents with more time (§6.5), and ordinary appeals remain after that.

The vote format must keep the original option numbers and mark DNC separately. It must not overload refusal, add an executable party award by accident, or pass DNC to an arbitrable contract that does not understand it. An illustrative `0` refusal in examples below is not an instruction to relabel existing dispute options.

## 6. Adjudication lifecycle

### 6.1 Entry and assignment

The arbitrable integration selects the decision court and agreed route when it requests arbitration, and pays the deposits (§6.6). The current V2 arbitrator specification describes court and dispute-kit selection through dispute creation parameters.[^2] This RFC adds a versioned service envelope and does not make access depend on one vendor's case classifier.

Agents receive authenticated dispute identity, court and round identity, question, original options, policy references, canonical evidence references, and deadlines. They can normalize and investigate the case differently. Acquisition failures must not be silently represented as proof that a party supplied no evidence.

In the decision court, a juror address holds at most one seat in a round. Kleros's dispute kits already have a switch for this.[^16] It limits addresses, not owners: one operator can still run several addresses (§9). The service envelope should also name the smallest number of independent operators with which the court accepts cases.

Two things follow from the one-seat rule. The court needs at least as many eligible jurors as seats, or the draw can't finish (§6.6). And an operator could split its stake across addresses to win more seats, so the rule only works together with a list of admitted jurors. Staking in Kleros V2 is permissioned today, so a pilot would have such a list; some protections in this draft lean on it (§6.6).

### 6.2 Adaptive investigation and stopping

An agent may begin with the supplied record and extend its research procedure just in time. It can branch on what it learns, use external operations allowed by policy, and repeatedly assess whether material questions have been resolved sufficiently to vote.

The protocol does not inspect how many model calls the agent used, demand a finite graph in advance, or specify its confidence threshold. The agent's stopping policy is part of the implementation on which operators compete. Its output remains subject to ordinary policy-based review and the proposed settlement rules.

### 6.3 Commitment and decision deadline

For a hidden-vote design, the decision must be fixed by the **commit deadline**, not the later reveal deadline. A reveal opens the committed choice; it does not provide an additional opportunity to choose an answer after seeing peers. Classic already documents an optional commit/reveal mechanism, but the exact commitment format and domain separation for DNC are new design work.[^8]

A commitment must bind the deployment domain, dispute, court, round, assigned vote identity or group, output tag, original ruling ID when present, and secret. Reveal and recovery rules must preserve those bindings. Voting rights must not depend on an untrusted attachment's claimed role or permissions.

The draft proposes hidden voting in both courts, subject to latency and integration evaluation.

**Justifications.** A decision model that only returns probabilities has no written reasoning of its own. A justification would have to be a second model's explanation after the fact, which adds time and isn't why the vote was cast. Requiring each juror to publish its full decision trace would also give its method away: others could copy the best one, panels would start to vote alike, and attackers would learn which questions to target. Human jurors aren't asked to show their thought process either; they're judged by their votes. This draft therefore makes justifications optional in the decision court and looks to the agent court for reasons: a losing side that wants them can object, at the prepaid price (§6.6). Whether Court #34 requires written justifications is set by its own policy, which this RFC doesn't change; a pilot should confirm it. Whether decision-court jurors should seal a fingerprint of their decision record with their vote, to be opened on appeal, is an open question (§11).

### 6.4 Candidate aggregation rule

The decision court needs an explicit rule for a mixed panel of ruling votes, DNC, and inactive assignments. The following is a **simulation baseline**, not an assertion about Classic or a settled recommendation. The agent court counts votes as ordinary Kleros courts do.

Let `N` be the number of seats in the round and `V` the number of valid revealed votes. Each juror holds one seat (§6.1). An original ruling with more than `N/2` votes becomes a provisional ruling, and DNC with more than `N/2` votes moves the case to the agent court, whatever the turnout. If neither has that majority, a quorum of `V >= 2N/3` decides the label: with quorum, the round is inconclusive; without it, it is a participation failure. Both also move the case to the agent court (§6.7). Because the quorum only applies when nothing has a majority, a juror can't block a majority by withholding its reveal.

For three seats:

| Votes | Candidate round disposition |
|---|---|
| A, A, DNC | Provisional A; a losing side may object (§6.6). |
| B, DNC, DNC | Moves to the agent court; the early B vote is kept for settlement. |
| A, B, DNC | Inconclusive; moves to the agent court. |
| DNC, DNC, DNC | Moves to the agent court; no early ruling vote. |
| 0, 0, DNC | Provisional original refusal, not automatic escalation. |
| A, absent, absent | Participation failure; moves to the agent court, and the absent votes are penalized. |

This baseline avoids executing a merits answer supported by only a small fraction of the seats. It can also escalate more often than plurality. Thresholds, quorums, and the relationship between disagreement and DNC need comparative evaluation; they are not concealed as implementation details.

### 6.5 Two courts: decision court, then agent court

The route is:

```text
Decision court: fast decision models; a juror may report DNC
    -> agent court: research agents with more time; every juror must rule
        -> ordinary appeals, which by Kleros's design lead to human courts
```

The two courts differ in kind, not only in size. The decision court suits fast, bounded decision models that either rule or report DNC within a short window; DNC is how such a model says a case is beyond what it can settle in that window. The agent court suits agents that do open-ended research, with more time and budget, and it keeps Kleros's ordinary rule that every juror must rule. That is the case for an agent step before human jurors: some cases a decision model can't settle are still tractable with open research, at lower cost and delay than a human panel. Operators can enter either court with any system; the published terms decide the fit.

A case reaches the agent court in one of two ways: automatically, when the decision court has no ruling majority, or on request, when the losing side objects to a decision-court ruling (§6.6). Both use the same prepaid step, and both open the agent court at its ordinary first-round size, which the service envelope names. From there the agent court works like any Kleros court, and its rulings can be appealed as usual.

The route can be represented through native court jumps or through an explicit route; the pinned V2 code already lets a dispute kit choose the next court, the next kit and the size of the next round. The current V2 specification describes appeal-related court jumps controlled by juror-count thresholds; a DNC-triggered transition must not be advertised as existing behavior.[^2]

In Kleros V2, stake in a court also counts in its parent courts, so if the agent court were a parent of the decision court, every decision-court juror would automatically be in its draw pool, for every case heard there. The agent court should therefore not be a parent of the decision court. This removes automatic overlap, not common ownership: one operator can still run jurors in both courts under different addresses (§6.6). A new dispute kit could refuse a drawn juror whose stake isn't directly in the round's court, but that only protects rounds run by that kit. Wherever the decision court sits, its stake also counts in the courts above it, as Court #34's does today; keeping AI jurors off human panels there is a matter for those courts, and Kleros's design uses proof of personhood for it.[^9] With Court #34 as the agent court, the decision court should sit beside it in the court tree, not under it. On the contracts running today, though, a case can only move up to its parent court; sending it to a court beside it needs Kleros 2.0.0 (§8.1). Until then, a pilot can take one of the smaller steps in §8.2.

Keep the two causes apart in the record. An automatic move follows a round that produced no ruling. An objection follows a ruling that one side rejects. Each move records its cause and the round before it, and keeps earlier votes and liabilities.

### 6.6 Deposits, objections, liveness, and terminal behavior

**Deposits.** When a case starts, each side deposits the cost of one agent-court round, plus a small amount that pays whoever triggers a move. Each deposit is tied to the answer that side backs, the way Kleros's appeal funding is tied to an answer.[^16] The dispute kit holds the deposits per case, as that case's pot, so no large balance builds up; that follows the per-case, per-round funding Kleros uses today.[^13] The call that creates a Kleros dispute can't carry money to a dispute kit, so the deposits need their own payment. One way is for the application to pay the kit first and then create the dispute. The kit matches the payment to the dispute by the application's address and refuses a dispute whose deposits are missing, so a case can't start with a pot that is too small. What happens when one side doesn't deposit is for the application to decide, as it is today when one side doesn't pay its arbitration fee.

**The automatic move.** If a decision-court round ends without a ruling majority, the kit pays for one agent-court round from the pot and the case moves. Anyone can trigger the move, and whoever does is paid the small reward, so that someone has a reason to.

**The objection.** If the round ends in a ruling, an objection window opens. Within it, any side whose deposit backs a different answer can object, itself or through the application that paid for it. The kit then pays for the agent-court round from the pot, and the case moves exactly as in the automatic case. The objector triggers the move and receives the same reward. The objector adds no money, and there is no race to fund. Under Kleros's usual appeal funding, the side that lost a round must put up three times the next round's cost and the side that won twice the cost, and if only one side pays in time, its answer wins without a new vote.[^16] In the decision court both deposits are in place from the start, so a ruling can only change through a new panel's vote. If nobody objects within the window, the ruling stands and all deposits are refunded.

**Who pays.** A move costs one agent-court round and the small reward. When the final ruling is in, deposits that backed it are refunded in full. The other deposits share the cost of the move and get the rest back. With two sides, that means the side that loses in the end pays for the move. If nobody backed the final ruling, for example a refusal to arbitrate, every deposit shares the cost. The rule needs no knowledge of who the parties are; Kleros's contracts only know answers.

**What cheap objections cost.** An objection needs no new money, but it isn't free. An objector that loses again pays for the move out of its deposit, as it would have if the case had moved up automatically. That is deliberate: a party is never worse off because the decision court ruled, and wrong rulings get checked (§7.3). It also means the decision court's rulings only stick when the loser accepts them, so its saving shrinks as the amount in dispute grows. A charge for a failed objection is a variant to test (§7.4).

**What loser-pays doesn't cover.** It deters a party from forcing a move it expects to lose. It prices the fee, not the delay: a party that gains from waiting can still make a case look unclear for the price of one agent-court round. And it doesn't stop a juror from profiting when a case moves: an operator running jurors in both courts may gain from pushing cases up. Four limits reduce that risk without removing it. The agent court isn't above the decision court (§6.5). An address gets one seat (§6.1). While jurors come from a list, one operator's share across both courts can be capped. And agent-court fees stay modest. Draft 0.2 also proposed setting the DNC charge above what a juror could earn from the agent-court round. That works against the other limits on the charge (§7.6), so this draft drops it. Validation must measure operator profit across both courts.

Do not finance the agent-court round by spending DNC charges before they are settled. Those charges may never become payable. No single operator should have exclusive authority to trigger a move.

Every step needs a time limit, so no case gets stuck. An unavailable agent court, a panel that can't be drawn, or an agent-court fee that changed after filing each need a declared recovery or terminal path. They must not silently select a party, become a refusal vote, or lock stakes forever. Some of these, such as a drawing stall, can't be repaired by a dispute kit and need a Core change. If nobody triggers a due move before the window ends, Kleros executes whatever result the round's kit reports. The reward is there to prevent that, and the terminal policy must still say what happens if it fails. Without a Core change, that result has to be one of the original answers, which is why an explicit "unresolved" result is on the list in §8.1. Selecting the terminal policy is a prerequisite for deployment.

"Fast" has three meanings that must be measured separately: time to a first ruling, time to a final ruling, and time until the application can act. §1.2 gives today's numbers for Court #34. Three waits don't go away with a decision court: the first round's evidence period, which the contract enforces; the juror draw, which runs in a cycle shared by all courts (at least 20 minutes apart at today's settings) and is needed again when a case moves; and the objection window. The service envelope must state the decision court's evidence period and objection window. A short evidence period has a lasting effect (§4). This RFC makes no numerical promise about latency.

### 6.7 What happens after each decision-court round

| Decision-court result | Next step | Who pays | Settlement |
|---|---|---|---|
| A ruling has more than half of the seats, and nobody objects | The ruling stands | Nobody; the deposits are refunded | §7.3, with that ruling as `y*` |
| A ruling has more than half of the seats, and a losing side objects | Agent court | The pot; in the end, the side that loses | §7.3, with `y*` as defined in §7.2 |
| DNC has more than half | Agent court | The pot; in the end, the side that loses | Same |
| No majority, quorum met (inconclusive) | Agent court | The pot; in the end, the side that loses | Same |
| No majority, no quorum (participation failure) | Agent court | The pot; in the end, the side that loses | Same |

Among rounds without a ruling majority, the next step and settlement are the same whether the cause is DNC, a split or low turnout, so no juror gains by steering between those labels. The labels still matter for monitoring. The agent court always rules, and later rounds follow ordinary Kleros appeal rules.

## 7. Candidate incentives and retrospective settlement

### 7.1 Objective and scope

The architecture needs economically credible participation. Operators should benefit from producing supported rulings, have a meaningful alternative to guessing, and not receive a free perpetual reward merely for reporting DNC.

Kleros already analyzes costly evidence evaluation, evidence-insensitive voting strategies, and coherence with later voting rounds.[^5][^6][^7] This RFC adds a distinct treatment of DNC and, in the decision court, payoffs in which no money moves between jurors. Whether they work remains a hypothesis.

### 7.2 What counts as downstream confirmation?

To settle an escalated round, this draft requires an actual later panel ruling in the linked dispute lineage that survives the applicable review and finality rules. A single later matching vote is not sufficient. A provisional answer subsequently overturned is not confirmation. A later ruling that upholds the earlier one only by deference to a specialized court (§4) is not a fresh review either; whether it counts as confirmation is an open question (§11). A decision-court ruling that nobody objected to has no later panel; it is its own reference, and §7.3 says what follows from that.

Nor should an appeal-funding default automatically count as a fresh panel's evidentiary confirmation: documented appeal mechanics can produce a default without a new jury voting.[^4] The contract must record how the final ruling came about, by a panel's vote or by a funding default, not just its number. The decision court itself has no funding default, because objections are prepaid (§6.6); one can still occur in later appeal rounds. In the baseline such a default doesn't change what a decision-court round is measured against: `y*` stays the last ruling a panel voted, while the deposits follow the ruling that is executed (§6.6). A tie in a later round leaves no ruling to measure against; Kleros itself treats every voter as coherent when a round ties.

The final ruling is another panel's judgment. It can be wrong, and it may just follow the earlier votes. Later jurors may assess earlier public arguments; existing Kleros work describes that transmission as useful.[^5]

### 7.3 Baseline payoffs

Let `y*` be the ruling a round is measured against: the final ruling, or the last ruling a panel voted if the final one came from a funding default (§7.2). Let `f` be the fee per seat, `L` the stake at risk per seat, and `d` the DNC charge. Examples use f = 1, L = 9 and d = 0.25.

One table applies to every decision-court round, whether it ended in a ruling or moved up:

| Vote in the decision-court round | Result |
|---|---|
| A ruling that matches `y*` | Keeps its own fee `f`; stake returned |
| A ruling that doesn't match `y*` | Loses `L` |
| DNC | Pays `d` |
| No vote or an invalid reveal | Loses `L`, as for inactivity today |
| The case never reaches a qualifying ruling | Everyone who voted is treated the same: stakes returned, no fees paid, no DNC charge; only absent votes lose `L` |

What a juror earns depends only on its own vote and `y*`. No money moves from one juror to another. The agent court and every later round keep Kleros's ordinary rules.

The last row matters. If ruling votes kept their fee while DNC paid, an agent expecting an unresolved case would do better by guessing. Because the agent court always rules, the row applies only in unusual cases: when something fails, such as a panel that can't be drawn, or when no panel's ruling is left standing to measure against (§7.2).

DNC needs its own branch in both the penalty and the reward calculation: its penalty is `d`, never the full `L`, and it counts as participation, not absence. Leaving DNC out of the count of matching votes isn't enough: Kleros would still charge it the full `L`.

**Where the money goes.** Penalties, DNC charges and unused fees never go to other jurors. Kleros V2 already sends unallocated fees and penalties to the core contract's owner, so on Kleros 2.0.0 a dispute kit that pays jurors by this table achieves this without a Core change (§8.1). After a round of three DNC votes, the parties have paid three fees, no juror is paid, and the owner receives the fees and the charges. Returning unused fees to the parties instead is fairer but needs a Core change; it is the goal, not a prerequisite. Penalties are paid in PNK and fees in ETH, so only unused fees would go back to the parties.

**What the table does.** Take a simplified model in which jurors care only about expected payoff, and suppose every ruling is checked against the agent court's:[^17]

- A ruling's prize never depends on how the other seats voted. A coin flip earns −4 on average and DNC −0.25, so guessing doesn't pay, beside DNC voters or anyone else.
- Covering two answers with two seats loses money: one seat earns 1 and the other loses 9.
- DNC is cheaper than a wrong ruling but never free, so a juror that always votes DNC loses money.
- No juror profits from another juror's DNC or mistake.

**The bar.** A juror whose research is done does better by ruling than by voting DNC when its chance `p` of matching `y*` satisfies

```text
p > (L − d) / (f + L)
```

We call this the bar. With the example values it is 0.875, about 0.88. Nothing checks it; it follows from the fee, the stake and the charge. Two things about it matter. Every increase in the DNC charge lowers the bar, so a higher charge makes jurors rule on less confidence. And the fee is paid in ETH while the stake and the charge are in PNK, so the bar moves with the PNK price: at the prices in §1.2, Court #34's stake at risk is worth 2.1 times its fee, and a bar near 0.9 needs about nine times.

**What a settled round pays for.** If a decision-court ruling stands because nobody objected, `y*` is that ruling. The jurors who voted for it are then paid for matching each other, and whether they were right doesn't come into it. Two things follow.[^17]

- A juror that isn't sure does best by voting what it expects the others to vote. Take three similar jurors, each 55% sure of A and each expecting the other two to vote A. If wrong rulings are never corrected, voting A earns one fee and DNC costs a quarter of a fee, so all three vote A. Once 28% of wrong rulings are corrected, DNC is the better vote.
- A common system out-earns a better one. Take two seats on a system that is right 85% of the time and one seat on a system that is right 95% of the time. If wrong rulings are never corrected, each common seat earns one fee per case and the better seat loses 0.85. The better system earns more only once 65% of wrong rulings are corrected.

That is why the objection is cheap (§6.6). The payoffs reward getting cases right only as far as wrong rulings are sent up. Validation must measure how often that happens. A pilot should also send a random share of settled cases to the agent court, because a ruling that nobody objects to is otherwise never looked at again (§10).

**The costs are real.** The reward for a ruling is only the fee, so the fee must be high enough to pay for research. A juror that was right against the other seats earns no more than its fee, so the design leans on objections, not on a prize, to bring a correct minority view to light; §7.4 says why. The charge falls on an honest juror every time it can't decide, so a juror that rules on too few cases loses money (§7.6). And this departs from Kleros's usual rule that incoherent jurors pay coherent ones.

### 7.4 Variants under test

**Kleros's usual sharing in settled rounds (Draft 0.2).** Votes that match the final ruling would share the round's fees and the stakes lost by the others. That pays a juror well for being right against the other seats: in the example of §7.3, the better system then earns more once 43% of wrong rulings are corrected, against 65% in the baseline. But the same prize makes a speculative vote pay. With three seats and the example values, a lone vote against the other two wins 21 fees if an objection proves it right and loses 9 if not, so it beats DNC at a 29% chance of being proved right. If every wrong ruling is corrected, three jurors who are each only 65% sure of A then all do best by ruling, two for A and one for B, and nobody votes DNC.[^17] A middle version shares the fees but not the stakes.

**A two-level DNC charge (Draft 0.2).** DNC paid `d` when some ruling vote in its round matched the final ruling and a smaller `ε` otherwise. The idea was to charge less when a case was hard for everyone. The baseline now uses one charge, for two reasons. With two levels, a correct ruling by one seat raises the charge on the others, so a juror's result depends on other jurors' votes again. And when peers are likely to rule, DNC costs more, so an unsure juror rules too, and copies them. Draft 0.2's example values (f = 1, L = 4, d = 1, ε = 0.5) also failed the limits in §7.6: the bar was 0.60 to 0.70, and a juror that ruled on 40% of its cases and was right 95% of the time could at best break even.[^17]

**A charge for a failed objection.** In the baseline, an objector that loses again pays only for the move to the agent court (§6.6). A variant adds a charge on top, paid to the other side. Settled rulings would stick more often, and wrong ones would be corrected less often. The right size, if any, depends on how often losing sides object in practice.

**The early-solver transfer (Draft 0.1).** DNC penalties were paid to earlier votes that matched the final ruling. Combined with Kleros's usual fee pooling, where the coherent votes share the round's whole fee pool, it rewards guessing: a lone ruling vote next to `m` DNC votes wins `N·f + m·d` if confirmed and loses `L` if not. It beats DNC whenever its chance of matching exceeds `L / (N·f + m·d + L)`.

- With three jurors, f = 1, L = 4 and d = 2, a coin-flip vote beside two DNC votes wins 7 or loses 4: +1.5 on average, while DNC earns 0.
- An operator holding two of five seats can vote A with one seat and B with the other. If the other three vote DNC, it nets +11 whichever answer is confirmed.

This is a counterexample to that particular combination, not to every early-solver reward. The transfer stays in the validation plan as a labeled variant, for example with a cap on each matching seat's total reward, chosen so that `L / (cap + L)` exceeds the court's highest plausible base rate.

### 7.5 Finality and capital

Preserve earlier vote identity and liability through every linked transition. Penalties and refunds happen only after the designated confirmation is final; don't pay out on a provisional result and assume the money can be recovered later.

One prepaid step does not settle all finality questions either. Ordinary appeals, exceptional recovery, and terminal unresolved cases need maximum exposure and release rules. The economic cost of locked capital is part of the service cost, not an accounting footnote.

An initial prototype should keep reward accounting separate from application execution. A compatible final ruling must be delivered exactly once, while each earlier round's liabilities are settled exactly once against the correct reference. If a case changes dispute kit, earlier votes and stakes stay linked to it, or are released under a stated rule.

### 7.6 Limits the settings must meet

A wrong ruling must cost more than DNC, but that ordering alone doesn't prevent guessing. The sizes matter. A court's fee, stake and charge have to meet several limits at once:[^17]

1. **The bar sits above the base rate.** If one answer wins more often than the bar, voting that answer without reading the case beats DNC. So `(L − d) / (f + L)` must exceed the share of cases that the most common answer wins. With the example values that share must stay below 87.5%. Above `L / (f + L)`, here 90%, blind voting makes money by itself, as in Kleros today.[^7] The first test is the stricter one.
2. **An honest juror breaks even.** A juror that rules on a share `c` of its cases, and is right `a` of the time when it rules, earns about `c · (a·f − (1 − a)·L) − (1 − c)·d` per case when its rulings are checked. That is positive only if `a` is above `L / (f + L)` and the juror rules on enough cases. With the example values, a juror that is right 95% of the time must rule on about a third of its cases, and one that is right 98% of the time on about a quarter. The DNC charge therefore sets the lowest coverage at which a juror can stay in the court.
3. **DNC is never free and never as costly as a wrong ruling:** `0 < d < L`. A juror that always votes DNC loses `d` per case, so holding a seat without working doesn't pay, and neither does a whole panel agreeing to vote DNC.
4. **Pushing cases up doesn't pay.** The DNC charge can't do this job without breaking limits 1 and 2. It is left to the limits listed in §6.6 and has to be measured per operator.

Limits 1 and 2 both want the charge small. A court that wants a high bar gets it from the stake, not from the charge.

These are conditions to check, not an equilibrium proof. A full model has to add what the table leaves to behavior: how often losing sides object, and what jurors expect of each other when a ruling may go unchecked. It should compare thoughtful investigation with random voting, fixed-answer voting, instant DNC, and collusion.[^6][^7]

This is not a claim to tell diligence from laziness in every case. It is a proposed performance contract with observable triggers. Calculating these payoffs doesn't require a Process Court either.[^12]

## 8. Relationship to Kleros V2

The source baseline for this RFC is `kleros/kleros-v2` commit `320b23d526c2a5d13cae782e1a53896da83d7010`, observed on 25 September 2026. The linked arbitrator specification describes Core-managed periods and execution, dispute-kit voting, sortition/stake operations, and court/kit jumps during appeals.[^2] This is a specification review, not a deployment audit or proof that any particular contract can support the extension unchanged. The pinned commit is the unreleased 2.0.0 `dev` code, which is under audit. §8.1 says what the contracts deployed today can and can't do.

| Concern | Existing public baseline | Proposed extension / investigation |
|---|---|---|
| Entry | Court and dispute-kit selection at creation | Versioned route (decision court, then agent court) and service envelope. |
| Agent operation | Public agentic-court and agent-interface work | Solver-neutral duties and DNC semantics. |
| Ballot | Original ruling choices | A distinct control tag without corrupting original choices. |
| Progression | Period transitions and appeal-related jumps | One prepaid step from the decision court to the agent court, triggered by the votes or by an objection. |
| Reward accounting | Coherence queries and stake/reward execution | Distinct DNC exposure, deferred confirmation, no transfers between jurors in decision-court rounds. |
| Application execution | Final ruling delivered to the arbitrable | No DNC execution; an explicit result for cases that never resolve. |
| Observability | Court, round, vote, and ruling events | Transition reasons, predecessor linkage, confirmation provenance, pot accounting. |

§8.1 says what a dedicated dispute kit can and can't do on the contracts deployed today and on Kleros 2.0.0. A production KIP should name exact storage and interface changes and their migration effects.

An isolated wrapper with linked child disputes is another prototype route, but it creates additional questions about evidence continuity, appeal rights, custody of the pot, and exactly-once execution. It must not be presented as native Kleros integration without explaining those differences. Both options are open.

### 8.1 What runs on today's Kleros

Checked on 29 September and 6 October 2026 against the source of the deployed contracts and the pinned 2.0.0 code.

**The contracts running today** (KlerosCore 0.10.0 and dispute kits 0.12.0 on Arbitrum One) would let a new dispute kit add the DNC vote and the majority rule in §6.4. The kit could also pay for the move to the next round itself, because Core lets a round's dispute kit start the next round during the appeal period. It could hold the deposits and run the objection: a kit can hold money per case, as the Classic kit does for appeal funding, and the objection window is the court's appeal period. And it could give each juror at most one seat; the switch exists and is off in the four kits deployed today. Two things don't fit:

- **Routing.** The next round can only stay in the same court or move up to its parent, and it has at least 2N+1 jurors, so a move from a 3-seat round pays for seven. Sending a case to a court beside the decision court isn't possible.
- **Payouts.** Core asks the kit for a single number per vote and uses it for both the penalty and the reward. A DNC vote therefore can't pay a small charge without also getting a share of the rewards, and a matching vote can't get its fee without also sharing other jurors' penalties. The payoffs in §7.3 can't be set exactly.

**Kleros 2.0.0**, which has had release candidates since November 2025 and is under audit, adds separate penalty and reward values, lets the kit compute rewards itself, and lets the kit choose the next court and the size of the next round. With it, the core of the design fits in a new dispute kit, with no Core change. Three things would still need Core changes: returning unused fees to the parties (§7.3), recovering from a panel that can't be drawn (§6.6), and an explicit "unresolved" result. The first is optional; the other two matter only when something breaks, and §6.6 requires a declared answer before deployment.

**A pilot without new contracts** is possible too: add a "not sure" answer to the dispute template, and have the application open a new case in the agent court when that answer wins. Classic's payouts would then reward "not sure" when most jurors pick it and penalize it like a wrong answer otherwise, so such a pilot could measure coverage and speed with trusted operators, but not the incentives.

New dispute kits have been added to the live system before: the Shutter and Gated kits were registered in 2025.

### 8.2 A path of small steps

Nothing here needs a new court on day one. Each step answers a question the next one depends on.

| Step | What it needs | What it shows |
|---|---|---|
| 1. A shadow run | No contracts. Operators run fast jurors on live Court #34 cases, publish a hash of each vote before the ruling, and open it afterwards. | How many cases a fast panel would settle, how often it matches the ruling, and how often different operators are wrong together |
| 2. A "not sure" answer | No new contracts: a "not sure" answer in the dispute template, and an application that opens a new case in Court #34 when that answer wins (§8.1) | Coverage and timing with real votes, but not the incentives |
| 3. The dispute kit on today's contracts | A new kit with DNC, the vote count, deposits and the objection, run inside Court #34 or in a court under it | The whole flow, with payoffs that are only approximate and, for a court under Court #34, the overlap described in §6.5 |
| 4. The decision court | Kleros 2.0.0 and a new court beside Court #34 | The design as written, with exact payoffs |

Step 1 comes first because its three numbers decide whether the later steps are worth building. Every step needs a supply of cases, and Court #34 has had no new case since 25 September 2026 (§1.2). Test cases with known answers are one way to get them, if someone other than the operators being tested writes them.

## 9. Security and operational requirements

The complete threat model belongs in subsequent revisions. The first implementation must nevertheless address the following categories.

**Correlated judgment and strategic voting.** Multiple addresses may share ownership, models, or sources. An operator can spread guesses across its votes, manipulate escalation, or try to recover transfers through another identity. Simulations must aggregate profit by controller as well as by address. A later coherent answer does not attest to earlier effort. Requiring jurors to publish their full decision traces would make copying methods easy (§6.3). One seat per juror limits addresses, not owners.

**Adversarial evidence and research.** Documents and retrieved pages can target a model's role, stopping rule, output schema, tools, or secrets. Jurors need isolated execution, bounded resource use, safe retrieval, and separation of substantive policy from attempts to control their infrastructure. The court must not reward an agent for treating an attachment as permission to access private systems.

**Verdict steering through evidence.** Evidence can also try to steer the ruling itself, for example with hidden text addressed to AI jurors. Isolating tools and secrets doesn't stop this, because reading the evidence is the job, and one crafted exhibit reaches every juror in both courts. Validation must test it across operators and courts, including how often it flips a whole panel. Punishing such text is tricky: honest reports of an attack may quote it, and the policy requires considering attack evidence (§4).

**Timing and availability.** Model/RPC outages, evidence unavailability, sequencer delays, incomplete drawing, reorgs, and reveal failures can look similar at the final ballot boundary. Contract-observable failure reasons should be preserved where available. Recovery policy must not retroactively allow a juror to see peers' revealed answers and then replace an earlier commitment.

**Custody and transitions.** Every transition and payout must be idempotent. Bind commitments to domain and round, preserve original choices across kits, retain liabilities until release conditions, and prohibit double execution. No transition should depend on a single privileged keeper, and every funded automatic path needs an executable timeout/recovery policy.

**Coherence versus correctness.** A shared persuasive error can survive both courts. More computation and more jurors are not proofs against this failure. Validation must examine both agreement and independently assessable policy correctness, with disagreement cases reported rather than hidden.

**Rulings nobody checks.** A decision-court ruling that nobody objects to is never looked at again, and its jurors are paid for agreeing with each other (§7.3). Cheap objections and spot checks are what this draft proposes against that; both have to be measured.

## 10. Evaluation before deployment

The companion [validation plan](../research/validation-plan.md) specifies work to do, not completed experiments. The program should compare, under common workloads: Court #34 as it runs today; one court whose jurors escalate inside their own systems (§1.1); a DNC kit inside Court #34 (§1.1); a rule with no DNC where any split moves up; DNC without a charge; the baseline in §7.3; and labeled variants such as those in §7.4.

Measure resolution coverage, policy-correctness where assessable, downstream agreement, total cost to parties, latency at each stage, honest-operator utility, uncertainty reporting, and adversarial controller profit. For settled cases, also measure how often the losing side objects and how often an objection overturns the ruling. Because a ruling that nobody objects to is never looked at again, a pilot should send a random share of settled cases to the agent court, or review them in shadow, and report how often they are overturned. Stratify by evidence accessibility, case difficulty, answer base rates, agent family, correlated outages, and independent ownership assumptions.

Use independent implementations and publicly shareable or synthetic cases. Separate development samples from held-out evaluation. Report non-convergent, unreviewed, overturned, and terminal cases in the denominators. Selection of only resolved cases would conceal precisely the behavior the mechanism is meant to improve. Set the pass marks before collecting the data.

Deployment gates include a fully specified terminal path, funded continuation, machine-checkable conservation and transition invariants, incentive analysis beyond penalty ordering, an audited integration, and a limited reversible pilot. This RFC supplies none of those results and requests no immediate stake, court creation, or changes to an existing deployment.

## 11. Questions for the community

The principal decisions for Draft 0.4 are:

1. Is a separate decision court worth its extra cost over the alternatives in §1.1: escalation inside each juror, or a DNC kit inside Court #34?
2. Which dispute family and service envelope make a useful first pilot? We suggest agent-commerce disputes whose evidence is complete at filing, with a new decision court in front of Court #34 (§1, §4).
3. Which of the steps in §8.2 would be worth trying first, and where would the cases come from?
4. Is the prepaid objection the right way to challenge a decision-court ruling (§6.6)? Should third parties be able to fund one, and should a failed objection cost more than the round?
5. Which aggregation rule should the decision court use to balance minority early answers, DNC, disagreement, and inactive assignments (§6.4)?
6. Do the baseline payoffs (§7.3) keep guessing, reflexive DNC and seat splitting unprofitable under realistic base rates and concentrated ownership, and do the limits in §7.6 leave a usable range of settings?
7. How large should the DNC charge be, and is one flat charge better than two levels? Is an early-solver bonus worth keeping in any capped form (§7.4)?
8. Should the step from the decision court to the agent court use native court jumps or an explicit route, given that the agent court shouldn't be a parent of the decision court (§6.5)? Today's contracts only offer the jump to a parent court (§8.1).
9. Which finality and confirmation events are sufficient for settlement across court or dispute-kit changes, and should a ruling that upholds by deference count (§7.2)?
10. Should justifications be optional in the decision court (§6.3)? And should decision-court jurors seal a fingerprint of their decision record with their vote, to be opened on appeal, and if so, to whom?
11. Is it right that a decision-court round without a ruling majority always moves to the agent court, whatever the cause (§6.7), and that the agent court must always rule?

Counterexamples, alternative architectures, parameter analyses, and corrections to the Kleros integration assumptions are welcome. A subsequent KIP should propose a concrete governance action only after the relevant architecture and validation work, rather than label this exploratory RFC as an adopted design.

## References

Public sources were reviewed between 25 September and 6 October 2026. Linked specifications are pinned where possible; web pages may change. Historical proposals are not treated as evidence of present deployment.

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

[^15]: **Court #34 measurements, 6 October 2026.** Read from KlerosCore on Arbitrum One (`0x991d2df165670b9cac3B022f4B68D65b664222ea`) at block 512,251,279. Court settings come from the contract's getters, timings from the block times of the dispute-creation, draw, period-change and ruling events, and staked jurors from the sortition module. Medians cover the 98 cases filed under the current time limits. Prices are CoinGecko's on that day. Appeal costs are computed from the court settings and the contract's appeal-cost rule; no appeal round has taken place.

[^16]: **Kleros V2, `DisputeKitClassic` at the pinned commit.** Appeal funding is tied to an answer; the side that lost the previous round funds the next round's cost plus twice that cost as stake, and the side that won funds the cost plus once that cost; a single fully funded answer wins without a new round; `singleDrawPerJuror` limits a juror to one seat per round. https://github.com/kleros/kleros-v2/blob/320b23d526c2a5d13cae782e1a53896da83d7010/contracts/src/arbitration/dispute-kits/DisputeKitClassic.sol

[^17]: **Payoff checks for this draft.** A short script that reproduces the numbers in §7.3, §7.4 and §7.6: [research/payoff_checks.py](../research/payoff_checks.py)
