import ast
from .base_spell import BaseSpell

class OperatorSpell(BaseSpell):
    def __init__(self, start_pos, direction, new_operator_str):
        super().__init__(start_pos, direction, (150, 0, 255))
        self.new_operator = self._parse_operator(new_operator_str)
    
    def _parse_operator(self, op_str):
        operators = {
            '>': ast.Gt(), '<': ast.Lt(),
            '>=': ast.GtE(), '<=': ast.LtE(),
            '==': ast.Eq(), '!=': ast.NotEq(),
            '+': ast.Add(), '-': ast.Sub(),
            '*': ast.Mult(), '/': ast.Div()
        }
        return operators.get(op_str, ast.Gt())