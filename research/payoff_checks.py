"""Payoff checks for RFC-0001, Draft 0.3.

Reproduces the numbers quoted in sections 7.3, 7.4 and 7.6 of the RFC.

These are small expected-value calculations, not a simulation of real jurors
and not an equilibrium analysis. Assumptions: jurors care only about expected
payoff, research costs nothing, and the agent court's ruling is correct.
All amounts are in units of the fee per seat (f = 1).

Baseline payoffs in every decision-court round (section 7.3):
  a ruling that matches the final ruling keeps its fee f,
  a ruling that doesn't loses its stake at risk L,
  DNC pays the charge d.
No money moves between jurors.

Run:  python3 research/payoff_checks.py
"""

F = 1.0  # fee per seat


# --- Section 7.3: the bar -------------------------------------------------

def bar(L, d, f=F):
    """Confidence above which ruling beats DNC."""
    return (L - d) / (f + L)


def blind_vote_pays_above(L, f=F):
    """Base rate above which voting the common answer blindly makes money."""
    return L / (f + L)


# --- Section 7.6: an honest juror's result ---------------------------------

def profit(c, a, L, d, f=F):
    """Profit per case of a juror that rules on a share c of its cases and is
    right a of the time when it rules, with rulings checked against the truth."""
    return c * (a * f - (1 - a) * L) - (1 - c) * d


def min_coverage(a, L, d, f=F):
    """Smallest share of cases a juror must rule on to break even (None if it never does)."""
    edge = a * f - (1 - a) * L
    return None if edge <= 0 else d / (edge + d)


# --- Section 7.3: what a settled round pays for ----------------------------

def follow_the_others(p, corrected, L, d, f=F):
    """A juror p sure of A that expects the other two to vote A.
    `corrected` is the share of wrong rulings that an objection gets corrected.
    Returns (payoff of voting A, payoff of DNC)."""
    vote_a = p * f + (1 - p) * ((1 - corrected) * f + corrected * -L)
    return vote_a, -d


def common_vs_better(a_common, a_better, L, corrected, shared=False, f=F):
    """Three seats, everyone rules. Two seats run the same system (identical
    votes); one runs a better, independent system. Returns the profit per case
    of (a common seat, the better seat).
    shared=False: the baseline, each seat is paid on its own vote only.
    shared=True:  Kleros's usual sharing (variant in 7.4): matching seats share
                  all three fees and the stakes lost by the others."""
    common = better = 0.0
    for pair_right, p1 in ((True, a_common), (False, 1 - a_common)):
        for third_right, p2 in ((True, a_better), (False, 1 - a_better)):
            p = p1 * p2
            lone, pair = (3 * f + 2 * L, (3 * f + L) / 2) if shared else (f, f)
            if pair_right:  # the ruling is right and stands
                common += p * (f if third_right else pair)
                better += p * (f if third_right else -L)
            elif third_right:  # the pair outvotes the seat that was right
                common += p * ((1 - corrected) * pair + corrected * -L)
                better += p * ((1 - corrected) * -L + corrected * lone)
            else:  # all three wrong
                common += p * ((1 - corrected) * f + corrected * -L)
                better += p * ((1 - corrected) * f + corrected * -L)
    return common, better


def crossover(L, shared):
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        c, b = common_vs_better(0.85, 0.95, L, mid, shared)
        lo, hi = (mid, hi) if c > b else (lo, mid)
    return hi


# --- Section 7.4: Kleros's usual sharing in settled rounds ------------------

def lone_dissent_bar(L, d, n=3, f=F):
    """With sharing: chance of being proved right above which a lone vote
    against the other n-1 seats beats DNC (every wrong ruling corrected)."""
    return (L - d) / (n * (f + L))


def shared_two_against_one(p, L, f=F):
    """With sharing, three jurors each p sure of A; two vote A, one votes B;
    every wrong ruling is corrected. Returns (payoff of an A vote, of the B vote)."""
    a_vote = p * (3 * f + L) / 2 + (1 - p) * -L
    b_vote = (1 - p) * (3 * f + 2 * L) + p * -L
    return a_vote, b_vote


