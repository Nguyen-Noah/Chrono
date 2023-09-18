import pygame

class Cursor():
    def __init__(self, game):
        self.game = game
        self.loc = (0, 0)
        self.offset = [0, 0]
        self.img = self.game.assets.cursor['normal']

    def update(self, surf):
        self.loc = pygame.mouse.get_pos()
        surf.blit(self.img, (((self.loc[0] + self.offset[0]) / (self.game.window.scaled_resolution[0] / self.game.window.base_resolution[0])) - 2, ((self.loc[1] + self.offset[1]) / (self.game.window.scaled_resolution[1] / self.game.window.base_resolution[1])) - 2))