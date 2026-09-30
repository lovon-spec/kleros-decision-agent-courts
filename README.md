# Decision-Agent Courts for Kleros V2

**Discussion draft 0.2 · 30 September 2026**

A proposal for Kleros courts whose jurors are AI systems ("decision agents") run by different operators. The goal is to settle straightforward disputes quickly and cheaply, and to pass the rest on to more thorough courts.

Kleros already runs a court for AI jurors: Court #34, the Agentic Commerce Court, whose rulings can be appealed to human jurors ([ai.kleros.io](https://ai.kleros.io/)). This proposal builds on it: Court #34 would be the agent court, with a new fast court in front of it.

**New to Kleros?** Jurors stake PNK tokens to be randomly drawn onto panels. Those who vote with the final ruling share the fees and the stake lost by those who don't. Either side can pay for an appeal, which adds jurors or moves the case to a higher court. AI jurors would join the same way.

**[Read the full proposal (RFC-0001) →](rfcs/0001-decision-agent-courts.md)**

## The proposal in brief

**1. The court defines the job, not the bot.** Apps opt in to a court whose terms are published up front: what case materials jurors get, which answers they can give, the deadlines, and the fees. Operators bring their own systems, open source or proprietary. These can range from a fast decision model to an agent that does open-ended research, as long as they work within the court's evidence rules and deadlines. Nobody has to run a shared bot or reveal how theirs works. Operators compete, and the payouts reward the systems that get it right.

**2. In the first court, jurors can say "I couldn't decide."** Cases start in a *decision court* of fast AI models. Besides the usual ruling options, a juror there can vote **Did Not Converge** (DNC): it couldn't reach a well-supported ruling before the deadline. That's different from voting "refuse to arbitrate", which is a ruling that the case itself shouldn't be decided, and from not voting at all. DNC gives these jurors an honest alternative to guessing, though it isn't meant to be a free pass.

**3. Unsettled cases move to the agent court, based on the votes alone.** If more than half the decision court backs one ruling, that's the result, and the losing side can appeal as usual. Otherwise, whether most jurors voted DNC, the votes split, or too few voted, the case moves automatically to the *agent court* (Court #34 is the natural choice), where research agents get more time under the same evidence rules. Agent-court jurors must always rule, like any Kleros juror, and their rulings can be appealed as usual, all the way to human jurors. The move is paid from a pot both parties fund when the case starts, and charged to the party that loses in the end.

**4. "I couldn't decide" is cheap; guessing isn't.** Say the decision court votes **B, DNC, DNC**. The case moves up, the agent court rules **B**, and that ruling becomes final. The early B voter keeps its fee. The two DNC voters each pay a small penalty, smaller than the penalty for voting against the final ruling, and it never goes to another juror, so nobody profits from someone else's DNC. If the whole panel had voted DNC, each would pay an even smaller charge.

These payoffs are a baseline to test, not a finished design. An earlier draft paid the DNC penalties to the early B voter instead, but under Kleros's usual fee rules that rewards guessing, so it's now only a variant under test. Vote thresholds, penalty sizes, how the move is funded, and other key design choices are still open too.

## What's in this repo

| Document | What it covers |
|---|---|
| [RFC-0001](rfcs/0001-decision-agent-courts.md) | The full proposal: how the court works, how votes are counted, escalation, payouts, security risks, and open questions. |
| [Validation plan](research/validation-plan.md) | How to test the idea before any real use: simulations, attack scenarios, what to measure, and checkpoints before launch. None of it has been run yet. |
| [Forum post draft](community/forum-post.md) | A shorter introduction written for the Kleros Forum. It hasn't been posted yet. |
| [Contributing](CONTRIBUTING.md) | How to give feedback, and what to keep out of it. |
| [Changelog](CHANGELOG.md) | Version history. |

## Where things stand

- This is an independent proposal for discussion. Kleros hasn't adopted it, and it isn't a KIP (Kleros Improvement Proposal).
- None of this proposal has been built, simulated, benchmarked, or audited yet.
- Publishing it doesn't create a court, change anything Kleros runs today, or ask anyone for funding or stake.
- Most of it would fit in a new dispute kit on Kleros 2.0.0, which is under audit. The contracts running today can't route cases or set payouts the way it needs ([RFC §8.1](rfcs/0001-decision-agent-courts.md#81-what-runs-on-todays-kleros)).

## Join the discussion

Found a flaw, have a better design, or think we've got something about Kleros wrong? [Open an issue](https://github.com/lovon-spec/kleros-decision-agent-courts/issues/new/choose) using the short template. Please name the RFC section, and say whether you've demonstrated the problem or only suspect it.

We'd especially like input on:

- what kind of dispute would make a good first pilot (we suggest agent-commerce disputes, with Court #34 as the agent court);
- how to count votes when a panel mixes rulings, DNC votes, and no-shows;
- how to pay for automatic escalation up front without weakening normal appeals;
- whether the payoffs keep guessing and automatic DNC unprofitable, including when one operator runs many jurors;
- whether justifications should be optional in the fast court and required in the agent court;
- how a first pilot could run on the contracts deployed today.

More open questions are in [section 11 of the RFC](rfcs/0001-decision-agent-courts.md#11-questions-for-the-community).

We plan to hold the wider discussion in the [Proposal category of the Kleros Forum](https://forum.kleros.io/c/proposal/15). A formal governance proposal would only come after a specific implementation and its testing requirements are worked out.

## License

The documents in this repository are licensed under [CC BY 4.0](LICENSE).
