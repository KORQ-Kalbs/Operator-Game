import pygame
from .base_entity import BaseEntity

class Enemy(BaseEntity):
    def __init__(self, x, y, code_expression="speed = 3"):
        super().__init__(x, y, code_expression)
        self.original_x = x
        self.image = pygame.Surface((35, 35))
        self.image.fill((255, 0, 0))  # Merah
        self.direction = 1
    
    def apply_code_result(self, result):
        speed = result if isinstance(result, (int, float)) else 3
        
        if speed == 0:
            self.image.fill((100, 100, 255))  # Beku
            return
            
        # Gerakkan musuh
        self.rect.x += speed * self.direction
        
        # Reverse direction di batas
        if abs(self.rect.x - self.original_x) > 150:
            self.direction *= -1