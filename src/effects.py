import random
import pygame
import numpy as np
from .settings import COLORS, PARTICLE_COUNT, PARTICLE_LIFETIME, FLASH_DURATION

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        angle = random.uniform(0, 2 * np.pi)
        speed = random.uniform(2, 5)
        self.vx = speed * np.cos(angle)
        self.vy = speed * np.sin(angle)
        self.alpha = 255

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # 重力效果
        self.lifetime -= 1
        self.alpha = int((self.lifetime / PARTICLE_LIFETIME) * 255)
        return self.lifetime > 0

    def draw(self, screen):
        if self.alpha > 0:
            color = (*self.color, self.alpha)
            surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (2, 2), 2)
            screen.blit(surface, (int(self.x - 2), int(self.y - 2)))

class Effects:
    def __init__(self):
        self.particles = []
        self.flash_timer = 0
        self.flash_lines = []

    def add_line_clear_effect(self, y, width, block_size):
        # 添加消行粒子效果
        for _ in range(PARTICLE_COUNT):
            x = random.randint(0, width * block_size)
            particle = Particle(x, y * block_size + block_size // 2, COLORS['WHITE'])
            self.particles.append(particle)
        
        # 添加闪光效果
        if y not in self.flash_lines:
            self.flash_lines.append(y)
            self.flash_timer = FLASH_DURATION

    def update(self):
        # 更新粒子
        self.particles = [p for p in self.particles if p.update()]
        
        # 更新闪光效果
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0:
                self.flash_lines.clear()

    def draw(self, screen):
        # 绘制闪光效果
        if self.flash_timer > 0 and self.flash_lines:
            flash_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            alpha = int((self.flash_timer / FLASH_DURATION) * 128)
            for y in self.flash_lines:
                pygame.draw.rect(flash_surface, (255, 255, 255, alpha),
                               (0, y * 30, screen.get_width(), 30))
            screen.blit(flash_surface, (0, 0))
        
        # 绘制粒子
        for particle in self.particles:
            particle.draw(screen)
