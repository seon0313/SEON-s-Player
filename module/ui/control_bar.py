import pygame


class Control_Bar:
    def __init__(self, img:dict,color = pygame.Color(255,255,255)):
        self.color = color
        self.img:dict = img
    def run(self, sf:pygame.Surface) -> pygame.Surface:
        sf.fill(self.color)
        w,h = sf.get_size()
        sf.set_alpha(125)
        size = self.img['play'].get_size()
        sf.blit(self.img['play'], (w/2-size[0]/2,h/2-size[1]/2))
        return sf