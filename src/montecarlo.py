# -*- coding: UTF-8 -*-
import random, sys, operator, logging
import board

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class MonteCarlo:
    def __init__(self, settings, board) -> None:
        self.__settings = settings
        self.__board = board
        self.__limit = self.__settings.getConfig('level')['mc']
        self.__depth = 25
        
        self.__log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self.__log.setLevel(logging.DEBUG)
            self.__log.debug('Debug mode is on')

    def calculate(self):
        solutions = dict()
        for nx in self.__board.expand() : # every possible postion for limit times
            pos = nx.index(max(nx))
            for one in range(0, self.__limit) : # MC for limit times
                clone = list(nx) 
                for rd in range(0, self.__depth) : # depth
                    if board.checkWin(clone) and rd % 2 == 0 : # win
                        solutions[pos] = solutions.get(pos, 0) + self.__depth - rd
                        break
                    elif board.checkWin(clone) and rd % 2 == 1 : # lose
                        if rd == 1 : solutions[pos] = solutions.get(pos, 0) - self.__depth * 10
                        else : solutions[pos] = solutions.get(pos, 0) - self.__depth + rd
                        break
                    nxlist = board.expandBoard(clone)
                    clone = nxlist[random.randint(0, len(nxlist) - 1)] # random choose a step

                    if rd >= 39 : # tie 
                        pass # do nothing
        # avoid illegal moves
        for i in range(0, 9) :
            if self.__board.getBoard()[i] != 0 : solutions[i] = self.__depth * self.__limit * -10

        ii = 1
        for k,v in solutions.items() : # for debug
            tt = float(v + self.__limit * self.__depth)/float(self.__limit * self.__depth * 2)
            pp = "%0.3f" % tt
            if v <= -10 * self.__limit * self.__depth : color = '\033[0;30m'
            elif v < -1 * self.__limit * self.__depth : color = '\033[1;31m'
            elif v < 0 : color = '\033[1;32m'
            else : color = '\033[1;36m'
            self.__log.debug(str(k+1) + ':' + color + pp + "%\033[0m\t")
            if ii % 3 == 0: self.__log.debug(' ')
            ii += 1
        return max(solutions.items(), key=operator.itemgetter(1))[0]
