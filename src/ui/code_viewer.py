import pygame
from config import *

class CodeViewer:
    def __init__(self, font):
        self.font = font
        self.visible = True
    
    def draw(self, surface, entities, player):
        if not self.visible:
            return
        
        # Background panel
        panel = pygame.Rect(10, 10, 400, 200)
        pygame.draw.rect(surface, (30, 30, 30), panel)
        pygame.draw.rect(surface, WHITE, panel, 2)
        
        # Title
        title = self.font.render("THE PYTHON CODEX", True, WHITE)
        surface.blit(title, (20, 15))
        
        # List entities dan kode mereka
        y_offset = 40
        for i, entity in enumerate(entities):
            if y_offset > 180:
                break
            
            # Dapatkan kode string yang aman
            code_str = entity.get_code_string()
            
            # Buat text yang aman untuk rendering (hindari f-string issue)
            entity_name = type(entity).__name__
            code_text = f"{entity_name}: {code_str}"
            
            # Render text
            text_surface = self.font.render(code_text, True, WHITE)
            surface.blit(text_surface, (20, y_offset))
            y_offset += 20
        
        # Player spell selection
        spell_info = f"Spell: '{player.selected_spell}' | Number: {player.selected_number}"
        spell_surface = self.font.render(spell_info, True, YELLOW)
        surface.blit(spell_surface, (20, 180))