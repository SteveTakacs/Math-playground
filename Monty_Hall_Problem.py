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

"""
def run_simulations(num_simulations: int, switch: bool) -> float:
    wins = 0
    for _ in range(num_simulations):
        if monty_hall_game(switch):
            wins += 1
    return wins / num_simulations
"""

if __name__ == "__main__":

    num_simulations = 10_000
    switch_win_rate = win_ratios_over_time(num_simulations, True)[-1]
    stick_win_rate = win_ratios_over_time(num_simulations, False)[-1]
    print(f"Switching win rate: {switch_win_rate:.2%}")
    print(f"Sticking win rate: {stick_win_rate:.2%}")





# More than looking at the number, let's make some plots to visualize the results!
#For this, you will have to install numpy and matplotlib if you haven't already.

ratios = win_ratios_over_time(num_simulations, False)
plot_limit = 3000
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




"""
x = np.arange(1, plot_limit + 1)  
y = ratios[:plot_limit]  
plt.title(r"Win ratio over (n) if we say 'no'")  
plt.xlabel("n = number of rounds played")  
plt.ylabel(r"Cumulative win percentage")  
plt.axhline(y = 1/3, color = 'k', linestyle='--', alpha = 0.6, label = r"Probability of wining")  
plt.plot(x,y)  
plt.xlim(-5,plot_limit)  
plt.ylim(0.1,0.6)  
plt.legend()  
plt.show()
"""