import time

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
        self.time: float = 0
        self.ani = None
        self.heights: list[int] = []
        self.now: int = 0
        self.old_size:tuple = (0,0)
    def reset(self):
        self.heights = [0 for i in range(len(self.lyric.items()))]

    def lyric_render(self):
        if self.lyric == None or self.lyric == '' or len(self.lyric) <= 0: return
        self.items = []
        for index, i in enumerate(self.lyric.items()):
            self.items.append([])
            for i in i[1]:
                if i['msg'].replace(' ','') == '': i['msg'] = ''
                self.items[index].append(
                    {'start':i['start'], 'end':i['end'],'sf':self.font.render(i['msg'],True,self.color),'start_t': 0, 'end_t':0}
                )

    def run(self, sf: pygame.Surface) -> pygame.Surface:
        sf.fill(pygame.Color(255,0,255,120))
        size = sf.get_size()
        if self.items != [] and self.lyric != None:
            app = 0
            for i in self.heights[:self.now]: app-=i
            render = True
            size_p = size[1]/2
            for index, _i in enumerate(self.items):
                x_ = self.border
                _h = 0
                for index2, i in enumerate(_i):
                    s:pygame.Surface = i['sf']
                    s.set_alpha(180)
                    if i['start']-.2 <= self.time:
                        if i['start_t'] == 0:
                            self.items[index][index2]['start_t'] = time.time()
                            i['start_t'] = self.items[index][index2]['start_t']
                        v = (time.time() - i['start_t']) / .8#1.3
                        v = self.ani(v if v < 1 else 1)
                        s.set_alpha(180+(255-180)*v)

                    if self.time >= _i[-1]['end']:
                        if i['end_t'] == 0:
                            self.items[index][index2]['end_t'] = time.time()
                            i['end_t'] = self.items[index][index2]['end_t']
                            self.now = index + 1
                        v = (time.time() - i['end_t']) / 1.3 #3
                        v = self.ani(v if v < 1 else 1)
                        s.set_alpha(255 - (255 - 180) * v)
                    w,h = s.get_size()
                    h = self.h
                    if index2 == 0: _h = h+(h/2)+h
                    if x_+w>size[0]-self.margin:
                        app += h+5
                        _h += h+5
                        x_ = self.border

                    if self.time >= i['end']:
                        if x_ == self.border and index2 >= len(_i)-1:
                            #if not self.now > index: self.now = index + 1
                            pass
                    print(self.now)

                    hv = (index*h)+(index*(h+(h/2)))+app+size_p
                    if hv < 0: break
                    if hv>size[1]:
                        render = False
                        break
                    sf.blit(s,(x_,hv))
                    x_ += w+self.space[0]
                if self.heights[index] == 0 or self.old_size != size:self.heights[index] = _h
                if not render: break
        self.old_size = size
        return sf