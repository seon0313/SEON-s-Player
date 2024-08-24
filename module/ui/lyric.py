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
        self.size_p: int = 0
        self.old_size:tuple = (0,0)
        self.reload = False
        self.app = 0
        self.app_t = 0
        self.app_s = 0
    def reset(self):
        self.heights = [0 for i in range(len(self.lyric.items()))]
        self.app = 0

    def lyric_render(self):
        if self.lyric == None or self.lyric == '' or len(self.lyric) <= 0: return
        self.items = []
        for index, i in enumerate(tuple(self.lyric.items())):
            self.items.append([])
            for i in tuple(i[1]):
                if i['msg'].replace(' ','') == '': i['msg'] = ''
                try:
                    self.items[index].append(
                        {'start':i['start'], 'end':i['end'],'sf':self.font.render(i['msg'],True,self.color),'start_t': 0, 'end_t':0}
                    )
                except:
                    self.items[index].append(
                        {'start': i['start'], 'end': i['end'], 'sf': self.font.render('Render ERROR', True, self.color),
                         'start_t': 0, 'end_t': 0}
                    )


    def run(self, sf: pygame.Surface) -> pygame.Surface:
        sf.fill(pygame.Color(255,0,255,120))
        size = sf.get_size()
        reload = False
        if self.items != [] and self.lyric is not None and not len(self.lyric) <= 0 and len(self.heights) > 0:
            if self.size_p <= 0 or self.old_size != size:
                self.size_p = size[1]/2
            app = 0#self.size_p
            target_app = 0
            for i in tuple(self.heights[:self.now]): target_app+=i
            if self.app != target_app:
                if self.app_t <= 0: self.app_t, self.app_s = (time.time(), self.app)
                v = (time.time() - self.app_t) / 1.0
                v = self.ani(v if v < 1 else 1)
                self.app = self.app_s+(((max(self.app_s,target_app)-min(self.app_s,target_app))*v) * 1 if target_app > self.app_s else -1)
                print(v)
                if v >= 1:
                    self.app = target_app
                    self.app_t, self.app_s = (-1,0)

            elif self.app_t != 0: self.app_t, self.app_s = (0,0)
            render = True
            for index, _i in enumerate(tuple(self.items)):
                x_ = self.border
                _h = 1
                breaked = False
                for index2, i in enumerate(_i):
                    s:pygame.Surface = i['sf']
                    s.set_alpha(180)
                    if i['start'] <= self.time:
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
                    if x_+w>size[0]-self.margin:
                        app += h+5
                        _h += 1
                        x_ = self.border

                    if self.time >= i['end']:
                        if x_ == self.border and index2 >= len(_i)-1:
                            #if not self.now > index: self.now = index + 1
                            pass

                    hv = (index*h)+(index*(h+(h/2)))+app-self.app
                    if hv < 0 and False:
                        breaked = True
                        break
                    if hv>size[1]:
                        render = False
                        break
                    sf.blit(s,(x_,hv+self.size_p))
                    x_ += w+self.space[0]
                if self.old_size != size or self.heights[index] <= 0 or (not reload and self.reload):
                    self.heights[index] = _h*(h+5) + h+(h/2) -5
                    if (index >= len(self.items)-1 and index2 >= len(_i)) or not render:
                        self.reload = False
                elif self.heights[index] != _h*(h+5) + h+(h/2) -5:
                    reload = True
                    self.reload = True
                if not render: break
        self.old_size = size
        return sf