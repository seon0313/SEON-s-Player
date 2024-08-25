import time

import pygame
from module.api.vlc import VLC
from module.ui.lyric import Lyric
class Control_Bar:
    def __init__(self, img:dict, vlc: VLC,lyric: Lyric, color = pygame.Color(255,255,255)):
        self.color = color
        self.img:dict = img
        self.vlc = vlc
        self.old = 0
        self.lyric = lyric
        self.mp = (0,0)
        self.start = 0
        self.l = None
    def run(self, sf:pygame.Surface) -> pygame.Surface:
        sf.fill(self.color)
        w,h = sf.get_size()
        sf.set_alpha(125)
        size = self.img['play'].get_size()
        sf.blit(self.img['play'], (w/2-size[0]/2,h/2-size[1]/2))

        pygame.draw.rect(sf, (150,150,150),(0,h-10,w*self.vlc.getPosition(),10))
        x,y = self.mp
        click = pygame.mouse.get_pressed()[0]
        if pygame.Rect((0,h-10,w,10)).collidepoint(x,y):
            if self.start <= 0: self.start = time.time()
            if time.time() - self.start >= .8:
                if self.l == None or self.l[1] <= self.vlc.getTimeOfPosition(x/w) <= self.l[2]:
                    self.l = self.lyric.getLyric(self.vlc.getTimeOfPosition(x/w))
                #print(self.l)
            if click and not self.old:
                self.vlc.setPosition(x/w)
                self.lyric.resetNow(self.vlc.getTime())
        elif self.start > 0: self.start = 0
        self.old = click
        return sf