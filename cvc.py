# Libraries
import chess
import chess.svg
import chess.polyglot
import sys
import time

# Chessboard to operate from
board = chess.Board()

try:
  # https://www.chessprogramming.org/Simplified_Evaluation_Function#Piece-Square_Tables
  # Pawn positions table
  pawn = [0,  0,  0,  0,  0,  0,  0,  0,
  50, 50, 50, 50, 50, 50, 50, 50,
  10, 10, 20, 30, 30, 20, 10, 10,
  5,  5, 10, 25, 25, 10,  5,  5,
  0,  0,  0, 20, 20,  0,  0,  0,
  5, -5,-10,  0,  0,-10, -5,  5,
  5, 10, 10,-20,-20, 10, 10,  5,
  0,  0,  0,  0,  0,  0,  0,  0]

  # Knight positions table
  knight = [-50,-40,-30,-30,-30,-30,-40,-50,
  -40,-20,  0,  0,  0,  0,-20,-40,
  -30,  0, 10, 15, 15, 10,  0,-30,
  -30,  5, 15, 20, 20, 15,  5,-30,
  -30,  0, 15, 20, 20, 15,  0,-30,
  -30,  5, 10, 15, 15, 10,  5,-30,
  -40,-20,  0,  5,  5,  0,-20,-40,
  -50,-40,-30,-30,-30,-30,-40,-50]

  # Bishop positions table
  bishop = [-20,-10,-10,-10,-10,-10,-10,-20,
  -10,  0,  0,  0,  0,  0,  0,-10,
  -10,  0,  5, 10, 10,  5,  0,-10,
  -10,  5,  5, 10, 10,  5,  5,-10,
  -10,  0, 10, 10, 10, 10,  0,-10,
  -10, 10, 10, 10, 10, 10, 10,-10,
  -10,  5,  0,  0,  0,  0,  5,-10,
  -20,-10,-10,-10,-10,-10,-10,-20]

  # Rook positions table
  rook = [0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
  -5,  0,  0,  0,  0,  0,  0, -5,
  -5,  0,  0,  0,  0,  0,  0, -5,
  -5,  0,  0,  0,  0,  0,  0, -5,
  -5,  0,  0,  0,  0,  0,  0, -5,
  -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0]

  # Queen positions table
  queen = [-20,-10,-10, -5, -5,-10,-10,-20,
  -10,  0,  0,  0,  0,  0,  0,-10,
  -10,  0,  5,  5,  5,  5,  0,-10,
  -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
  -10,  5,  5,  5,  5,  5,  0,-10,
  -10,  0,  5,  0,  0,  0,  0,-10,
  -20,-10,-10, -5, -5,-10,-10,-20]

  # King positions tables
  king = [-30,-40,-40,-50,-50,-40,-40,-30,
  -30,-40,-40,-50,-50,-40,-40,-30,
  -30,-40,-40,-50,-50,-40,-40,-30,
  -30,-40,-40,-50,-50,-40,-40,-30,
  -20,-30,-30,-40,-40,-30,-30,-20,
  -10,-20,-20,-20,-20,-20,-20,-10,
  20, 20,  0,  0,  0,  0, 20, 20,
  20, 30, 10,  0,  0, 10, 30, 20]

  # If this move results in a check
  def gives_check(move):
    board.push(move)
    if board.is_check():
      x = True
    else:
      x = False
    board.pop()
    return x

  def evaluate():
    # In case of checkmate
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    # In case of draw by stalemate
    if board.is_stalemate():
        return 0
    # In case of draw by insufficient material
    if board.is_insufficient_material():
        return 0

    # Material for each side
    material = (100 * (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK))) + 310 * (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK))) + 320 * (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK))) + 500 * (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK))) + 900 * (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK))))

    # Ratings given by piece-square tables
    position = (sum([pawn[i] for i in board.pieces(chess.PAWN, chess.WHITE)]) + sum([-pawn[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)]) + sum([knight[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]) + sum([-knight[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)]) + sum([bishop[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]) + sum([-bishop[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)]) + sum([rook[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) + sum([-rook[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)]) + sum([queen[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) + sum([-queen[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)]) + sum([king[i] for i in board.pieces(chess.KING, chess.WHITE)]) + sum([-king[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)]))

    # Board evaluation by material and position
    evaluation = material + position
    if board.turn:
      # White
      return evaluation
    else:
      # Black
      return -evaluation

  # Alphabeta Search
  # https://www.chessprogramming.org/Alpha-Beta#Negamax_Framework
  def alphabeta(alpha, beta, depthleft):
    if depthleft == 0:
      return capture(alpha, beta)
    for move in board.legal_moves:  
      score = -alphabeta(-beta, -alpha, depthleft - 1)
      if score >= beta:
        return beta
      if score > alpha:
        alpha = score  
    return alpha

  # Quiescence Search
  # https://www.chessprogramming.org/Quiescence_Search#Pseudo_Code
  def capture(alpha, beta):
    stand_pat = evaluate()
    if stand_pat >= beta:
      return beta
    if alpha < stand_pat:
      alpha = stand_pat
    for move in board.legal_moves:
      if board.is_capture(move):
        board.push(move)        
        score = -capture(-beta, -alpha)
        board.pop()
        if score >= beta:
          return beta
        if score > alpha:
          alpha = score
    return alpha

  # Push the final move to the board by returning the best possible move
  def select(depth):
    try:
      # Read the Polyglot opening book (Baron 30)
      move = chess.polyglot.MemoryMappedReader("baron30.bin").weighted_choice(board).move
      return move
    except IndexError:
      best = chess.Move.null()
      limit = -float('inf')
      alpha = -float('inf')
      beta = float('inf')
      for move in board.legal_moves:
        board.push(move)
        value = -alphabeta(-beta, -alpha, depth - 1)
        if value > limit:
          limit = value
          best = move
        if value > alpha:
          alpha = value
        board.pop()
      return best

  # Input for search depth
  print("Welcome to the ChessCore Engine.")
  time.sleep(1)
  received = input("Depth: ")
  try:
    depth = int(received)
  except ValueError:
    length = 164
    for i in range(length + len(received)):
      print("\b", end="")
    print("Error: You must provide an integer in the range of 1 and 10.")
    sys.exit(1)

  # Convert depth to odd number
  depth = int(received)
  if depth > 10:
    print("Error: You must provide an integer in the range of 1 and 10.")
    sys.exit(1)
    
  for i in range(10):
    print("-", end="")
  print("")
  if depth % 2 == 0:
    depth += 1

  while board.is_game_over() == False:
    output = select(depth)
    display = board.san(output)
    if board.turn:
      print(f"White: {display}")
    else:
      print(f"Black: {display}")
    board.push(output)
    print(board)
    time.sleep(1 / 3)

  # Save results of game
  with open("data.txt", "a") as file:
    for i in range(10):
      print("-", end="")
    print("")
    time.sleep(1)
    # Mate
    if board.is_checkmate():
      if board.turn:
        print("Checkmate, white is victorious.")
        file.write("Computer VS Computer. 1 - 0 (Checkmate).\n")
      else:
        print("Checkmate, black is victorious.")
        file.write("Computer VS Computer. 0 - 1 (Checkmate).\n")
    # Stalemate
    elif board.is_stalemate():
      print("Draw by stalemate.")
      file.write("Computer VS Computer. 1/2 - 1/2 (Stalemate).\n")
    # Insufficient material to mate
    elif board.is_insufficient_material():
      print("Draw by insufficient material.")
      file.write("Computer VS Computer. 1/2 - 1/2 (Insufficient Material).\n")
    # Fivefold repetition (as of July 1, 2014)
    elif board.is_fivefold_repetition():
      print("Draw by fivefold repetition.")
      file.write("Computer VS Computer. 1/2 - 1/2 (Automatic Repetition).\n")
    # Seventy-five moves game limit (as of July 1, 2014)
    elif board.is_seventyfive_moves():
      print("Draw by seventy-five moves.")
      file.write("Computer VS Computer. 1/2 - 1/2 (Seventy-five Moves).\n")
  print("Analyse this game at https://lichess.org/analysis")
  sys.exit(0)
except KeyboardInterrupt:
  print("\b\bYou have quit the ChessCore Engine.")

# Created by Ethan Ali