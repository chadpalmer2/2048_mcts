import pdb
import random
import math

### helper functions

def ucbBestMove(position, table):
    if position._player == 1:
        minMove = None
        minVal = None

        for move in position.mcts_legal_moves():
            child = position.mcts_result(move)
            if not minMove or minVal > table[child]["totalVisits"]:
                minMove = move
                minVal = table[child]["totalVisits"]

        return minMove

    bestMove = -1
    ucb = None

    for move in position.mcts_legal_moves():
        childPosition = position.mcts_result(move)

        if table[childPosition]["totalVisits"] == 0 or table[position]["moveDict"][move]["edgeVisits"] == 0:
            return move

        exploit = table[childPosition]["totalReward"] / table[childPosition]["totalVisits"]
        explore = math.sqrt(0.5 * math.log(table[position]["totalVisits"]) / table[position]["moveDict"][move]["edgeVisits"])

        total = (exploit + explore)

        if not ucb or ucb < total:
            ucb = total
            bestMove = move

    return bestMove

def hasChildren(position, table):
    return ("moveDict" in table[position])

def addChildren(position, table):
    table[position]["moveDict"] = {}

    for move in position.mcts_legal_moves():
        table[position]["moveDict"][move] = { "edgeReward": 0, "edgeVisits": 0 }

        childPosition = position.mcts_result(move)

        if childPosition not in table:
            table[childPosition] = {
                "totalReward": 0,
                "totalVisits": 0
            }

def randomChild(position):
    return position.mcts_result(random.choice(position.mcts_legal_moves()))

def recommendation(position, table):
    bestMove = -1
    bestAvgVal = None

    if "moveDict" not in table[position]:
        return random.choice(position.mcts_legal_moves())

    for move, val in table[position]["moveDict"].items():
        if val["edgeVisits"] == 0:
            return move

        avgVal = val["edgeReward"] / val["edgeVisits"]

        if not bestAvgVal or bestAvgVal < avgVal:
            bestMove = move
            bestAvgVal = avgVal
    
    return bestMove

### mcts_strategy

def mcts_agent(iterations):

    def mcts_recommend_move(position):

        table = {
            position: {
                "totalReward": 0,
                "totalVisits": 0
            }
        }

        for i in range(iterations):

            # pass through tree, searching for leaf, adding children if node encountered without children explicitly populated
            path = []
            leaf = position

            while True:
                if leaf.game_over() or table[leaf]["totalVisits"] == 0:
                    break
                
                if not hasChildren(leaf, table):
                    addChildren(leaf, table)

                move = ucbBestMove(leaf, table)
                path.append(move)

                leaf = leaf.mcts_result(move)

            # simulate random game
            curr = leaf
            while not curr.game_over():
                curr = randomChild(curr)

            # Experimented with different value functions - score scled
            # value = math.log(curr.high_tile(), 2) / 15
            # value = curr.high_tile() / 131072
            # value = curr.score()
            value = curr.score() / 3932156

            # propagate new statistics from top
            curr = position

            for move in path:
                table[curr]["totalVisits"] += 1
                table[curr]["totalReward"] += value
                table[curr]["moveDict"][move]["edgeVisits"] += 1
                table[curr]["moveDict"][move]["edgeReward"] += value
                
                curr = curr.mcts_result(move)

            table[curr]["totalVisits"] += 1
            table[curr]["totalReward"] += value

        return recommendation(position, table)

    return mcts_recommend_move