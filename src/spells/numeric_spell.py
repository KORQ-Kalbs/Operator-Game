from .base_spell import BaseSpell

class NumericSpell(BaseSpell):
    def __init__(self, start_pos, direction, value):
        super().__init__(start_pos, direction, (255, 255, 0))
        self.value = value