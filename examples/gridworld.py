import val_iteration

"""
This example implements the gridworld MDP with stochastic actions.
A robot moves around a grid (environment). Each time, it can move from some location to neighboring locations, collecting rewards and punishments.
Theoretical details are provided in Example 9.28 from Artificial Intelligence: Foundations and Computational Agents 2nd edition
"""

GRIDWORLD_SIZE = 10

STATES_WITH_POSITIVE_REWARDS = {
    (7, 8): 10,
    (2, 7): 3
}

STATES_WITH_NEGATIVE_REWARDS = {
    (4, 3): -5,
    (7, 3): -10
}

ACTIONS = ['up', 'down', 'left', 'right']

CORNERS = [(0, 0), (0, GRIDWORLD_SIZE-1), (GRIDWORLD_SIZE-1, 0), (GRIDWORLD_SIZE-1, GRIDWORLD_SIZE-1)]

# Function to check if still within grid
def in_bounds(state):
    r, c = state
    return 0 <= r < GRIDWORLD_SIZE and 0 <= c < GRIDWORLD_SIZE

# Generate all state names i,j as strings
states = [f"{r},{c}" for r in range(GRIDWORLD_SIZE) for c in range(GRIDWORLD_SIZE)]

# Each state has the same action set unless it's terminal
actions = {s: ACTIONS.copy() for s in states}
ACTION_UPDATE = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

# Transitions and rewards
transitions = {}
rewards = {}

for r in range(GRIDWORLD_SIZE):
    for c in range(GRIDWORLD_SIZE):
        state = f"{r},{c}"
        for action in ACTIONS:
            intended = ACTION_UPDATE[action]
            other_actions = [a for a in ACTIONS if a != action]
            transition_probs = [
                (0.7, intended),
                (0.1, ACTION_UPDATE[other_actions[0]]),
                (0.1, ACTION_UPDATE[other_actions[1]]),
                (0.1, ACTION_UPDATE[other_actions[2]])
            ] # Transition probabilities of stochastic action (0.7 intended, 0.1 to move in each of 3 other directions)
            
            transitions[(state, action)] = []

            # Simulate action a and extract each outcome with its probability and state update
            for prob, delta in transition_probs:
                new_r, new_c = r + delta[0], c + delta[1] 
                # First check if a wall would be hit
                if in_bounds((new_r, new_c)):
                    # No wall hit: simulate move to next state
                    next_state = f"{new_r},{new_c}"
                    reward = 0.0
                    if (r, c) in STATES_WITH_POSITIVE_REWARDS:
                        # Reached state with a positive reward
                        reward = STATES_WITH_POSITIVE_REWARDS[(r, c)]
                        # Send to a random corner (simulate all with equal probability prob/4)
                        for corner in CORNERS:
                            corner_state = f"{corner[0]},{corner[1]}"
                            transitions[(state, action)].append((prob / 4, corner_state))
                            rewards[(state, action, corner_state)] = reward
                        break  # skip adding normal transition
                    else:
                        transitions[(state, action)].append((prob, next_state))
                        if (r, c) in STATES_WITH_NEGATIVE_REWARDS:
                            # Reached negative state, add reward after action to next state
                            rewards[(state, action, next_state)] = STATES_WITH_NEGATIVE_REWARDS[(r, c)]
                        else:
                            rewards[(state, action, next_state)] = 0.0
                else:
                    # Hit wall: stay in place with penalty
                    transitions[(state, action)].append((prob, state))
                    rewards[(state, action, state)] = -1.0

gamma = 0.9 # Set new gamma to 0.9, as per Example 9.32

V, policy = val_iteration.val_iteration(states, actions, transitions, rewards, gamma)

print("Optimal Value Function:")
for s in V:
    print(f"  {s}: {V[s]:.2f}")

print("\nOptimal Policy:")
for s in policy:
    print(f"  {s}: {policy[s]}")