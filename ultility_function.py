import chess

def move_ordering(board: chess.Board) -> list:
    # Generate all legal moves
    moves = list(board.legal_moves)

    # Create a dictionary to store the priority of each move
    move_priority = {}

    # Assign a priority to each move
    for move in moves:
        priority = 0

        # If the move is a capture, increase its priority
        if board.is_capture(move):
            priority += 100

        # If the move gives a check, increase its priority
        if board.gives_check(move):
            priority += 50

        move_priority[move] = priority

    # Sort the moves based on their priority (descending order)
    sorted_moves = sorted(moves, key=lambda move: move_priority[move], reverse=True)

    return sorted_moves