import pygame
from .base_entity import BaseEntity

class Bridge(BaseEntity):
    def __init__(self, x, y, width, code_expression="stability > 0"):
        super().__init__(x, y, code_expression)
        self.width = width
        self.image = pygame.Surface((width, 20))
        self.image.fill((101, 67, 33))  # Kayu
        self.rect.width = width
        self.rect.height = 20
    
    def apply_code_result(self, result):
        if result:  # stability > 0
            self.image.set_alpha(255)
            self.collideable = True
        else:       # stability <= 0
            self.image.set_alpha(50)  # Transparan
            self.collideable = False