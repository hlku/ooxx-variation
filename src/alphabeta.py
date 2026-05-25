# -*- coding: UTF-8 -*-
import logging, random

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class AlphaBeta:
    def __init__(self, settings, board) -> None:
        self.__settings = settings
        self.__board = board
        self.__limit = 3 + self.__settings.getConfig('level')['ab'] * 2
        
        self.__log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self.__log.setLevel(logging.DEBUG)
            self.__log.debug('Debug mode is on')
    
    def calculate(self):
        solutions = set([9])
        value = -100

        for nx in self.__expand(self.__board) :
            v = self.__findMin(nx, 1, value)
            if value == v :
                solutions.add(nx.index(max(nx)))
            elif value < v :
                solutions = set([nx.index(max(nx))])
                value = v

        self.__log.debug("Solutions: %s, Value: %d", str(solutions), value)
        return list(solutions)[random.randint(0, len(solutions) - 1)]

    def __findMin(self, tsumeru, depth, MAX):
        value = 100
        if self.checkWin(tsumeru) : return 99 - depth
        elif depth >= self.__limit : return 0
        
        for nx in self.__expand(tsumeru) :
            value = min(value, self.__findMax(nx, depth + 1, value))
            if value < MAX : return value
            
        return value
        
    def __findMax(self, tsumeru, depth, MIN) :
        value = -100
        if self.checkWin(tsumeru) : return -99 + depth
        elif depth >= self.__limit : return 0
        
        for nx in self.__expand(tsumeru) :
            value = max(value, self.__findMin(nx, depth + 1, value))
            if value > MIN : return value
            
        return value
    
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
