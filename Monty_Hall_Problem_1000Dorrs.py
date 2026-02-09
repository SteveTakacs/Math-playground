"""
Monty_Hall_Problem in a Nushell
In this case not with the original 3, but with 1000 doors.

The Monty Hall problem is a famous probability puzzle based on a game show scenario. The problem is named after Monty Hall, the original host of the television game show "Let's Make a Deal." The puzzle goes as follows:
1. You are a contestant on a game show, and you are presented with (in this case) 1000 doors. Behind one door is a car (the prize you want), and behind the other 999 doors are goats (which you do not want).
2. You choose one of the 1000 doors, but it is not opened immediately.
3. The host, Monty Hall, who knows what is behind each door, opens 998 of the remaining 999 doors that you did not choose, revealing a goat for each.
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
2. Each Door has a 1/1000 chance at the beginning, so in the separation 1 to 2 you have 0.1% to have the car and the host has 99.9% to have the car. The host will have 99.9% even after revealing a door and therefore the remaining door will have 99.9% chance to have the car.
"""

"""
In this case our "gur feeling" is that it is almost impossible to have picked the right door at the beginning, so we should switch (as the host is "hiding" the door where the car is). Let's see if the numbers confirm this intuition!
"""

import random
import numpy as np
import matplotlib.pyplot as plt

N_DOORS = 1000

def monty_hall_game(switch: bool) -> bool:
    # defining what's behind the doors (0 -> car, 1 -> goat)
    #The first door has the car, the other 999 have goats:
    doors = [0] + [1] * 999
    #We shuffle the doors to randomize their positions:
    random.shuffle(doors)

    # Player get's to choose a door of her liking
    choice = random.randint(0, 999)

    # Host keeps exactly ONE other door closed
    if doors[choice] == 0:
        # player picked the car -> host keeps a random goat door closed
        remaining = [i for i in range(1000) if i != choice and doors[i] == 1]
        other_door = random.choice(remaining)
    else:
        # player picked a goat -> host must keep the car door closed
        other_door = doors.index(0)

    # If the player decides to switch, she picks the remaining door
    if switch:
        choice = other_door

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
plt.axhline(y=1/1000, linestyle="--", alpha=0.6, label="Theoretical 1/1000")
plt.plot(x, y)
plt.xlim(1, plot_limit)
plt.ylim(0.1, 0.01)
plt.legend()
plt.savefig("monty_hall_1000Doors_stay.png", dpi=200)
#plt.show()
