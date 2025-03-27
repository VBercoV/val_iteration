import val_iteration

"""
This example implements the "partying-when-sick" MDP.
A student wants to make an informed decision on whether to party or relax over the weekend. They'd prefer to party, but are worried about being sick.
Theoretical details are provided in Example 9.27 from Artificial Intelligence: Foundations and Computational Agents 2nd edition
"""

states = ['healthy', 'sick']
actions = {
    'healthy': ['relax','party'],
    'sick': ['relax','party'] 
}
transitions = {
    ('healthy', 'relax'): [(0.95, 'healthy'), (0.05, 'sick')],
    ('healthy', 'party'): [(0.7, 'healthy'), (0.3, 'sick')],
    ('sick', 'relax'): [(0.5, 'healthy'), (0.5, 'sick')],
    ('sick', 'party'): [(0.1, 'healthy'), (0.9, 'sick')]
}
rewards = {
    ('healthy', 'relax', 'healthy'): 7,
    ('healthy', 'relax', 'sick'): 7,
    ('healthy', 'party', 'healthy'): 10,
    ('healthy', 'party', 'sick'): 10,
    ('sick', 'relax', 'healthy'): 0,
    ('sick', 'relax', 'sick'): 0,
    ('sick', 'party', 'healthy'): 2,
    ('sick', 'party', 'sick'): 2
 }

V, policy = val_iteration.val_iteration(states, actions, transitions, rewards)

print("Optimal Value Function:")
for s in V:
    print(f"  {s}: {V[s]:.2f}")

print("\nOptimal Policy:")
for s in policy:
    print(f"  {s}: {policy[s]}")