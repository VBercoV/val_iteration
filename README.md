{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "b074e1a9-19fb-4bf3-8710-d581c8290578",
   "metadata": {},
   "source": [
    "# Value iteration for MDPs (val_iteration)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "87f68815-e418-49c6-acdb-a7f007018386",
   "metadata": {},
   "source": [
    "val_iteration is a Python library that implements the value iteration algorithm for computing the optimal policy and value of an MDP. This package provides a valid implementation for MDPs where actions have stochastic effects, and rewards are dependent on the final state, but can be easily adapted to simpler cases. The code is based on the algorithm presented in Chapter [9.5.2](https://artint.info/2e/html2e/ArtInt2e.Ch9.S5.SS2.html) of [Artificial Intelligence: Foundations and Computational Agents 2nd edition](https://artint.info/2e/html2e/ArtInt2e.html)."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "024aa1e2-d490-443a-b1a1-10e7d1a1a854",
   "metadata": {},
   "source": [
    "## Installation"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f99271eb-6e2c-410b-b231-fdccc98fd379",
   "metadata": {},
   "source": [
    "The only requirement is to use any Python version at least above 3.12 (included). More importantly, there are no dependencies on other packages.\n",
    "\n",
    "The simplest way to install this package is by using the package manager pip in your preferred programming environment."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3ee0528e-f480-4c58-9295-0701279772a2",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install \"git+https://github.com/VBercoV/val_iteration\""
   ]
  },
  {
   "cell_type": "markdown",
   "id": "dce98abf-482a-4065-acea-570d3a3f668b",
   "metadata": {},
   "source": [
    "Once the package is installed, it can be straight-forwardly imported within the same IDE."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c3671535-d788-4682-b55a-9d8b40d24ec7",
   "metadata": {},
   "outputs": [],
   "source": [
    "import val_iteration"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6baf83a1-54cb-42ea-a566-414fc893f373",
   "metadata": {},
   "source": [
    "## How to use"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5b4c9253-4c81-49a7-a567-941915c49612",
   "metadata": {},
   "source": [
    "This version requires very specific data types for each user-defined element of the MDP, and this is crucial information for the implementation to work.\n",
    "\n",
    "- states: must be defined as a list of strings, where each string represents a state of the MDP from the set of states S."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "74953a6f-e335-4326-9d3d-f44a080f998c",
   "metadata": {},
   "outputs": [],
   "source": [
    "states = ['healthy', 'sick']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3c5b0f2c-46e8-417e-86c9-5b972a1bc18d",
   "metadata": {},
   "source": [
    "- actions: must be defined as a dictionary where, for each key-value pair, the key is a state of the MDP, and the value is a list of all available actions from that state, represented as strings."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "610b8b59-8a9b-4a37-911f-faae77127e96",
   "metadata": {},
   "outputs": [],
   "source": [
    "actions = {\n",
    "    'healthy': ['relax','party'],\n",
    "    'sick': ['relax','party'] \n",
    "}"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d1a623fa-c4cd-407d-aaba-27531863f5bd",
   "metadata": {},
   "source": [
    "- transitions: must be defined as a dictionary where, for each key-value pair, the key is a state-action pair (s,a), and the value is a list of tuples (prob, next_state), such that prob represents the probability that next_state is the effect of stochastic action a at initial state s."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c93c0ab4-3f1e-45b5-a1c8-d36d86115bb8",
   "metadata": {},
   "outputs": [],
   "source": [
    "transitions = {\n",
    "    ('healthy', 'relax'): [(0.95, 'healthy'), (0.05, 'sick')],\n",
    "    ('healthy', 'party'): [(0.7, 'healthy'), (0.3, 'sick')],\n",
    "    ('sick', 'relax'): [(0.5, 'healthy'), (0.5, 'sick')],\n",
    "    ('sick', 'party'): [(0.1, 'healthy'), (0.9, 'sick')]\n",
    "}"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5dad2ad5-cdb3-4d3f-9393-e0d8b5cf1c5d",
   "metadata": {},
   "source": [
    "- rewards: must be defined as a dictionary where, for each key-value pair, the key is a state-action-next_state pair (s,a,s'), and the value is the associated reward R(s,a,s'). If rewards are independent of next state - in the form R(s,a) -, then simply assign the same value for all effects s' of stochastic action a at state s."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7486958a-179f-4b3c-bb0a-aeca753abd66",
   "metadata": {},
   "outputs": [],
   "source": [
    "rewards = {\n",
    "    ('healthy', 'relax', 'healthy'): 7,\n",
    "    ('healthy', 'relax', 'sick'): 7,\n",
    "    ('healthy', 'party', 'healthy'): 10,\n",
    "    ('healthy', 'party', 'sick'): 10,\n",
    "    ('sick', 'relax', 'healthy'): 0,\n",
    "    ('sick', 'relax', 'sick'): 0,\n",
    "    ('sick', 'party', 'healthy'): 2,\n",
    "    ('sick', 'party', 'sick'): 2\n",
    " }"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0276c561-1108-4987-97fa-5f460fd79348",
   "metadata": {},
   "source": [
    "Once these are defined, one can use the value iteration implementation with default settings, and display the optimal policy and value function in an elegant way."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "accc12ec-14f5-4524-9835-b1ca86ba5275",
   "metadata": {},
   "outputs": [],
   "source": [
    "V, policy = val_iteration.val_iteration(states, actions, transitions, rewards)\n",
    "\n",
    "print(\"Optimal Value Function:\")\n",
    "for s in V:\n",
    "    print(f\"  {s}: {V[s]:.2f}\")\n",
    "\n",
    "print(\"\\nOptimal Policy:\")\n",
    "for s in policy:\n",
    "    print(f\"  {s}: {policy[s]}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "251cd3e6-5c37-4dc4-b326-464b3f651dc8",
   "metadata": {},
   "source": [
    "But what are the \"default settings\" here? Essentially, these are 3 values concerned with the iteration algorithm and termination:\n",
    "\n",
    "- gamma: Discount factor $\\gamma$. By default set to 0.8\n",
    "- theta: Convergence threshold $\\theta$. Iteration ends when $max_{s \\in S}|V_{k+1}(s) - V_k(s)| < \\theta$. By default set to $10^{-6}$\n",
    "- nr_iter: Maximum number of iterations. Must be non-zero. By default set to 100000.\n",
    "\n",
    "These can also be modified depending on the requirements of the problem."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "87a7e335-d105-409d-982c-50a610346fba",
   "metadata": {},
   "outputs": [],
   "source": [
    "gamma = 0.9\n",
    "theta = 1e-5\n",
    "nr_iter = 10000\n",
    "\n",
    "V, policy = val_iteration.val_iteration(states, actions, transitions, rewards, gamma, theta, nr_iter)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "dbec1ad8-bc0b-46f4-9cf0-a7194de8d02b",
   "metadata": {},
   "source": [
    "## Examples"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "59c78479-2450-47a2-bcc6-c499d564caac",
   "metadata": {},
   "source": [
    "To provide an even better understanding of the implementation, we also provide a folder with 2 [examples](https://github.com/VBercoV/val_iteration/tree/main/examples) where the MDP is set up and then the value iteration algorithm is applied.\n",
    "\n",
    "The first example, party.py, is taken from Example [9.27](https://artint.info/2e/html2e/ArtInt2e.Ch9.S5.html#Ch9.Thmciexamplered27) in [Artificial Intelligence: Foundations and Computational Agents 2nd edition](https://artint.info/2e/html2e/ArtInt2e.html). This is a simple MDP which models whether a student should party or relax over the weekend to avoid being sick, yet extract maximum enjoyment. For this example, running the [code](https://github.com/VBercoV/val_iteration/blob/main/examples/party.py) should reveal the exact answers as the theoretical values derived in the book, at Example 9.31 in Chapter [9.5.2](https://artint.info/2e/html2e/ArtInt2e.Ch9.S5.SS2.html)."
   ]
  },
  {
   "attachments": {
    "d608f4f4-447d-4a8f-9fd2-35d666e70b43.png": {
     "image/png": "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"
    }
   },
   "cell_type": "markdown",
   "id": "a31572bc-a2c9-417c-a616-357f0e32ea54",
   "metadata": {},
   "source": [
    "![exemple.png](attachment:d608f4f4-447d-4a8f-9fd2-35d666e70b43.png)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ba718494-b7e2-406a-a7ca-d99d7db684e6",
   "metadata": {},
   "source": [
    "The second example, gridworld.py, is taken from Example [9.28](https://artint.info/2e/html2e/ArtInt2e.Ch9.S5.html#Ch9.Thmciexamplered28) in [Artificial Intelligence: Foundations and Computational Agents 2nd edition](https://artint.info/2e/html2e/ArtInt2e.html). This MDP models a robot trying to move through (an idealization of) an environment, represented as a grid, collecting rewards along the way. Defining transitions and rewards turns out to be quite difficult, due to the data structure choice, but [not](https://github.com/VBercoV/val_iteration/blob/main/examples/gridworld.py) impossible."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
