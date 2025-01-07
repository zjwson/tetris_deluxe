import pygame
import time
from typing import Optional
from .board import Board
from .tetromino import Tetromino
from .effects import Effects
from .sound_manager import SoundManager
from .settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLOCK_SIZE,
    COLORS, SCORES, INITIAL_FALL_SPEED, SPEED_INCREASE,
    SOFT_DROP_SPEED
)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("俄罗斯方块 Deluxe")
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        try:
            self.font = pygame.font.Font("/System/Library/Fonts/PingFang.ttc", 36)
        except:
            self.font = pygame.font.Font(None, 36)
        
        self.board = Board()
        self.effects = Effects()
        self.sound_manager = SoundManager()
        self.current_piece: Optional[Tetromino] = None
        self.next_piece = Tetromino()
        self.held_piece: Optional[Tetromino] = None
        self.can_hold = True
        self.show_ghost = False
        
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.game_started = False
        
        self.last_fall_time = time.time()
        self.fall_speed = INITIAL_FALL_SPEED
        self.soft_dropping = False
        
        self.board_offset_x = (WINDOW_WIDTH - self.board.width * BLOCK_SIZE) // 2
        self.board_offset_y = 20

    def start_game(self):
        self.__init__()
        self.game_started = True
        self.spawn_new_piece()

    def toggle_pause(self):
        if self.game_started and not self.game_over:
            self.paused = not self.paused

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started:
                        self.start_game()
                    else:
                        self.toggle_pause()
                    continue
                
                if event.key == pygame.K_r and self.game_over:
                    self.start_game()
                    return True
                    
                if not self.game_started or self.paused or self.game_over:
                    continue
                
                if event.key == pygame.K_LEFT:
                    new_pos = self.current_piece.move(-1, 0)
                    if self.board.is_valid_move(new_pos):
                        self.sound_manager.play('MOVE')
                    else:
                        self.current_piece.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    new_pos = self.current_piece.move(1, 0)
                    if self.board.is_valid_move(new_pos):
                        self.sound_manager.play('MOVE')
                    else:
                        self.current_piece.move(-1, 0)
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate(True)
                    if self.board.is_valid_move(self.current_piece.get_positions()):
                        self.sound_manager.play('ROTATE')
                    else:
                        self.current_piece.rotate(False)
                elif event.key == pygame.K_z:
                    self.current_piece.rotate(False)
                    if self.board.is_valid_move(self.current_piece.get_positions()):
                        self.sound_manager.play('ROTATE')
                    else:
                        self.current_piece.rotate(True)
                elif event.key == pygame.K_DOWN:
                    self.soft_dropping = True
                elif event.key == pygame.K_c:
                    self.hold_piece()
                elif event.key == pygame.K_g:
                    self.show_ghost = not self.show_ghost
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.soft_dropping = False
                
        return True

    def update(self):
        if not self.game_started or self.paused or self.game_over:
            return

        self.effects.update()
        
        current_time = time.time()
        fall_delay = 1.0 / (self.fall_speed * (SOFT_DROP_SPEED if self.soft_dropping else 1))
        
        if current_time - self.last_fall_time >= fall_delay:
            self.last_fall_time = current_time
            
            new_positions = self.current_piece.move(0, 1)
            if self.board.is_valid_move(new_positions):
                return
            
            self.current_piece.move(0, -1)
            self.board.place_tetromino(self.current_piece)
            self.sound_manager.play('DROP')
            
            lines = self.board.clear_lines()
            if lines > 0:
                self.handle_line_clear(lines)
            
            self.spawn_new_piece()
            self.can_hold = True
            self.soft_dropping = False
            
            if self.board.is_game_over():
                self.game_over = True
                self.sound_manager.play('GAME_OVER')

    def draw(self):
        self.screen.fill(COLORS['BACKGROUND'])
        
        self.board.draw(self.screen, self.board_offset_x, self.board_offset_y)
        
        if not self.game_started:
            self.draw_start_screen()
        else:
            if self.current_piece:
                if self.show_ghost:
                    self.board.draw_tetromino(self.screen, self.current_piece,
                                            self.board_offset_x, self.board_offset_y, ghost=True)
                self.board.draw_tetromino(self.screen, self.current_piece,
                                        self.board_offset_x, self.board_offset_y)
            
            self.effects.draw(self.screen)
            
            self.draw_info_panel()
            
            if self.paused:
                self.draw_pause_screen()
            elif self.game_over:
                self.draw_game_over_screen()
        
        pygame.display.flip()

    def draw_start_screen(self):
        title_text = self.font.render('俄罗斯方块 Deluxe', True, COLORS['WHITE'])
        start_text = self.font.render('按空格键开始游戏', True, COLORS['WHITE'])
        
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(start_text, start_rect)

    def draw_pause_screen(self):
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        
        pause_text = self.font.render('游戏暂停', True, COLORS['WHITE'])
        continue_text = self.font.render('按空格键继续', True, COLORS['WHITE'])
        
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)

    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if not self.board.is_valid_move(self.current_piece.get_positions()):
            self.game_over = True
            self.sound_manager.play('GAME_OVER')

    def hold_piece(self):
        if not self.can_hold:
            return
        
        if self.held_piece is None:
            self.held_piece = Tetromino(self.current_piece.shape_name)
            self.current_piece = self.next_piece
            self.next_piece = Tetromino()
        else:
            self.current_piece, self.held_piece = (
                Tetromino(self.held_piece.shape_name),
                Tetromino(self.current_piece.shape_name)
            )
        self.can_hold = False

    def handle_line_clear(self, lines):
        self.score += SCORES[lines]
        self.lines_cleared += lines
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = INITIAL_FALL_SPEED + (self.level - 1) * SPEED_INCREASE
        
        self.sound_manager.play('CLEAR')
        
        for y in range(self.board.height - lines, self.board.height):
            self.effects.add_line_clear_effect(y, self.board.width, BLOCK_SIZE)

    def draw_info_panel(self):
        score_text = self.font.render(f'分数: {self.score}', True, COLORS['WHITE'])
        level_text = self.font.render(f'等级: {self.level}', True, COLORS['WHITE'])
        lines_text = self.font.render(f'行数: {self.lines_cleared}', True, COLORS['WHITE'])
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(level_text, (20, 60))
        self.screen.blit(lines_text, (20, 100))
        
        next_text = self.font.render('下一个:', True, COLORS['WHITE'])
        self.screen.blit(next_text, (WINDOW_WIDTH - 150, 20))
        self.draw_preview(self.next_piece, WINDOW_WIDTH - 150, 60)
        
        hold_text = self.font.render('保持:', True, COLORS['WHITE'])
        self.screen.blit(hold_text, (20, 160))
        if self.held_piece:
            self.draw_preview(self.held_piece, 20, 200)

    def draw_preview(self, piece: Tetromino, x: int, y: int):
        if not piece:
            return
            
        preview_size = BLOCK_SIZE * 4
        for px, py in piece.shape:
            pygame.draw.rect(self.screen, piece.color,
                           (x + (px + 1) * BLOCK_SIZE,
                            y + (py + 1) * BLOCK_SIZE,
                            BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def draw_game_over_screen(self):
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        
        game_over_text = self.font.render('游戏结束!', True, COLORS['WHITE'])
        score_text = self.font.render(f'最终分数: {self.score}', True, COLORS['WHITE'])
        restart_text = self.font.render('按 R 键重新开始', True, COLORS['WHITE'])
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
