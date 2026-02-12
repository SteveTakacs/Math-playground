"""
Let's assume, we have an old wall clock, with marings between 1 and 12. 
Let's also assume that we have a ladybug on the clock, and that the ladybug can only move to the next marking in a clockwise or counter-clockwise direction with 50-50% chance.

Now let's follow the movements of the ladybug! Whenever the ladybug reaches a marking, let's color that marking to know that the ladybug has been there.
The questions we want to answer is: What is the percentage for each marking to be the last marking (lastly colored) that the ladybug visits?
The ladybug starts at marking 12, so 6 is the furthest away and from 12 it can move to either 1 or 11 with equal probability.

An example for ladybug movements: 12 -> 1 -> 2 -> 1 -> 12 -> 11 -> 10 -> 9 -> 8 -> 9 -> 8 -> ...
"""

"""
Our Simulation in a nutshell
In main() we define the number of rounds we play and call win_ratios_over_time -> In win_ratios_over_time we call match over and over again, keeping track of win and lose rates. Each match goes until a player recives 11 points.
"""

"""
Let's see how much chance a mark has to be the last one visited!
"""

import random
import numpy as np
import matplotlib.pyplot as plt

def one_full_round_the_clock() -> int:
    #Clock markings from 1 to 12.
    visited_markings = [1] + [0] * 11 # Start at marking 12 current_marking = 12 visited_mark
    current_marking = 12
    last_marking = 0

    #A Full round is when the ladybug has visited all markings at least once.
    #If there is a marking with 0, it means that the ladybug has not visited it yet, and we need to keep simulating.
    while ((np.array(visited_markings) == 0).any()):
        # Simulate a point
        if current_marking == 12:
            if random.random() < 0.5:  # 50% chance to move clockwise
                current_marking = 1
                visited_markings[1] = 1
            else:  # 50% chance to move counter-clockwise
                current_marking = 11
                visited_markings[1] = 11


    return last_marking            
            
            
            


def distributions_over_time(num_rounds: int) -> np.ndarray:
    wins = 0
    ratios = np.zeros(num_rounds, dtype=float)

    for t in range(num_rounds):
        ratios[t] = one_full_round_the_clock()
    return ratios

if __name__ == "__main__":
    num_simulations = 10_000
    distritbutions = distributions_over_time(num_simulations)
    print(f"Starters win rate: {distritbutions:.2%}")

# More than looking at the number, let's make some plots to visualize the results!
#For this, you will have to install numpy and matplotlib if you haven't already.

ratios = win_ratios_over_time(num_simulations)
plot_limit = 10000
# Plot how the ratio changes by increasing $n$  

x = np.arange(1, plot_limit + 1)
y = ratios[:plot_limit]

plt.title("Win ratio for the player who serves first in a squash match")
plt.xlabel("n = number of rounds played")
plt.ylabel("Cumulative win percentage")
plt.axhline(y=0.55, linestyle="--", alpha=0.6, label="Theoretical 55% win rate")
plt.axhline(y=0.50, linestyle="--", alpha=0.3, color="gray", label="50% win rate")
plt.plot(x, y)
plt.xlim(1, plot_limit)
plt.ylim(0.1, 0.6)
plt.legend()
plt.savefig("SquashServe.png", dpi=200)
#plt.show()
