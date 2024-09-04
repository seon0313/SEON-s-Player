import time

import pygame


class NextPop:
    def __init__(self, smallfont: pygame.Font, bigFont: pygame.Font):
        self.mp: tuple[int, int] = (0,0)
        self._title = ''
        self._title_render: pygame.Surface = None
        self.img: pygame.Surface = None
        self._font: pygame.Font = bigFont
        self._font2: pygame.Font = smallfont
        self.sec: int = 0
        self.blit: bool = False
        self._blit: int = 0
        self.ani = None
        self._old_blit = False
        self.cooltime = 4

    def getTitle(self) -> str: return self._title

    def setTitle(self, title: str):
        self._title = title
        self._title_render = self._font.render(self._title, True,(0,0,0))

    def run(self, size):
        if self._blit <= 0 and self.blit: self._blit = time.time()
        elif not self.blit:
            self._blit = 0
            return None
        f = self._font2.render(f'{self.sec}초 뒤 다음 곡이 재생 됩니다.', True, (100,100,180))

        t = None
        if len(self._title) > 0:
            t = self._font.render(self._title, True, (0,0,0))

        fr = f.get_rect()
        fr.x, fr.y = (10, 10)
        if t != None: tr = t.get_rect()

        w1 = fr.w
        w2 = 0 if t==None else tr.w
        sf = pygame.Surface((max(w1 + 20, w2 + 20), 80), pygame.SRCALPHA)
        w,h = sf.get_size()
        pygame.draw.rect(sf,(195, 226, 221),(0,0,w,h),0, -1,10,-1,10,-1)
        sf.set_alpha(180)
        #sf.fill(pygame.Color(200, 150, 210, 180))
        w, h = sf.get_size()
        sf.blit(f, fr)

        if t != None:
            tr.center = (w, ((h-fr.h+10) / 2)+(fr.h+10)/2)
            tr.x = 10
            sf.blit(self._title_render, tr)

        t = time.time() if time.time()-self._blit<=self.cooltime else time.time()-self.cooltime
        v = (t - self._blit) / .8
        v = self.ani(v if v < 1 else 1)
        a = False
        if not self.blit: x = size[0]
        elif time.time()-self._blit<=self.cooltime: x = size[0] - ((size[0] - (size[0] - w)) * v)
        else:
            x = (size[0] - w) + (w * v)
            a = True
        if a and v>=1: self.blit = False
        self._old_blit = self.blit
        return sf, x