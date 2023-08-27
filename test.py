# Import the ChessGame class
from Chess import chesseng
# Create an instance of the ChessGame class
chess_game = chesseng.Gamestate()

# Test cases
board_1 = [['bR', 'bN', 'bB', 'bQ', 'bK', '--', 'bN', 'bR'], ['bp', 'bp', 'bp', 'bp', '--', 'bp', 'bp', 'bp'], ['--', '--', '--', '--', '--', '--', '--', '--'], ['--', '--', '--', '--', 'bp', '--', '--', '--'], ['--', 'bB', '--', 'wp', '--', '--', '--', '--'], ['--', '--', '--', '--', 'wp', '--', '--', '--'], ['wp', 'wp', 'wp', 'wK', '--', 'wp', 'wp', 'wp'], ['wR', 'wN', 'wB', 'wQ', '--', 'wB', 'wN', 'wR']]

print("Is White King in check?", chess_game.is_in_check(board_1,True))  # Should print False

# board_2 = [
#     ['--', '--', '--', '--', '--', '--', '--', '--'],
#     ['--', '--', '--', '--', '--', '--', '--', '--'],
#     ['--', '--', '--', '--', '--', '--', '--', '--'],
#     ['--', '--', '--', '--', '--', '--', '--', '--'],
#     ['--', '--', '--', '--', '--', '--', '--', '--'],
#     ['--', '--', '--', '--', '--', '--', '--', '--'],
#     ['--', '--', '--', '--', '--', '--', 'bB', '--'],
#     ['--', '--', '--', '--', '--', '--', '--', 'wK'],
# ]
#
# print("Is White King in check?", chess_game.is_in_check(board_2))  # Should print True
