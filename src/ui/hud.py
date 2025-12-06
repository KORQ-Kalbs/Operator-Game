# src/ui/hud.py - Heads-Up Display
import pygame
from config import *

class HUD:
    def __init__(self, font):
        """Inisialisasi HUD"""
        self.font = font
        self.font_small = pygame.font.Font(None, 16)
    
    def draw(self, surface, player):
        """Render UI info"""
        # Health bar
        health_text = f"Health: {player.health}/100"
        text = self.font.render(health_text, True, WHITE)
        surface.blit(text, (WINDOW_WIDTH - 150, 10))
        
        # Controls info (bottom right)
        controls = [
            "A/D: Move",
            "SPACE: Jump",
            "Mouse Left: Operator Spell",
            "Mouse Right: Numeric Spell",
            "Scroll/↑↓: Change Operator",
            "1-9: Select Number"
        ]
        
        y = WINDOW_HEIGHT - 100
        for control in controls:
            text = self.font_small.render(control, True, WHITE)
            surface.blit(text, (WINDOW_WIDTH - 180, y))
            y += 15