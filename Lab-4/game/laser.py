import pygame

class Laser:
    SPEED = 11
    WIDTH = 4
    HEIGHT = 16

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (x, y)
        self.alive = True

    def update(self):
        self.rect.y -= self.SPEED
        if self.rect.bottom < 0:
            self.alive = False

    def hits(self, meteor):
        """Circle (meteor) vs. point-ish rect (laser) overlap test."""
        nx = max(self.rect.left, min(meteor.x, self.rect.right))
        ny = max(self.rect.top, min(meteor.y, self.rect.bottom))
        return (meteor.x - nx) ** 2 + (meteor.y - ny) ** 2 <= meteor.radius ** 2

    def draw(self, screen):
        pygame.draw.rect(screen, (120, 255, 160), self.rect, border_radius=2)
        glow = self.rect.inflate(4, 4)
        pygame.draw.rect(screen, (60, 180, 100), glow, width=1, border_radius=3)
