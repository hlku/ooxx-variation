# -*- coding: UTF-8 -*-
import logging, random
import settings, alphabeta, montecarlo

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class OOXX:
    def __init__(self) -> None:
        """Initialize the game based on the settings."""
        self.__settings = settings.Settings()

        self.__log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self.__log.setLevel(logging.DEBUG)
            self.__log.debug('Debug mode is on')

        self.__board = [0] * 9

        if self.__settings.getConfig('engine') == 'MonteCarlo':
            self.__engine = montecarlo.MonteCarlo(self.__settings, self.__board)
        elif self.__settings.getConfig('engine') == 'AlphaBeta':
            self.__engine = alphabeta.AlphaBeta(self.__settings, self.__board)
        

    def start(self) -> None:
        """Start the game loop."""
        self.__log.info('game started')

        self.__mode = self.__getMode()
        match self.__mode:
            case 2 | 4: self.__playStep(self.__engine.calculate()) #computer goes first 
            case _: pass
        if self.__mode == 4 : #computer starts with 2 steps
            self.__playStep(self.__engine.calculate(), 2)

        while True:
            self.__displayBoard()
            if self.__checkStatus("Computer"): break

            nextStep = self.__getUserNext()

            if self.__mode == 3: #user starts with 2 steps
                if max(self.__board) == 0: #no move on the board
                    self.__playStep(nextStep) #1st step 
                    continue #to play addtion step in the next loop
                else: #only 1st step on the board            
                    self.__playStep(nextStep, 2) #3rd step
                    self.__mode = 1 #switch to normal mode, to avoid if condition in every loop
            else: self.__playStep(nextStep)

            self.__displayBoard()
            if self.__checkStatus("You"): break

            self.__playStep(self.__engine.calculate()) #computer's turn
            
    def __getMode(self) -> int:
        """Get the mode of the game from user input."""
        while True:
            print("""
\n====== Choose a mode ======
\t0 : random
\t1 : you go first
\t2 : computer goes first
\t3 : you start with 2 steps
\t4 : computer starts with 2 steps""")
            try:
                i = int(input('mode : '))
                if i < 0 or i > 4 : raise
            except:
                print('Error input!')
                continue
            
            if i == 0 and random.randint(0, 1) == 0: #computer randomly gets first 
                i = 2
            return i
        
    def __getUserNext(self) -> int:
        """Get the next step from user input."""
        while True:
            try:
                i = int(input('Input your next step position (1-9): ')) - 1 #minus 1 to convert to 0-based index
                if i < 0 or i > 8 or self.__board[i] != 0 : raise
            except:
                print('Illegal move!')
                continue
            return i
        
    def __playStep(self, step:int, times:int=1) -> None:
        """Play a step on the board.
        step: the position to play, from 0 to 8
        times: the next step offset, 1 or 2"""
        self.__board[step] = max(self.__board) + times 
        self.__freshBoard()

    def __freshBoard(self) -> None:
        """Game rules: at most 3 steps of one side can be on the board, remove the oldest step."""
        oldest = max(self.__board) - 6
        if oldest <= 0: return #no step needs to be removed
        for i in range(9):
            if self.__board[i] == oldest: self.__board[i] = 0

    def __displayBoard(self) -> None:
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

    def __checkStatus(self, player:str) -> bool:
        """Check whether the game has ended."""
        if self.__engine.checkWin(self.__board):
            print('====== %s won! ======', player)
            return True
        elif max(self.__board) >= 50 : 
            print('====== Tie! ======')
            return True
        else: return False #game continues
        