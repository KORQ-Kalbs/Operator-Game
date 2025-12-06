import pygame
import ast

class BaseEntity(pygame.sprite.Sprite):
    """Basis semua objek di dunia yang bisa dimanipulasi kodenya"""
    
    def __init__(self, x, y, code_expression="True"):
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 40)
        self.original_expression = code_expression
        
        # TAMBAHKAN INI - atribut collision
        self.collideable = True
        
        # Parse kode
        try:
            if '=' in code_expression and not ('==' in code_expression or '!=' in code_expression):
                self.parsed_expression = ast.parse(code_expression, mode='exec').body[0]
                self.is_assignment = True
            else:
                self.parsed_expression = ast.parse(code_expression, mode='eval')
                self.is_assignment = False
        except:
            self.parsed_expression = ast.parse("True", mode='eval')
            self.is_assignment = False
        
        # Default image
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 255))  # Magenta sebagai placeholder
    
    def get_code_string(self):
        """Mengembalikan representasi kode yang aman untuk UI"""
        try:
            if self.is_assignment:
                module = ast.Module(body=[self.parsed_expression], type_ignores=[])
                code_str = ast.unparse(module).strip()
            else:
                code_str = ast.unparse(self.parsed_expression).strip()
            
            # Fallback untuk Python < 3.9
            if '`' in code_str:
                code_str = code_str.replace('`', "'")
            return code_str
        except Exception as e:
            return f"Error: {repr(e)}"
    
    def update(self):
        """Update state berdasarkan evaluasi kode"""
        try:
            if self.is_assignment:
                namespace = {}
                exec(compile(self.parsed_expression, '', 'exec'), namespace)
                if hasattr(self.parsed_expression, 'targets') and self.parsed_expression.targets:
                    var_name = self.parsed_expression.targets[0].id
                    result = namespace.get(var_name)
                    self.apply_code_result(result)
            else:
                result = eval(compile(self.parsed_expression, '', 'eval'))
                self.apply_code_result(result)
        except Exception:
            pass
    
    def apply_code_result(self, result):
        """Override di subclass"""
        pass
    
    def cast_operator_spell(self, new_operator):
        """Mengubah operator di ekspresi"""
        try:
            if not self.is_assignment:
                tree = self.parsed_expression.body
                if isinstance(tree, ast.Compare):
                    tree.ops[0] = new_operator
                elif isinstance(tree, ast.BinOp):
                    tree.op = new_operator
        except:
            pass
    
    def cast_numeric_spell(self, new_value):
        """Mengubah nilai numerik di ekspresi"""
        try:
            target = self.parsed_expression if self.is_assignment else self.parsed_expression.body
            
            for node in ast.walk(target):
                if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                    node.value = new_value
                    break
        except:
            pass
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)