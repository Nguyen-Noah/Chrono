import pygame, math, random

from .tile_map import TileMap
from . import spritesheet_loader
from .config import config
from .camera import Camera
from .entities import EntityManager
from .particles import ParticleManager

class World():
    def __init__(self, game):
        self.game = game

        self.load_map()

    def load_map(self):
        self.tile_map = TileMap((16, 16), self.game.window.base_resolution)
        self.tile_map.load_map('data/maps/save.json')

        self.camera = Camera(self.game)

        self.entities = EntityManager(self.game)
        self.player = self.entities.gen_player()

        self.camera.set_tracked_entity(self.entities.player)

        self.master_clock = 0

        self.destruction_particles = ParticleManager

    def render(self, surf):
        render_list = self.tile_map.get_visible(self.camera.true_pos)
        self.collideables = []
        for layer in render_list:
            for tile in layer:
                offset = [0, 0]
                if tile[1][0] in self.game.assets.spritesheet_data:
                    tile_id = str(tile[1][1]) + ';' + str(tile[1][2])
                    if tile_id in self.game.assets.spritesheet_data[tile[1][0]]:
                        if 'tile_offset' in self.game.assets.spritesheet_data[tile[1][0]][tile_id]:
                            offset = self.game.assets.spritesheet_data[tile[1][0]][tile_id]['tile_offset']
                img = spritesheet_loader.get_img(self.game.assets.spritesheets, tile[1])
                surf.blit(img, (math.floor(tile[0][0] - self.camera.true_pos[0] + offset[0]), math.floor(tile[0][1] - self.camera.true_pos[1] + offset[1])))
                if tile[1][0] == 'ground':
                    self.collideables.append(pygame.Rect(tile[0][0], tile[0][1], 16, 16))
                if tile[1][0] == 'fireplace':
                    self.game.renderer.fireplace_particles((tile[0][0] + 15, tile[0][1] + 26))

    def update(self):
        self.master_clock += self.game.window.dt
        
        self.camera.update()

        # TODO:
            # check for a save json in data/saves
            # if isfile, load it
                # set use_save to True
                # load all of the saved progress
            # create the main init method for the game
                # initiate the inventory_menu and world_animatinos
            # load_map
                # get the map id
                # initate the camera
                # initiate the grass manager
                # initiate the entities
                # spawn the player