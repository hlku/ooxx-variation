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

        for nx in self.__board.expand() :
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
        if self.__board.check(tsumeru) : return 99 - depth
        elif depth >= self.__limit : return 0
        
        for nx in self.__board.expand(tsumeru) :
            value = min(value, self.__findMax(nx, depth + 1, value))
            if value < MAX : return value
            
        return value
        
    def __findMax(self, tsumeru, depth, MIN) :
        value = -100
        if self.__board.check(tsumeru) : return -99 + depth
        elif depth >= self.__limit : return 0
        
        for nx in self.__board.expand(tsumeru) :
            value = max(value, self.__findMin(nx, depth + 1, value))
            if value > MIN : return value
            
        return value
    