# src/level.py - Level parser & loader
import json
import pygame
from .entities.door import Door
from .entities.bridge import Bridge
from .entities.enemy import Enemy
from .entities.lava import Lava

class Level:
    def __init__(self, level_file):
        """Load level dari file JSON"""
        self.entities = pygame.sprite.Group()
        self.platforms = []
        self.load_level(level_file)
    
    def load_level(self, level_file):
        """Parse level JSON"""
        try:
            with open(level_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Level file {level_file} tidak ditemukan!")
            return
        
        # Load tile platforms
        for tile in data.get('tiles', []):
            platform = pygame.sprite.Sprite()
            platform.rect = pygame.Rect(tile['x'], tile['y'], tile['w'], tile['h'])
            platform.collideable = True  # Default collideable
            platform.image = pygame.Surface((tile['w'], tile['h']))
            platform.image.fill((100, 100, 100))
            self.platforms.append(platform)
        
        # Load entities
        for ent in data.get('entities', []):
            entity_type = ent.get('type')
            try:
                if entity_type == 'door':
                    door = Door(
                        ent['x'], 
                        ent['y'], 
                        ent.get('code', 'closed == True')
                    )
                    self.entities.add(door)
                    self.platforms.append(door)
                elif entity_type == 'bridge':
                    bridge = Bridge(
                        ent['x'], 
                        ent['y'], 
                        ent['w'], 
                        ent.get('code', 'stability > 0')
                    )
                    self.entities.add(bridge)
                    self.platforms.append(bridge)
                elif entity_type == 'enemy':
                    enemy = Enemy(
                        ent['x'], 
                        ent['y'], 
                        ent.get('code', 'speed = 3')
                    )
                    self.entities.add(enemy)
                elif entity_type == 'lava':
                    lava = Lava(
                        ent['x'], 
                        ent['y'], 
                        ent['w'], 
                        ent.get('code', 'damage = 10')
                    )
                    self.entities.add(lava)
                    self.platforms.append(lava)
            except Exception as e:
                print(f"Error loading entity {ent}: {e}")
    
    def update(self):
        """Update semua entities"""
        self.entities.update()
    
    def draw(self, surface):
        """Render level dan entities"""
        # Draw platforms
        for platform in self.platforms:
            if hasattr(platform, 'image') and hasattr(platform, 'rect'):
                surface.blit(platform.image, platform.rect)
        
        # Draw entities
        self.entities.draw(surface)