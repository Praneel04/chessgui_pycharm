import math


class Gamestate():
    def __init__(self):

        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.wKingMoved = False
        self.wKingsideRookMoved = False
        self.wQueensideRookMoved = False
        self.bKingMoved = False
        self.bKingsideRookMoved = False
        self.bQueensideRookMoved = False

    def handleCastling(self, move):
        # row = move.endRow
        if move.pieceMoved == 'wK':
            if move.endCol == 2:  # Queen-side castling
                self.board[move.startRow][2] = 'wK'
                self.board[move.startRow][3] = 'wR'
                self.board[move.startRow][0] = "--"
                self.board[move.startRow][4] = "--"  # Update the original king and rook positions
            elif move.endCol == 6:  # King-side castling
                self.board[move.startRow][6] = 'wK'
                self.board[move.startRow][5] = 'wR'
                self.board[move.startRow][7] = "--"
                self.board[move.startRow][4] = "--"  # Update the original king and rook positions
        elif move.pieceMoved == 'bK':
            if move.endCol == 2:  # Queen-side castling
                self.board[move.startRow][2] = 'bK'
                self.board[move.startRow][3] = 'bR'
                self.board[move.startRow][0] = "--"
                self.board[move.startRow][4] = "--"  # Update the original king and rook positions
            elif move.endCol == 6:  # King-side castling
                self.board[move.startRow][6] = 'bK'
                self.board[move.startRow][5] = 'bR'
                self.board[move.startRow][7] = "--"
                self.board[move.startRow][4] = "--"  # Update the original king and rook positions

    def promotePawn(self):
        piece = input("Choose promotion piece (Q/R/N/B): ")
        if piece not in ['Q', 'R', 'N', 'B']:
            piece = 'Q'  # Default to Queen
        return piece
    def is_in_check(self, board,whitetoMove):
        king_row = -1
        king_col = -1
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == ('wK' if whitetoMove else 'bK'):
                    king_row = row
                    king_col = col
                    break

        opponent_color = 'b' if whitetoMove else 'w'
        opponent_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Add possible knight move combinations
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in opponent_directions + knight_moves:
            r, c = king_row + dr, king_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "--":
                    if piece[0] == opponent_color:
                        if (piece[1] == 'Q' or
                                (abs(dr) == 1 and abs(dc) == 0 and piece[1] == 'R') or  # Rook
                                (abs(dr) == 0 and abs(dc) == 1 and piece[1] == 'R') or  # Rook
                                (abs(dr) == 1 and abs(dc) == 1 and piece[1] == 'B') or  # Bishop
                                (abs(dr) == 2 and abs(dc) == 1 and piece[1] == 'N') or  # Knight
                                (abs(dr) == 1 and abs(dc) == 2 and piece[1] == 'N')):  # Knight
                            return True
                    break  # Stop checking in this direction if an obstacle is encountered
                r += dr
                c += dc

        return False

    def find_king(self, board):

        king_type = "wK" if self.whiteToMove else "bK"
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c] == king_type:
                    return r, c

    def is_checkmate(self):
        print(self.is_in_check(self.board, self.whiteToMove))
        # First, check if the current player is in check
        if len(self.moveLog) == 0:
            return False
        # elif not self.is_in_check(self.board,self.whiteToMove):
        #     return False


        elif self.is_in_check(self.board,self.whiteToMove):
            # king_row, king_col = self.find_king(self.board)

            # Generate all possible moves for the current player
            possible_moves = self.generate_possible_moves()
            print(possible_moves)
            if(len(possible_moves))==0:
                return True
            else:
                return False

            # Check if any of the possible moves can get the king out of check
        #     for move_obj in possible_moves:
        #         temp_board = [row[:] for row in self.board]
        #         temp_board[move_obj.startRow][move_obj.startCol] = "--"
        #         temp_board[move_obj.endRow][move_obj.endCol] = move_obj.pieceMoved
        #         if not self.is_in_check(temp_board,self.whiteToMove):
        #             return False  # At least one legal move can escape check
        #
        #     return True  # No legal moves to escape check, it's checkmate
        # return False
    def is_stalemate(self):
        if not self.is_in_check(self.board, self.whiteToMove):
            possible_moves1 = self.generate_possible_moves()
            # print(possible_moves1)
            if(len(possible_moves1))==0:
                return True
            else:
                return False
        #     if not possible_moves1:
        #         return True  # No legal moves available, it's stalemate
        #
        #     for move_obj in possible_moves1:
        #         temp_board1 = [row[:] for row in self.board]
        #         temp_board1[move_obj.startRow][move_obj.startCol] = "--"
        #         temp_board1[move_obj.endRow][move_obj.endCol] = move_obj.pieceMoved
        #
        #         if not self.is_in_check(temp_board1, self.whiteToMove):
        #             return False  # At least one legal move is available
        #
        #     return True  # All moves lead to check, it's stalemate
        # else:
        #
        #     return False  # Player is in check, not stalemate

    def generate_possible_moves(self):
        possible_moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if (piece[0] == 'w' and self.whiteToMove) or (piece[0] == 'b' and not self.whiteToMove):
                    for row in range(8):
                        for col in range(8):
                            move_obj = move((r, c), (row, col), self.board,self.whiteToMove, self)
                            temp_board = [row[:] for row in self.board]
                            temp_board[move_obj.startRow][move_obj.startCol] = "--"
                            temp_board[move_obj.endRow][move_obj.endCol] = move_obj.pieceMoved


                            if self.is_in_check(temp_board,self.whiteToMove):
                                pass
                            elif move_obj.isValid(self.board):
                                possible_moves.append(move_obj)
        # print(possible_moves)
        print(len(possible_moves))
        for i in possible_moves:
            print(i.startRow, i.startCol)
            print(i.endRow, i.endCol)
        return possible_moves

    def makeMove(self, move):
        # if move.checkmate(self.board):
        #     print("Checkmate!")

        promotion_row = 0 if move.pieceMoved[0] == 'w' else 7

        if move.pieceMoved == 'wp' and move.endRow == promotion_row:
            piece = self.promotePawn()  # Get the chosen promotion piece
            promotion_piece = 'w' + piece
            # print(move.endRow,move.endCol)
            self.board[move.endRow][move.endCol] = promotion_piece
            self.board[move.startRow][move.startCol] = "--"



        elif (
                self.board[move.startRow][move.startCol] == 'wK'
                or self.board[move.startRow][move.startCol] == 'bK'
        ):
            if abs(move.startCol - move.endCol) == 2:  # Castling move
                # print(move.pieceMoved)
                self.handleCastling(move)
                self.whiteToMove = not self.whiteToMove
            else:
                self.board[move.startRow][move.startCol] = "--"

                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.moveLog.append(move)
                self.whiteToMove = not self.whiteToMove
        else:
            if (
                    move.pieceMoved[1] == 'p'
                    and abs(move.startCol - move.endCol) == 1
                    and abs(move.startRow - move.endRow) == 1
                    and self.board[move.endRow][move.endCol] == "--"
            ):  # En passant capture
                self.board[move.startRow][move.startCol] = "--"
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.board[move.startRow][move.endCol] = "--"  # Remove the captured pawn
                self.moveLog.append(move)
                self.whiteToMove = not self.whiteToMove
            else:
                self.board[move.startRow][move.startCol] = "--"
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.moveLog.append(move)
                self.whiteToMove = not self.whiteToMove


    # def is_in_check(self, board):
    #     king_row = -1
    #     king_col = -1
    #     for row in range(len(board)):
    #         for col in range(len(board[row])):
    #             if self.board[row][col] == ('wK' if self.whiteToMove else 'bK'):
    #                 king_row = row
    #                 king_col = col
    #                 break
    #
    #     opponent_color = 'b' if self.whiteToMove else 'w'
    #     opponent_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    #
    #     # Add possible knight move combinations
    #     knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    #
    #     # Add possible pawn attack directions
    #     pawn_attacks = [(-1, 1), (-1, -1)] if self.whiteToMove else [(1, 1), (1, -1)]
    #
    #     for dr, dc in opponent_directions + knight_moves + pawn_attacks:
    #         r, c = king_row + dr, king_col + dc
    #         if 0 <= r < 8 and 0 <= c < 8:
    #             piece = board[r][c]
    #             if piece != "--":
    #                 if piece[0] == opponent_color:
    #                     if (piece[1] == 'Q' or
    #                             (abs(dr) == 1 and abs(dc) == 0 and piece[1] == 'R') or  # Rook
    #                             (abs(dr) == 0 and abs(dc) == 1 and piece[1] == 'R') or  # Rook
    #                             (abs(dr) == 1 and abs(dc) == 1 and piece[1] == 'B') or  # Bishop
    #                             (abs(dr) == 2 and abs(dc) == 1 and piece[1] == 'N') or  # Knight
    #                             (abs(dr) == 1 and abs(dc) == 2 and piece[1] == 'N') or  # Knight
    #                             (abs(dr) == 1 and abs(dc) == 1 and piece[1] == 'P')):  # Pawn
    #                         return True
    #
    #     return False


