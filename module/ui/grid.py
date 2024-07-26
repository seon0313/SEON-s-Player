import pygame
from math import ceil

class Grid:
    def __init__(self, items:list=[],align: int = 0):
        self.items = items
        self.align = align
        self.percent = 50
        self.move = False
        self.border_size = 20
        self.border_icon_size = 50
        self.min_ = 20
        self.max_ = 80

    def run(self, sf: pygame.Surface) -> pygame.Surface:
        size_ = sf.get_size()
        v = size_[0] / len(self.items) if self.align == 0 else size_[1] / len(self.items)
        v = ceil(v)
        size = (v, size_[1]) if self.align == 0 else (size_[0], v)
        for index, i in enumerate(self.items):
            if len(self.items) == 2:
                a = size_[0] if self.align == 0 else size_[1]
                if index == 0: v = (self.percent / 100) * a
                else: v = ((100 - self.percent) / 100) * a
                v = ceil(v)

                sf.blit(i.run(pygame.Surface((v, size[1]) if self.align == 0 else (size[0], v), pygame.SRCALPHA)),
                        (((self.percent / 100) * a) if index != 0 else 0, 0) if self.align == 0 else (0, ((self.percent / 100) * a) if index != 0 else 0))
            else:
                sf.blit(i.run(pygame.Surface((v,size[1]) if self.align==0 else (size[0],v), pygame.SRCALPHA)), (index * v, 0) if self.align == 0 else (0, index * v))

        if len(self.items) == 2:
            size = sf.get_size()
            if self.align == 0:
                border = pygame.Rect((size[0] * (self.percent / 100) - (self.border_size / 2)), 0, self.border_size, size[1])
                border_icon = pygame.Rect((size[0] * (self.percent / 100) - (self.border_size / 2))+self.border_size/4, size[1]/2-self.border_icon_size/2, self.border_size/2, self.border_icon_size)
            else:
                border = pygame.Rect(0, (size[1] * (self.percent / 100) - (self.border_size / 2)), size[0], self.border_size)
                border_icon = pygame.Rect(size[0]/2-self.border_icon_size/2, (size[1] * (self.percent / 100) - (self.border_size / 2))+self.border_size/4, self.border_icon_size, self.border_size/2)
            mx, my = pygame.mouse.get_pos()
            if border.collidepoint(mx,my) or self.move:
                pygame.draw.rect(sf,pygame.Color(0,0,0,125),border)
                pygame.draw.rect(sf,pygame.Color(255,255,255),border_icon)
                if pygame.mouse.get_pressed()[0]:
                    self.move = True


        if self.move:
            if not pygame.mouse.get_pressed()[0]:
                self.move = False
            self.percent = mx / size[0] * 100
            if self.align != 0: self.percent = my / size[1] * 100

        if self.percent > self.max_: self.percent = self.max_
        elif self.percent < self.min_: self.percent = self.min_

        return sf
