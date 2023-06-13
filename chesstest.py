import chess

board = chess.Board()
print(list(board.legal_moves))
for move in board.legal_moves:
    print(move.to_square)