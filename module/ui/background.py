import pygame
from module.ui.particle import Particle
from random import randrange as r

class Background:
    def __init__(self, sf:pygame.Surface):
        self.particle: list[Particle] = []
        self.sf_ = sf
        self.sf: pygame.Surface = None
        for i in range(10):
            self.particle.append(Particle((r(0,256),r(0,256),r(0,256))))
    def run(self):
        self.sf_.fill((255,255,255))
        self.sf_ = pygame.transform.smoothscale(self.sf_,self.sf_.get_size())
        for i in self.particle:
            i.run(self.sf_)
        self.sf = pygame.transform.box_blur(self.sf_,100)
    def setColor(self):
        pass