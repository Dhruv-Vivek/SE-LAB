import math
import random
import pygame

class ShieldOrb:
    RADIUS = 12

    def __init__(self, width):
        self.base_x = random.randint(40, width - 40)
        self.x = float(self.base_x)
        self.y = -20.0
        self.vy = 1.4
        self.phase = random.uniform(0, math.tau)
        self.t = 0
        self.alive = True

    def update(self, height):
        self.t += 1
        self.y += self.vy
        self.x = self.base_x + math.sin(self.t * 0.04 + self.phase) * 40  # gentle sideways drift
        if self.y > height + 30:
            self.alive = False

    def collected_by(self, rect):
        dx, dy = self.x - rect.centerx, self.y - rect.centery
        return (dx * dx + dy * dy) ** 0.5 < self.RADIUS + 18

    def draw(self, screen):
        pulse = 2 * math.sin(self.t * 0.15)
        r = int(self.RADIUS + pulse)
        s = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        pygame.draw.circle(s, (80, 220, 255, 60), (r * 2, r * 2), r * 2)
        pygame.draw.circle(s, (120, 240, 255, 255), (r * 2, r * 2), r)
        pygame.draw.circle(s, (255, 255, 255, 255), (r * 2 - r // 3, r * 2 - r // 3), max(2, r // 3))
        screen.blit(s, (self.x - r * 2, self.y - r * 2))
