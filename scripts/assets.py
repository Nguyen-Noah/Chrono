import pygame, os

from . import spritesheet_loader
from . import animation_handler

class Assets:
    def __init__(self, game):
        self.game = game

        self.spritesheets, self.spritesheet_data = spritesheet_loader.load_spritesheets('data/graphics/tilesets')
        self.animations = animation_handler.AnimationManager()
        self.cursor = self.load_dir('data/graphics/cursor')
        self.particles = self.load_dirs('data/graphics/particles')

        # TODO:
            # create a font dictionary
            # initiate (spritesheets, spritesheet_data), weapons, skills, projectiles, particles

    def load_dirs(self, path):
        dirs = {}
        for dir in os.listdir(path):
            dirs[dir] = self.load_dir(path + '/' + dir)
        return dirs

    def load_dir(self, path):
        image_dir = {}
        for file in os.listdir(path):
            image_dir[file.split('.')[0]] = self.load_img(path + '/' + file, (0, 0, 0))
        return image_dir
    
    def load_img(self, path, colorkey):
        img = pygame.image.load(path).convert()
        img.set_colorkey(colorkey)
        return img