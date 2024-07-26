import pygame
from module.ui.particle import Particle
from random import randrange as r

class Background:
    def __init__(self):
        self.particle: list[Particle] = []
        for i in range(10):
            self.particle.append(Particle((r(0,256),r(0,256),r(0,256))))
    def run(self, sf: pygame.Surface) -> pygame.Surface:
        sf.fill((255,255,255))
        sf = pygame.transform.smoothscale(sf,sf.get_size())
        for i in self.particle:
            i.run(sf)
        sf = pygame.transform.box_blur(sf,100)
        return sf
    def setColor(self):
        pass