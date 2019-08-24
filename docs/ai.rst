.. _ai:

Markov Decision Processes
=========================

Introduction
------------

In an MDP, we have an agent that interacts with it's environment. These interactions occur sequentially over time. At
each time step, the agent will get some representation of the environment’s. Then, the agent selects an action to take.
The environment is then transitioned into a new state and the agent is given a reward as a consequence of the previous
action.

Components:

- Agent
- State
- Action
- Reward

The agent’s goal is to maximize the rewards that it receives from taking actions.

In an MDP, we have a set of states :math:`S`, a set of actions :math:`A`, and a set of rewards :math:`R`.

At each time step :math:`t=0,1,2,...`, the agent receives some representation of the environment’s state
:math:`S_t \in S`. Based on this state, the agent selects an action :math:`A_t \in A`.

Time is then incremented to the next time step :math:`t+1.`, and the environment is transitioned to a new state
:math:`S_{t+1} \in S`. At this time, the agent receives a numerical reward :math:`R_{t+1} \in S` for the action
:math:`A_t` taken from state :math:`S_t`.

Episodic tasks
--------------

TicTacToe is an episodic task, being each episode a round. In episodic tasks, each episode ends in a terminal state at
time :math:`T`, which is followed by resetting the environment to its initial state. The next episode then begins
independently from how the previous episode ended.

Exploration VS Exploitation
---------------------------

Think of a row of slot machines. Each machine has its own probability of winning. As a player you want to
make as much money as possible. How do you figure out which of the machine has the best odds, while
at the same time maximizing your profit? If you constantly played one of the machines (exploitation) you would never
learn anything about the odds of the other machines. If you always picked a machine at random (exploration) you would
learn a lot about the odds of each machine but probably wouldn’t make as much money as you could have always playing the
“best” machine.

Agents are trained using a mixed approach:

- First, an agent is trained playing against itself with random moves.
- Then, the agent is trained playing against itself with the best moves it learnt.
- Finally, the agent is trained playing against itself but this time it choses both random and best moves.

.. note:: Transition weights are updated at each round.
