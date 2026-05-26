# -*- coding: UTF-8 -*-
import logging, random
from . import settings, alphabeta, montecarlo, board

logging.basicConfig(level=logging.INFO, format = "%(asctime)s %(filename)s %(levelname)s:%(message)s")
class OOXX:
    def __init__(self) -> None:
        """Initialize the game based on the settings."""
        self.__settings = settings.Settings()

        self.__log = logging.getLogger(__name__)
        if self.__settings.getConfig('debug'):
            self.__log.setLevel(logging.DEBUG)
            self.__log.debug('Debug mode is on')

        self.__board = board.Board(self.__settings)

        if self.__settings.getConfig('engine') == 'MonteCarlo':
            self.__engine = montecarlo.MonteCarlo(self.__settings, self.__board)
        elif self.__settings.getConfig('engine') == 'AlphaBeta':
            self.__engine = alphabeta.AlphaBeta(self.__settings, self.__board)
        

    def start(self) -> bool:
        """Start the game loop."""
        self.__log.info('game started')
        self.__board.clear()

        self.__mode = self.__getMode()
        match self.__mode:
            case 2 : self.__board.playStep(self.__engine.calculate()) #computer goes first 
            case 4 : #computer starts with 2 steps
                steps = self.__engine.calculate2()
                self.__board.playStep(steps[0])
                self.__board.playStep(steps[1], 2)
            case _: pass

        while True:
            self.__board.display()
            if self.__checkStatus("Computer"): break

            nextStep = self.__getUserNext()

            if self.__mode == 3: #user starts with 2 steps
                if self.__board.getMaxStep() == 0: #no move on the board
                    self.__board.playStep(nextStep) #1st step 
                    continue #to play addtion step in the next loop
                else: #only 1st step on the board            
                    self.__board.playStep(nextStep, 2) #3rd step
                    self.__mode = 1 #switch to normal mode, to avoid if condition in every loop
            else: self.__board.playStep(nextStep)

            self.__board.display()
            if self.__checkStatus("You"): break

            self.__board.playStep(self.__engine.calculate()) #computer's turn
        return self.__newGame()
            
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
                if i < 0 or i > 8 or self.__board.getBoard()[i] != 0 : raise
            except:
                print('Illegal move!')
                continue
            return i

    def __checkStatus(self, player:str) -> bool:
        """Check whether the game has ended."""
        if self.__board.check():
            print('====== %s won! ======\n\n' % player)
            return True
        elif self.__board.getMaxStep() >= 50 : 
            print('====== Tie! ======\n\n')
            return True
        else: return False #game continues

    def __newGame(self) -> bool:
        """Ask the user whether to start a new game."""
        while True:
            i = input('Start a new game? (y/n) : ')
            if i == 'Y' or i == 'y' or i == 'yes': return True
            elif i == 'N' or i == 'n' or i == 'no': return False
            else: print('Error input!')