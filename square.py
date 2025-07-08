class Square:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col] if col in self.ALPHACOLS else None
    
    def __eq__(self, other):
        """
        Check if two squares are equal based on their row and column.
        """
        return self.row == other.row and self.col == other.col
    
    def has_piece(self):
        """
        Check if the square has a piece.
        """
        return self.piece is not None
    
    def is_empty(self):
        """
        Check if the square is empty.
        """
        return not self.has_piece()
    
    def has_team_piece(self, color):
        """
        Check if the square has a piece of the same color.
        """
        return self.has_piece() and self.piece.color == color
    
    def has_rival_piece(self, color):
        """
        Check if the square has a piece of the rival color.
        """
        return self.has_piece() and self.piece.color != color
    
    def is_empty_OR_rival(self, color):
        """
        Check if the square is empty or has a rival piece.
        """
        return self.is_empty() or (self.has_piece() and self.piece.color != color)
    
    @staticmethod
    def in_range(*args):
        """
        Check if the given coordinates are within the board's range.
        """
        return all(0 <= arg < 8 for arg in args)
    
    @staticmethod
    def get_alphacol(col):
        """
        Get the alphabetic column representation for a given column index.
        """
        return Square.ALPHACOLS.get(col, None)

# print(Square.in_range(0, 1, 2))  # True
# print(Square.in_range(0, 1, 8))  # False