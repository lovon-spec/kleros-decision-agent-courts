# Decision-Agent Courts for Kleros V2

**Discussion draft 0.3 · 6 October 2026**

A proposal for a first court in front of Kleros's AI court. Its jurors are AI systems run by different operators, and it makes two promises: a juror there never has to guess, and either side can reject its ruling at a price paid in advance.

Kleros already runs a court for AI jurors: Court #34, the Agentic Commerce Court, whose rulings can be appealed to human jurors ([ai.kleros.io](https://ai.kleros.io/)). This proposal builds on it: Court #34 would be the agent court, with a new first court in front of it.

**New to Kleros?** Jurors stake PNK tokens to be randomly drawn onto panels. Those who vote with the final ruling share the fees and the stake lost by those who don't. Either side can pay for an appeal, which adds jurors or moves the case to a higher court. AI jurors would join the same way.

**[Read the full proposal (RFC-0001) →](rfcs/0001-decision-agent-courts.md)**

## The proposal in brief

**1. The court defines the job, not the bot.** Apps opt in to a court whose terms are published up front: what case materials jurors get, which answers they can give, the deadlines, and the fees. Operators bring their own systems, open source or proprietary. These can range from a fast decision model to an agent that does open-ended research, as long as they work within the court's evidence rules and deadlines. Nobody has to run a shared bot or reveal how theirs works.

**2. In the first court, jurors can say "not sure."** Cases start in a *decision court* of fast AI models. Besides the usual ruling options, a juror there can vote **Did Not Converge** (DNC): it couldn't reach a well-supported ruling before the deadline. That's different from voting "refuse to arbitrate", which is a ruling that the case itself shouldn't be decided, and from not voting at all. Each juror gets at most one seat per round.

**3. Unsettled cases move to the agent court, based on the votes alone.** If more than half of the seats back one ruling, that's the result. Otherwise, whether most jurors voted DNC, the votes split, or too few voted, the case moves automatically to the *agent court* (Court #34 is the natural choice), where research agents get more time under the same evidence rules. Agent-court jurors must always rule, like any Kleros juror, and their rulings can be appealed as usual. By Kleros's design those appeals lead to human jurors.

**4. Either side can reject a fast ruling at a price paid in advance.** When a case starts, each side deposits the cost of one agent-court round, about $2 to $4 at Court #34's prices today. If the decision court rules, the losing side has a short window to object, and the case moves to the agent court as if the decision court hadn't settled it. Nobody has to find new money or race to fund an appeal. The side that loses in the end pays for the round, and everyone else gets their deposit back.

**5. "Not sure" is cheap; a wrong ruling isn't.** Say the decision court votes **B, DNC, DNC**. The case moves up, the agent court rules **B**, and that ruling becomes final. The early B voter keeps its fee. The two DNC voters each pay a small flat charge. No money moves between jurors, so nobody profits from someone else's DNC or mistake. That departs from Kleros's usual sharing, in the first court only. A juror that had voted A would have lost its stake at risk, which is many times the charge.

**Why a court and not a feature inside each juror?** A juror can already try a fast model first and fall back to a slower agent, so this isn't mainly about speed. What a juror can't change are its court's settings: the fee, the stake at risk, the evidence period and who is in the pool. A separate court can charge less for clear cases, set a higher bar for ruling, admit operators that run only a fast model, and put "not sure" on the record. [Section 1.1 of the RFC](rfcs/0001-decision-agent-courts.md#11-why-a-court-and-not-a-feature-inside-each-juror) compares the options.

These rules are a baseline to test, not a finished design. Vote thresholds, the sizes of the charge and the stake, the objection window, and other key choices are still open.

## What's in this repo

| Document | What it covers |
|---|---|
| [RFC-0001](rfcs/0001-decision-agent-courts.md) | The full proposal: how the court works, how votes are counted, deposits and objections, payouts, security risks, and open questions. |
| [Validation plan](research/validation-plan.md) | How to test the idea before any real use: comparisons, attack scenarios, what to measure, and checkpoints before launch. None of it has been run yet. |
| [Payoff checks](research/payoff_checks.py) | A short script that reproduces the payoff numbers quoted in the RFC. |
| [Forum post draft](community/forum-post.md) | A shorter introduction written for the Kleros Forum. It hasn't been posted yet. |
| [Contributing](CONTRIBUTING.md) | How to give feedback, and what to keep out of it. |
| [Changelog](CHANGELOG.md) | Version history. |

## Where things stand

- This is an independent proposal for discussion. Kleros hasn't adopted it, and it isn't a KIP (Kleros Improvement Proposal).
- None of this proposal has been built, benchmarked, or audited. The only numbers so far are small payoff calculations and measurements of Court #34 as it runs today ([RFC §1.2](rfcs/0001-decision-agent-courts.md#12-court-34-today-in-numbers)).
- Publishing it doesn't create a court, change anything Kleros runs today, or ask anyone for funding or stake.
- Most of it would fit in a new dispute kit on Kleros 2.0.0, which is under audit. The contracts running today can't route cases or set payouts the way it needs ([RFC §8.1](rfcs/0001-decision-agent-courts.md#81-what-runs-on-todays-kleros)). Smaller first steps need less, and the first needs no contracts at all ([RFC §8.2](rfcs/0001-decision-agent-courts.md#82-a-path-of-small-steps)).

## Join the discussion

Found a flaw, have a better design, or think we've got something about Kleros wrong? [Open an issue](https://github.com/lovon-spec/kleros-decision-agent-courts/issues/new/choose) using the short template. Please name the RFC section, and say whether you've demonstrated the problem or only suspect it.

We'd especially like input on:

- whether a separate court is worth it over the simpler options: escalation inside each juror, or a "not sure" vote inside Court #34;
- what kind of dispute would make a good first pilot (we suggest agent-commerce disputes, with Court #34 as the agent court);
- whether the prepaid objection is the right way to challenge a fast ruling;
- how to count votes when a panel mixes rulings, DNC votes, and no-shows;
- whether the payoffs keep guessing and automatic DNC unprofitable, including when one operator runs many jurors;
- which small first step would be worth trying, and where the cases would come from.

More open questions are in [section 11 of the RFC](rfcs/0001-decision-agent-courts.md#11-questions-for-the-community).

We plan to hold the wider discussion in the [Proposal category of the Kleros Forum](https://forum.kleros.io/c/proposal/15). A formal governance proposal would only come after a specific implementation and its testing requirements are worked out.

## License

The documents in this repository are licensed under [CC BY 4.0](LICENSE).
