import pygame
from .base_entity import BaseEntity

class Door(BaseEntity):
    def __init__(self, x, y, code_expression="closed == True"):
        super().__init__(x, y, code_expression)
        self.closed_image = pygame.Surface((40, 60))
        self.closed_image.fill((139, 69, 19))  # Coklat
        self.open_image = pygame.Surface((40, 60))
        self.open_image.fill((0, 255, 0))      # Hijau transparan
        self.image = self.closed_image
        self.rect.height = 60
        self.collideable = True 
    
    def apply_code_result(self, result):
        if result:  # Jika True (tertutup)
            self.image = self.closed_image
            self.collideable = True
        else:       # Jika False (terbuka)
            self.image = self.open_image
            self.collideable = False