# --- Section 7.4: the early-solver transfer (Draft 0.1) ---------------------

def lone_ruling_prize(n, m, d, f=F):
    """Draft 0.1 with pooled fees: a lone matching ruling beside m DNC votes wins this."""
    return n * f + m * d


def pct(x):
    return "never" if x is None else f"{100 * x:.0f}%"


if __name__ == "__main__":
    L, d = 9.0, 0.25
    print("== Example values: f = 1, L = 9, d = 0.25 ==")
    print(f"bar (7.3): ruling beats DNC above {bar(L, d):.3f} confidence")
    print(f"a coin flip earns {0.5 * F - 0.5 * L:+.2f}; two seats on two answers earn {F - L:+.2f}; DNC earns {-d:+.2f}")
    print(f"limit 1 (7.6): blind voting beats DNC above a base rate of {bar(L, d):.3f},"
          f" and makes money above {blind_vote_pays_above(L):.2f}")
    print("limit 2 (7.6): smallest share of cases a juror must rule on to break even")
    for a in (0.95, 0.98):
        print(f"  right {a:.0%} of the time: {pct(min_coverage(a, L, d))}")
    print("profit per case, right 95% of the time:")
    for c in (0.2, 0.4, 0.6):
        print(f"  rules on {c:.0%} of cases: {profit(c, 0.95, L, d):+.2f}")

    print("\n== What a settled round pays for (7.3) ==")
    print("three similar jurors, each 55% sure of A, each expecting the others to vote A:")
    for r in (0.0, 0.25, 0.5, 1.0):
        va, dn = follow_the_others(0.55, r, L, d)
        print(f"  {r:.0%} of wrong rulings corrected: voting A {va:+.2f}, DNC {dn:+.2f}")
    print(f"  DNC is better once {(F + d) / (0.45 * (F + L)):.0%} of wrong rulings are corrected")
    print("two seats on a system right 85% of the time, one seat on a system right 95% of the time:")
    for r in (0.0, 0.5, 1.0):
        cm, bt = common_vs_better(0.85, 0.95, L, r)
        print(f"  {r:.0%} of wrong rulings corrected: common seat {cm:+.2f}, better seat {bt:+.2f}")
    print(f"  the better system earns more once {crossover(L, False):.0%} of wrong rulings are corrected")

    print("\n== Variant: Kleros's usual sharing in settled rounds (7.4) ==")
    print(f"the better system earns more once {crossover(L, True):.0%} of wrong rulings are corrected")
    print(f"a lone vote against the other two wins {3 * F + 2 * L:.0f} or loses {L:.0f};"
          f" it beats DNC above a {lone_dissent_bar(L, d):.0%} chance of being proved right")
    av, bv = shared_two_against_one(0.65, L)
    print(f"three jurors each 65% sure of A, voting A, A, B: each A vote {av:+.2f}, the B vote {bv:+.2f}, DNC {-d:+.2f}")

    print("\n== Draft 0.2's example values: f = 1, L = 4, d = 1, eps = 0.5 (7.4) ==")
    print(f"bar: {bar(4, 1):.2f} to {bar(4, 0.5):.2f}")
    print(f"juror ruling on 40% of cases, right 95% of the time:"
          f" {profit(0.4, 0.95, 4, 1):+.2f} to {profit(0.4, 0.95, 4, 0.5):+.2f} per case")

    print("\n== Draft 0.1's early-solver transfer with pooled fees (7.4) ==")
    prize = lone_ruling_prize(3, 2, 2)
    print(f"three jurors, L = 4, d = 2: a coin flip beside two DNC votes wins {prize:.0f} or loses 4:"
          f" {0.5 * prize - 0.5 * 4:+.1f} on average")
    print(f"two of five seats voting A and B beside three DNC votes: {lone_ruling_prize(5, 3, 2):+.0f} whichever wins")
