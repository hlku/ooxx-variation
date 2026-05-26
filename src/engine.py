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

    def _optimizeStep(self, tsumeru) -> tuple:
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
                if board.checkWin(nx2): return (2, nx2.index(max(nx2)))
                if board.checkmate(nx2) and ret[0] == 0:
                    ret = (4, nx2.index(max(nx2)))

        return ret

    def calculate(self) : #virtual method, to be implemented by subclasses
        """Calculate the best next step."""
        pass
