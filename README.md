ooxx-variation
------
A variation of tic-tac-toe found in my old electronic dictionary.  

* A small toy that I wrote to practice `Python` and my undergradue course - artificial Intelligence.  
* The rule is expand of tic-tac-toe (which often be called `ooxx` in Chinese).  
    + The board will always be less than (contain) six moves.
    + When the seventh move is done, the eariest move will be erased from board.
    + Who gets a line will win the game.
    + To identify both sides' moves, it can use number or color.
        - In low level, the program use both number and color.
        - In middle level, the program use only number.
        - In high level, both sides' move just use O and X to represent. Players have to remember the move order.
* There are two implements, `ooxx_ab.py` using [Alpha–beta_pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning), and `ooxx_mc.py` using [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method).

