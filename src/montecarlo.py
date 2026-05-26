# -*- coding: UTF-8 -*-
import random, sys, operator, logging
import board

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class MonteCarlo:
    def __init__(self, settings, board) -> None:
        """Initialize the AlphaBeta engine based on the settings."""
        self.__settings = settings
        self.__board = board
        #search depth limit, the higher the smarter computer, but more time computing
        self.__depth = 3 + self.__settings.getConfig('level') * 2 
        #number of simulations for each random possible next step, the higher the more accurate, but more time computing
        self.__limit = self.__settings.getConfig('mctimes')
        
        self.__log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self.__log.setLevel(logging.DEBUG)
            self.__log.debug('Debug mode is on')

    def calculate(self):
        """Calculate the best next step using the Monte Carlo Algorithm."""
        solutions = [0] * 9 #the score of each possible next step
        for nx in self.__board.expand() : #every possible postion for the next step
            pos = nx.index(max(nx))
            for _ in range(self.__limit) : #Do MC for limit times
                clone = list(nx) #don't touch the nx 
                for rd in range(self.__depth) : #searching until reach the depth
                    if board.checkWin(clone):
                        if rd % 2 == 0 : #win
                            solutions[pos] += (self.__depth - rd) #the sooner the better
                        elif rd % 2 == 1 : #lose
                            if rd == 1 : #immediate lose, give a heavy penalty to avoid this step
                                solutions[pos] -= (self.__depth * 10)
                            else : #the sooner the worse
                                solutions[pos] -= (self.__depth + rd)
                        break
                    
                    nxlist = board.expandBoard(clone) #keep expanding the board until reach the depth or win/lose
                    clone = nxlist[random.randint(0, len(nxlist) - 1)] #MC's spirit, random choose a next step

        for i in range(9) : #avoid illegal steps, should not happen, but just in case
            if self.__board.getBoard()[i] != 0 : solutions[i] = 0

        self.__showScore(solutions))
        return solutions.index(max(solutions))
    
    def __showScore(self, solutions:list) -> None:
        """Get the score of each possible next step."""
        msg='Score of next steps:\n'
        for i in range(9):
            score = solutions[i]
            winRate = float(score + self.__limit * self.__depth)/float(self.__limit * self.__depth * 2)
            winRateStr = "%0.3f" % winRate
            if score <= -10 * self.__limit * self.__depth : color = '\033[0;30m'
            elif score < -1 * self.__limit * self.__depth : color = '\033[1;31m'
            elif score < 0 : color = '\033[1;32m'
            else : color = '\033[1;36m'
            msg += str(i+1) + ':' + color + winRateStr + "%\033[0m\t"
            if i % 3 == 2: msg += '\n'
        self.__log.debug(msg)
