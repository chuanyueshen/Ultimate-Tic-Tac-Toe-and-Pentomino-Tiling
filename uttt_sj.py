from time import sleep
from math import inf
from random import randint
from collections import Counter
import itertools

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

            diagonals.append([self.board[x][y], self.board[x + 1][x + 1], self.board[x + 2][y + 2]])
            diagonals.append([self.board[x][y + 2], self.board[x + 1][x + 1], self.board[x + 2][y]])

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

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score

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
            return self.evaluatePredefined(isMax)

        x, y = self.globalIdx[currBoardIdx]
        
        

        if isMax:
            player = "X"
        else:
            player = "O"
        
        succ = successors(self, currBoardIdx, player)
        best_move = (-inf, None)
        for s in succ:
            val = min_turn(s[1], opponent(player), depth-1,-inf, inf)
            if val > best_move[0]:
               best_move = (val, s)
 #        print("val = ", val)
 #        print_board(s[0])
        return best_move[1]
    
    def opponent(player):
        """
        This function returns the opponent of the current player
        """
        return "O" if player == "X" else "X"

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
        bestValue=0.0
        return bestValue

    def successors(self, currBoardIdx, player):
        """
        This function checks possible moves for the successor
        """
        succ = []
        moves_idx = []
        x, y = self.globalIdx[currBoardIdx]
        for xm, ym in self.moves:
            if self.board[x + xm][y + ym] == "_":
                moves_idx.append[x + xm, y + ym]
                succ.append(add_piece([x+xm, y + ym], player))
        return zip(succ, moves_idx)

    def add_piece(self, move, player):
        """
        This function adds the current player's move to the board
        """
        return self.board[: move] + player + self.board[move+1:]
    def get_currbd_idx(self, glb_idx):
        """
         This function takes the global index and returns the current boad index.
        """
        return glb_idx[0]//3 * 3 + glb_idx[1] // 3

    def min_turn(self, lst_mv, player, depth, alpha, beta):
        if depth <=0 or self.checkWinner() != 0:
            return evaluatePredefined(player)
        curr_bd_idx = get_currbd_idx(lst_mv)
        succ = successors(curr_bd_idx, player)
        
        for s in succ:
            val = max_turn(s[1], opponent(player), depth-1, alpha, beta)
            if val < beta:
                beta = val
            if alpha >= beta:
                break
        return beta

    def max_turn(self, lst_mv, player, depth, alpha, beta):
        if depth < 0 or self.checkWinner() != 0:
            return evaluatePredefined(self, player)
        curr_bd_idx = get_currbd_idx(lst_mv)
        succ = successors(curr_bd_idx, player)
        for s in succ:
            val = min_turn(s[1], opponent(player), depth -1, alpha, beta)
            if alpha < val:
                alpha = val
            if alpha >=beta:
                break
        return alpha 

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
        gameBoards=[]
        winner=0
        expandedNodes=[]
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
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

    def take_input(self, lst_mv):
        print("#" * 40)
        box_dict = {0: "Upper Left", 1: "Upper Center", 2: "Upper Right",
                    3: "Center Left", 4: "Center", 5: "Center Right",
                    6: "Bottom Left", 7: "Bottom Center", 8: "Bottom Right"}
        print("Where would you like to place 'X' in ~"
              + box_dict[get_currbd_idx(lst_mv)] + "~ box?")
        x = int(input("Row = "))
        if x == -1:
            raise SystemExit
        y = int(input("Col = "))
        print("")
        if bot_move != -1 and index(x, y) not in possible_moves(bot_move):
            raise ValueError
        if not valid_input(state, (x, y)):
            raise ValueError
        return (x, y)

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
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    uttt.board = [['X', '_', 'O', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                  ['O', '_', 'X', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', 'X', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', 'X', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                  ['_', '_', '_', '_', '_', 'O', 'O', 'X', 'O']]
    uttt.printGameBoard()

    print(uttt.checkWinner())
    print(uttt.checkMovesLeft())
    print(uttt.evaluatePredifined(True))
    print(uttt.evaluatePredifined(False))

    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
