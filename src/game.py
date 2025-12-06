# src/game.py - Main game loop
import pygame
import sys
from config import *
from .player import Player
from .level import Level
from .ui.code_viewer import CodeViewer
from .ui.hud import HUD
from .spells.operator_spell import OperatorSpell
from .spells.numeric_spell import NumericSpell

class Game:
    def __init__(self):
        """Inisialisasi game"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Operator Mage: The Python Codex")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.font_small = pygame.font.Font(None, 16)
        
        # Game objects
        self.player = Player(100, 500)
        self.level = Level('levels/level1.json')
        self.code_viewer = CodeViewer(self.font)
        self.hud = HUD(self.font)
        
        self.spells = []
        self.current_level = 1
    
    def handle_events(self):
        """Handle semua input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Select number (1-9, 0 = 10)
                if pygame.K_1 <= event.key <= pygame.K_0:
                    num = event.key - pygame.K_0
                    if num == 0:
                        num = 10
                    self.player.selected_number = num
                
                # Scroll operator
                if event.key == pygame.K_UP:
                    self._cycle_operator(1)
                if event.key == pygame.K_DOWN:
                    self._cycle_operator(-1)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click = Operator Spell
                if event.button == 1:
                    self._cast_spell('operator')
                # Right click = Numeric Spell
                elif event.button == 3:
                    self._cast_spell('numeric')
        
        return True
    
    def _cycle_operator(self, direction):
        """Ganti operator yang dipilih"""
        operators = ['>', '<', '>=', '<=', '==', '!=', '+', '-']
        try:
            current_index = operators.index(self.player.selected_spell)
            new_index = (current_index + direction) % len(operators)
            self.player.selected_spell = operators[new_index]
        except:
            self.player.selected_spell = '>'
    
    def _cast_spell(self, spell_type):
        """Cast spell sesuai tipe"""
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.player.rect.center)
        
        if direction.length() > 0:
            direction = direction.normalize()
        
        spell_pos = self.player.rect.center
        
        if spell_type == 'operator':
            spell = OperatorSpell(spell_pos, direction, self.player.selected_spell)
        else:
            spell = NumericSpell(spell_pos, direction, self.player.selected_number)
        
        self.spells.append(spell)
    
    def update(self):
        """Update semua game logic"""
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.level.platforms)
        self.level.update()
        
        # Update spells
        for spell in self.spells[:]:
            spell.update()
            
            # Collision dengan entities
            for entity in self.level.entities:
                if spell.rect.colliderect(entity.rect):
                    if isinstance(spell, OperatorSpell):
                        entity.cast_operator_spell(spell.new_operator)
                    elif isinstance(spell, NumericSpell):
                        entity.cast_numeric_spell(spell.value)
                    self.spells.remove(spell)
                    break
            
            # Hapus spell keluar layar
            if not self.screen.get_rect().colliderect(spell.rect):
                if spell in self.spells:
                    self.spells.remove(spell)
        
        # Win condition (selesaikan level)
        if self.player.rect.x > WINDOW_WIDTH - 50:
            self.next_level()
        
        # Game over
        if self.player.health <= 0:
            self.reset_level()
    
    def next_level(self):
        """Pindah ke level berikutnya"""
        self.current_level += 1
        try:
            self.level = Level(f'levels/level{self.current_level}.json')
            self.player.rect.topleft = (100, 500)
            self.spells.clear()
        except FileNotFoundError:
            print("🎉 Selamat! Kamu menyelesaikan game!")
            pygame.quit()
            sys.exit()
    
    def reset_level(self):
        """Reset level saat ini"""
        self.level = Level(f'levels/level{self.current_level}.json')
        self.player.rect.topleft = (100, 500)
        self.player.health = 100
        self.spells.clear()
    
    def draw(self):
        """Render semua ke layar"""
        self.screen.fill(BLACK)
        
        # Draw level dan entities
        self.level.draw(self.screen)
        
        # Draw spells
        for spell in self.spells:
            spell.draw(self.screen)
        
        # Draw player
        self.screen.blit(self.player.image, self.player.rect)
        
        # Draw UI
        self.code_viewer.draw(self.screen, self.level.entities, self.player)
        self.hud.draw(self.screen, self.player)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()