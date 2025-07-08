import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move

class Main:
    """
    Main entry point of the chess game.
    Initializes pygame and handles the game loop.
    """
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Initialize screen with dimensions from constants
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        
        # Initialize the game object as per UML composition
        self.game = Game()
        
        # Start the game
        # self.game.start()
    
    def mainLoop(self):
        """
        Main game loop that handles events and updates the display
        """
        running = True
        clock = pygame.time.Clock()

        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        screen = self._screen
        
        while running:
            # Draw Game Elements
            # Show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            # Event handling
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    running = False
                
                # Click event
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE    # Row depends on y-coordinate
                    clicked_col = dragger.mouseX // SQSIZE    # Column depends on x-coordinate

                    # If clicked sq has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        # Valid piece(Color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial_pos(event.pos)
                            dragger.drag_piece(piece)
                            # Show methods
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # Mouse motion event
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # Show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)

                        dragger.update_blit(screen)
                
                # Click release event
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        release_row = dragger.mouseY // SQSIZE
                        release_col = dragger.mouseX // SQSIZE

                        # Create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(release_row, release_col)
                        move = Move(initial, final)

                        # Valid move ?
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[release_row][release_col].has_piece()
                            # Move piece
                            board.move(dragger.piece, move)

                            # Play sound
                            game.play_sound(captured)

                            # Show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # next turn
                            game.next_turn()

                    dragger.undrag_piece()
                
                # Key Press event
                elif event.type == pygame.KEYDOWN:
                    # Changing theme
                    if event.key == pygame.K_t:
                        game.config.change_theme()
                    
                    # Reset game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
            
            # Update display
            pygame.display.update()
            clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
        sys.exit()

# Entry point
if __name__ == "__main__":
    main = Main()
    main.mainLoop()