class move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, whiteToMove, gamestate):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.whitetomove = whiteToMove
        self.gamestate = gamestate
        self.has_king_moved = (
            gamestate.wKingMoved if self.pieceMoved == 'wK' else gamestate.bKingMoved
        )
        if self.pieceMoved == 'wR':
            self.has_queenside_rook_moved = gamestate.wQueensideRookMoved
            self.has_kingside_rook_moved = gamestate.wKingsideRookMoved
        elif self.pieceMoved == 'bR':
            self.has_queenside_rook_moved = gamestate.bQueensideRookMoved
            self.has_kingside_rook_moved = gamestate.bKingsideRookMoved
        else:
            self.has_queenside_rook_moved = False
            self.has_kingside_rook_moved = False

    # def is_in_check_after_move(self):
    #     # Simulate the move and check if it leads to check
    #     temp_board = [row[:] for row in self.gamestate.board]
    #     temp_board[self.endRow][self.endCol] = temp_board[self.startRow][self.startCol]
    #     temp_board[self.startRow][self.startCol] = "--"
    #
    #     return self.is_in_check(temp_board)

    def is_square_attacked(self, row, col, board):
        opponent_color = 'w' if self.whitetomove else 'b'

        # Check for attacks from opponent's pawns
        pawn_direction = 1 if self.whitetomove else -1
        pawn_attack_offsets = [(pawn_direction, 1), (pawn_direction, -1)]

        for dr, dc in pawn_attack_offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece == opponent_color + 'p':
                    return True

        knight_offsets = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

        for dr, dc in knight_offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece == opponent_color + 'N':
                    return True

        # Check for attacks from opponent's diagonally moving pieces
        diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in diagonal_directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "--":
                    if piece[0] == opponent_color and (piece[1] == 'B' or piece[1] == 'Q'):
                        return True
                    break
                r += dr
                c += dc

        straight_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in straight_directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece != "--":
                    if piece[0] == opponent_color and (piece[1] == 'R' or piece[1] == 'Q'):
                        return True
                    break
                r += dr
                c += dc

        king_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in king_offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece == opponent_color + 'K':
                    return True

        return False

    # def is_checkmate(self,board,whitetomove,gamestate):
    #     if self.is_in_check(board):
    #         if self.whitetomove:
    #             king_row, king_col = self.find_king(board)
    #         else:
    #             king_row, king_col = self.find_king(board)
    #
    #         for r in range(8):
    #             for c in range(8):
    #                 piece = board[r][c]
    #                 if piece[0] == ("w" if self.whitetomove else "b"):
    #                     for row in range(8):
    #                         for col in range(8):
    #                             move_obj = move((r, c), (row, col), board[r][c],whitetomove,gamestate)
    #                             if self.isValid(move_obj):
    #                                 # Simulate the move
    #                                 temp_board = [row[:] for row in board]
    #                                 temp_board[row][col] = temp_board[r][c]
    #                                 temp_board[r][c] = "--"
    #
    #                                 if not self.is_in_check(temp_board):
    #                                     return False  # At least one legal move can escape check
    #         return True  # No legal moves to escape check, it's checkmate
    #     return False  # King is not in check, no checkmate
    # def find_king(self,board):
    #     for r in range(8):
    #         for c in range(8):
    #             if board[r][c] == ('wK' if self.whitetomove else 'bK'):
    #                 return r, c
    # def checkmate(self,board):
    #     king_row, king_col = self.find_king(board)
    #
    #     for r in range(8):
    #         for c in range(8):
    #             piece = board[r][c]
    #             if piece[0] == ("w" if self.whitetomove else "b"):
    #                 for row in range(8):
    #                     for col in range(8):
    #                         move_obj = move((r, c), (row, col), board,self.whitetomove,self.gamestate)
    #
    #                         if move_obj.isValid(board):
    #                             # Simulate the move and check if it leads to check
    #                             if not move_obj.is_in_check_after_move():
    #                                 return False
    #     return True

    def isValid(self, board):
        # possible_moves=self.gamestate.generate_possible_moves()

        # if self.is_pinned(board) and self.startRow != -1:
        # Piece is pinned and is not the king (startRow != -1)
        # return False  # The piece is pinned, it cannot move
        if (self.pieceMoved[0] == 'w' and self.whitetomove == True) or (
                self.pieceMoved[0] == 'b' and self.whitetomove == False):
            temp_board = [row[:] for row in board]
            temp_board[self.startRow][self.startCol] = "--"
            temp_board[self.endRow][self.endCol] = self.pieceMoved

            # print(temp_board)
            # print(self.gamestate.is_in_check(temp_board,self.gamestate.whiteToMove))

            # Check if the move would put the king in check after it is made
            if self.gamestate.is_in_check(temp_board,self.gamestate.whiteToMove):
                return False
            elif self.pieceMoved == 'bN' or self.pieceMoved == 'wN':
                if (abs(self.endRow - self.startRow) == 2 and abs(self.endCol - self.startCol) == 1) or (
                        abs(self.endRow - self.startRow) == 1 and abs(self.endCol - self.startCol) == 2):
                    if board[self.endRow][self.endCol] == "--" or (
                            board[self.endRow][self.endCol][0] != self.pieceMoved[0]):
                        return True
                    else:
                        return False
                else:
                    return False



            elif (self.pieceMoved == 'bB' or self.pieceMoved == 'wB'):

                if abs(self.endRow - self.startRow) == abs(self.endCol - self.startCol):

                    row_direction = 1 if self.endRow > self.startRow else -1

                    col_direction = 1 if self.endCol > self.startCol else -1

                    for i in range(1, abs(self.endRow - self.startRow)):

                        row = self.startRow + i * row_direction

                        col = self.startCol + i * col_direction

                        if board[row][col] != "--":
                            return False

                    if board[self.endRow][self.endCol] == "--" or (
                            board[self.endRow][self.endCol][0] != self.pieceMoved[0]):

                        return True

                    else:

                        return False

                else:

                    return False





            elif (self.pieceMoved == 'bR' or self.pieceMoved == 'wR'):

                if self.endRow == self.startRow:

                    for col in range(min(self.startCol, self.endCol) + 1, max(self.startCol, self.endCol)):

                        if board[self.startRow][col] != "--":
                            return False

                    if board[self.endRow][self.endCol] == "--" or (
                            board[self.endRow][self.endCol][0] != self.pieceMoved[0]):

                        return True

                    else:

                        return False

                elif self.endCol == self.startCol:

                    for row in range(min(self.startRow, self.endRow) + 1, max(self.startRow, self.endRow)):

                        if board[row][self.startCol] != "--":
                            return False

                    if board[self.endRow][self.endCol] == "--" or (
                            board[self.endRow][self.endCol][0] != self.pieceMoved[0]):

                        return True

                    else:

                        return False

                else:

                    return False


            elif (self.pieceMoved == 'bQ' or self.pieceMoved == 'wQ'):

                if abs(self.endRow - self.startRow) == abs(self.endCol - self.startCol):

                    row_direction = 1 if self.endRow > self.startRow else -1

                    col_direction = 1 if self.endCol > self.startCol else -1

                    for i in range(1, abs(self.endRow - self.startRow)):

                        row = self.startRow + i * row_direction

                        col = self.startCol + i * col_direction

                        if board[row][col] != "--":
                            return False

                    if board[self.endRow][self.endCol] == "--" or (
                            board[self.endRow][self.endCol][0] != self.pieceMoved[0]):

                        return True

                    else:

                        return False

                elif (self.endRow == self.startRow) or (self.endCol == self.startCol):

                    for col in range(min(self.startCol, self.endCol) + 1, max(self.startCol, self.endCol)):

                        if board[self.startRow][col] != "--":
                            return False

                    for row in range(min(self.startRow, self.endRow) + 1, max(self.startRow, self.endRow)):

                        if board[row][self.startCol] != "--":
                            return False

                    if board[self.endRow][self.endCol] == "--" or (
                            board[self.endRow][self.endCol][0] != self.pieceMoved[0]):

                        return True

                    else:

                        return False

                else:

                    return False









            elif self.pieceMoved == 'bp' or self.pieceMoved == 'wp':

                if abs(self.endCol - self.startCol) == 1:

                    if (

                            (self.endRow - self.startRow) == 1 if not self.whitetomove else (
                            self.endRow - self.startRow) == -1

                            and board[self.endRow][self.endCol] != "--"

                    ):  # Regular capture

                        return True

                    elif (

                            self.startRow == 4 and not self.whitetomove

                            and self.endRow == 5

                            and board[4][self.endCol] == "wp"

                            and board[5][self.endCol] == "--"

                    ):  # En passant capture

                        return True

                    elif (

                            self.startRow == 3 and self.whitetomove

                            and self.endRow == 2

                            and board[3][self.endCol] == "bp"

                            and board[2][self.endCol] == "--"

                    ):  # En passant capture

                        return True

                    else:

                        return False

                elif (

                        (self.endRow - self.startRow) == 1 if not self.whitetomove else (
                                                                                                self.endRow - self.startRow) == -1

                                                                                        and self.endCol - self.startCol == 0

                ):

                    if board[self.endRow][self.endCol] == "--":

                        return True

                    else:

                        return False

                elif (

                        abs(self.endRow - self.startRow) == 2

                        and self.endCol - self.startCol == 0

                ):

                    if (


                            (self.startRow == 1 or self.startRow == 6)

                            and (((board[2][self.endCol] == "--"

                            and board[3][self.endCol] == "--") and not self.whitetomove)
                            or
                                 ((board[5][self.endCol]=="--") and board[4][self.endCol]=="--" and self.whitetomove)
                    )

                    ):

                        return True

                    else:

                        return False

            elif (self.pieceMoved == 'bK' or self.pieceMoved == 'wK'):

                # Calculate absolute differences in row and column positions

                row_diff = abs(self.endRow - self.startRow)

                col_diff = abs(self.endCol - self.startCol)

                if row_diff <= 1 and col_diff <= 1:
                    return self.pieceCaptured == "--" or self.pieceCaptured[0] == ('b' if self.whitetomove else 'w')

                if (

                        self.startRow == self.endRow

                        and abs(self.endCol - self.startCol) == 2

                        and self.startRow in (0, 7)

                ):

                    if self.pieceMoved == 'wK' and self.startRow == 7:

                        if self.endCol == 6:  # King-side castling
                            return (
                                    board[7][5] == "--"
                                    and board[7][6] == "--"
                                # and not self.is_in_check(board)
                                # and not self.is_square_attacked(7, 4, board)
                                # and not self.is_square_attacked(7, 5, board)
                                # and not self.is_square_attacked(7, 6, board)
                                # and not self.has_king_moved
                                # and not self.has_kingside_rook_moved
                            )
                        elif self.endCol == 2:  # Queen-side castling
                            return (
                                    board[7][1] == "--"
                                    and board[7][2] == "--"
                                    and board[7][3] == "--"
                                # and not self.is_in_check(board)
                                # and not self.is_square_attacked(7, 4, board)
                                # and not self.is_square_attacked(7, 3, board)
                                # and not self.is_square_attacked(7, 2, board)
                                # and not self.has_king_moved
                                # and not self.has_queenside_rook_moved
                            )

                        # Similar conditions for black king
                    elif self.pieceMoved == 'bK' and self.startRow == 0:
                        if self.endCol == 6:  # King-side castling
                            return (
                                    board[0][5] == "--"
                                    and board[0][6] == "--"
                                    and not self.gamestate.is_in_check(board,self.whitetomove)
                                # and not self.is_square_attacked(0, 4, board)
                                # and not self.is_square_attacked(0, 5, board)
                                # and not self.is_square_attacked(0, 6, board)
                                # and not self.has_king_moved
                                # and not self.has_kingside_rook_moved
                            )
                        elif self.endCol == 2:  # Queen-side castling
                            return (
                                    board[0][1] == "--"
                                    and board[0][2] == "--"
                                    and board[0][3] == "--"
                                    and not self.gamestate.is_in_check(board,self.whitetomove)
                                # and not self.is_square_attacked(0, 4, board)
                                # and not self.is_square_attacked(0, 3, board)
                                # and not self.is_square_attacked(0, 2, board)
                                # and not self.has_king_moved
                                # and not self.has_queenside_rook_moved
                            )

                    return False

        else:
            return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
