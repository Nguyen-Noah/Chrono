import pygame, math

from ..entity import Entity
from ..core_funcs import normalize
from ..ability import ABILITIES

class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = [0, 0]
        self.air_timer = 0
        self.in_air = False
        self.allow_movement = True
        self.gravity_on = True
        self.jumps = 200
        self.aim_angle = 0
        self.abilities = [ABILITIES['blink'](self.game, self), ABILITIES['dash'](self.game, self)]

    def attempt_move(self, direction):
        if self.allow_movement:
            # movement for left and right
            if direction == 1:
                self.frame_motion[0] += self.speed * direction * self.game.window.dt
            if direction == -1:
                self.frame_motion[0] += self.speed * direction * self.game.window.dt

    def attempt_jump(self):
        if self.allow_movement:
            if self.jumps:
                self.in_air = True
                self.velocity[1] = -1.1
                self.jumps -= 1
                # a bit of a hack to deal with cases where the player is stuck in the ground
                self.pos[1] += self.velocity[1] * self.game.window.dt

    def reset_gravity(self):
        self.velocity[1] = 0

    def gravity(self, dt, force):
        if self.allow_movement:
         self.velocity[1] = min(6, self.velocity[1] + dt * force)

    def update(self, dt):
        self.frame_motion = self.velocity.copy()

        # calls the Entity update method
        r = super().update(dt)
        if not r:
            return r

        self.air_timer += dt

        if self.gravity_on:
            self.gravity(dt, 3)

        if self.game.input.states['move-right']:
            self.attempt_move(1)
            self.flip[0] = True
        elif self.game.input.states['move-left']:
            self.attempt_move(-1)
            self.flip[0] = False
        if self.game.input.states['jump']:
            self.attempt_jump()

        # get the collisions
        self.collisions = self.move(self.frame_motion, self.game.world.collideables)

        # set speed to dt timing
        self.frame_motion[0] *= dt
        self.frame_motion[1] *= dt

        # stop movement if player touches top or bottom of a block
        if self.collisions['top'] or self.collisions['bottom']:
            self.velocity[1] = 0
        if self.collisions['bottom']:
            if self.game.world.entities.player:
                self.game.world.camera.set_restriction(self.center)
            self.velocity[1] = 0
            self.jumps = 200
            self.in_air = False
            self.air_timer = 0

        # set action for animation
        if self.air_timer > 4 or self.in_air:
            self.set_action('jump')
        elif self.frame_motion[0] != 0 and not self.in_air:
            self.set_action('run')
        else:
            self.set_action('idle')
        if self.velocity[1] >= 0 and self.in_air:
            self.set_action('fall')

        # abilities
        angle = math.atan2(self.game.input.mouse_pos[1] - self.center[1] + self.game.world.camera.true_pos[1], self.game.input.mouse_pos[0] - self.center[0] + self.game.world.camera.true_pos[0])
        self.aim_angle = angle

        for ability in self.abilities:
            ability.update()

        if self.game.input.states['blink']:
            if self.abilities[0]:
                self.abilities[0].use()

        if self.game.input.mouse_state['right_click']:
            if self.abilities[1]:
                self.abilities[1].use()

    def render(self, surf, offset):
        super().render(surf, offset)