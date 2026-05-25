# -*- coding: UTF-8 -*-
import random, sys, operator, logging

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
        for nx in self.__expand(self.__board) : # every possible postion for limit times
            pos = nx.index(max(nx))
            for one in range(0, self.__limit) : # MC for limit times
                clone = list(nx) 
                for rd in range(0, self.__depth) : # depth
                    if self.checkWin(clone) and rd % 2 == 0 : # win
                        solutions[pos] = solutions.get(pos, 0) + self.__depth - rd
                        break
                    elif self.check(clone) and rd % 2 == 1 : # lose
                        if rd == 1 : solutions[pos] = solutions.get(pos, 0) - self.__depth * 10
                        else : solutions[pos] = solutions.get(pos, 0) - self.__depth + rd
                        break
                    nxlist = self.__expand(clone)
                    clone = nxlist[random.randint(0, len(nxlist) - 1)] # random choose a step

                    if rd >= 39 : # tie 
                        pass # do nothing
        # avoid illegal moves
        for i in range(0, 9) :
            if self.__board[i] != 0 : solutions[i] = self.__depth * self.__limit * -10

        ii = 1
        for k,v in solutions.items() : # for debug
            tt = float(v + self.__limit * self.__depth)/float(self.__limit * self.__depth * 2)
            pp = "%0.3f" % tt
            if v <= -10 * self.__limit * self.__depth : color = '\033[0;30m'
            elif v < -1 * self.__limit * self.__depth : color = '\033[1;31m'
            elif v < 0 : color = '\033[1;32m'
            else : color = '\033[1;36m'
            sys.stderr.write(str(k+1) + ':' + color + pp + "%\033[0m\t")
            if ii % 3 == 0: print(' ', file=sys.stderr)
            ii += 1
        return max(solutions.items(), key=operator.itemgetter(1))[0]

    def __expand(self, pos) :
        def rotate(t) :
            return [t[6], t[3], t[0], t[7], t[4], t[1], t[8], t[5], t[2]]
        def mirror(t) :
            return [t[2], t[1], t[0], t[5], t[4], t[3], t[8], t[7], t[6]]
        biggest = max(pos)
        ret = []
        for i in range(0, 9) :
            if pos[i] == 0 :
                tmp = list(pos)
                tmp[i] = biggest + 1
                fresh(tmp)
                if tmp.count(0) > 3 :
                    if rotate(tmp) in ret or \
                       rotate(rotate(tmp)) in ret or \
                       rotate(rotate(rotate(tmp))) in ret or \
                       mirror(tmp) in ret or \
                       mirror(rotate(tmp)) in ret or \
                       mirror(rotate(rotate(tmp))) in ret or \
                       mirror(rotate(rotate(rotate(tmp)))) in ret : pass
                    else : ret.append(tmp)
                else : ret.append(tmp)
        return ret

    def checkWin(self, board) :
        k = lambda a, b, c : True if \
            (board[a] % 2 == board[b] % 2 == board[c] % 2) and \
            board[a] != 0 and board[b] != 0 and board[c] != 0 \
            else False
        if k(0, 1, 2) or k(3, 4, 5) or k(6, 7, 8) or k(0, 3, 6) or \
           k(1, 4, 7) or k(2, 5, 8) or k(0, 4, 8) or k(2, 4, 6) : return True
        return False