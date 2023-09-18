import pygame, math, random
from .core_funcs import normalize_vector

class Ability():
    def __init__(self, game, owner, skill_type):
        self.game = game
        self.owner = owner
        self.skill_type = skill_type
        self.charges = 1
        self.cooldown = 0
        self.charges_max = 1
        self.charges = self.charges_max
        self.charge_rate = 1

    def update(self):
        if self.charges < self.charges_max:
            self.charge += self.game.window.dt
            if self.charge > self.charge_rate:
                self.charge = 0
                self.charges += 1

    def use(self):
        if self.charges:
            self.charges -= 1
            return True
        else:
            return False

class BlinkSkill(Ability):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'blink')
        self.dash_timer = 0
        self.charge = 0

    def use(self):
        if super().use():
            self.owner.reset_gravity()

            self.owner.pos[0] += math.cos(self.owner.aim_angle) * 75
            self.owner.pos[1] += math.sin(self.owner.aim_angle) * 75
            self.dash_timer = 0.2

            self.game.window.add_freeze(0.005, 0.12)

    def update(self):
        super().update()
        dt = self.game.window.dt

        self.dash_timer -= dt
        self.dash_timer = max(0, self.dash_timer)

        if self.dash_timer:
            normalize_vector(self.owner.velocity, 2000 * dt)
            
class DashSkill(Ability):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'dash')
        self.dash_timer = 0
        self.charge = 0

    def use(self):
        if super().use():
            print(math.cos(self.owner.aim_angle))
            self.owner.velocity[0] = math.cos(self.owner.aim_angle) * 3
            self.owner.velocity[1] = math.sin(self.owner.aim_angle) * 3
            self.dash_timer = 0.2

            if self.owner.velocity[0] > 0:
                self.owner.flip[0] = True
            else:
                self.owner.flip[0] = False

    def update(self):
        super().update()
        dt = self.game.window.dt

        self.dash_timer -= dt
        self.dash_timer = max(0, self.dash_timer)

        if self.dash_timer:
            normalize_vector(self.owner.velocity, 16 * dt)

            img = self.owner.img.copy()
            img.set_alpha(70)
            #self.game.world.destruction_particles.add_particle(img, self.owner.center.copy(), [0, 0, 0], duration=0.1, gravity=False)

        if self.dash_timer and (self.dash_timer < 0.1):
            self.game.window.add_freeze(0.1, 0.001)

        self.owner.allow_movement = not bool(self.dash_timer)

class RageSkill(Ability):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'rage')

class TimeFreeze(Ability):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'freeze')

class Rewind(Ability):
    def __init__(self, game, owner):
        super().__init__(game, owner, 'rewind')

class Clone(Ability):
    def __init__(self, game, owner):
        super().__init__(self, owner, 'clone')

ABILITIES = {
    'blink': BlinkSkill,
    'dash': DashSkill,
    'rage': RageSkill,
    'time_freeze': TimeFreeze,
    'rewind': Rewind,
    'clone': Clone
}