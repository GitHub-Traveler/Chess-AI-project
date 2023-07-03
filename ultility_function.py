import chess
from chess import Move, Piece


def distance_to_center(move: Move, board : chess.Board):
    #Function to calculate the distance to the center
    print(move.to_square)
    print(type(board.piece_at(move.to_square)))
    end_pos = move.to_square
    print(end_pos)

    dis_center = float(end_pos) - 32.5
    return int(dis_center)

def extra_value(move: Move, board: chess.Board):
    # Calculate the value that get whenever detect a capture
    point_for_piece = {10: ["p", "P"], 30: ["b","B","n","N"], 50 :["r", "R"], 90: ["q","Q"]}
    a =  board.piece_at(move.from_square).symbol()
    b =  board.piece_at(move.to_square).symbol()
    a_value = 0
    b_value = 0
    for v in point_for_piece.values():
        if a_value == 0:
            if a in v:
                a_value = list(point_for_piece.keys())[list(point_for_piece.values()).index(v)]

        if b_value == 0:
            if b in v:
                b_value = list(point_for_piece.keys())[list(point_for_piece.values()).index(v)]
        if a_value != 0 and b_value!= 0:
            break 
    return b_value - a_value


def move_ordering(board: chess.Board):

    # Generate all legal moves
    moves = list(board.legal_moves)


    # Create a dictionary to store the priority of each move
    move_priority = {}

    # Assign a priority to each move
    for move in moves:

        priority = 0
        #Prioritize moves that occupie the center of te board
        #priority -= distance_to_center(move, board)*5

        # If the move is a capture, increase its priority
        if board.is_capture(move) and not board.is_en_passant(move):            
            priority += (extra_value(move, board)*100 +  100)
        if board.is_en_passant(move):
            priority += 10

        # If the move gives a check, increase its priority
        if board.gives_check(move):
            priority += 50
        if move.promotion != None:
            priority += 100
        if board.is_castling(move):
            priority += 100


        """"
        #Try to that move
        board.push(move)
        new_moves = list(board.legal_moves)
        #Potential additional number of squares in the next turn when choose that move
        extra_potential_area = len(moves) - len(new_moves) 
        priority += 5*extra_potential_area #The more potential squares it create, the higher priority it has
        #Undo the move
        board.pop()
        """



        move_priority[move] = priority

    # Sort the moves based on their priority (descending order)
    sorted_moves = sorted(moves, key=lambda move: move_priority[move], reverse=True)



    return sorted_moves