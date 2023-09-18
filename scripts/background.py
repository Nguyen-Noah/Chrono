import pygame, math
from .config import config

class Background:
    def __init__(self, game):
        self.game = game
        self.color = (37, 50, 70)
        self.angle = math.radians(-30)
        self.thickness = 20
        self.pos = 0
        self.speed = 20

    def update(self):
        self.pos = (self.pos + self.speed * self.game.window.dt) % (self.thickness * 2)

    def render(self, surf):
        angle = math.sin(self.angle) / math.cos(self.angle)
        offset = angle * self.game.window.base_resolution[0]
        for i in range(int((self.thickness * 4 + abs(offset) + self.game.window.base_resolution[1]) // (self.thickness * 2))):
            base_y = i * self.thickness * 2 + self.pos
            if offset > 0:
                base_y -= offset
            pygame.draw.line(surf, self.color, (0, base_y), (self.game.window.display.get_width(), base_y + offset), self.thickness)