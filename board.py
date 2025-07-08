from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:
    
    def __init__(self):
        self.squares = []
        self.last_move = None
        self._create()
        self._add_pieces('w')
        self._add_pieces('b')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # Console Board Move Update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Pawn Promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)
        
        # King Castling
        if isinstance(piece, King) and self.castling(initial, final):
            diff = final.col - initial.col
            rook = piece.left_rook if (diff < 0) else piece.right_rook
            self.move(rook, rook.validMoves[-1])

        # move
        piece.moved = True

        # Clear valid moves
        piece.clear_moves()

        # Set last move
        self.last_move = move

    def in_check(self, piece, move):
        """
        Check if the move puts the King in check.
        """
        # Store original positions
        initial = move.initial
        final = move.final
        original_piece = self.squares[final.row][final.col].piece
        
        # Temporarily make the move
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        # Find our king
        king_row, king_col = None, None
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    p = self.squares[row][col].piece
                    if isinstance(p, King) and p.color == piece.color:
                        king_row, king_col = row, col
                        break
            if king_row is not None:
                break
        
        # Check if any enemy piece can attack our king
        in_check = False
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    enemy_piece = self.squares[row][col].piece
                    if enemy_piece.color != piece.color:
                        # Store enemy's current moves to restore later
                        old_moves = enemy_piece.validMoves.copy()
                        # Clear previous moves and calculate new ones
                        enemy_piece.clear_moves()
                        self.calc_moves(enemy_piece, row, col, bool=False)
                        
                        # Check if any move attacks our king
                        for m in enemy_piece.validMoves:
                            if m.final.row == king_row and m.final.col == king_col:
                                in_check = True
                                break
                        
                        # Restore enemy's original moves
                        enemy_piece.validMoves = old_moves
                        
                        if in_check:
                            break
            if in_check:
                break
        
        # Restore original board state
        self.squares[initial.row][initial.col].piece = piece  
        self.squares[final.row][final.col].piece = original_piece
        
        return in_check

    def valid_move(self, piece, move):
        return move in piece.validMoves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def calc_moves(self, piece, row, col, bool = True):
        """
        Calculate Possible/Valid moves for a piece at a given position.
        """
        def pawn_moves():
            # Steps
            steps = 1 if piece.moved else 2

            """
            Vertical Moves
            """
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        # Create Squares of new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # Create Move
                        move = Move(initial, final)

                        # Check potential CHECKS
                        if bool:
                            if not self.in_check(piece, move): 
                                # Bool->True, we are calculating moves for actual game
                                # append new valid move
                                piece.add_move(move)
                        else: 
                            # Bool->False, we are checking for Potential Checks
                            piece.add_move(move)
                    # Blocked
                    else: break
                
                # Not in range
                else: break

            """
            Diagonal Moves
            """
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        # Create Squares of new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create Move
                        move = Move(initial, final)
                        # Check potential CHECKS
                        if bool:
                            if not self.in_check(piece, move): 
                                # Bool->True, we are calculating moves for actual game
                                # append new valid move
                                piece.add_move(move)
                        else: 
                            # Bool->False, we are checking for Potential Checks
                            piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1)
            ]

            # Add debug print to troubleshoot
            print(f"Knight color: {piece.color}")
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    target_square = self.squares[possible_move_row][possible_move_col]
                    # Add debugging to verify team piece detection
                    if target_square.has_piece():
                        target_piece = target_square.piece
                        print(f"Target piece at {possible_move_row},{possible_move_col}: {target_piece.name}, color: {target_piece.color}")
                        print(f"Is team piece: {target_square.has_team_piece(piece.color)}")
                    
                    if self.squares[possible_move_row][possible_move_col].is_empty() or self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            # else: break
                        else:
                            # append new move
                            piece.add_move(move)

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # Create Squares of new possible move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        # Empty Square -> Continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            # Create Move
                            move = Move(initial, final)
                            # Check potential CHECKS
                            if bool:
                                if not self.in_check(piece, move): 
                                    # Bool->True, we are calculating moves for actual game
                                    # append new valid move
                                    piece.add_move(move)
                            else: 
                                # Bool->False, we are checking for Potential Checks
                                piece.add_move(move)
                        
                        # Rival Piece -> Add move and break
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            # Create Move
                            move = Move(initial, final)
                            # Check potential CHECKS
                            if bool:
                                if not self.in_check(piece, move): 
                                    # Bool->True, we are calculating moves for actual game
                                    # append new valid move
                                    piece.add_move(move)
                            else: 
                                # Bool->False, we are checking for Potential Checks
                                piece.add_move(move)
                            break
                        
                        # Team Piece -> Blocked
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                        
                        # Increment position INSIDE the loop
                        possible_move_row += row_incr
                        possible_move_col += col_incr
                    
                    # Not in range
                    else: break

        def king_moves():
            # 8 possible moves
            possible_moves = [
                (row-1, col-1), # up-left
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col-1), # left
                (row+0, col+1), # right
                (row+1, col-1), # down-left
                (row+1, col+0), # down
                (row+1, col+1)  # down-right
            ]

            for move in possible_moves:
                move_row, move_col = move
                
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].is_empty() or self.squares[move_row][move_col].has_rival_piece(piece.color):
                        # Create Squares of new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        # Create Move
                        move = Move(initial, final)
                        # Check potential CHECKS
                        if bool:
                            if not self.in_check(piece, move): 
                                # Bool->True, we are calculating moves for actual game
                                # append new valid move
                                piece.add_move(move)
                        else: 
                            # Bool->False, we are checking for Potential Checks
                            piece.add_move(move)
            
            # Castling moves
            if not piece.moved:
                # Castling is only possible if the King has not moved and is not in check
                # Queen-side
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook) and not left_rook.moved:
                    for c in range(1,4):
                        # Castling is not possible if there are pieces in the way
                        if self.squares[row][c].has_piece(): 
                            break
                        if c == 3:
                            # Adds left_rook to King
                            piece.left_rook = left_rook

                            # Rook Move
                            initial = Square(row, 0)
                            final = Square(row, 3)
                            move = Move(initial, final)
                            left_rook.add_move(move)

                            # King Move
                            initial = Square(row, col)
                            final = Square(row, 2)
                            move = Move(initial, final)
                            piece.add_move(move)

                # King-side
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook) and not right_rook.moved:
                    for c in range(5,7):
                        # Castling is not possible if there are pieces in the way
                        if self.squares[row][c].has_piece(): 
                            break
                        if c == 6:
                            # Adds right_rook to King
                            piece.right_rook = right_rook

                            # Rook Move
                            initial = Square(row, 7)
                            final = Square(row, 5)
                            move = Move(initial, final)
                            right_rook.add_move(move)

                            # King Move
                            initial = Square(row, col)
                            final = Square(row, 6)
                            move = Move(initial, final)
                            piece.add_move(move)
        """
        Pieces  
        """

        if isinstance(piece, Pawn): 
            pawn_moves()
        elif isinstance(piece, Knight): 
            knight_moves()
        
        elif isinstance(piece, Bishop): 
            straight_line_moves([
                (-1,-1), # up-left
                (-1,1),  # up-right
                (1,-1), # down-left
                (1,1),   # down-right
            ])
        elif isinstance(piece, Rook): 
            straight_line_moves([
                (-1,0), # up
                (1,0),  # down
                (0,-1), # left
                (0,1),   # right
            ])
        elif isinstance(piece, Queen): 
            straight_line_moves([
                (-1,-1), # up-left
                (-1,1),  # up-right
                (1,-1), # down-left
                (1,1),   # down-right
                (-1,0), # up
                (1,0),  # down
                (0,-1), # left
                (0,1),   # right
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        # Initialize the 2D list structure first
        self.squares = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        # print(self.squares)
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
                # print(self.squares[row][col])

    def _add_pieces(self, color):
        """
        Add pieces to the board based on the color.
        """

        row_pawn, row_other = (6,7) if color == 'w' else (1,0)

        # All Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))