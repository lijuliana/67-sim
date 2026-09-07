#!/usr/bin/env python3

import argparse
import random
import sys
import time
from collections import Counter
from itertools import combinations_with_replacement
from math import comb, factorial


# ─── core solver ────────────────────────────────────────────────────────────

def can_reach(numbers, target, eps=1e-9):
    """Return True if *target* is reachable using every number in *numbers*
    exactly once, combined with +, -, *, /.

    The algorithm picks every unordered pair, applies all six directed
    operations (a+b, a-b, b-a, a*b, a/b, b/a), replaces the pair with
    the result, and recurses until one number remains.
    """
    n = len(numbers)
    if n == 1:
        return abs(numbers[0] - target) < eps

    for i in range(n):
        for j in range(i + 1, n):
            remaining = [numbers[k] for k in range(n) if k != i and k != j]
            a, b = numbers[i], numbers[j]

            for result in _ops(a, b, eps):
                remaining.append(result)
                if can_reach(remaining, target, eps):
                    return True
                remaining.pop()

    return False


def _ops(a, b, eps=1e-9):
    """Yield every result obtainable from *a* and *b* via +, -, *, /."""
    yield a + b
    yield a - b
    yield b - a
    yield a * b
    if abs(b) > eps:
        yield a / b
    if abs(a) > eps:
        yield b / a


# ─── solution finder (returns a human-readable expression) ──────────────────

def find_solution(tagged, target, eps=1e-9):
    """Return an expression string or *None*.

    *tagged* is a list of ``(value, expr_string)`` tuples.
    """
    if len(tagged) == 1:
        val, expr = tagged[0]
        return expr if abs(val - target) < eps else None

    n = len(tagged)
    for i in range(n):
        for j in range(i + 1, n):
            rest = [tagged[k] for k in range(n) if k != i and k != j]
            av, ae = tagged[i]
            bv, be = tagged[j]

            candidates = [
                (av + bv, f"({ae} + {be})"),
                (av - bv, f"({ae} - {be})"),
                (bv - av, f"({be} - {ae})"),
                (av * bv, f"({ae} * {be})"),
            ]
            if abs(bv) > eps:
                candidates.append((av / bv, f"({ae} / {be})"))
            if abs(av) > eps:
                candidates.append((bv / av, f"({be} / {ae})"))

            for rv, re in candidates:
                rest.append((rv, re))
                sol = find_solution(rest, target, eps)
                if sol is not None:
                    return sol
                rest.pop()

    return None


# ─── helpers ────────────────────────────────────────────────────────────────

def multiset_weight(ms):
    """Number of distinct orderings of the multiset *ms* (a sorted tuple)."""
    counts = Counter(ms)
    w = factorial(len(ms))
    for c in counts.values():
        w //= factorial(c)
    return w


# ─── exact enumeration ─────────────────────────────────────────────────────

def exact_solve(target, num_cards, max_val=13, quiet=False):
    """Enumerate all multisets, return *(solvable_draws, total_draws, pct)*."""
    multisets = list(
        combinations_with_replacement(range(1, max_val + 1), num_cards)
    )
    total_draws = max_val ** num_cards
    solvable_draws = 0

    if not quiet:
        print(f"  Unique multisets : {len(multisets):,}")
        print(f"  Total draws      : {total_draws:,}")
        print()

    start = time.time()
    for idx, ms in enumerate(multisets, 1):
        w = multiset_weight(ms)
        if can_reach(list(ms), target):
            solvable_draws += w

        if not quiet and (idx % 200 == 0 or idx == len(multisets)):
            elapsed = time.time() - start
            print(
                f"\r  Checked {idx:,}/{len(multisets):,} "
                f"({idx / len(multisets) * 100:.1f}%) — {elapsed:.1f}s",
                end="", flush=True,
            )

    if not quiet:
        print()
        print()

    pct = solvable_draws / total_draws * 100 if total_draws else 0
    return solvable_draws, total_draws, pct


# ─── Monte Carlo simulation ────────────────────────────────────────────────

def simulate(target, num_cards, num_trials=10_000, max_val=13, quiet=False):
    """Run *num_trials* random draws, return *(solvable, total, pct)*."""
    solvable = 0
    start = time.time()

    for t in range(1, num_trials + 1):
        hand = [random.randint(1, max_val) for _ in range(num_cards)]
        if can_reach(hand, target):
            solvable += 1

        if not quiet and (t % 500 == 0 or t == num_trials):
            elapsed = time.time() - start
            rate = solvable / t * 100
            print(
                f"\r  Trial {t:,}/{num_trials:,} "
                f"({t / num_trials * 100:.1f}%) — "
                f"rate so far: {rate:.2f}% — {elapsed:.1f}s",
                end="", flush=True,
            )

    if not quiet:
        print()
        print()

    pct = solvable / num_trials * 100 if num_trials else 0
    return solvable, num_trials, pct


