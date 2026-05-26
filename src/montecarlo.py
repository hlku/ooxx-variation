# -*- coding: UTF-8 -*-
import random, logging
from . import board, engine

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class MonteCarlo(engine.Engine):
    def __init__(self, settings, board) -> None:
        """Initialize the AlphaBeta engine based on the settings."""
        super().__init__(settings, board)

        #number of simulations for each random possible next step, the higher the more accurate, but more time computing
        self.__limit = self._settings.getConfig('mctimes')

    def calculate(self) -> int:
        """Calculate the best next step using the Monte Carlo Algorithm."""
        optimization = self._optimizeStep(self._board.getBoard()) #quick solve 
        if optimization[0] != 0: return optimization[1]

        solutions = [0] * 9 #the score of each possible next step
        illegal = [i for i in range(9)]
        for nx in self._board.expand() : #every possible postion for the next step
            pos = nx.index(max(nx))
            illegal.remove(pos) #legal step, remove from illegal list
            for _ in range(self.__limit) : #Do MC for limit times
                clone = list(nx) #don't touch the nx 
                for rd in range(self._depth) : #searching until reach the depth
                    if board.checkWin(clone):
                        if rd % 2 == 0 : #win
                            solutions[pos] += (self._depth - rd) #the sooner the better
                        elif rd % 2 == 1 : #lose
                            if rd == 1 : #immediate lose, give a heavy penalty to avoid this step
                                solutions[pos] -= (self._depth * 10)
                            else : #the sooner the worse
                                solutions[pos] -= (self._depth + rd)
                        break
                    
                    nxlist = board.expandBoard(clone) #keep expanding the board until reach the depth or win/lose
                    clone = nxlist[random.randint(0, len(nxlist) - 1)] #MC's spirit, random choose a next step

        for i in illegal : #avoid illegal steps
            solutions[i] = self._depth * self.__limit * - 10

        self.__showScore(solutions)
        return solutions.index(max(solutions))
    
    def __showScore(self, solutions:list) -> None:
        """Get the score of each possible next step."""
        msg='Score of next steps:\n'
        for i in range(9):
            score = solutions[i]
            winRate = float(score + self.__limit * self._depth)/float(self.__limit * self._depth * 2)
            winRateStr = "%0.3f" % winRate
            if score <= -10 * self.__limit * self._depth : color = '\033[0;30m'
            elif score < -1 * self.__limit * self._depth : color = '\033[1;31m'
            elif score < 0 : color = '\033[1;32m'
            else : color = '\033[1;36m'
            msg += str(i+1) + ':' + color + winRateStr + " \033[0m\t"
            if i % 3 == 2: msg += '\n'
        self._log.debug(msg)
