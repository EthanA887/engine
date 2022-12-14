# ChessCore Engine 
### Description 
---------- 
#### Introduction 
The ChessCore Engine is an interactive program in Python that allows you to play a chess game against a computer or another human. After thousands of tests and more than half a dozen versions, this intelligent chess engine will quickly rank, test, and assign a score to all possible chess moves on a given board and decisively attack or defend based on the position. 

#### Usage 
##### Usage: Chess Engine 
To run the chess engine, you can execute ``` python3 pvc.py ``` in your terminal. It prints the initial board with the numbers and letters to represent each square and starts accepting moves. The computer takes approximately 2.5 seconds to respond after sorting through the dynamic list of legal moves (see Algorithms). Moves are written in long algebraic notation, although the program has been configured so that other common notations (standard algebraic notation, reversible algebraic notation, and Smith notation) are also usable. 

##### Usage: Multiplayer Games 
To run a multiplayer game, you can execute ``` python3 pvp.py ``` in your terminal. It prompts the players for their names and starts accepting moves with Player One as white and Player Two as black. There is no time limit to move or respond. 

##### General Usage 
The ChessCore Engine requires the chess and python-chess libraries (see "requirements.txt") to access functions such as displaying the board or retrieving a list of legal moves. To install these libraries, run
``` pip install -r requirements.txt ``` in the /project/chess directory. The goal of the game is to checkmate the computer or your opponent in seventy-five moves or less. You can press Ctrl + C to resign and automatically exit. Some common chess openings include: ``` e2e4, d2d4, g1f3, c2c4 ``` If your move is invalid, you will be asked to move again. After the game is over, the program will save the results in a file called data.txt 

#### Algorithms 
Below is part of the code for minimax, the fastest algorithm for analysing and assigning scores to nodes in a graph. In this case, the nodes are chess moves and the graph is the board. 

``` if turn: best = -float("inf") moves = order() current = moves[0] for move in moves: board.push(move) current = minimax(depth - 1, alpha, beta, not turn) if current > DISTANCE: current -= 1 elif current < -DISTANCE: current += 1 best = max( best, current, ) board.pop() alpha = max(alpha, best) if beta <= alpha: return best return best else: best = float("inf") moves = order() current = moves[0] for move in moves: board.push(move) current = minimax(depth - 1, alpha, beta, not turn) if current > DISTANCE: current -= 1 elif current < -DISTANCE: current += 1 best = min( best, current, ) board.pop() beta = min(beta, best) if beta <= alpha: return best return best ``` 

This function aids the chess engine by assigning scores to each legal move (see pvc.select() for the minimax root function which sorts the moves by score). First, the moves are ordered by immediate value (see pvc.value() for the square and capture evaluations) and the first is initialised as the best. Then, each and every possible move is pushed to the board (made), assigned a score*, and popped from the board (unmade). Next, the move is compared to the previous best compared on how far away it is from checkmate, and the alpha-beta pruning is applied for moves with a theoretical score of infinity. Finally, the function will return the maximum (or minimum, depending on turn) of all scores for pvc.select() to return the best move and push it to the board. 

*Score is assigned by how the player will respond after the computer's move, and how the computer will respond to the player's counter. The highest-scoring move is the one with the highest evaluation after several moves with both the player and the computer. 
###### Created by Ethan Ali
