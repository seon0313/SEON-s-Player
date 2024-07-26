import time

import pygame

from module.ui.easing import Easing
from random import randrange as rand

class Particle:
    def __init__(self, color):
        self.color = color
        self.max_ = 0
        self.min_ = 0
        self.now = 0
        self.start = 0
        self.ani = 1.8
        self.i = 0
        self.pos: list[float | int, float | int] = [0, 0]
        self.vel: list[float | int, float | int] = [0, 0]
        self.old = time.time()

    def run(self, sf: pygame.Surface) -> pygame.Surface:
        w, h = sf.get_size()
        if self.start <= 0:
            self.pos = [rand(0,w), rand(0,h)]
            self.vel = [rand(-60,60), rand(-60,60)]
            self.max_ = rand(int(w/1.5), int(w/0.5))
            self.min_ = rand(int(w/2), self.max_)
            self.now = self.max_ - self.min_
            self.start = time.time()
            self.i = 0
        s = pygame.Surface((self.now, self.now),pygame.SRCALPHA)
        v = 1
        if self.i==0:
            v = Easing.ease_in_out_expo((time.time() - self.start) / self.ani)
            if v >= 1: self.i=1
        if self.i >= 0: s.set_alpha(255 * v)
        else:
            v = Easing.ease_in_out_expo((time.time() - self.start) / self.ani)
            s.set_alpha(255-(255*v))
            if s.get_alpha() <= 0:
                self.start = -1
        w2, h2 = s.get_size()
        pygame.draw.circle(s,self.color,(w2/2,h2/2),w2/2)

        dt = time.time()-self.old

        if self.pos[0] > w or self.pos[0] < 0 or self.pos[1] > h or self.pos[1] < 0:
            if not self.i < 0:
                self.i = -1
                self.start = time.time()
        else:
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt

        self.old = time.time()

        sf.blit(s,self.pos)
