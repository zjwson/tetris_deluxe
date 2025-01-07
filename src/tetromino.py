import random
from typing import List, Tuple
from .settings import SHAPES, COLORS

class Tetromino:
    def __init__(self, shape_name: str = None):
        if shape_name is None:
            shape_name = random.choice(list(SHAPES.keys()))
        
        self.shape_name = shape_name
        self.shape = SHAPES[shape_name]
        self.color = self._get_color()
        self.rotation = 0
        self.x = 3  # 起始位置
        self.y = 0
        
    def _get_color(self) -> Tuple[int, int, int]:
        color_map = {
            'I': COLORS['CYAN'],
            'J': COLORS['BLUE'],
            'L': COLORS['ORANGE'],
            'O': COLORS['YELLOW'],
            'S': COLORS['GREEN'],
            'T': COLORS['PURPLE'],
            'Z': COLORS['RED']
        }
        return color_map[self.shape_name]
    
    def rotate(self, clockwise: bool = True) -> List[Tuple[int, int]]:
        if self.shape_name == 'O':  # O形方块不需要旋转
            return self.get_positions()
            
        new_positions = []
        for x, y in self.shape:
            if clockwise:
                new_positions.append((-y, x))
            else:
                new_positions.append((y, -x))
        
        self.shape = new_positions
        return self.get_positions()
    
    def get_positions(self) -> List[Tuple[int, int]]:
        return [(x + self.x, y + self.y) for x, y in self.shape]
    
    def move(self, dx: int, dy: int) -> List[Tuple[int, int]]:
        self.x += dx
        self.y += dy
        return self.get_positions()
    
    def get_ghost_positions(self, board) -> List[Tuple[int, int]]:
        ghost_y = self.y
        while board.is_valid_move([(x + self.x, y + ghost_y + 1) for x, y in self.shape]):
            ghost_y += 1
        return [(x + self.x, y + ghost_y) for x, y in self.shape]
