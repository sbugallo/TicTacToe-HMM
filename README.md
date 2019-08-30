# Tic-Tac-Toe AI - Markov Decision Process

[![CodeFactor](https://www.codefactor.io/repository/github/sbugallo/tictactoe-hmm/badge)](https://www.codefactor.io/repository/github/sbugallo/tictactoe-hmm)
[![Build Status](https://travis-ci.com/sbugallo/TicTacToe-HMM.svg)](https://travis-ci.com/sbugallo/TicTacToe-HMM)
[![Coverage Status](https://coveralls.io/repos/github/sbugallo/TicTacToe-HMM/badge.svg?branch=master)](https://coveralls.io/github/sbugallo/TicTacToe-HMM?branch=master)

<img src="https://raw.githubusercontent.com/sbugallo/TicTacToe-HMM/maseter/docs/_static/logo-color.png" width="50%" />

## Game description

"Tic-tac-toe (American English), noughts and crosses (British English), or Xs and Os is a paper-and-pencil game for two
players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their
marks in a horizontal, vertical, or diagonal row wins the game."

-- Wikipedia

## Installation usage

See [documentation](https://sbugallo.github.io/TicTacToe-HMM/).

A docker image is available at [https://hub.docker.com/r/sbugallo/ttt](https://hub.docker.com/r/sbugallo/ttt). Simply
run `docker run -ti sbugallo/ttt` and then 

```bash
ttt-human-vs-cpu \
--cpu_weights_path pretrained_models/25000_15000_10000_weights.json \
--cpu_mode best
```