"""
Monty_Hall_Problem in a Nushell, but with the twist of using French Cards instead of doors. 

The problem is the same, but instead of 3 doors we have 52 cards, one of which is the Ace of Spades (the "car") and the other 51 are "goats". 
The host will reveal 50 goats and give you the option to switch to the remaining card or stick with your original choice. The question remains: Should you switch or stick?
"""

"""
Our Simulation in a nutshell
In main() we define the number of rounds we play and call win_ratios_over_time (both for switching and sticking) -> In win_ratios_over_time we call monty_hall_game over and over again, keeping track of win and lose rates.
"""

"""
The result should confirm one of 2 theories:
1. There should be a 50-50 chance of winning whether you switch or not (i.e. it doesn't matter if you switch or not) -> We are choosing between 2 cards, what happened earlier doesn't matter.
2. Each Card has a 1/52 chance at the beginning, so in the separation 1 to 51 you have 1.92% to have the car and the host has 98.08% to have the car. The host will have 98.08% even after revealing 50 cards and therefore the remaining card will have 98.08 % chance to have the car.

I think we all have a "gut feeling" that it is almost impossible to have picked the right card at the beginning, so we should switch (as the host is "hiding" the card where the car is). Let's see if the numbers confirm this intuition!
"""

import random
import numpy as np
import matplotlib.pyplot as plt

def monty_hall_game(switch: bool) -> bool:
    # defining what's behind the cards (0 -> car, 1 -> goat)
    #The first card has the car, the other 51 have goats:
    cards = [0] + [1] * 51
    #We shuffle the cards to randomize their positions:
    random.shuffle(cards)

    # Player get's to choose a card of her liking
    choice = random.randint(0, 51)

    # Host keeps exactly ONE other card closed
    if cards[choice] == 0:
        # player picked the car -> host keeps a random goat card closed
        remaining = [i for i in range(52) if i != choice and cards[i] == 1]
        other_card = random.choice(remaining)
    else:
        # player picked a goat -> host must keep the car card closed
        other_card = cards.index(0)

    # If the player decides to switch, she picks the remaining card
    if switch:
        choice = other_card

    # Win if chosen card has the car
    return cards[choice] == 0


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
plt.axhline(y=1/52, linestyle="--", alpha=0.6, label="Theoretical 1/52")
plt.plot(x, y)
plt.xlim(1, plot_limit)
plt.ylim(0.01, 0.1)
plt.legend()
plt.savefig("monty_hall_stay_FrenchCards.png", dpi=200)
#plt.show()
