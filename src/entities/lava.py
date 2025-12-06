import pygame
from .base_entity import BaseEntity

class Lava(BaseEntity):
    def __init__(self, x, y, width, code_expression="damage = 10"):
        super().__init__(x, y, code_expression)
        self.width = width
        self.image = pygame.Surface((width, 30))
        self.image.fill((255, 100, 0))  # Oranye lava
    
    def apply_code_result(self, result):
        damage = result if isinstance(result, (int, float)) else 10
        
        if damage < 0:
            self.image.fill((0, 255, 255))  # Cyan (menyembuhkan)
            self.healing = True
        elif damage == 0:
            self.image.fill((255, 255, 0))  # Kuning (netral)
            self.healing = False
        else:
            self.image.fill((255, 100, 0))  # Merusak
            self.healing = False