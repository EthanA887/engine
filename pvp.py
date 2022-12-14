import chess
import time
import sys

board = chess.Board()
print("Welcome to the ChessCore Engine.")
for i in range(10):
  print("-", end="")
print("")

try:
  p1 = input("Player One, enter your name: ")
  p2 = input("Player Two, enter your name: ")
  print(board)
  while board.is_game_over() == False:
    if board.turn:
      try:
        white = input("Player One: ")
        board.push_san(white.rstrip())
      except ValueError: print("Sorry, illegal move.")
    else:
      try:
        black = input("Player Two: ")
        board.push_san(black.rstrip())
      except ValueError: print("Sorry, illegal move.")
    print(board)
  
  # Save results of game
  with open("data.txt", "a") as file:
    for i in range(10):
      print("-", end="")
    print("")
    time.sleep(1)
    file.write("{} VS {}. ".format(p1, p2))
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
  sys.exit(1)

# Created by Ethan Ali