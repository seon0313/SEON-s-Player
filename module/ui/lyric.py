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
        self.app = 0 # lyric top margin
        self.app_t = 0 # music playing time
        self.app_s = 0 # start-time
        self.mp = (0,0)
        self.reset_now = False
        self.loaded = False
        self.isreset = False
    def reset(self):
        self.heights = [0 for i in range(len(self.lyric.items()))]
        self.app = 0
        self.app_t = 0
        self.app_s = 0
        self.now = 0

    def lyric_render(self):
        if self.lyric == None or self.lyric == '' or len(self.lyric) <= 0: return
        self.items = []
        for index, i in enumerate(tuple(self.lyric.items())):
            self.items.append([])
            for i in tuple(i[1]):
                if i['msg'].replace(' ','') == '': i['msg'] = ''
                try:
                    self.items[index].append(
                        {'start':i['start'], 'end':i['end'],'sf':self.font.render(i['msg'],True,self.color),'start_t': 0, 'end_t':0, 'msg': i['msg']}
                    )
                except:
                    self.items[index].append(
                        {'start': i['start'], 'end': i['end'], 'sf': self.font.render('Render ERROR', True, self.color),
                         'start_t': 0, 'end_t': 0, 'msg': i['msg']}
                    )

    def getLyric(self, t: float) -> tuple:
        try:
            if self.items != [] and len(self.items) > 0:
                for i in tuple(self.items):
                    if i[0]['start'] <= t <= i[-1]['end']:
                        le = len(i)-1
                        ly = ''
                        start = 0
                        end = 0
                        for index, l in enumerate(i):
                            ly += l['msg']+' '
                            if index == 0: start = l['start']
                            if index >= le: end = l['end']

                        return ly[:-1], start, end
        except Exception as e: print('getLyric',e)

    def resetNow(self, t):
        if self.items != [] and len(self.items) > 0:
            place = False
            now_ = [0,-1]
            for index, i in enumerate(tuple(self.items)):
                if not t and i[0]['start'] <= t <= i[-1]['end']:
                    self.now = index
                    place = True
                    break
                if now_[1] < 0 or now_[1] > max(i[0]['start'], t) - min(i[0]['start'], t):
                    now_[0], now_[1] = (index, max(i[0]['start'], t) - min(i[0]['start'], t))
            if not place:
                self.now = now_[0]
            self.reset_now = True


    def run(self, sf: pygame.Surface) -> pygame.Surface:
        sf.fill(pygame.Color(106, 205, 230, 120))
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
                self.app = self.app_s+((target_app-self.app_s)*v)
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

                    if _i[-1]['end'] <= self.time:
                        if i['start_t'] > 0: i['start_t'] = 0
                        if i['end_t'] == 0:
                            self.items[index][index2]['end_t'] = time.time()
                            i['end_t'] = self.items[index][index2]['end_t']
                            if not self.reset_now: self.now = index + 1
                        v = (time.time() - i['end_t']) / 1.3 #3
                        v = self.ani(v if v < 1 else 1)
                        s.set_alpha(255 - (255 - 180) * v)

                    elif i['start'] <= self.time:
                        if i['start_t'] == 0:
                            self.items[index][index2]['start_t'] = time.time()
                            i['start_t'] = self.items[index][index2]['start_t']
                            self.items[index][index2]['end_t'] = 0
                            i['end_t'] = self.items[index][index2]['end_t']
                        v = (time.time() - i['start_t']) / .8#1.3
                        v = self.ani(v if v < 1 else 1)
                        s.set_alpha(180+(255-180)*v)

                    w,h = s.get_size()
                    h = self.h
                    if x_+w>size[0]-self.margin:
                        app += h+5
                        _h += 1
                        x_ = self.border

                    hv = (index*h)+(index*(h+(h/2)))+app-self.app
                    if hv < 0 and False:
                        breaked = True
                        break
                    if hv>size[1]:
                        render = False
                        break
                    sf.blit(s,(x_,hv+self.size_p))
                    x_ += w+self.space[0]
                try: self.heights[index]+=0
                except:
                    for i in range(len(self.heights)-1-index): self.heights.append(0)
                if self.old_size != size or self.heights[index] <= 0 or (not reload and self.reload):
                    self.heights[index] = _h*(h+5) + h+(h/2) -5
                    if (index >= len(self.items)-1 and index2 >= len(_i)) or not render:
                        self.reload = False
                elif self.heights[index] != _h*(h+5) + h+(h/2) -5:
                    reload = True
                    self.reload = True
                if not render: break
        self.old_size = size
        if self.reset_now: self.reset_now = False
        return sf