"""
In every squash game, someone has to start the game with a serve. The player who serves first has a slight advantage, as they have the opportunity to score points before their opponent. 
This is because the server can dictate the pace of the game and put pressure on their opponent from the very beginning.
In this simulation we will explore the importance of a squash serve by simulating a game and analyzing the outcomes based on who serves first. We will use a simple model where the server has a certain probability of winning each point, and we will run multiple simulations to see how this advantage plays out over time.
We will use the assumption that the server has a 55% chance of winning each point, while the receiver has a 45% chance.

After winning a set, the winner of the set gets to seve again, having a bigger advantage in the next set. We will simulate multiple sets to see how this advantage accumulates over time and how it affects the overall outcome of the match.
One match is played until a player wins 11 sets with at least 2 points difference.
"""

"""
Our Simulation in a nutshell
In main() we define the number of rounds we play and call win_ratios_over_time -> In win_ratios_over_time we call match over and over again, keeping track of win and lose rates. Each match goes until a player recives 11 points.
"""

"""
Let's see how much chance a player has (of equal skill) to win only by making the first serve!
"""

import random
import numpy as np
import matplotlib.pyplot as plt

def match() -> bool:
    #Player 1 is the player who starts serving.
    pointsOfPlayer1 = 0
    pointsOfPlayer2 = 0

    currentServer = True # True for Player 1, False for Player 2

    # Simulate a match until one player reaches 11 points

    while (pointsOfPlayer1 < 11 and pointsOfPlayer2 < 11) and (abs(pointsOfPlayer1 - pointsOfPlayer2) < 2):
        # Simulate a point
        if currentServer:  # Player 1 is serving
            if random.random() < 0.55:  # Server wins the point
                pointsOfPlayer1 += 1
            else:  # Receiver wins the point
                pointsOfPlayer2 += 1
                currentServer = False  # Switch server
        else:
            if random.random() < 0.55:  # Server wins the point
                pointsOfPlayer2 += 1
            else:  # Receiver wins the point
                pointsOfPlayer1 += 1
                currentServer = True  # Switch server

    if pointsOfPlayer1 > pointsOfPlayer2:
        return True  # Player 1 wins
    else:
        return False  # Player 2 wins

def win_ratios_over_time(num_rounds: int) -> np.ndarray:
    wins = 0
    ratios = np.zeros(num_rounds, dtype=float)

    for t in range(num_rounds):
        if match():
            wins += 1
        ratios[t] = wins / (t + 1)

    return ratios

if __name__ == "__main__":
    num_simulations = 10_000
    win_rate = win_ratios_over_time(num_simulations)[-1]
    print(f"Starters win rate: {win_rate:.2%}")

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
