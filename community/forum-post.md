# Forum post draft

*For the Proposal category of the Kleros Forum. It hasn't been posted yet.*

**Title:** [Discussion, not a KIP] A fast first court in front of Court #34, where AI jurors can say "not sure"

---

Kleros already runs Court #34, the Agentic Commerce Court, where the jurors are expected to be AI agents and rulings can be appealed to humans. I'd like feedback on adding a fast first step in front of it.

**The idea**

1. A new **decision court** holds fast decision models: systems built to quickly pick one of a few answers. Operators bring their own.
2. Besides the usual answers, a juror there can vote **"did not converge" (DNC)**: it couldn't reach a well-supported ruling in time. That's different from "refuse to arbitrate" and from not voting.
3. A ruling needs **more than half of all seats**. Otherwise the case moves automatically to **Court #34**, where agents get more time and must always rule. Normal appeals follow, up to human jurors.
4. The move is **prepaid**: both sides put a bit extra in at the start. It's refunded if the fast court settles the case; otherwise the loser pays it.
5. **Payouts** for a round that moved up: a ruling that matches the final one earns its fee, a wrong ruling loses its stake, and DNC pays a small charge. No juror's penalty goes to another juror. The payouts are designed so that guessing doesn't pay, and neither does always voting DNC.

**Why a court and not one tool**

Nobody picks the method. Anyone can enter with their own decision system, and the payouts decide which ones last. That also keeps panels mixed, so one trick in the evidence is less likely to fool them all.

**What runs today**

Most of the design fits in a new dispute kit on Kleros 2.0.0. On the contracts deployed today, a case can only move up to its parent court, and the payouts can't be set exactly as proposed. A small pilot could start with a "not sure" answer in the case template, but Kleros's normal payouts would reward "not sure" when most jurors pick it and penalize it like a wrong answer otherwise, so it could only measure speed and coverage.

**Questions for the people running Court #34**

1. Would a decision court in front of Court #34 be worth piloting, and for which kind of dispute?
2. Should justifications be optional in the fast court and required in Court #34?
3. For the move up: a native court jump, or an explicit route to Court #34?

Full proposal (RFC-0001, Draft 0.2): https://github.com/lovon-spec/kleros-decision-agent-courts/blob/main/rfcs/0001-decision-agent-courts.md

It's a discussion draft. Nothing has been built, simulated or audited, and it doesn't ask for funding or stake. Counterexamples and corrections are very welcome, here or as [GitHub issues](https://github.com/lovon-spec/kleros-decision-agent-courts/issues).
