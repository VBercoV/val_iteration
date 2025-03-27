def val_iteration(states: list, actions: dict, transitions: dict, rewards: dict, gamma=0.8, theta=1e-6, nr_iter=100000):
    """
    Perform value iteration for a given MDP.
    Implements reward function dependent on final state R(s,a,s'), and hence allows stochastic actions.
    To implement independent version R(s,a), simply assign the same value to all R(s,a,s') for fixed s and a.

    Parameters:
        states (list): List of state names (strings)
        actions (dict): Dictionary mapping state -> list of available actions (strings)
        transitions (dict): Dictionary mapping (state, action) -> list of (probability, next_state) tuples
        rewards (dict): Dictionary mapping (state, action, next_state) -> reward (float)
        gamma (float): Discount factor, set to 0.8 by default
        theta (float): Convergence threshold, set to 1e-6 by default
        nr_iter (int): Maximum number of iterations allowed, set to 100000 by default

    Returns:
        V (dict): Optimal value function
        policy (dict): Optimal policy mapping state to best action
    """
    # Initialize value function
    V = {s: 0.0 for s in states} # V_0
    policy = {s: None for s in states} # Initial policy
    k = 0 # Counter for iterations

    while True:
        delta = 0 
        for s in states:
            if s not in actions or len(actions[s]) == 0:
                continue  # Skip terminal or dead-end states

            action_values = {} # Store Q(s,a) for all actions a available to state s
            for a in actions[s]:
                q_value = 0 # Initially Q(s,a) = 0
                for prob, s_next in transitions.get((s, a), []):
                    reward = rewards.get((s, a, s_next), 0.0) # R(s,a,s')
                    q_value += prob * (reward + gamma * V[s_next]) # Sum of P(s'|s,a) * (R(s,a,s') + gamma * V[s']) over s'
                action_values[a] = q_value

            best_action = max(action_values, key=action_values.get) # Select argmax Q(s,a)
            best_value = action_values[best_action] # Select max Q(s,a)

            delta = max(delta, abs(V[s] - best_value)) # Final value of delta = max(abs(V_k(s)-V_{k+1}(s)))
            V[s] = best_value
            policy[s] = best_action
        
        k = k+1

        if delta < theta or k > nr_iter: # Terminate when below uniform upper bound, or iteration number is reached.
            break

    return V, policy
        