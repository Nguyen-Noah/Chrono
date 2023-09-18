import math, time

from .config import config
from .entity_objs.player import Player

class EntityManager:
    def __init__(self, game):
        self.game = game
        self.entities = []

    def gen_player(self):
        self.entities.append(Player(self.game, (0, 0), (12, 20), 'player'))
        self.player = self.entities[-1]

    def render(self, surf):
        for entity in self.entities:
            entity.render(surf, self.game.world.camera.true_pos)
            entity.update(self.game.window.dt)