# class checkmate:
#     def __init__(self, gamestate,move1):
#         self.gamestate = gamestate
#         self.move1 = move1
#     def find_king(self,board):
#         king_type = "wK" if self.gamestate.whiteToMove else "bK"
#         for r in range(len(board)):
#             for c in range(len(board[r])):
#                 if board[r][c] == king_type:
#                     return r, c
#
#     def is_checkmate(self,board):
#         if self.move1.is_in_check(board):
#             if self.gamestate.whiteToMove:
#                 king_row, king_col = self.find_king(board)
#             else:
#                 king_row, king_col = self.find_king(board)
#
#             for r in range(8):
#                 for c in range(8):
#                     piece = board[r][c]
#                     if piece[0] == ("b" if self.gamestate.whiteToMove else "w"):
#                         for row in range(8):
#                             for col in range(8):
#                                 move_obj = move((r, c), (row, col), board[r][c], self.gamestate.whiteToMove, self.gamestate)
#                                 if self.move1.isValid(move_obj):
#                                     # Simulate the move
#                                     temp_board = [row[:] for row in board]
#                                     temp_board[row][col] = temp_board[r][c]
#                                     temp_board[r][c] = "--"
#
#                                     if not self.move1.is_in_check(temp_board):
#                                         return False  # At least one legal move can escape check
#             return True  # No legal moves to escape check, it's checkmate
#         return False  # King is not in check, no checkmate
