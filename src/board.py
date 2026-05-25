# -*- coding: UTF-8 -*-
import logging
logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")

class Board:
    def __init__(self, settings) -> None:
        """Initialize the board based on the settings."""
        self.__settings = settings
        self.__board = [0] * 9

        self.__log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self.__log.setLevel(logging.DEBUG)
            self.__log.debug('Debug mode is on')

    def __fresh(self, pos:list = None) -> None:
        """Game rules: at most 3 steps of one side can be on the board, remove the oldest step."""
        if pos is None: pos = self.__board

        oldest = max(pos) - 6
        if oldest <= 0: return #no step needs to be removed
        for i in range(9):
            if pos[i] == oldest: pos[i] = 0

    def check(self, pos:list = None) -> bool:
        """Check whether someone has won."""
        if pos is None: pos = self.__board
        k = lambda a, b, c : True if \
            (pos[a] % 2 == pos[b] % 2 == pos[c] % 2) and \
            pos[a] != 0 and pos[b] != 0 and pos[c] != 0 \
            else False #check whether a line of three steps belongs to the player's side
        if k(0, 1, 2) or k(3, 4, 5) or k(6, 7, 8) or k(0, 3, 6) or \
           k(1, 4, 7) or k(2, 5, 8) or k(0, 4, 8) or k(2, 4, 6) : return True
        return False
    
    def expand(self, pos:list = None) -> list:
        """Expand the current board state to all possible next states and remove duplicates."""
        def rotate(t) : #rotate the board 90 degrees clockwise
            return [t[6], t[3], t[0], t[7], t[4], t[1], t[8], t[5], t[2]]
        def mirror(t) : #mirror the board horizontally
            return [t[2], t[1], t[0], t[5], t[4], t[3], t[8], t[7], t[6]]

        if pos is None: pos = self.__board
        biggest = max(pos)
        ret = [] #list of possible next states, without duplicates
        for i in range(0, 9) :
            if pos[i] == 0 : #this position is empty, can be played
                tmp = list(pos)
                tmp[i] = biggest + 1
                self.__fresh(tmp)
                if tmp.count(0) > 3 : #duplicate states only exist when there are more than 3 empty positions
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

    def playStep(self, step:int, times:int=1) -> None:
        """Play a step on the board.
        step: the position to play, from 0 to 8
        times: the next step offset, 1 or 2"""
        self.__board[step] = max(self.__board) + times 
        self.__fresh()

    def display(self) -> None:
        """Display the board based with the display mode."""
        q = list()
        displayMode = self.__settings.getConfig('display')
        for i in self.__board :
            if i == 0: #no step on this position
                q.append('  ')
                continue

            match displayMode:
                case 0: #display the step number with color, odd steps in green, even steps in cyan
                    k = '%2d' % tuple([i]) #step number, right aligned with width 2
                    if i % 2 == 1: k2 = '\033[1;32m' + k + '\033[0m' #green 
                    else : k2 = '\033[1;36m' + k + '\033[0m' #cyan
                    q.append(k2)
                case 1: #display the step number only, without color
                    q.append('%2d' % tuple([i]))
                case 2: #display O and X, O for odd steps, X for even steps
                    if i % 2 == 1 : q.append('Ｏ')
                    else : q.append('Ｘ')
                case _: #should not happen, but just in case
                    q.append('  ') 

        if max(self.__board) != 0 :
            #highlight the latest step with red background
            q[self.__board.index(max(self.__board))] = \
                '\033[41m' + q[self.__board.index(max(self.__board))] + '\033[0m' 
        p = """\
+--+--+--+
|%s|%s|%s|
+--+--+--+
|%s|%s|%s|
+--+--+--+
|%s|%s|%s|
+--+--+--+
"""
        print('\n' + p % tuple(q) )

    def getMaxStep(self) -> int:
        """Get the maximum step number on the board."""
        return max(self.__board)

    def getBoard(self) -> list:
        """Get the current board state as a list of 9 integers."""
        return self.__board