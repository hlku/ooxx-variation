ooxx-variation
------
A variation of tic-tac-toe found in my old electronic dictionary.  

* A small toy that I wrote to practice `Python` and my undergradue course - artificial Intelligence.  
* The rule is expand of tic-tac-toe (which often be called `ooxx` in Chinese).  
    + The board will always be less than (contain) six moves.
    + When the seventh move is done, the eariest move will be erased from board.
    + Who gets a line will win the game.
* You can modify the `conf/config.yml` to choose your preferring
	+ There are two engine: [Alpha–beta_pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) and [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method).
	+ You can change the computer's level.
	+ To identify both sides' moves, there are three `display` style: 
        - The program uses both number and color.
        - The program uses only number without color.
        - Both sides' moves just use O and X to represent. Players have to remember the move order.
		