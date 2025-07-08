import os

class Piece:
    
    def __init__(self, name, color, value, texture=None, texture_rect=None):   # texture equivalent to img path or url
        self.name = name
        self.color = color

        value_sign = 1 if color == 'w' else -1
        self.value = value * value_sign
        self.validMoves = []
        self.moved = False
        self.texture = texture
        self.set_texture(texture)
        self.texture_rect = texture_rect
    
    def set_texture(self, texture=None):
        if texture:
            self.texture = texture
        else:
            # Fix the path separators and ensure the directory exists
            self.texture = os.path.join("assets", "pieces-basic-svg", f"{self.name.lower()}-{self.color}.svg")

    def add_move(self, move):
        """
        Add a move to the list of valid moves.
        """
        self.validMoves.append(move)

    def clear_moves(self):
        """
        Clear the list of valid moves.
        """
        self.validMoves = []

# Subclasses of Piece
class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'w' else 1    # Up for white, Down for black

        # Initialize the Pawn with Parent class
        super().__init__(name='Pawn', color=color, value=1.0)

class Knight(Piece):

    def __init__(self, color):
        # Initialize the Knight with Parent class
        super().__init__(name='Knight', color=color, value=3.0)

class Bishop(Piece):

    def __init__(self, color):
        # Initialize the Bishop with Parent class
        super().__init__(name='Bishop', color=color, value=3.001)

class Rook(Piece):

    def __init__(self, color):
        # Initialize the Rook with Parent class
        super().__init__(name='Rook', color=color, value=5.0)

class Queen(Piece):

    def __init__(self, color):
        # Initialize the Queen with Parent class
        super().__init__(name='Queen', color=color, value=9.0)

class King(Piece):

    def __init__(self, color):
        # Initialize the King with Parent class
        self.left_rook = None
        self.right_rook = None
        super().__init__(name='King', color=color, value=10000.0)