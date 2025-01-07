import numpy as np
from typing import List, Tuple
from .settings import BOARD_WIDTH, BOARD_HEIGHT, COLORS, BLOCK_SIZE
import pygame

class Board:
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.colors = np.zeros((BOARD_HEIGHT, BOARD_WIDTH, 3), dtype=int)
        
    def is_valid_move(self, positions: List[Tuple[int, int]]) -> bool:
        for x, y in positions:
            if not (0 <= x < self.width and 0 <= y < self.height):
                return False
            if y >= 0 and self.grid[y][x] != 0:  # 只检查在板内的位置
                return False
        return True
    
    def place_tetromino(self, tetromino) -> None:
        positions = tetromino.get_positions()
        for x, y in positions:
            if 0 <= y < self.height:  # 确保在有效范围内
                self.grid[y][x] = 1
                self.colors[y][x] = tetromino.color
            
    def clear_lines(self) -> int:
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            if all(self.grid[y]):
                # 将当前行以上的所有行向下移动一行
                for row in range(y, 0, -1):
                    self.grid[row] = self.grid[row - 1].copy()
                    self.colors[row] = self.colors[row - 1].copy()
                # 清空最上面的行
                self.grid[0] = np.zeros(self.width, dtype=int)
                self.colors[0] = np.zeros((self.width, 3), dtype=int)
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared

    def is_game_over(self) -> bool:
        # 只检查最上面一行是否有方块
        return any(self.grid[0])

    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        # 绘制游戏板背景
        pygame.draw.rect(screen, COLORS['GRAY'],
                        (offset_x - 2, offset_y - 2,
                         self.width * BLOCK_SIZE + 4,
                         self.height * BLOCK_SIZE + 4), 2)
        
        # 绘制已放置的方块
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    color = tuple(self.colors[y][x])
                    pygame.draw.rect(screen, color,
                                   (offset_x + x * BLOCK_SIZE,
                                    offset_y + y * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, COLORS['WHITE'],
                                   (offset_x + x * BLOCK_SIZE,
                                    offset_y + y * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_tetromino(self, screen: pygame.Surface, tetromino, offset_x: int, offset_y: int,
                      ghost: bool = False) -> None:
        positions = tetromino.get_ghost_positions(self) if ghost else tetromino.get_positions()
        color = tetromino.color
        
        for x, y in positions:
            if 0 <= y < self.height:  # 确保在有效范围内
                if ghost:
                    ghost_color = (*color, 128)
                    ghost_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(ghost_surface, ghost_color,
                                   (0, 0, BLOCK_SIZE, BLOCK_SIZE))
                    screen.blit(ghost_surface,
                              (offset_x + x * BLOCK_SIZE,
                               offset_y + y * BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, color,
                                   (offset_x + x * BLOCK_SIZE,
                                    offset_y + y * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, COLORS['WHITE'],
                                   (offset_x + x * BLOCK_SIZE,
                                    offset_y + y * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE), 1)
