import pygame, random

from .cursor import Cursor
from .particles import ParticleManager
from .background import Background
from .vfx import render_glow

class Renderer():
    def __init__(self, game):
        self.game = game

        self.particles = ParticleManager(self.game)
        self.background = Background(game)
        self.cursor = Cursor(game)
        self.overlay_particles()

    def render(self):
        surf = self.game.window.display
        ui_surf = surf.copy()

        self.background.update()
        self.background.render(surf)
        self.game.world.render(surf)
        self.cursor.update(self.game.window.display)

        self.particles.update()
        self.update_overlay_particles(surf)
        self.update_fireplace_particles(surf)
        render_glow(surf)

        self.game.world.entities.render(surf)
        
    def overlay_particles(self):
        for i in range(100):
            loc = [random.random() * self.game.window.display.get_width(), random.random() * self.game.window.display.get_height()]
            r = random.randint(1, 4)
            if r == 4:
                self.particles.add_particle('overlay', loc, 'p', [random.random() * -25 - 15, random.random() * 25 + 25], 0, random.choice([5, 5, 4]), custom_color=(200, 200, 200), glow=(10, 10, 10), glow_radius=4) #(201, 255, 229)
            else:
                self.particles.add_particle('overlay', loc, 'p', [random.random() * -25 - 15, random.random() * 25 + 25], 0, random.choice([5, 5, 4]), custom_color=(50, 50, 50))

    def update_overlay_particles(self, surf):
        offset = [self.game.world.camera.pos[0] // 3, self.game.world.camera.pos[1] // 4]

        for particle in self.particles.particle_groups['overlay']:
            if particle.pos[0] + particle.internal_offset[0] < offset[0] - 1:
                particle.pos[0] += self.game.window.display.get_width()
            if particle.pos[0] + particle.internal_offset[0] > offset[0] + self.game.window.display.get_width() + 1:
                particle.pos[0] -= self.game.window.display.get_width()
            if particle.pos[1] + particle.internal_offset[1] < offset[1] - 1:
                particle.pos[1] += self.game.window.display.get_height()
            if particle.pos[1] + particle.internal_offset[1] > offset[1] + self.game.window.display.get_height() + 1:
                particle.pos[1] -= self.game.window.display.get_height()

        self.particles.render('overlay', surf, offset)

    def fireplace_particles(self, loc):
        self.particles.add_particle('fireplace', loc, 'p', [(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10], 4, 0 + random.randint(0, 20) / 10, custom_color=(random.randint(235, 255), 2 * random.randint(0,100), 0), glow=(18, 6, 6), glow_radius=2)

    def update_fireplace_particles(self, surf):
        self.particles.render('fireplace', surf, offset=[self.game.world.camera.true_pos[0], self.game.world.camera.true_pos[1]])

        # TODO:
            # initiate a background module and import it
            # create a particle manager module and import it
            # create a render function that
                # gets the surface and copies it to ui_surf
                # renders game.world
                # updates particle overlay
                # initiates ui color and font
                # holds the core game UI
                    # weapon
                        # loop through weapon masks
                            # set the color
                            # set the weapon image to the weapon's mask
                            # blit to ui_surf
                            # set the offset to the height of the image + N
                    # health
                        # set a background color surface for the missing health
                        # blit to ui_surf
                        # get the health the player has and blit a rectangle to ui_surf
                        # blit the health ui to the ui_surf
                    # skills
                        # establish the amount of skills
                        # set skills equal to player.skills
                        # iterate through skill_count
                            # set the position on the display
                            # if the skill is used, render the skill
                        # blit the skills ui to ui_surf
                # blit the custom cursor