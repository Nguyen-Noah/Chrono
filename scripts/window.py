import pygame, time

from .config import config

class Window():
    def __init__(self, game):
        self.game = game

        pygame.init()

        self.base_resolution = config['window']['base_resolution']
        self.scaled_resolution = config['window']['scaled_resolution']
        self.offset = config['window']['offset']
        self.fps = config['window']['FPS']
        self.background_color = config['window']['background']
        #self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.scaled_resolution)
        self.display = pygame.Surface((self.base_resolution[0] - self.offset[0] * 2, self.base_resolution[1] - self.offset[0] * 2))

        pygame.display.set_caption(config['window']['caption'])

        pygame.mouse.set_visible(False)

        self.freeze_frame = {}

        self.dt = 0.1
        self.frame_history = [0.01]
        self.frame_start = time.time()

    def add_freeze(self, rate, duration):
        self.freeze_frame[rate] = duration

    def show_fps(self):
        avg_dt = sum(self.frame_history) / len(self.frame_history)
        avg_fps = 1 / avg_dt
        return avg_fps

    def render_frame(self):
        #print(self.show_fps())
        self.screen.blit(pygame.transform.scale(self.display, self.scaled_resolution), (0, 0))
        self.display.fill(self.background_color)

        self.dt = time.time() - self.frame_start
        self.ui_dt = self.dt

        delete_list = []

        orig_dt = self.dt

        if self.freeze_frame != {}:
            slowest_freeze = min(list(self.freeze_frame))
            if self.freeze_frame[slowest_freeze] > self.dt:
                self.dt *= slowest_freeze
            else:
                self.dt -= self.freeze_frame[slowest_freeze] * (1 - slowest_freeze)

        for freeze_amount in self.freeze_frame:
            if self.freeze_frame[freeze_amount] > orig_dt:
                self.freeze_frame[freeze_amount] -= orig_dt
            else:
                self.freeze_frame[freeze_amount] = 0
                delete_list.append(freeze_amount)

        for freeze in delete_list:
            del self.freeze_frame[freeze]

        pygame.display.update()

        self.dt = min(max(0.00001, self.dt), 0.1)
        self.frame_start = time.time()
        self.frame_history.append(self.ui_dt)
        self.frame_history = self.frame_history[-200:]

        '''delete_list = []
        orig_dt = self.dt

        if self.freeze_frame != {}:
            slowest_freeze = min(list(self.freeze_frame))
            if self.freeze_frame[slowest_freeze] > self.dt:
                self.dt *= slowest_freeze
            else:
                self.dt -= self.freeze_frame[slowest_freeze] * (1 - slowest_freeze)

        for freeze_amount in self.freeze_frame:
            if self.freeze_frame[freeze_amount] > orig_dt:
                self.freeze_frame[freeze_amount] -= orig_dt
            else:
                self.freeze_frame[freeze_amount] = 0
                delete_list.append(freeze_amount)

        for freeze in delete_list:
            del self.freeze_frame[freeze]

        pygame.display.update()
        self.clock.tick(self.fps)

        self.dt = time.time() - self.frame_start
        self.ui_dt = self.dt

        self.dt = min(max(0.00001, self.dt), 0.1)
        self.frame_start = time.time()
        self.frame_history.append(self.ui_dt)
        self.frame_history = self.frame_history[-200:]'''
        
    # TODO: 
        # set the mouse to invisible
        # initiated dt
        # create function for fps