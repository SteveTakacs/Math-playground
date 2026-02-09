"""
Monty_Hall_Problem in a Nushell

The Monty Hall problem is a famous probability puzzle based on a game show scenario. The problem is named after Monty Hall, the original host of the television game show "Let's Make a Deal." The puzzle goes as follows:
1. You are a contestant on a game show, and you are presented with three doors. Behind one door is a car (the prize you want), and behind the other two doors are goats (which you do not want).
2. You choose one of the three doors, but it is not opened immediately.
3. The host, Monty Hall, who knows what is behind each door, opens one of the two doors that you did not choose, revealing a goat.
4. Monty then gives you the option to either stick with your original choice or switch to the other unopened door.
The question is: Should you stick with your original choice, switch to the other door, or does it not matter?
"""

"""
Our Simulation in a nutshell
In main() we define the number of rounds we play and call win_ratios_over_time (both for switching and sticking) -> In win_ratios_over_time we call monty_hall_game over and over again, keeping track of win and lose rates.
"""

"""
The result should confirm one of 2 theories:
1. There should be a 50-50 chance of winning whether you switch or not (i.e. it doesn't matter if you switch or not) -> We are choosing between 2 doors, what happened earlier doesn't matter.
2. Each Door has a 1/3 chance at the beginning, so in the separation 1 to 2 you have 33% to have the car and the host has 66% to have the car. The host will have 66% even after revealing a door and therefore the remaining door will have 66% chance to have the car.
"""

import random
import numpy as np
import matplotlib.pyplot as plt

def monty_hall_game(switch: bool) -> bool:
    # defining what's behind the doors (0 -> car, 1 -> goat)
    #The first door has the car, the other two have goats:
    doors = [0, 1, 1]
    #We shuffle the doors to randomize their positions:
    random.shuffle(doors)

    # Player get's to choose a door of her liking
    choice = random.randint(0, 2)

    # Host reveals a door that has a goat behind it
    eligible = [i for i in range(3) if i != choice and doors[i] == 1]
    host_reveal = random.choice(eligible)

    # If the player decides to switch, she picks the remaining door
    if switch:
        choice = next(i for i in range(3) if i != choice and i != host_reveal)

    # Win if chosen door has the car
    return doors[choice] == 0


def win_ratios_over_time(num_rounds: int, switch: bool) -> np.ndarray:
    wins = 0
    ratios = np.zeros(num_rounds, dtype=float)

    for t in range(num_rounds):
        if monty_hall_game(switch):
            wins += 1
        ratios[t] = wins / (t + 1)

    return ratios

if __name__ == "__main__":
    num_simulations = 10_000
    switch_win_rate = win_ratios_over_time(num_simulations, True)[-1]
    stick_win_rate = win_ratios_over_time(num_simulations, False)[-1]
    print(f"Switching win rate: {switch_win_rate:.2%}")
    print(f"Sticking win rate: {stick_win_rate:.2%}")

# More than looking at the number, let's make some plots to visualize the results!
#For this, you will have to install numpy and matplotlib if you haven't already.

ratios = win_ratios_over_time(num_simulations, False)
plot_limit = 10000
# Plot how the ratio changes by increasing $n$  

x = np.arange(1, plot_limit + 1)
y = ratios[:plot_limit]

plt.title("Win ratio over n if we stay (no switch)")
plt.xlabel("n = number of rounds played")
plt.ylabel("Cumulative win percentage")
plt.axhline(y=1/3, linestyle="--", alpha=0.6, label="Theoretical 1/3")
plt.plot(x, y)
plt.xlim(1, plot_limit)
plt.ylim(0.1, 0.6)
plt.legend()
plt.savefig("monty_hall_stay.png", dpi=200)
#plt.show()
