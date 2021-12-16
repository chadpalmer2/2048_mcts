import os
import random
from game import Board, Direction

def random_agent():
    def policy(position):
        return random.choice(position.legal_moves())

    return policy

def greedy_agent():
    def policy(position):
        best_move = None
        best_score = None

        for move in position.legal_moves():
            score = position.result(move).score()

            if not best_move or score > best_score:
                best_move = move
                best_score = score
        
        return best_move

    return policy

def bottom_left_agent():
    def policy(position):
        for move in [Direction.LEFT, Direction.DOWN, Direction.RIGHT, Direction.UP]:
            if move in position.legal_moves():
                return move

    return policy


def flat_mc(games):
    def policy(position):
        best_move = None
        best_total_score = None

        for move in position.legal_moves():
            total_score = 0

            for _ in range(games // len(position.legal_moves())):
                succ = position.result(move)

                while not succ.game_over():
                    succ = succ.result(random.choice(succ.legal_moves()))
                
                total_score += succ.score()
            
            if not best_move or total_score > best_total_score:
                best_move = move
                best_total_score = total_score

        return best_move
    
    return policy

def test_agent(policy, games = 1, size = 4, display = False):
    ''' Plays 2048 on a board of size "size" with a given policy for "games" number of games
    '''

    board = Board(size)

    if games < 1:
        return

    totalTurns = 0
    totalScore = 0
    highTiles = {}

    for i in range(games):
        position = board.initial_position()

        def refresh_screen():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Score: { position.score() }")
            position.print()

        while not position.game_over():
            if display:
                refresh_screen()

            position = position.result(policy(position))

        if display:
            refresh_screen()

        totalTurns += position.turn()
        totalScore += position.score()
        highTile = position.high_tile()

        if highTile in highTiles:
            highTiles[highTile] += 1
        else:
            highTiles[highTile] = 1
        
    print(f"Average score: { totalScore / games }")
    print(f"Average turn count: { totalTurns / games }")
    print(f"High tile distribution:")
    for tile, count in sorted(highTiles.items(), reverse=True):
        print(f"{ tile }: { count } ({count * 100 / games}%)")

def head_to_head(policy1, policy2, games = 1, size = 4):
    ''' Pits two policies against each other, reports win rate of first policy '''

    board = Board(size)

    if games < 1:
        return

    win1 = 0
    win2 = 0
    draw = 0

    for i in range(games):
        position = board.initial_position()

        while not position.game_over():
            position = position.result(policy1(position))

        score1 = position.score()

        position = board.initial_position()

        while not position.game_over():
            position = position.result(policy2(position))

        score2 = position.score()

        if score1 > score2:
            win1 += 1
        elif score1 < score2:
            win2 += 1
        else:
            draw += 1

        
    print(f"Policy 1 win rate: { win1 / games }")