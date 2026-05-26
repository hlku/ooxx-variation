# -*- coding: UTF-8 -*-
import logging

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class Engine:
    def __init__(self, settings, board) -> None:
        """Initialize the engine based on the settings."""
        self._settings = settings
        self._board = board
        #search depth limit, the higher the smarter computer, but more time computing
        self._depth = 3 + self.__settings.getConfig('level') * 2 
        
        self._log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self._log.setLevel(logging.DEBUG)
            self._log.debug('Debug mode is on')

    def optimizeStep(self, step:int) -> int:
        """Optimize calculating step, don't use engine when it's too easy."""
        pass
    
    def calculate(self) :
        """Calculate the best next step."""
        pass
