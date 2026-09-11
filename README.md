# 67-sim

a little simulator for a generalized version of the Game of 24. i wanted to know how often a random hand of cards can actually hit a given number, so i just wrote something to count it :)

## the game

classic 24: you get 4 cards, you have to combine all of them with + - * / to make 24. each card gets used exactly once, and you can group things however you want with parentheses.

this version loosens it up a bit:

- you draw any number of cards (1 to 10), each one a number from 1 to 13
- the target can be anything from 1 to 200, not just 24
- every card has to be used exactly once
- the only moves are + - * / and you can pair things up in any order
- fractions in the middle are totally fine, so 8 / (3 - 8/3) = 24 counts!!

a hand is "solvable" if there is at least one way to do it. the sim just asks, out of every possible hand, how many are solvable?

## running it

everything runs from the repo root.

```
python 67sim.py                          # classic, target 24, 4 cards, exact count
python 67sim.py -t 100 -n 5              # target 100 with 5 cards
python 67sim.py -t 24 -n 6 -s -T 10000   # monte carlo with 10k random hands
python 67sim.py --solve 3 8 7 2 -t 24    # show an actual solution for one hand
python 67sim.py --sweep 1 100 -n 4       # table of rates for targets 1 to 100
```

exact mode goes through every possible hand, which is fine for 4 cards but gets slow after that, so use `-s` for 5+ cards. `--seed` makes the random runs repeatable.

## whats in here

- `67sim.py` the simulator
- `sweeps/` scripts and raw results for running a whole range of targets at once
- `figures/` the plots those sweeps make

## some results

with 4 cards, 24 is solvable for about 79% of hands, which is honestly higher than i expected. target 2 is the easiest at 97.6%, and by the time you get up to 199 it drops to under 5%.

with 5 and 6 cards it gets silly. in my sweeps of 1 to 200, basically everything is solvable nearly all the time (the 6 card plot is just one big flat wall of blue lol). more cards = way more ways to build a number.
