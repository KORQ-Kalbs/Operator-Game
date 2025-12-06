import pygame

class BaseSpell:
    def __init__(self, start_pos, direction, color):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], 12, 12)
        self.direction = direction
        self.color = color
        self.speed = 8
    
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, 6)