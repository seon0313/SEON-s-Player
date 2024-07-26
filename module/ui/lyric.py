import pygame
from module.api.music import Music

class Lyric:
    def __init__(self, font:pygame.font.Font):
        self.lyric: dict = None
        self.font:pygame.font.Font = font
        self.items = []
        self.color = pygame.Color((255,255,255))
        self.space: tuple[float,float] = self.font.render(' ', True, self.color).get_size()
        self.h: tuple[float,float] = self.font.render('a', True, self.color).get_size()[1]
        self.border = 50
        self.margin = 10
    def lyric_render(self):
        if self.lyric == None or self.lyric == '' or len(self.lyric) <= 0: return
        self.items = []
        for index, i in enumerate(self.lyric.items()):
            self.items.append([])
            for i in i[1]:
                self.items[index].append(
                    {'start':i['start'], 'end':i['end'],'sf':self.font.render(i['msg'],True,self.color)}
                )

    def run(self, sf: pygame.Surface) -> pygame.Surface:
        sf.fill(pygame.Color(255,0,255,120))
        size = sf.get_size()
        if self.items != [] and self.lyric != None:
            app = 0
            render = True
            for index, i in enumerate(self.items):
                x_ = self.border
                for index2, i in enumerate(i):
                    s:pygame.Surface = i['sf']
                    s.set_alpha(180)
                    w,h = s.get_size()
                    h = self.h
                    if x_+w>size[0]-self.margin:
                        app += h+5
                        x_ = self.border
                    hv = (index*h)+(index*(h+(h/2)))+app
                    if hv < 0: break
                    if hv>size[1]:
                        render = False
                        break
                    sf.blit(s,(x_,hv))
                    x_ += w+self.space[0]
                if not render: break
        return sf