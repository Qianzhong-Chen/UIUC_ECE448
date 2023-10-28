from time import sleep
from math import inf
from random import randint
import time

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

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    
    def evaluatePredifined(self, isMax):
        '''
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        '''
        #YOUR CODE HERE
        score=0
        # maxPlayer
        if isMax: 
            if self.checkWinner() == 1:
                return self.winnerMaxUtility
            # *check for first rule*
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility

                # in a col
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility

                # in a diag
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
            if score != 0:
                return score
            
            # *check for second rule*
            # form two-in-a-row
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] != '_' and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] != '_': 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] != '_': 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMaxUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMaxUtility
            
            # prevention
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility

            if score != 0:
                return score
            
            # *check for third rule*
            for upper_left_id in self.globalIdx: 
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer:
                    score += self.cornerMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer:
                    score += self.cornerMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer:
                    score += self.cornerMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer:
                    score += self.cornerMaxUtility
            return score
        

        # minplayer
        else:
            if self.checkWinner == -1:
                return self.winnerMinUtility 
            # *check for first rule*
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility

                # in a col
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility

                # in a diag
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
            if score != 0:
                return score
            
            # *check for second rule*
            # form two-in-a-row
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] != '_' and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] != '_': 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] != '_': 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMinUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != '_' and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != '_': 
                    score += self.twoInARowMinUtility
            
            # prevention
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility

            if score != 0:
                return score
            
            # *check for third rule*
            for upper_left_id in self.globalIdx: 
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer:
                    score += self.cornerMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer:
                    score += self.cornerMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer:
                    score += self.cornerMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer:
                    score += self.cornerMinUtility
            return score
            

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
        # maxPlayer
        if isMax: 
            # *check for first rule*
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility

                # in a col
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility

                # in a diag
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score = self.winnerMaxUtility
            if score != 0:
                return score
            
            # *check for second rule*
            # form two-in-a-row
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != self.minPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] != self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] != self.minPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] != self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != self.minPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] != self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] != self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] != self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] != self.minPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] != self.minPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != self.minPlayer: 
                    score += self.twoInARowMaxUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] != self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != self.minPlayer: 
                    score += self.twoInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != self.minPlayer: 
                    score += self.twoInARowMaxUtility
            
            # prevention
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMaxUtility

            if score != 0:
                return score
            
            # *check for third rule*
            for upper_left_id in self.globalIdx: 
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer:
                    score += self.cornerMaxUtility
                    next_index = (upper_left_id[0]%3)*3 + upper_left_id[1]%3
                    if self.check_empty(next_index) == 1:
                        score += 20
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer:
                    score += self.cornerMaxUtility
                    next_index = ((upper_left_id[0]+2)%3)*3 + upper_left_id[1]%3
                    if self.check_empty(next_index) == 1:
                        score += 20
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer:
                    score += self.cornerMaxUtility
                    next_index = (upper_left_id[0]%3)*3 + (upper_left_id[1]+2)%3
                    if self.check_empty(next_index) == 1:
                        score += 20
                if self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer:
                    score += self.cornerMaxUtility
                    next_index = ((upper_left_id[0]+2)%3)*3 + (upper_left_id[1]+2)%3
                    if self.check_empty(next_index) == 1:
                        score += 20
            return score
        

        # minplayer
        else: 
            # *check for first rule*
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility

                # in a col
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility

                # in a diag
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score = self.winnerMinUtility
            if score != 0:
                return score
            
            # *check for second rule*
            # form two-in-a-row
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != self.maxPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] != self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] != self.maxPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] != self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != self.maxPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] != self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] != self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] != self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] != self.maxPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] != self.maxPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != self.maxPlayer: 
                    score += self.twoInARowMinUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] != self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] != self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] != self.maxPlayer: 
                    score += self.twoInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] != self.maxPlayer: 
                    score += self.twoInARowMinUtility
            
            # prevention
            for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility

                # in a col
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility

                # in a diag
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    score += self.preventThreeInARowMinUtility

            if score != 0:
                return score
            
            # *check for third rule*
            for upper_left_id in self.globalIdx: 
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer:
                    score += self.cornerMinUtility
                    next_index = (upper_left_id[0]%3)*3 + upper_left_id[1]%3
                    if self.check_empty(next_index) == 1:
                        score -= 20
                if self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer:
                    score += self.cornerMinUtility
                    next_index = ((upper_left_id[0]+2)%3)*3 + upper_left_id[1]%3
                    if self.check_empty(next_index) == 1:
                        score -= 20
                if self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer:
                    score += self.cornerMinUtility
                    next_index = (upper_left_id[0]%3)*3 + (upper_left_id[1]+2)%3
                    if self.check_empty(next_index) == 1:
                        score -= 20
                if self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer:
                    score += self.cornerMinUtility
                    next_index = ((upper_left_id[0]+2)%3)*3 + (upper_left_id[1]+2)%3
                    if self.check_empty(next_index) == 1:
                        score -= 20
            return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        movesLeft=False

        for upper_left_id in self.globalIdx: 
            for i in range(3):
                for j in range(3):
                    if self.board[upper_left_id[0]+1][upper_left_id[1]+j] != self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+j] != self.minPlayer:
                        movesLeft = True
                        return movesLeft
        return movesLeft

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
        winner = 0
        # check if maxPlayer has won
        for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    winner = 1
                elif self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer: 
                    winner = 1
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    winner = 1

                # in a col
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer: 
                    winner = 1
                elif self.board[upper_left_id[0]][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.maxPlayer: 
                    winner = 1
                elif self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    winner = 1

                # in a diag
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.maxPlayer: 
                    winner = 1
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.maxPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.maxPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.maxPlayer: 
                    winner = 1
        if winner != 0:
            return winner
        
        # check if maxPlayer has won
        for upper_left_id in self.globalIdx: 
                # in a row
                if self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    winner  = -1
                elif self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer: 
                    winner  = -1
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    winner  = -1

                # in a col
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer: 
                    winner  = -1
                elif self.board[upper_left_id[0]][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+1] == self.minPlayer: 
                    winner  = -1
                elif self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+2] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    winner  = -1

                # in a diag
                elif self.board[upper_left_id[0]][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]+2][upper_left_id[1]+2] == self.minPlayer: 
                    winner  = -1
                elif self.board[upper_left_id[0]+2][upper_left_id[1]] == self.minPlayer and self.board[upper_left_id[0]+1][upper_left_id[1]+1] == self.minPlayer and self.board[upper_left_id[0]][upper_left_id[1]+2] == self.minPlayer: 
                    winner  = -1
        return winner

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
        if depth == self.maxDepth:
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)
        if self.checkMovesLeft() == False:
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)
        if self.checkWinner() != 0:
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)
        
        if isMax:
            bestValue = -inf
            move_list = []
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        move_list.append((x+i, y+j))
                        

            for motion in move_list:
                self.board[motion[0]][motion[1]] = self.maxPlayer
                next_index = (motion[0]%3)*3 + motion[1]%3
                bestValue = max(bestValue, self.alphabeta(depth+1, next_index, alpha, beta, not isMax))
                self.board[motion[0]][motion[1]] = '_'
                if bestValue >= beta: return bestValue
                alpha = max(alpha, bestValue)

        else:
            bestValue = inf
            move_list = []
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        move_list.append((x+i, y+j))
                        

            for motion in move_list:
                self.board[motion[0]][motion[1]] = self.minPlayer
                next_index = (motion[0]%3)*3 + motion[1]%3
                bestValue = min(bestValue, self.alphabeta(depth+1, next_index, alpha, beta, not isMax))
                self.board[motion[0]][motion[1]] = '_'
                if bestValue <= alpha: return bestValue
                beta = min(beta, bestValue)

        return bestValue


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
        # if termination condition reached at this step, the last step made it terminated 
        if depth == self.maxDepth:
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)
        if self.checkMovesLeft() == False:
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)
        if self.checkWinner() != 0:
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)
        
        if isMax:
            bestValue = self.winnerMinUtility
            move_list = []
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        move_list.append((x+i, y+j))
                        

            for motion in move_list:
                self.board[motion[0]][motion[1]] = self.maxPlayer
                next_index = (motion[0]%3)*3 + motion[1]%3
                self.expandedNodes += 1
                current_value = self.minimax(depth+1, next_index, not isMax)
                
                self.board[motion[0]][motion[1]] = '_'
                bestValue = max(bestValue, current_value)
            return bestValue

        else:
            bestValue = self.winnerMaxUtility
            move_list = []
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        move_list.append((x+i, y+j))
                        

            for motion in move_list:
                self.board[motion[0]][motion[1]] = self.minPlayer
                next_index = (motion[0]%3)*3 + motion[1]%3
                self.expandedNodes += 1
                current_value = self.minimax(depth+1, next_index, not isMax)
                self.board[motion[0]][motion[1]] = '_'
                bestValue = min(bestValue, current_value)

            return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        current_player_is_max = maxFirst
        curr_board_idx = self.startBoardIdx
        self.expandedNodes = 0
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes = []
        winner=0
        alpha = -inf
        beta = inf
        while self.checkMovesLeft() == True and self.checkWinner() == 0:
            if current_player_is_max == True:
                self.currPlayer = True
                x,y = self.globalIdx[curr_board_idx]
                best_move_this_step = (0,0)
                best_value_this_step = -inf
                move_list = []
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == '_':
                            move_list.append((x+i, y+j))

                for motion in move_list:
                    #print(motion)
                    self.board[motion[0]][motion[1]] = self.maxPlayer
                    curr_board_idx = (motion[0]%3)*3 + motion[1]%3
                    if isMinimaxOffensive:
                        current_value = self.minimax(1, curr_board_idx, not current_player_is_max)
                    else:
                        current_value = self.alphabeta(1, curr_board_idx, alpha, beta, not current_player_is_max)
                    self.board[motion[0]][motion[1]] = '_'
                    if current_value > best_value_this_step:
                        best_value_this_step = current_value
                        best_move_this_step = (motion[0],motion[1])

                self.board[best_move_this_step[0]][best_move_this_step[1]] = self.maxPlayer
                curr_board_idx = (best_move_this_step[0]%3)*3 + best_move_this_step[1]%3
                current_player_is_max = not current_player_is_max
                bestMove.append(best_move_this_step)
                bestValue.append(best_value_this_step)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                print('Number of expanded nodes:', self.expandedNodes)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                
                #print(bestMove)

            else:
                self.currPlayer = False
                x,y = self.globalIdx[curr_board_idx]
                best_move_this_step = (0,0)
                best_value_this_step = inf
                move_list = []
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == '_':
                            move_list.append((x+i, y+j))

                for motion in move_list:
                    self.board[motion[0]][motion[1]] = self.minPlayer
                    curr_board_idx = (motion[0]%3)*3 + motion[1]%3
                    if isMinimaxDefensive:
                        current_value = self.minimax(1, curr_board_idx, not current_player_is_max)
                    else:
                        current_value = self.alphabeta(1, curr_board_idx, alpha, beta, not current_player_is_max)
                    self.board[motion[0]][motion[1]] = '_'
                    if current_value < best_value_this_step:
                        best_value_this_step = current_value
                        best_move_this_step = (motion[0],motion[1])

                self.board[best_move_this_step[0]][best_move_this_step[1]] = self.minPlayer
                curr_board_idx = (best_move_this_step[0]%3)*3 + best_move_this_step[1]%3
                current_player_is_max = not current_player_is_max
                bestMove.append(best_move_this_step)
                bestValue.append(best_value_this_step)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                print('Number of expanded nodes:', self.expandedNodes)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner
    
    def designed_minimax(self, depth, currBoardIdx, isMax):
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
        # if termination condition reached at this step, the last step made it terminated 
        if depth == self.maxDepth:
            self.expandedNodes += 1
            return self.evaluateDesigned(self.currPlayer)
        if self.checkMovesLeft() == False:
            self.expandedNodes += 1
            return self.evaluateDesigned(self.currPlayer)
        if self.checkWinner != 0:
            self.expandedNodes += 1
            return self.evaluateDesigned(self.currPlayer)
        
        if isMax:
            bestValue = self.winnerMinUtility
            move_list = []
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        move_list.append((x+i, y+j))
                        

            for motion in move_list:
                self.board[motion[0]][motion[1]] = self.maxPlayer
                next_index = (motion[0]%3)*3 + motion[1]%3
                bestValue = max(bestValue, self.designed_minimax(depth+1, next_index, not isMax))
                self.board[motion[0]][motion[1]] = '_'
            return bestValue

        else:
            bestValue = self.winnerMaxUtility
            move_list = []
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == '_':
                        move_list.append((x+i, y+j))
                        

            for motion in move_list:
                self.board[motion[0]][motion[1]] = self.minPlayer
                next_index = (motion[0]%3)*3 + motion[1]%3
                bestValue = min(bestValue, self.designed_minimax(depth+1, next_index, not isMax))
                self.board[motion[0]][motion[1]] = '_'

        return bestValue 

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
        current_player_is_max = True # Ture--max first; False--min first
        curr_board_idx = self.startBoardIdx
        self.expandedNodes = 0
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes = []
        winner=0
        alpha = -inf
        beta = inf
        while self.checkMovesLeft() == True and self.checkWinner() == 0:
            if current_player_is_max == True:
                self.currPlayer = True
                x,y = self.globalIdx[curr_board_idx]
                best_move_this_step = (0,0)
                best_value_this_step = -inf
                move_list = []
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == '_':
                            move_list.append((x+i, y+j))

                for motion in move_list:
                    #print(motion)
                    self.board[motion[0]][motion[1]] = self.maxPlayer
                    curr_board_idx = (motion[0]%3)*3 + motion[1]%3
                    current_value = self.alphabeta(1, curr_board_idx, alpha, beta, not current_player_is_max)
                    self.board[motion[0]][motion[1]] = '_'
                    if current_value > best_value_this_step:
                        best_value_this_step = current_value
                        best_move_this_step = (motion[0],motion[1])

                self.board[best_move_this_step[0]][best_move_this_step[1]] = self.maxPlayer
                curr_board_idx = (best_move_this_step[0]%3)*3 + best_move_this_step[1]%3
                current_player_is_max = not current_player_is_max
                bestMove.append(best_move_this_step)
                bestValue.append(best_value_this_step)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print('Number of expanded nodes:', self.expandedNodes)
                #print(bestMove)

            else:
                self.currPlayer = False
                x,y = self.globalIdx[curr_board_idx]
                best_move_this_step = (0,0)
                best_value_this_step = inf
                move_list = []
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == '_':
                            move_list.append((x+i, y+j))

                for motion in move_list:
                    self.board[motion[0]][motion[1]] = self.minPlayer
                    curr_board_idx = (motion[0]%3)*3 + motion[1]%3
                    current_value = self.designed_minimax(1, curr_board_idx, not current_player_is_max)
                    self.board[motion[0]][motion[1]] = '_'
                    if current_value < best_value_this_step:
                        best_value_this_step = current_value
                        best_move_this_step = (motion[0],motion[1])

                self.board[best_move_this_step[0]][best_move_this_step[1]] = self.minPlayer
                curr_board_idx = (best_move_this_step[0]%3)*3 + best_move_this_step[1]%3
                current_player_is_max = not current_player_is_max
                bestMove.append(best_move_this_step)
                bestValue.append(best_value_this_step)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print('Number of expanded nodes:', self.expandedNodes)

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        current_player_is_max = True # Ture--max first; False--min first
        curr_board_idx = self.startBoardIdx
        self.expandedNodes = 0
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes = []
        winner=0
        alpha = -inf
        beta = inf
        while self.checkMovesLeft() == True and self.checkWinner() == 0:
            if current_player_is_max == True:
                self.currPlayer = True
                x,y = self.globalIdx[curr_board_idx]
                best_move_this_step = (0,0)
                best_value_this_step = -inf
                move_list = []
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == '_':
                            move_list.append((x+i, y+j))

                for motion in move_list:
                    #print(motion)
                    self.board[motion[0]][motion[1]] = self.maxPlayer
                    curr_board_idx = (motion[0]%3)*3 + motion[1]%3
                    current_value = self.designed_minimax(1, curr_board_idx, not current_player_is_max)
                    self.board[motion[0]][motion[1]] = '_'
                    if current_value > best_value_this_step:
                        best_value_this_step = current_value
                        best_move_this_step = (motion[0],motion[1])

                self.board[best_move_this_step[0]][best_move_this_step[1]] = self.maxPlayer
                curr_board_idx = (best_move_this_step[0]%3)*3 + best_move_this_step[1]%3
                current_player_is_max = not current_player_is_max
                bestMove.append(best_move_this_step)
                bestValue.append(best_value_this_step)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print('opponent plays at: ', best_move_this_step)
                print('you will play at block No.',curr_board_idx)
                print('upperleft left index of the block you will play is:', self.globalIdx[curr_board_idx])

            else:
                self.currPlayer = False
                x = input('please enter row value (0,1,2) now:')
                y = input('please enter col value (0,1,2) now:')
                x_global_index = self.globalIdx[curr_board_idx][0] + int(x)
                y_global_index = self.globalIdx[curr_board_idx][1] + int(y)
                self.board[x_global_index][y_global_index] = self.minPlayer
    
                curr_board_idx = (x_global_index%3)*3 + y_global_index%3
                current_player_is_max = not current_player_is_max
                gameBoards.append(self.board)
                self.printGameBoard()
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner


if __name__=="__main__":
    uttt=ultimateTicTacToe()
    # feel free to write your own test code
    start = time.time()
    
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True, True, False)
    print("time spent: ", time.time() - start)
    #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGameHuman()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
    """
    winner = uttt.checkWinner()
    print(winner)
    
    eva = uttt.evaluatePredifined( True)
    print(eva)
    """


