import chess
import chess.engine
def evaluation(board):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish\src\stockfish.exe")
    result = engine.play(board, chess.engine.Limit(depth=25))
    print(list(result))
    engine.close()
    return result['score']

board = chess.Board()
for move in board.legal_moves:
    print(i)
