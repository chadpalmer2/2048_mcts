import random
from enum import Enum
import os
import sys

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def reflect(m):
    return [row[::-1] for row in m]

class Board:
    def __init__(self, s = 4, fp = 0.1):
        ''' Creates a 2048 board of size s by s
        '''
        
        if s < 1:
            raise ValueError('Board dimension must be positive: %d' % s)
        
        self.size = s
        self.fp = fp

    def initial_position(self):
        tiles = [[0] * self.size for _ in range(self.size)]

        p = Board.Position(self, tiles)

        p = p.addRandomTile()
        p = p.addRandomTile()

        return p

    class Position:
        def __init__(self, board, tiles, score = 0, turn = 0):
            if board is None:
                raise ValueError('board cannot be None')

            if len(tiles) != board.size:
                raise ValueError('mismatch between size of tiles list and size of board: %d vs %d' % len(tiles), board.size)
            
            self._board = board
            self._tiles = tiles
            self._score = score
            self._turn = turn
            self._player = 0

            self._compute_hash()

        def duplicate(self):
            return Board.Position(self._board, [row[:] for row in self._tiles], score = self._score, turn = self._turn)

        def free_spaces(self):
            spaces = []

            for i in range(self._board.size):
                for j in range(self._board.size):
                    if self._tiles[i][j] == 0:
                        spaces.append((i, j))

            return spaces

        def addTile(self, i, j, val):
            succ = self.duplicate()
            succ._tiles[i][j] = val
            succ._player = 0

            return succ

        def addRandomTile(self):
            i, j = random.choice(self.free_spaces())

            if random.random() < self._board.fp:
                return self.addTile(i, j, 4)
            else:
                return self.addTile(i, j, 2)

        def _old_slide(self, move):
            ''' Attempt at speeding up slide by modifying array in-place - no faster '''

            succ = self.duplicate()

            # LEFT: i, j
            # RIGHT: i, -j - 1
            # UP: j, i
            # DOWN: j, -i - 1

            for i in range(succ._board.size):
                newRow = []

                justMerged = True
                for j in range(succ._board.size): 
                    if move == Direction.LEFT:
                        val = succ._tiles[i][j]
                    elif move == Direction.RIGHT:
                        val = succ._tiles[i][-j-1]
                    elif move == Direction.UP:
                        val = succ._tiles[j][i]
                    elif move == Direction.DOWN:
                        val = succ._tiles[-j-1][i]

                    if val != 0:
                        if not justMerged and val == newRow[-1]:
                            newRow[-1] *= 2
                            succ._score += newRow[-1]
                            justMerged = True
                        else:
                            newRow.append(val)
                            justMerged = False
                
                newRow += ([0] * (self._board.size - len(newRow)))

                for j in range(succ._board.size):
                    if move == Direction.LEFT:
                        succ._tiles[i][j] = newRow[j]
                    elif move == Direction.RIGHT:
                        succ._tiles[i][-j-1] = newRow[j]
                    elif move == Direction.UP:
                        succ._tiles[j][i] = newRow[j]
                    elif move == Direction.DOWN:
                        succ._tiles[-j-1][i] = newRow[j]

            if succ._tiles == self._tiles:
                return None

            succ._player = 1

            return succ

        def _compress(self, row):
            newRow = []
            
            justMerged = False
            for val in row:
                if val != 0:
                    if not len(newRow) == 0 and not justMerged and val == newRow[-1]:
                        newRow[-1] *= 2
                        self._score += newRow[-1]
                        justMerged = True
                        continue
                    
                    newRow.append(val)
                    justMerged = False

            return newRow + ([0] * (self._board.size - len(newRow)))

        def slide(self, move):
            succ = self.duplicate()

            transposed = (move == Direction.DOWN or move == Direction.UP)
            flipped = (move == Direction.RIGHT or move == Direction.DOWN)

            if transposed:
                succ._tiles = transpose(succ._tiles)
            if flipped:
                succ._tiles = reflect(succ._tiles)
            
            succ._tiles = [ succ._compress(row) for row in succ._tiles ]

            if flipped:
                succ._tiles = reflect(succ._tiles)
            if transposed:
                succ._tiles = transpose(succ._tiles)

            if succ._tiles == self._tiles:
                return None

            succ._player = 1

            return succ

        def result(self, move):
            succ = self.slide(move)

            if not succ:
                return None

            succ = succ.addRandomTile()
            succ._turn += 1

            return succ

        def score(self):
            return self._score

        def turn(self):
            return self._turn

        def high_tile(self):
            return max(max(row) for row in self._tiles)

        def game_over(self):
            return self._player == 0 and len(self.free_spaces()) == 0 and not self.slide(Direction.LEFT) and not self.slide(Direction.DOWN)

        def legal_moves(self):
            moves = []

            for direction in Direction:
                if self.slide(direction):
                    moves.append(direction)

            return moves

        def _compute_hash(self):
            self.hash = hash(tuple(tuple(row + [self._score, self._turn]) for row in self._tiles)) * 2 + self._player * 1

        def __hash__(self):
            return self.hash

        def __eq__(self, other):
            return isinstance(other, self.__class__) and self._tiles == other._tiles and self._turn == other._turn and self._board is other._board and self._score == other._score and self._player == other._player

        def print(self):
            for row in self._tiles:
                print(row)

        def mcts_legal_moves(self):
            ''' Version of function which splits sliding and tile placement into two turns for mcts '''
            
            if self._player == 0:
                return self.legal_moves()
            else:
                legal_moves = []
                for i, j in self.free_spaces():
                    legal_moves.append((i, j, 2))
                    legal_moves.append((i, j, 4))
                return legal_moves
        
        def mcts_result(self, move):
            ''' Version of function which splits sliding and tile placement into two turns for mcts '''

            if self._player == 0:
                return self.slide(move)
            else:
                return self.addTile(*move)

        def largest_tile_on_corner(self):
            ''' Testing some heuristics '''

            largest = self.high_tile()

            return largest in (self._tiles[0][0], self._tiles[-1][0], self._tiles[0][-1], self._tiles[-1][-1])

        def largest_tile_on_edge(self):
            ''' Testing some heuristics '''
            
            largest = self.high_tile()

            t_tiles = transpose(self._tiles)

            return largest in self._tiles[0] or largest in self._tiles[-1] or largest in t_tiles[0] or largest in t_tiles[-1]

def cli_play_game(size = 4):
    board = Board(size)
    pos = board.initial_position()

    message = "Select move (U/D/L/R/exit): "

    def refresh_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Score: { pos.score() }")
        pos.print()
        print(message)

    while not pos.game_over():
        refresh_screen()

        command = input()
        if command == "":
            message = "Invalid command. Select move (U/D/L/R/exit): "
            continue
        if command[0] in ["U", "u"]:
            succ = pos.result(Direction.UP)
        elif command[0] in ["D", "d"]:
            succ = pos.result(Direction.DOWN)
        elif command[0] in ["L", "l"]:
            succ = pos.result(Direction.LEFT)
        elif command[0] in ["R", "r"]:
            succ = pos.result(Direction.RIGHT)
        elif command[0] in ["E", "e", "Q", "q"]:
            print("Quitting...")
            exit()
        else:
            message = "Invalid command. Select move (U/D/L/R/exit): "
            continue
        
        if not succ:
            message = "Illegal move. Select move (U/D/L/R/exit): "
        else:
            pos = succ
            message = "Select move (U/D/L/R/exit): "

    message = "GAME OVER"
    refresh_screen()