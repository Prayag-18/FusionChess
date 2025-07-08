import pygame
from config import Config
from const import *
from board import Board
from dragger import Dragger
from square import Square

class Game:
    """
    Game class handles the chess game logic and rendering. 
    """
    def __init__(self):
        self.next_player = 'w'
        self.hovered_sq = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()


    """
    Show methods
    """

    def show_bg(self, surface):     # surface = self._screen
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # Color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # Draw the square
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)  # Start pos at x-axis, Start pos at y-axis, WIDTH, HEIGHT
                # Blit
                pygame.draw.rect(surface, color, rect)

                # Row Coordinates
                if col == 0:
                    # Color
                    color = theme.bg.dark if row%2 == 0 else theme.bg.light
                    # Label
                    label = self.config.font.render(str(ROWS - row), 1, color)
                    # Position
                    label_pos = (5, 5+ row * SQSIZE)
                    # Blit
                    surface.blit(label, label_pos)
                
                # Column Coordinates
                if row == ROWS - 1:
                    # Color
                    color = theme.bg.dark if (row + col)%2 == 0 else theme.bg.light
                    # Label
                    label = self.config.font.render(Square.get_alphacol(col), 1, color)
                    # Position
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # Blit
                    surface.blit(label, label_pos)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    
                    if piece is not self.dragger.piece:
                        # Make sure the texture is loaded as a pygame image
                        if not hasattr(piece, 'img'):
                            try:
                                piece.img = pygame.image.load(piece.texture)
                                # Scale pieces to 220% of square size for better proportions
                                piece_size = int(SQSIZE * 2.2)
                                piece.img = pygame.transform.scale(piece.img, (piece_size, piece_size))
                            except:
                                print(f"Failed to load image: {piece.texture}")
                                continue
                        
                        # Calculate position to properly center the piece in the square
                        img_width, img_height = piece.img.get_size()
                        pos_x = col * SQSIZE + (SQSIZE - img_width//2  + 30) // 2
                        pos_y = row * SQSIZE + (SQSIZE - img_height//2 + 30) // 2
                        
                        # Blit at the correct position
                        surface.blit(piece.img, (pos_x, pos_y))
    
    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # Loop all Valid moves
            for move in piece.validMoves:
                # Color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # Blit
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # Color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # Rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # Blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sq:
            # Color
            color = (180, 180, 180) if (self.hovered_sq.row + self.hovered_sq.col) % 2 == 0 else (255, 255, 0)
            # Rect
            rect = (self.hovered_sq.col * SQSIZE, self.hovered_sq.row * SQSIZE, SQSIZE, SQSIZE)
            # Blit
            pygame.draw.rect(surface, color, rect, width=4)

    """
    Other methods
    """

    def next_turn(self):
        """
        Switches the turn to the next player.
        """
        self.next_player = 'b' if self.next_player == 'w' else 'w'

    def set_hover(self, row, col):
        self.hovered_sq = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()
    
    def play_sound(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()