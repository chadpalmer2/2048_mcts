2048

Created by Chad Palmer for CPSC 474, Fall 2021

Overview:

This is an application which can play 2048 and simulate games of 2048 with a variety of different computational intelligences, the highest performing of which is MCTS. With MCTS with 1000 iterations (./Driver -simulate m 1000 -display), the agent achieves scores comparable to a skilled human player (usually wins, occasionally achieves the 4096 tile). Flat Monte Carlo also works very well. The entire program runs a bit slower than I would like; that the 2048 game tree is very deep and moves require matrix operations slowed down execution time such that running the same number of games as MCTS for Kalah was infeasible. (A potential speedup could be implementing the game as bitboards and introducing a move lookup table to prevent unnecessary overcalculation, but that is a project for another day.) All code is my own; mcts.py is adapted to single-player, stochastic play from my work on the Kalah project.

Usage:

./Driver -readme
    View this page
./Driver -play
    Play the game yourself
./Driver -simulate [agent] [agent args]
    Simulate games with a given computational intelligence
    Available agents:
        r - random
        g - greedy (highest score after next turn)
        b - bottom left (choose first legal move in following order: left, down, right, up)
        f [number of games] - flat monte carlo (arg indicates how many random rollouts performed, evenly split between legal moves)
        m [number of iterations] - MCTS (arg indicates how many tree iterations performed)
    Optional additional args:
        -size [size] - Change size of game board (available to -play as well)
        -games [number of games] - Change number of games simulated (defaults to 1)
        -display - View games as they are played (can slow down execution)
./Driver -compete [agent1] [agent1 args] [agent2] [agent2 args]
    Compete two computational intelligences against each other (win condition is a higher score)
    Optional additional args from -simulate also available (except display)

Sample commands:

./Driver -readme
./Driver -play
./Driver -play -size 3
./Driver -simulate r -display
./Driver -simulate r -games 1000
./Driver -simulate f 100 -display
./Driver -simulate m 1000 -display
./Driver -compete r r -games 1000
./Driver -compete b g -games 1000
./Driver -compete g m 100

...

Thank you for a great semester!
- Chad