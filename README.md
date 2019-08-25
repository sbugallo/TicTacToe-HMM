# Tic-Tac-Toe AI - Markov Decision Process

[![CodeFactor](https://www.codefactor.io/repository/github/sbugallo/tictactoe-mdp/badge)](https://www.codefactor.io/repository/github/sbugallo/tictactoe-mdp)
[![Build Status](https://travis-ci.com/sbugallo/TicTacToe-MDP.svg)](https://travis-ci.com/sbugallo/TicTacToe-MDP)
[![Coverage Status](https://coveralls.io/repos/github/sbugallo/TicTacToe-MDP/badge.svg?branch=dev)](https://coveralls.io/github/sbugallo/TicTacToe-MDP?branch=dev)

<img src="https://raw.githubusercontent.com/sbugallo/TicTacToe-MDP/dev/docs/_static/logo-color.png" width="50%" />

See [documentation](https://sbugallo.github.io/TicTacToe-MDP/)
## Game description

"Tic-tac-toe (American English), noughts and crosses (British English), or Xs and Os is a paper-and-pencil game for two
players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their
marks in a horizontal, vertical, or diagonal row wins the game."

-- Wikipedia

## Installation

### Prerequisites

- `conda` (included in Miniconda 3 and Anaconda 3 distributions)

### Steps

#### Clone the ttt's repository

```bash
git clone https://github.com/sbugallo/TicTacToe-MDP.git
cd TicTacToe-MDP
```

The following instructions assume that you are located in the root of `TicTacToe-MDP'`.

#### Install requirements

`conda` is the recommended way for installing all the requirements. You can install `conda` from
[this link](https://docs.conda.io/en/latest/miniconda.html). The following instructions assume that you have
conda installed on your system.

Predefined conda environments for different use cases are provided under `./envs`. There are 2
available environments:

- **dev.yml**: for simple execution usage.
- **prod.yml**: to generate docs, test and develope new features.

You can create a new conda environment as follows:

```bash
conda env create -f ./envs/{dev.yml | prod.yml}
```

Usage examples:

```bash
conda env create -f ./envs/dev.yml
conda env create -f ./envs/prod.yml
```

Once our environment is installed, we have to activate it running the following:

```bash
source activate ttt
```

Assuming that you have the environment activated, we install `ttt` module running:

```bash
python setup.py install
```

If you plan to modify de source code, run some tests or generate documentation you should install the module in
development mode:

```bash
python setup.py develop
```  

This will also install some scripts that can be run directly in your terminal:

- `ttt-human-vs-human`
- `ttt-human-vs-cpu`
- `ttt-cpu-vs-cpu`
- `ttt-train`

To see how they work, please go to Usage section

### Docker

To facilitate the usage, a docker image is available at
[https://hub.docker.com/r/sbugallo/ttt](https://hub.docker.com/r/sbugallo/ttt).

#### Prerequisites

 - `docker` (see [https://docs.docker.com/install/](https://docs.docker.com/install/))

## Usage

### Train agent

To train an agent simply run the following command:

```bash
ttt-train \
    --output_path <path where to save weights | str>\
    --lr <learning rate | float | Default: 0.1>\
    --exploration_iterations <number of games to be played during exploration phase | int | Default: 2500> \
    --exploitation_iterations <number of games to be played during exploitation phase | int | Default: 1500> \
    --exploration_exploitation_iterations <number of games to be played during exploration-exploitation phase | int | Default: 1000>

```

Example:

```bash
ttt-train \
    --output_path /home/sbugallo/Documents/weights.json \
    --lr 0.1 \
    --exploration_iterations 2500 \
    --exploitation_iterations 1500 \
    --exploration_exploitation_iterations 1000
```

### Play game CPU vs CPU

To make 2 CPU agents play a game, run the following command:

```bash
ttt-cpu-vs-cpu \
    ---cpu_1_weights_path <path from where to load weights | str> \
    ---cpu_1_mode <random or best | str> \
    ---cpu_2_weights_path <path from where to load weights | str> \
    ---cpu_2_mode <random or best | str> \
    ---num_rounds <number of rounds to be played | int> \
    ---display_board <whether to display the board with each move | bool | Default: True>
```

Example:

```bash
ttt-cpu-vs-cpu \
    ---cpu_1_weights_path /home/sbugallo/Documents/weights_1.json \
    ---cpu_1_mode best \
    ---cpu_2_weights_path /home/sbugallo/Documents/weights_2.json \
    ---cpu_2_mode best \
    ---num_rounds 5 \
    ---display_board True
```

### Play game Human vs CPU

To play a game against a CPU simply run the following command:

```bash
ttt-human-vs-cpu \
    --cpu_weights_path <path from where to load weights | str> \
    --cpu_mode <random or best | str>
```

Example:

```bash
ttt-human-vs-cpu \
    --cpu_weights_path /home/sbugallo/Documents/weights.json \
    --cpu_mode best
```

### Play game Human vs Human

```bash
ttt-human-vs-human
```

### Docker

First, we run the app with an interactive terminal as follows:

```bash
docker run -ti sbugallo/ttt
```

This will let you execute some commands in the running Docker container. This terminal will already have the conda
environment activated and will be inside the project's root. In this interactive terminal you will be able to run the
examples showed above.

## AI description

### Introduction

CPU agents are a simple implementation of a Markov Decision Process (MDP). In this algorithm, we have an agent that 
interacts with it's environment. These interactions occur sequentially over time. At each time step, the agent will get 
some representation of the environment’s. Then, the agent selects an action to take. The environment is then 
transitioned into a new state and the agent is given a reward as a consequence of the previous action.

Components:

- Agent
- State
- Action
- Reward

The agent’s goal is to maximize the rewards that it receives from taking actions.

In an MDP, we have a set of states S, a set of actions A, and a set of rewards R.

At each time step t=0,1,2,..., the agent receives some representation of the environment’s state
S_t ∈ S. Based on this state, the agent selects an action A_t ∈ A.

Time is then incremented to the next time step t+1., and the environment is transitioned to a new state
S_{t+1} ∈ S. At this time, the agent receives a numerical reward R_{t+1} ∈ R for the action
A_t taken from state S_t.

### Episodic tasks

TicTacToe is an episodic task, being each episode a round. In episodic tasks, each episode ends in a terminal state at
time T, which is followed by resetting the environment to its initial state. The next episode then begins
independently from how the previous episode ended.

### Exploration VS Exploitation

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

**Note**: Transition weights are updated at each round.
