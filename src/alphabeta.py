# -*- coding: UTF-8 -*-
import logging, random
from . import board

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class AlphaBeta:
    def __init__(self, settings, board) -> None:
        """Initialize the AlphaBeta engine based on the settings."""
        self.__settings = settings
        self.__board = board
        #search depth limit, the higher the smarter computer, but more time computing
        self.__depth = 3 + self.__settings.getConfig('level') * 2 
        
        self.__log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self.__log.setLevel(logging.DEBUG)
            self.__log.debug('Debug mode is on')
    
    def calculate(self):
        """Calculate the best next step using the Alpha–Beta Pruning Algorithm."""
        solutions = set() #positions of all best next steps 
        value = -100 #value of a step, the higher the better for the computer
        for nx in self.__board.expand() : #every possible postion for the next step
            v = self.__findMin(nx, 1, value) #get the value of this step
            if value == v : #same value to old solutions, add to set
                solutions.add(nx.index(max(nx)))
            elif value < v : #find a better solution, clear old solutions and add new one
                solutions = set([nx.index(max(nx))])
                value = v

        self.__log.debug("Solutions: %s, Value: %d", str(solutions), value)
        #randomly choose one of the best solutions if there are multiple ones
        return list(solutions)[random.randint(0, len(solutions) - 1)] 

    def __findMin(self, tsumeru, depth, MAX):
        """Find the minimum value of the next step
           which is best for user but worst for computer.
           tsumeru: the pending solving board state after computer's step
           depth: the current depth of the search tree
           MAX: the current best value of computer's possible next steps"""
        if board.checkWin(tsumeru) : return 99 - depth #computer win, the sooner the better
        elif depth >= self.__depth : return 0 #reach the depth limit, no best solution found
        
        value = 100
        for nx in board.expandBoard(tsumeru) : #every possible postion for user's next step
            #get the lowest value of this step, which is the best for user but worst for computer
            value = min(value, self.__findMax(nx, depth + 1, value))
            #the user will get better value than computer's current best value (MAX)
            #so computer will never choose this step (return immediately without searching deeper)
            if value < MAX : return value 
            
        return value
        
    def __findMax(self, tsumeru, depth, MIN) :
        """Find the maximum value of the next step
           which is best for computer but worst for user.
           tsumeru: the pending solving board state after user's step
           depth: the current depth of the search tree
           MIN: the current best value of user's possible next steps"""
        if board.checkWin(tsumeru) : return -99 + depth #user win, the sooner the worse
        elif depth >= self.__depth : return 0 #reach the depth limit, no best solution found
        
        value = -100
        for nx in board.expandBoard(tsumeru) : #every possible postion for computer's next step
            #get the highest value of this step, which is the best for computer but worst for user
            value = max(value, self.__findMin(nx, depth + 1, value))
            #the computer will get better value than user's current best value (MIN)
            #so user will never choose this step (return immediately without searching deeper)
            if value > MIN : return value
            
        return value
    