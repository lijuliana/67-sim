# 67-sim

Simulator for the card game 67 (generalized 24 variant). © Juliana & Angeline :)

## The game

Classic 24: you get 4 cards and have to combine all of them with + - * / to make 24. Each card gets used exactly once, and you can group things however you want with parentheses.

67 works the same way, with these changes:

- You draw any number of cards (1 to 10), each a number from 1 to 13
- The target can be anything from 1 to 200, not just 24
- Every card has to be used exactly once
- The only moves are + - * / and you can pair things up in any order
- Fractions in the middle are fine, so 8 / (3 - 8/3) = 24 counts

A hand is "solvable" if there is at least one way to do it. The sim asks, out of every possible hand, how many are solvable.

## Running it

Everything runs from the repo root.

```
python 67sim.py                          # classic, target 24, 4 cards, exact count
python 67sim.py -t 100 -n 5              # target 100 with 5 cards
python 67sim.py -t 24 -n 6 -s -T 10000   # monte carlo with 10k random hands
python 67sim.py --solve 3 8 7 2 -t 24    # show an actual solution for one hand
python 67sim.py --sweep 1 100 -n 4       # table of rates for targets 1 to 100
```

Exact mode goes through every possible hand, which is fine for 4 cards but gets slow after that, so use `-s` for 5+ cards. `--seed` makes the random runs repeatable.

## What's in here

- `67sim.py` the simulator
- `sweeps/` scripts and raw results for running a whole range of targets at once
- `figures/` the plots those sweeps make

## Some results

With 4 cards, 24 is solvable for about 79% of hands, which is higher than I expected. Target 2 is the easiest at 97.6%, and by 199 it drops to under 5%.

With 5 and 6 cards it gets silly. In my sweeps of 1 to 200, basically everything is solvable nearly all the time (the 6 card plot is just one big flat wall of blue). More cards means way more ways to build a number.
