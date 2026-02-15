"""
Let's assume, we have an old wall clock, with markings between 1 and 12. 
Let's also assume that we have a ladybug on the clock, and that the ladybug can only move to the next marking in a clockwise or counter-clockwise direction with 50-50% chance.

Now let's follow the movements of the ladybug! Whenever the ladybug reaches a marking, let's color that marking to know that the ladybug has been there.
The questions we want to answer is: What is the percentage for each marking to be the last marking (lastly colored) that the ladybug visits?
The ladybug starts at marking 12, so 6 is the furthest away and from 12 it can move to either 1 or 11 with equal probability.

An example for ladybug movements: 12 -> 1 -> 2 -> 1 -> 12 -> 11 -> 10 -> 9 -> 8 -> 9 -> 8 -> ...

A very good explanation of the problem can be found in this video: https://www.youtube.com/shorts/t3jZ2xGOvYg
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
                visited_markings[11] = 1
        elif current_marking == 1:
            if random.random() < 0.5:  # 50% chance to move clockwise
                current_marking = 2
                visited_markings[2] = 1
            else:  # 50% chance to move counter-clockwise
                current_marking = 12
                last_marking = 12
        elif (current_marking > 1 and current_marking < 11):
            if random.random() < 0.5:  # 50% chance to move clockwise
                current_marking = current_marking + 1
                visited_markings[current_marking] = 1
            else:  # 50% chance to move counter-clockwise
                current_marking = current_marking - 1
                visited_markings[current_marking] = 1
        elif current_marking == 11:
            if random.random() < 0.5:  # 50% chance to move clockwise
                current_marking = 12
            else:  # 50% chance to move counter-clockwise
                current_marking = 10
                visited_markings[10] = 1
    return current_marking            
            
def distributions_over_time(num_rounds: int) -> np.ndarray:
    winNumbers = np.zeros(12, dtype=int)
    for t in range(num_rounds):
        last_marking = one_full_round_the_clock()
        winNumbers[last_marking] += 1
    return winNumbers / num_rounds

if __name__ == "__main__":
    num_simulations = 10_000
    distritbutions = distributions_over_time(num_simulations)
    print(f" 1'clock: {distritbutions[1]:.2%} \n 2'clock: {distritbutions[2]:.2%} \n 3'clock: {distritbutions[3]:.2%} \n 4'clock: {distritbutions[4]:.2%} \n 5'clock: {distritbutions[5]:.2%} \n 6'clock: {distritbutions[6]:.2%} \n 7'clock: {distritbutions[7]:.2%} \n 8'clock: {distritbutions[8]:.2%} \n 9'clock: {distritbutions[9]:.2%} \n 10'clock: {distritbutions[10]:.2%} \n 11'clock: {distritbutions[11]:.2%}")

#Let's also create a diagram to visualize the distribution of the last markings.
#For this, you will have to install numpy and matplotlib if you haven't already.

    for i, value in enumerate(distritbutions, start=1):
        print(f"Marking {i}: {value:.2%}")

    # ---- Diagram ----
    markings = np.arange(1, 13)

    plt.figure()
    plt.bar(markings-1, distritbutions, color="skyblue", edgecolor="black")
    plt.xlabel("Clock Marking")
    plt.ylabel("Probability of Being Last Visited")
    plt.title("Ladybug – Probability of Each Marking Being Last")
    plt.xticks(markings)
    plt.ylim(0, max(distritbutions) * 1.1)

    plt.savefig("Ladybug_Distribution.png", dpi=300)
    print("Diagram saved as Ladybug_Distribution.png")