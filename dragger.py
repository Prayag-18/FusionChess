import pygame
from const import *


class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
    
    """
    Blit Method
    """

    def update_blit(self, surface):
        # Texture is the image of the piece
        # Texture
        self.piece.set_texture(self.piece.texture)
        texture = self.piece.texture
        
        # img
        img = pygame.image.load(texture)
        img_size = int(SQSIZE * 2.6)
        img = pygame.transform.scale(img, (img_size, img_size))

        # rect
        img_center = (self.mouseX + 78, self.mouseY + 80)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # print(f"img_center: {img_center}")

        # blit
        surface.blit(img, self.piece.texture_rect)


    """
    Other Methods
    """

    def update_mouse(self, pos):
        """
        Update the mouse position.
        """
        self.mouseX, self.mouseY = pos
        # print(f"Mouse position: {self.mouseX}, {self.mouseY}")
    
    def save_initial_pos(self, pos):
        """
        Save the initial position of the mouse.
        """
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE
    
    def drag_piece(self, piece):
        """
        Save the piece we're dragging.
        """
        self.piece = piece
        self.dragging = True
    
    def undrag_piece(self):
        """
        Stop dragging the piece.
        """
        self.piece = None
        self.dragging = False