import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.health = 100
        
        # Spell selection
        self.selected_spell = '>'  # Default operator
        self.selected_number = 0
    
    def update(self, keys, platforms):
        # Horizontal movement
        self.vel.x = 0
        if keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
        
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = PLAYER_JUMP_FORCE
        
        # Gravity
        self.vel.y += GRAVITY
        
        # Update position
        self.rect.x += self.vel.x
        self._check_collisions(platforms, 'horizontal')
        
        self.rect.y += self.vel.y
        self._check_collisions(platforms, 'vertical')
        
        # Keep in bounds
        self.rect.x = max(0, min(WINDOW_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(WINDOW_HEIGHT - self.rect.height, self.rect.y))
    
    def _check_collisions(self, platforms, direction):
        for platform in platforms:
            if platform.collideable and self.rect.colliderect(platform.rect):
                if direction == 'horizontal':
                    if self.vel.x > 0:
                        self.rect.right = platform.rect.left
                    else:
                        self.rect.left = platform.rect.right
                    self.vel.x = 0
                elif direction == 'vertical':
                    if self.vel.y > 0:
                        self.rect.bottom = platform.rect.top
                        self.vel.y = 0
                        self.on_ground = True
                    else:
                        self.rect.top = platform.rect.bottom
                        self.vel.y = 0
    
    def shoot_spell(self, spell_type):
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        
        spell_pos = self.rect.center
        return (spell_pos, direction, self.selected_spell if spell_type == 'operator' else self.selected_number)
    
    def take_damage(self, amount):
        if hasattr(self, 'healing') and self.healing:
            self.health = min(100, self.health - amount)  # Negative damage = heal
        else:
            self.health -= amount