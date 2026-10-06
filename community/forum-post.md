# Forum post draft

*For the Proposal category of the Kleros Forum. It hasn't been posted yet.*

**Title:** [Discussion, not a KIP] A first court in front of Court #34, where AI jurors can say "not sure"

---

Kleros already runs Court #34, the Agentic Commerce Court, where the jurors are expected to be AI agents and rulings can be appealed to humans. I'd like feedback on adding a first step in front of it. It makes two promises: a juror there never has to guess, and either side can reject its ruling at a price paid in advance.

**The idea**

1. A new **decision court** holds fast decision models: systems built to quickly pick one of a few answers. Operators bring their own. Each juror gets at most one seat per round.
2. Besides the usual answers, a juror there can vote **"did not converge" (DNC)**: it couldn't reach a well-supported ruling in time. That's different from "refuse to arbitrate" and from not voting.
3. A ruling needs **more than half of all seats**. Otherwise the case moves automatically to **Court #34**, where agents get more time and must always rule. Normal appeals follow from there.
4. The move is **prepaid**. Each side deposits the cost of one Court #34 round at the start, about $2 to $4 at today's prices. If the decision court rules, the loser has a short window to **object**, and the case moves to Court #34 as if the decision court hadn't settled it. Nobody has to find new money or race to fund an appeal. The side that loses in the end pays for the round, and everyone else gets their deposit back.
5. **Payouts:** a ruling that matches the final one earns its fee, a wrong ruling loses its stake, and DNC pays a small flat charge. No money moves between jurors, so with the stake set high enough, guessing and splitting votes across seats lose money whenever a ruling is checked. When the decision court settles a case itself, the cheap objection is what checks it.

**Why a court and not a feature inside each juror**

A juror can already try a fast model first and fall back to a slower agent, and Court #34's voting periods already end once every juror has voted. So this isn't mainly about speed. What a juror can't change are its court's settings: the fee per juror, the stake at risk per vote, the first round's evidence period, and who is in the pool. A separate court can charge less for clear cases, set a higher bar for ruling, admit operators that run only a fast model, and put "not sure" on the record. The RFC also compares a middle option, a "not sure" vote inside Court #34 itself (§1.1).

**Court #34 today, for comparison**

129 cases so far and no appeal rounds. Under the current time limits, a first ruling takes about 46 minutes and a final one about 19 hours, 18 of them the appeal window. A round costs $2.20 with 3 jurors and $3.67 with 5. So the saving per case is small in dollars, and it matters most for small jobs. These numbers were read from the contracts on 6 October 2026 (§1.2).

**What runs today**

Most of the design fits in a new dispute kit on Kleros 2.0.0. On the contracts deployed today, a case can only move up to its parent court, and the payouts can't be set exactly as proposed. The RFC lists smaller steps (§8.2). The first needs no contracts: operators run fast jurors on live Court #34 cases and publish a hash of each vote before the ruling.

**Questions for the people running Court #34**

1. Is a separate court worth it over the simpler options: escalation inside each juror, or a "not sure" vote inside Court #34?
2. Is the prepaid objection a reasonable way to challenge a fast ruling?
3. Which of the small steps would you be willing to try, and where would the cases come from?

Full proposal (RFC-0001, Draft 0.3): https://github.com/lovon-spec/kleros-decision-agent-courts/blob/main/rfcs/0001-decision-agent-courts.md

It's a discussion draft. Nothing has been built or audited, and it doesn't ask for funding or stake. Counterexamples and corrections are very welcome, here or as [GitHub issues](https://github.com/lovon-spec/kleros-decision-agent-courts/issues).
