from time import sleep
from math import inf
from collections import defaultdict
from random import randint, choice

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]

        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)
        self.curt_board_idx = 0
        self.box_dict = {0: "Upper Left", 1: "Upper Center", 2: "Upper Right",
                    3: "Center Left", 4: "Center", 5: "Center Right",
                    6: "Bottom Left", 7: "Bottom Center", 8: "Bottom Right"}

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True
        self.curt_evaluation = self.evaluatePredifined

        self.moves = list((x, y) for x in range(3) for y in range(3))

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def two_in_row(self, isMax):
        """
        :return: the number of unblocked two-in-row for the player
                 and the number of blocked two-in-row for the opponent
        """
        mine, yours = 'O', 'X'
        mine_unblocked, yours_blocked = 0, 0

        if isMax:
            mine, yours = yours, mine

        for x, y in self.globalIdx:
            diagonals, rows, columns = list(), list(), list()

            diagonals.append([self.board[x][y], self.board[x + 1][y + 1], self.board[x + 2][y + 2]])
            diagonals.append([self.board[x][y + 2], self.board[x + 1][y + 1], self.board[x + 2][y]])

            for row in range(3):
                rows.append([self.board[x + row][y], self.board[x + row][y + 1], self.board[x + row][y + 2]])

            for column in range(3):
                columns.append([self.board[x][y + column], self.board[x + 1][y + column], self.board[x + 2][y + column]])

            for line in diagonals + rows + columns:
                if line.count(mine) == 2 and line.count(yours) == 0:
                    mine_unblocked += 1
                if line.count(yours) == 2 and line.count(mine) == 1:
                    yours_blocked += 1

        return mine_unblocked, yours_blocked

    def corner_taken(self, isMax):
        if isMax:
            mine = 'X'
        else:
            mine = 'O'

        num_corner_taken = 0

        for x, y in self.globalIdx:
            if self.board[x][y] == mine:
                num_corner_taken += 1

            if self.board[x + 2][y] == mine:
                num_corner_taken += 1

            if self.board[x][y + 2] == mine:
                num_corner_taken += 1

            if self.board[x + 2][y + 2] == mine:
                num_corner_taken += 1

        return num_corner_taken

    def center_taken(self, isMax):
        if isMax:
            mine = 'X'
        else:
            mine = 'O'

        num_center_taken = 0

        for x, y in self.globalIdx:
            if self.board[x + 1][y + 1] == mine:
                num_center_taken += 1

        return num_center_taken

    def side_taken(self, isMax):
        if isMax:
            mine = 'X'
        else:
            mine = 'O'

        num_side_taken = 0

        for x, y in self.globalIdx:
            if self.board[x][y + 1] == mine:
                num_side_taken += 1
            if self.board[x + 1][y] == mine:
                num_side_taken += 1
            if self.board[x + 2][y + 1] == mine:
                num_side_taken += 1
            if self.board[x + 1][y + 2] == mine:
                num_side_taken += 1

        return num_side_taken

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        if isMax:
            if self.checkWinner() == 1:
                return self.winnerMaxUtility

            mine_unblocked, yours_blocked = self.two_in_row(isMax)
            if mine_unblocked or yours_blocked:
                return mine_unblocked * self.twoInARowMaxUtility + yours_blocked * self.preventThreeInARowMaxUtility

            return self.corner_taken(isMax) * self.cornerMaxUtility
        else:
            if self.checkWinner() == -1:
                return self.winnerMinUtility

            mine_unblocked, yours_blocked = self.two_in_row(isMax)
            if mine_unblocked or yours_blocked:
                return mine_unblocked * self.twoInARowMinUtility + yours_blocked * self.preventThreeInARowMinUtility

            return self.corner_taken(isMax) * self.cornerMinUtility

    def check_will_lose(self):
        mine, yours = 'O', 'X'
        x, y = self.globalIdx[self.curt_board_idx]

        diagonals, rows, columns = list(), list(), list()

        diagonals.append([self.board[x][y], self.board[x + 1][y + 1], self.board[x + 2][y + 2]])
        diagonals.append([self.board[x][y + 2], self.board[x + 1][y + 1], self.board[x + 2][y]])

        for row in range(3):
            rows.append([self.board[x + row][y], self.board[x + row][y + 1], self.board[x + row][y + 2]])

        for column in range(3):
            columns.append([self.board[x][y + column], self.board[x + 1][y + column], self.board[x + 2][y + column]])

        for line in diagonals + rows + columns:
            if line.count(yours) == 2 and line.count(mine) == 0:
                return True

        return False

    # def evaluateDesigned(self, isMax):
    #     """
    #     This function implements the evaluation function for ultimate tic tac toe for your own agent.
    #     input args:
    #     isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
    #                  True for maxPlayer, False for minPlayer
    #     output:
    #     score(float): estimated utility score for maxPlayer or minPlayer
    #     """
    #     #YOUR CODE HERE
    #     if self.checkWinner() == 1:
    #         return float('inf')
    #
    #     if self.checkWinner() == -1:
    #         return -float('inf')
    #
    #     mine_unblocked, yours_blocked = self.two_in_row(isMax)
    #     if mine_unblocked or yours_blocked:
    #         return mine_unblocked * (-500) + yours_blocked * (-50)
    #
    #     return self.corner_taken(isMax) * (-30)

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        if self.checkWinner() == 1:
            return float('inf')

        if self.checkWinner() == -1:
            return -float('inf')

        utility = 0
        # two-in-a-row
        mine_unblocked, yours_blocked = self.two_in_row(False)
        if mine_unblocked or yours_blocked:
            utility -= mine_unblocked * 200 + yours_blocked * 100

        yours_unblocked, mine_blocked = self.two_in_row(True)
        if mine_unblocked or yours_blocked:
            utility += yours_unblocked * 200 + mine_blocked * 100

        # corner
        utility += self.corner_taken(True) * 30 + self.corner_taken(False) * (-30)

        # center
        utility += self.center_taken(True) * 60 + self.center_taken(False) * (-60)

        # side
        utility += self.side_taken(True) * 10 + self.side_taken(False) * (-10)

        return utility


    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        return any(self.board[x][y] == '_' for x in range(len(self.board)) for y in range(len(self.board[0])))

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        for x, y in self.globalIdx:
            if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2] \
             or self.board[x][y + 2] == self.board[x + 1][y + 1] == self.board[x + 2][y]:
                if self.board[x + 1][y + 1] == 'X':
                    return 1
                elif self.board[x + 1][y + 1] == 'O':
                    return -1

            for row in range(3):
                if self.board[x + row][y] == self.board[x + row][y + 1] == self.board[x + row][y + 2]:
                    if self.board[x + row][y] == 'X':
                        return 1
                    elif self.board[x + row][y] == 'O':
                        return -1

            for column in range(3):
                if self.board[x][y + column] == self.board[x + 1][y + column] == self.board[x + 2][y + column]:
                    if self.board[x][y + column] == 'X':
                        return 1
                    elif self.board[x][y + column] == 'O':
                        return -1

        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        self.expandedNodes += 1

        if depth == self.maxDepth:
            return self.curt_evaluation(isMax)

        x, y = self.globalIdx[currBoardIdx]

        if (isMax and depth % 2 == 1) or (not isMax and depth % 2 == 0):
            # the situation where we look for the minimum value
            curt_move = 'O'
            curt_best = float('inf')
        else:
            curt_move = 'X'
            curt_best = -float('inf')

        for xd, yd in self.moves:
            if self.board[x + xd][y + yd] != '_':
                continue

            self.board[x + xd][y + yd] = curt_move
            nxt_local_board = xd * 3 + yd
            new_best = self.alphabeta(depth + 1, nxt_local_board, alpha, beta, isMax)
            self.board[x + xd][y + yd] = '_'

            if (isMax and depth % 2 == 1) or (not isMax and depth % 2 == 0):
                curt_best = min(curt_best, new_best)
                if curt_best <= alpha:
                    return curt_best
                beta = min(beta, curt_best)

            else:
                curt_best = max(curt_best, new_best)
                if curt_best >= beta:
                    return curt_best
                alpha = max(alpha, curt_best)

        return curt_best

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        self.expandedNodes += 1

        if depth == self.maxDepth:
            return self.curt_evaluation(isMax)

        x, y = self.globalIdx[currBoardIdx]

        if (isMax and depth % 2 == 1) or (not isMax and depth % 2 == 0):
            # the situation where we look for the minimum value
            curt_move = 'O'
            curt_best = float('inf')
        else:
            curt_move = 'X'
            curt_best = -float('inf')

        for xd, yd in self.moves:
            if self.board[x + xd][y + yd] != '_':
                continue

            self.board[x + xd][y + yd] = curt_move
            nxt_local_board = xd * 3 + yd
            new_best = self.minimax(depth + 1, nxt_local_board, isMax)
            self.board[x + xd][y + yd] = '_'

            if (isMax and depth % 2 == 1) or (not isMax and depth % 2 == 0):
                curt_best = min(curt_best, new_best)
            else:
                curt_best = max(curt_best, new_best)

        return curt_best

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards = []
        expandedNodes = []
        winner=0

        isMax = True
        if not maxFirst:
            isMax = False

        if isMinimaxOffensive:
            offensive_algo = self.minimax
        else:
            offensive_algo = self.alphabeta

        if isMinimaxDefensive:
            defensive_algo = self.minimax
        else:
            defensive_algo = self.alphabeta

        curt_local_board = self.startBoardIdx

        while self.checkMovesLeft():
            winner = self.checkWinner()
            if winner:
                break

            self.expandedNodes = 0

            if isMax:
                curt_move = 'X'
                curt_algo = offensive_algo
                curt_best = -float('inf')
            else:
                curt_move = 'O'
                curt_algo = defensive_algo
                curt_best = float('inf')

            x, y = self.globalIdx[curt_local_board]
            best_x, best_y = self.globalIdx[curt_local_board]

            for xd, yd in self.moves:
                if self.board[x + xd][y + yd] != '_':
                    continue

                self.board[x + xd][y + yd] = curt_move
                if curt_algo == self.minimax:
                    new_best = curt_algo(1, xd * 3 + yd, isMax)
                else:
                    new_best = curt_algo(1, xd * 3 + yd, -float('inf'), float('inf'), isMax)

                self.board[x + xd][y + yd] = '_'

                if isMax:
                    if new_best > curt_best:
                        curt_best = new_best
                        best_x, best_y = x + xd, y + yd
                else:
                    if new_best < curt_best:
                        curt_best = new_best
                        best_x, best_y = x + xd, y + yd

            self.board[best_x][best_y] = curt_move

            bestMove.append((best_x, best_y))
            bestValue.append(curt_best)
            expandedNodes.append(self.expandedNodes)
            gameBoards.append([row[:] for row in self.board])

            isMax = not isMax
            curt_local_board = (best_x - x) * 3 + (best_y - y)

        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards = []
        expandedNodes = []
        winner=0

        offensive_algo = self.alphabeta
        defensive_algo = self.alphabeta

        curt_board_idx = randint(0, 8)
        isMax = choice([True, False])

        if not isMax:
            self.curt_evaluation = self.evaluateDesigned

        while self.checkMovesLeft():
            winner = self.checkWinner()
            if winner:
                break

            self.expandedNodes = 0

            if isMax:
                curt_move = 'X'
                curt_algo = offensive_algo
                curt_best = -float('inf')
            else:
                curt_move = 'O'
                curt_algo = defensive_algo
                curt_best = float('inf')

            x, y = self.globalIdx[curt_board_idx]
            best_x, best_y = self.globalIdx[curt_board_idx]

            for xd, yd in self.moves:
                if self.board[x + xd][y + yd] != '_':
                    continue

                self.board[x + xd][y + yd] = curt_move
                if curt_algo == self.minimax:
                    new_best = curt_algo(1, xd * 3 + yd, isMax)
                else:
                    new_best = curt_algo(1, xd * 3 + yd, -float('inf'), float('inf'), isMax)

                self.board[x + xd][y + yd] = '_'

                if isMax:
                    if new_best > curt_best:
                        curt_best = new_best
                        best_x, best_y = x + xd, y + yd
                else:
                    if new_best < curt_best:
                        curt_best = new_best
                        best_x, best_y = x + xd, y + yd

            self.board[best_x][best_y] = curt_move

            bestMove.append((best_x, best_y))
            gameBoards.append([row[:] for row in self.board])
            expandedNodes.append(self.expandedNodes)

            isMax = not isMax
            curt_board_idx = (best_x - x) * 3 + (best_y - y)

            if self.curt_evaluation == self.evaluatePredifined:
                self.curt_evaluation = self.evaluateDesigned
            else:
                self.curt_evaluation = self.evaluatePredifined

        print(expandedNodes)

        return gameBoards, bestMove, winner

    def human_input(self, curr_bd_idx):
        print("Where would you like to place 'X' in the "
                + self.box_dict[curr_bd_idx] + " local board?")
        x = int(input("Row = "))
        y = int(input("Col = "))
        print("")
        x_bd, y_bd = self.globalIdx[curr_bd_idx]
        if (x < 0 or x > 2) or (y < 0 or y > 2):
            print('Invalid input! Please input 0, 1, or 2.')
            return self.human_input(curr_bd_idx)
        if self.board[x_bd + x][y_bd + y] != "_":
            print('Invalid coordinates! Try again.')
            return self.human_input(curr_bd_idx)
        return x_bd + x, y_bd + y, x, y

    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards = []
        winner=0

        curt_board_idx = randint(0, 8)
        isMax = choice([True, False])
        players = {True: 'you', False: 'the AI'}
        self.curt_evaluation = self.evaluateDesigned

        print('The initial starting local board is the {} board.'.format(self.box_dict[curt_board_idx]))
        print('The initial first player is {}.'.format(players[isMax]))

        while self.checkMovesLeft():
            winner = self.checkWinner()
            print('The current local board is the {} board.'.format(self.box_dict[curt_board_idx]))
            print('The current player is {}.'.format(players[isMax]))
            print('The current board is:')
            self.printGameBoard()

            if winner:
                break

            if isMax:
                x, y, xd, yd = self.human_input(curt_board_idx)
                self.board[x][y] = 'X'
                bestMove.append((x, y))
                gameBoards.append([row[:] for row in self.board])
                isMax = not isMax
                curt_board_idx = xd * 3 + yd
                continue

            curt_move = 'O'
            curt_best = float('inf')

            x, y = self.globalIdx[curt_board_idx]
            best_x, best_y = self.globalIdx[curt_board_idx]

            for xd, yd in self.moves:
                if self.board[x + xd][y + yd] != '_':
                    continue

                self.board[x + xd][y + yd] = curt_move
                new_best = self.alphabeta(1, xd * 3 + yd, -float('inf'), float('inf'), isMax)

                self.board[x + xd][y + yd] = '_'

                if new_best < curt_best:
                    curt_best = new_best
                    best_x, best_y = x + xd, y + yd

            self.board[best_x][best_y] = curt_move
            print("The AI decided to put {} on coordinates ({}, {}).".format(curt_move, best_x, best_y))

            bestMove.append((best_x, best_y))
            gameBoards.append([row[:] for row in self.board])

            isMax = not isMax
            curt_board_idx = (best_x - x) * 3 + (best_y - y)

        if winner == 0:
            print('This Game is a Tie!')
        elif winner == -1:
            print('Game Over. You Lose!')
        else:
            print('Congrats! You Win!')

        return gameBoards, bestMove, winner

    # extra credit
    def checkWinner_new_rule(self, w):
        if (0 in w and 4 in w and 8 in w and w[0] == w[4] == w[8]) \
                or (2 in w and 4 in w and 6 in w and w[2] == w[4] == w[6]):
            return w[4]

        for i in [0, 3, 6]:
            if i in w and i + 1 in w and i + 2 in w and w[i] == w[i + 1] == w[i + 2]:
                return w[i]

        for i in range(3):
            if i in w and i + 3 in w and i + 6 in w and w[i] == w[i + 3] == w[i + 6]:
                return w[i]

        return 0

    def check_local_board(self, w, x, y):
        local_board_idx = 3 * (x % 3) + y % 3
        x, y = self.globalIdx[local_board_idx]

        if self.board[x][y] == self.board[x + 1][y + 1] == self.board[x + 2][y + 2] \
         or self.board[x][y + 2] == self.board[x + 1][y + 1] == self.board[x + 2][y]:
            if self.board[x + 1][y + 1] == 'X':
                w[local_board_idx] = 1
                return
            elif self.board[x + 1][y + 1] == 'O':
                w[local_board_idx] = -1
                return

        for row in range(3):
            if self.board[x + row][y] == self.board[x + row][y + 1] == self.board[x + row][y + 2]:
                if self.board[x + row][y] == 'X':
                    w[local_board_idx] = 1
                    return
                elif self.board[x + row][y] == 'O':
                    w[local_board_idx] = -1
                    return

        for column in range(3):
            if self.board[x][y + column] == self.board[x + 1][y + column] == self.board[x + 2][y + column]:
                if self.board[x][y + column] == 'X':
                    w[local_board_idx] = 1
                    return
                elif self.board[x][y + column] == 'O':
                    w[local_board_idx] = -1
                    return

    def check_vacancy(self, local_board_idx):
        x, y = self.globalIdx[local_board_idx]
        return any(self.board[x + xd][y + yd] == '_' for xd in range(3) for yd in range(3))

    def evaluate_new(self, isMax, w, x, y):
        new_w = dict(w)
        self.check_local_board(new_w, x, y)
        if len(new_w) != len(w):
            if self.checkWinner_new_rule(new_w):
                if isMax:
                    return 10000
                else:
                    return -10000

            if isMax:
                return 2000
            else:
                return -2000

        move = 'X'
        if not isMax:
            move = 'O'

        self.board[x][y] == move

        if isMax:
            mine_unblocked, yours_blocked = self.two_in_row(isMax)
            if mine_unblocked or yours_blocked:
                self.board[x][y] = '_'
                return mine_unblocked * self.twoInARowMaxUtility + yours_blocked * self.preventThreeInARowMaxUtility

            self.board[x][y] = '_'
            return self.corner_taken(isMax) * self.cornerMaxUtility
        else:
            mine_unblocked, yours_blocked = self.two_in_row(isMax)
            if mine_unblocked or yours_blocked:
                self.board[x][y] = '_'
                return mine_unblocked * self.twoInARowMinUtility + yours_blocked * self.preventThreeInARowMinUtility

            self.board[x][y] = '_'
            return self.corner_taken(isMax) * self.cornerMinUtility

    def playGameNewRule(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        bestMove = []
        gameBoards = []
        expandedNodes = []
        winner = 0

        offensive_algo = self.alphabeta
        defensive_algo = self.alphabeta

        curt_board_idx = [randint(0, 8)]
        isMax = choice([True, False])

        self.curt_evaluation = self.evaluate_new
        won_local_board = defaultdict(int)

        while self.checkMovesLeft():
            print(won_local_board)
            winner = self.checkWinner_new_rule(won_local_board)
            if winner:
                break

            self.expandedNodes = 0

            if isMax:
                curt_move = 'X'
                curt_algo = offensive_algo
                curt_best = -float('inf')
            else:
                curt_move = 'O'
                curt_algo = defensive_algo
                curt_best = float('inf')

            best_x, best_y = 0, 0
            best_xd, best_yd = 0, 0

            if len(curt_board_idx) == 1 and not self.check_vacancy(curt_board_idx[0]):
                curt_board_idx = [idx for idx in range(9) if idx not in won_local_board]

            for idx in curt_board_idx:

                x, y = self.globalIdx[idx]

                for xd, yd in self.moves:
                    if self.board[x + xd][y + yd] != '_':
                        continue

                    self.board[x + xd][y + yd] = curt_move
                    if curt_algo == self.minimax:
                        new_best = self.curt_evaluation(isMax, won_local_board, x + xd, y + yd)
                    else:
                        new_best = self.curt_evaluation(isMax, won_local_board, x + xd, y + yd)

                    self.board[x + xd][y + yd] = '_'

                    if isMax:
                        if new_best > curt_best:
                            curt_best = new_best
                            best_x, best_y = x + xd, y + yd
                            best_xd, best_yd = xd, yd
                    else:
                        if new_best < curt_best:
                            curt_best = new_best
                            best_x, best_y = x + xd, y + yd
                            best_xd, best_yd = xd, yd

            self.board[best_x][best_y] = curt_move

            bestMove.append((best_x, best_y))
            gameBoards.append([row[:] for row in self.board])
            expandedNodes.append(self.expandedNodes)

            isMax = not isMax
            curt_board_idx = [best_xd * 3 + best_yd]

            if curt_board_idx[0] in won_local_board:
                curt_board_idx = [idx for idx in range(9) if idx not in won_local_board]

            self.check_local_board(won_local_board, best_x, best_y)

            if not curt_board_idx:
                break

        print(expandedNodes)

        return gameBoards, bestMove, winner


if __name__=="__main__":
    uttt=ultimateTicTacToe()

    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    print(expandedNodes)
    print(gameBoards)
    print(bestMove)
    print(bestValue)

    uttt.printGameBoard()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")

    # win = 0
    # print("running")
    # for i in range(100):
    #     uttt = ultimateTicTacToe()
    #     if uttt.playGameYourAgent()[2] == -1:
    #         win += 1
    #
    # print("In 100 games, your agent winning times:")
    # print(win)

    # uttt = ultimateTicTacToe()
    # _, m, w = uttt.playGameNewRule()
    # print(m)
    # print(w)
    # uttt.printGameBoard()