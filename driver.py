import sys
import os
from agents import random_agent, greedy_agent, bottom_left_agent, flat_mc, test_agent, head_to_head
from mcts import mcts_agent
from game import cli_play_game

def refresh_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_readme():
    refresh_screen()
    print()
    print("2048 - Created by Chad Palmer for CPSC 474, Fall 2021")
    print()
    print("Usage:")
    print("./Driver -play")
    print("    Play the game yourself")
    print("./Driver -simulate [agent] [agent args]")
    print("    Simulate games with a given computational intelligence")
    print("    Available agents:")
    print("        r - random")
    print("        g - greedy (highest score after next turn)")
    print("        b - bottom left (choose first legal move in following order: left, down, right, up)")
    print("        f [number of games] - flat monte carlo (arg indicates how many random rollouts performed, evenly split between legal moves)")
    print("        m [number of iterations] - MCTS (arg indicates how many tree iterations performed)")
    print("    Optional additional args:")
    print("        -size [size] - Change size of game board (available to -play as well)")
    print("        -games [number of games] - Change number of games simulated (defaults to 1)")
    print("        -display - View games as they are played")
    print("./Driver -compete [agent1] [agent1 args] [agent2] [agent2 args]")
    print("    Compete two computational intelligences against each other")
    print("    Optional additional args from -simulate also available (except display)")
    print("./Driver -readme")
    print("    View this page")
    print()

def apology(message = "Input malformed, consult documentation or run ./Driver -readme"):
    print(message, file = sys.stderr)
    exit()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_readme()
        exit()
    
    if sys.argv[1] == '-play':
        if len(sys.argv) == 2:
            cli_play_game()
            exit()

        if sys.argv[2] != '-size':
            apology()
        
        try:
            size = int(sys.argv[3])
        except:
            apology("Size must be positive integer.")
        
        cli_play_game(size)
    elif sys.argv[1] == '-simulate':
        if len(sys.argv) < 3:
            apology()
        
        if sys.argv[2] == 'r':
            agent = random_agent()
        elif sys.argv[2] == 'g':
            agent = greedy_agent()
        elif sys.argv[2] == 'b':
            agent = bottom_left_agent()
        elif sys.argv[2] == 'f':
            try:
                games = int(sys.argv[3])
            except:
                apology("Missing games argument to agent.")
            if games < 1:
                apology("Games argument must be positive.")
            
            agent = flat_mc(games)
        elif sys.argv[2] == 'm':
            try:
                iterations = int(sys.argv[3])
            except:
                apology("Missing iterations argument to agent.")
            if iterations < 1:
                apology("Iterations argument must be positive.")
            
            agent = mcts_agent(iterations)
        else:
            apology("Agent not recognized.")

        gameCount = 1

        gamesIndex = None
        try:
            gamesIndex = sys.argv.index('-games') + 1
        except:
            pass
            
        if gamesIndex is not None:
            try:
                gameCount = int(sys.argv[gamesIndex])
            except:
                apology("Game count must be a positive integer.")

        boardSize = 4

        sizeIndex = None
        try:
            sizeIndex = sys.argv.index('-size') + 1
        except:
            pass
            
        if sizeIndex is not None:
            try:
                boardSize = int(sys.argv[sizeIndex])
            except:
                apology("Size must be a positive integer.")            
        
        display = ("-display" in sys.argv)

        test_agent(agent, gameCount, boardSize, display)
    elif sys.argv[1] == '-compete':
        if len(sys.argv) < 3:
            apology()
        
        if sys.argv[2] == 'r':
            agent1 = random_agent()
            i = 4
        elif sys.argv[2] == 'g':
            agent1 = greedy_agent()
            i = 4
        elif sys.argv[2] == 'b':
            agent1 = bottom_left_agent()
            i = 4
        elif sys.argv[2] == 'f':
            try:
                games = int(sys.argv[3])
            except:
                apology("Missing games argument to agent.")
            if games < 1:
                apology("Games argument must be positive.")
            
            agent1 = flat_mc(games)
            i = 5
        elif sys.argv[2] == 'm':
            try:
                iterations = int(sys.argv[3])
            except:
                apology("Missing iterations argument to agent.")
            if iterations < 1:
                apology("Iterations argument must be positive.")
            
            agent1 = mcts_agent(iterations)
            i = 5
        else:
            apology("Agent 1 not recognized.")

        if len(sys.argv) < i:
            apology()
        
        if sys.argv[i - 1] == 'r':
            agent2 = random_agent()
        elif sys.argv[i - 1] == 'g':
            agent2 = greedy_agent()
        elif sys.argv[i - 1] == 'b':
            agent2 = bottom_left_agent()
        elif sys.argv[i - 1] == 'f':
            try:
                games = int(sys.argv[i])
            except:
                apology("Missing games argument to agent.")
            if games < 1:
                apology("Games argument must be positive.")
            
            agent2 = flat_mc(games)
        elif sys.argv[i - 1] == 'm':
            try:
                iterations = int(sys.argv[i])
            except:
                apology("Missing iterations argument to agent.")
            if iterations < 1:
                apology("Iterations argument must be positive.")
            
            agent2 = mcts_agent(iterations)
        else:
            apology("Agent 2 not recognized.")

        gameCount = 1

        gamesIndex = None
        try:
            gamesIndex = sys.argv.index('-games') + 1
        except:
            pass
            
        if gamesIndex is not None:
            try:
                gameCount = int(sys.argv[gamesIndex])
            except:
                apology("Game count must be a positive integer.")

        boardSize = 4

        sizeIndex = None
        try:
            sizeIndex = sys.argv.index('-size') + 1
        except:
            pass
            
        if sizeIndex is not None:
            try:
                boardSize = int(sys.argv[sizeIndex])
            except:
                apology("Size must be a positive integer.")

        head_to_head(agent1, agent2, gameCount, boardSize)
    elif sys.argv[1] == '-readme':
        print_readme()
    else:
        apology()