# ─── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generalized Game of 24 Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s                                 Classic: target=24, 4 cards, exact
  %(prog)s -t 100 -n 5                    Target 100, 5 cards
  %(prog)s -t 24 -n 4 -s -T 10000         Monte Carlo, 10 000 trials
  %(prog)s --solve 3 8 7 2                 Show a solution for [3,8,7,2] -> 24
  %(prog)s --sweep 1 100 -n 4              Table of rates for targets 1-100
""",
    )

    parser.add_argument(
        "-t", "--target", type=int, default=24,
        help="target number to reach (1-200, default: 24)",
    )
    parser.add_argument(
        "-n", "--num-cards", type=int, default=4,
        help="how many cards to draw (1-10, default: 4)",
    )
    parser.add_argument(
        "-m", "--max-val", type=int, default=13,
        help="maximum card value (default: 13)",
    )
    parser.add_argument(
        "-s", "--simulate", action="store_true",
        help="use Monte Carlo simulation (recommended for n >= 6)",
    )
    parser.add_argument(
        "-T", "--trials", type=int, default=10_000,
        help="number of simulation trials (default: 10 000)",
    )
    parser.add_argument(
        "--solve", type=int, nargs="+", metavar="N",
        help="find a solution for specific card values (uses -t as target)",
    )
    parser.add_argument(
        "--sweep", type=int, nargs=2, metavar=("LO", "HI"),
        help="report success rate for every target in [LO, HI]",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="random seed for reproducibility",
    )

    args = parser.parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    # ── solve mode ──────────────────────────────────────────────────────
    if args.solve:
        numbers = args.solve
        target = args.target
        print(f"\nSolving: {numbers}  ->  {target}")
        if can_reach(list(numbers), target):
            tagged = [(v, str(v)) for v in numbers]
            expr = find_solution(tagged, target)
            print(f"  [YES]  {expr} = {target}")
        else:
            print("  [NO]   No solution exists.")
        print()
        return

    # ── validation ──────────────────────────────────────────────────────
    if not 1 <= args.target <= 200:
        parser.error("target must be between 1 and 200")
    if not 1 <= args.num_cards <= 10:
        parser.error("num-cards must be between 1 and 10")
    if args.max_val < 1:
        parser.error("max-val must be at least 1")

    # ── sweep mode ──────────────────────────────────────────────────────
    if args.sweep:
        lo, hi = args.sweep
        if lo > hi:
            lo, hi = hi, lo
        mode_label = "simulation" if args.simulate else "exact"
        sep = "=" * 60

        print()
        print(sep)
        print(f"  Sweep: targets {lo} - {hi}   |   "
              f"{args.num_cards} cards (1-{args.max_val})   |   {mode_label}")
        print(sep)
        print()
        print(f"  {'Target':>6}  {'Solvable':>10}  {'Total':>10}  {'Rate':>8}")
        print(f"  {'------':>6}  {'--------':>10}  {'-----':>10}  {'----':>8}")

        for t in range(lo, hi + 1):
            if args.simulate:
                s, tot, pct = simulate(
                    t, args.num_cards, args.trials, args.max_val, quiet=True
                )
            else:
                s, tot, pct = exact_solve(
                    t, args.num_cards, args.max_val, quiet=True
                )
            print(f"  {t:>6}  {s:>10,}  {tot:>10,}  {pct:>7.2f}%")

        print()
        return

    # ── single-target mode ──────────────────────────────────────────────
    sep = "=" * 60
    print()
    print(sep)
    print("  Generalized Game of 24 — Simulator")
    print(sep)
    print()
    print(f"  Target         : {args.target}")
    print(f"  Cards drawn    : {args.num_cards}")
    print(f"  Card range     : 1 - {args.max_val}")

    if args.simulate:
        print(f"  Mode           : Monte Carlo ({args.trials:,} trials)")
        print()
        s, tot, pct = simulate(
            args.target, args.num_cards, args.trials, args.max_val
        )
    else:
        num_ms = comb(args.num_cards + args.max_val - 1, args.num_cards)
        print(f"  Mode           : Exact enumeration")
        print()
        if num_ms > 50_000:
            print(
                f"  NOTE: {num_ms:,} multisets to check — this may be slow."
            )
            print(
                "  Consider using  -s  (simulation) for faster results.\n"
            )
        s, tot, pct = exact_solve(
            args.target, args.num_cards, args.max_val
        )

    thin = "-" * 60
    print(thin)
    print(f"  Solvable draws : {s:,} / {tot:,}")
    print(f"  Success rate   : {pct:.4f}%")
    print(thin)
    print()


if __name__ == "__main__":
    main()
