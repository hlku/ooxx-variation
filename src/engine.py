# -*- coding: UTF-8 -*-
import logging
from . import board

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Engine:
    def __init__(self, settings, board) -> None:
        """Initialize the engine based on the settings."""
        self._settings = settings
        self._board = board
        #search depth limit, the higher the smarter computer, but more time computing
        self._depth = 3 + self._settings.getConfig('level') * 2 
        
        self._log = logging.getLogger(__name__)
        if self._settings.getConfig('debug'):
            self._log.setLevel(logging.DEBUG)
            self._log.debug('Debug mode is on')

    def _optimizeStep(self, tsumeru:tuple) -> tuple:
        """Optimize calculating step, don't use engine when it's too easy.
           return 1 for immediately winning,
           return 2 for avoiding immediately losing,
           return 3 for winning in 3 steps (checkmate).
           return 4 for avoiding losing in 4 steps (beging checkmated)."""
        ret = (0, 0) #default return value, no optimize step found

        nextStates = board.expandBoard(tsumeru)
        for nx in nextStates: #find immediately winning step
            if board.checkWin(nx): return (1, nx.index(max(nx)))
            if board.checkmate(nx): #find winning in 3 steps, which is a special case of checkmate
                ret = (3, nx.index(max(nx)))
        for nx in nextStates: #if no immediately winning step, find immediately losing step to avoid
            for nx2 in board.expandBoard(nx):
                if board.checkWin(nx2): ret = (2, nx2.index(max(nx2)))
                if board.checkmate(nx2) and ret[0] == 0:
                    ret = (4, nx2.index(max(nx2)))

        if ret[1] != 0 and tsumeru[ret[1]] != 0: #the optimized step is illegal, ignore it
            ret = (0, 0)
        return ret
    
    def _engineCalculate(self) -> int : #virtual method, should be implemented by subclasses
        """Calculate the best next step by the engine."""
        pass

    def _engineCalculate2(self, tsumeru: tuple) -> tuple : #virtual method, should be implemented by subclasses
        """Calculate the best 1st, 3rd steps by the engine."""
        pass

    def calculate(self) -> int:
        """Calculate the best next step."""
        optimization = self._optimizeStep(self._board.getBoard()) #quick solve 
        if optimization[0] != 0:
            self._log.debug("Found a optimized step: %d, Type: %d", optimization[1], optimization[0])
            return optimization[1]        
        return self._engineCalculate() #call the real calculating method implemented by subclasses
    
    def calculate2(self) -> tuple : #virtual method, should be implemented by subclasses
        """Calculate the best 1st, 3rd steps if computer starts with 2 moves."""
        expandedBoard = ( #don't waste time to use expandBoard function because only 2 steps
            (1, 3, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 3, 0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 3, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 3, 0, 0, 0),
            (1, 0, 0, 0, 0, 0, 0, 0, 3),
            (0, 1, 3, 0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 3, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 3, 0, 0, 0),
            (0, 1, 0, 0, 0, 0, 0, 3, 0),
            (0, 1, 0, 0, 0, 0, 0, 0, 3),
            (3, 0, 0, 0, 1, 0, 0, 0, 0),
            (0, 3, 0, 0, 1, 0, 0, 0, 0)
        )
        return self._engineCalculate2(expandedBoard)
        