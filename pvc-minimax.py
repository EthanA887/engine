# Libraries
import chess
import chess.svg
import chess.polyglot
import sys
import time

# Chessboard to operate from
board = chess.Board()

try:
  def endgame():
    for square in chess.SQUARES:
      piece = board.piece_at(square)
      queens = 0
      bishops = 0
      knights = 0
      if piece and piece.piece_type == chess.QUEEN:
        queens += 1
      if piece and piece.piece_type == chess.BISHOP:
        bishops += 1
      if piece and piece.piece_type == chess.KNIGHT:
        knights += 1
    if queens == 0 or (queens == 2 and knights + bishops <= 1):
      return True
    else:
      return False

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
  rook = [0,  0,  0,  0,  0,  0,  100,  100,
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
  pawn_value = 0
  knight_value = 0
  bishop_value = 0
  rook_value = 0
  queen_value = 0
  if endgame() == False:
    king = [-30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20];
  else:
    king = [-50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50];

  def evaluate():
    # In case of checkmate
    if board.is_checkmate():
        if board.turn:
            return -float('inf')
        else:
            return float('inf')
    # In case of draw by stalemate
    if board.is_stalemate():
      return 0
    # In case of draw by insufficient material
    if board.is_insufficient_material():
      return 0

    if endgame == False:
      pawn_value = 198
      knight_value = 817
      bishop_value = 836
      rook_value = 1270
      queen_value = 2521
    else:
      pawn_value = 258
      knight_value = 846
      bishop_value = 857
      rook_value = 1281
      queen_value = 2558

    # Material for each side
    material = pawn_value * (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK))) + knight_value * (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK))) + bishop_value * (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK))) + rook_value * (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK))) + queen_value * (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK)))

    # Ratings given by piece-square tables
    position = (sum([pawn[i] for i in board.pieces(chess.PAWN, chess.WHITE)]) + sum([-pawn[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)]) + sum([knight[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]) + sum([-knight[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)]) + sum([bishop[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]) + sum([-bishop[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)]) + sum([rook[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) + sum([-rook[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)]) + sum([queen[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) + sum([-queen[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)]) + sum([king[i] for i in board.pieces(chess.KING, chess.WHITE)]) + sum([-king[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)]))

    # Board evaluation by material and position
    evaluation = 3 * material + position
    if board.turn:
      # White
      return evaluation
    else:
      # Black
      return -evaluation

  def minimax(depth, alpha, beta, turn):
    if depth == 0:
      return -evaluate()
    if turn == True:
      score = -float('inf')
      for move in board.legal_moves:
        board.push(move)
        score = max(score, minimax(depth - 1, alpha, beta, not turn))
        board.pop()
        alpha = max(alpha, score)
        if beta <= alpha:
          return score
      return score
    else:
      score = float('inf')
      for move in board.legal_moves:
        board.push(move)
        score = min(score, minimax(depth - 1, alpha, beta, not turn))
        board.pop()
        beta = min(beta, score)
        if beta <= alpha:
          return score
      return score

  # Push the final move to the board by returning the best possible move
  def select(depth):
    try:
      # Read the Polyglot opening book (Baron 30)
      move = chess.polyglot.MemoryMappedReader("baron30.bin").weighted_choice(board).move
      return move
    except IndexError:
      limit = -float('inf')
      best = chess.Move.null()
      for move in board.legal_moves:
        board.push(move)
        value = minimax(depth - 1, -float('inf'), float('inf'), False)
        board.pop()
        if value >= limit:
          limit = value
          best = move
      return best

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

  depth = int(received)
  if depth > 10:
    print("Error: You must provide an integer in the range of 1 and 10.")
    sys.exit(1)

  # Play the game
  print(board)
  while board.is_game_over() == False:
    if board.turn:
      try:
        move = input("Player: ").rstrip()
        board.push_san(move)
      except ValueError:
        print("Sorry, illegal move.")
    else:
      print("Thinking...")
      output = select(depth)
      display = board.san(output)
      print(f"Computer: {display}")
      board.push(output)
    print(board)

  # Save results of game
  with open("data.txt", "a") as file:
    for i in range(10):
      print("-", end="")
    print("")
    time.sleep(1)
    name = input("Enter your name: ")
    file.write("{} VS Computer. ".format(name))
    # Mate  
    if board.is_checkmate():
      if board.turn:
        print("Checkmate, black is victorious.")
        file.write("1 - 0 (Checkmate).\n")
      else:
        print("Checkmate, white is victorious.")
        file.write("0 - 1 (Checkmate).\n")
    # Stalemate
    elif board.is_stalemate():
      print("Draw by stalemate.")
      file.write("1/2 - 1/2 (Stalemate).\n")
    # Insufficient material to mate
    elif board.is_insufficient_material():
      print("Draw by insufficient material.")
      file.write("1/2 - 1/2 (Insufficient Material).\n")
    # Fivefold repetition (as of July 1, 2014)
    elif board.is_fivefold_repetition():
      print("Draw by fivefold repetition.")
      file.write("1/2 - 1/2 (Automatic Repetition).\n")
    # Seventy-five moves game limit (as of July 1, 2014)
    elif board.is_seventyfive_moves():
      print("Draw by seventy-five moves.")
      file.write("1/2 - 1/2 (Seventy-five Moves).\n")
  print("Analyse this game at https://lichess.org/analysis")
  sys.exit(0)
except KeyboardInterrupt:
  print("\b\bYou have quit the ChessCore Engine.")

# Created by Ethan Ali
