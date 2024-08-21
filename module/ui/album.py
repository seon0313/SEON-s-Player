import time
from random import randrange as r

import pygame
from module.api.music import Music
from module.ui.easing import Easing
class Album:
    def __init__(self):
        self.img = None
        self.padding = 35
        #self.color = (r(0,256),200,r(0,256)
        self.start = 0


    def setImage(self, image):
        self.img = pygame.image.load(image, namehint="")
        size = self.img.get_size()
        side = (size[0] - size[1]) / 2
        self.img = pygame.transform.chop(self.img, pygame.Rect(0, 0, side, 0))
        size = self.img.get_size()
        self.img = pygame.transform.chop(self.img, pygame.Rect(size[0] - side, 0, side, 0))

    def run(self, sf: pygame.Surface) -> pygame.Surface:
        if self.img != None:
            if self.start == 0: self.start = time.time()
            w,h = sf.get_size()
            vv = (time.time()-self.start)/2
            v = Easing.ease_in_out_expo(vv if vv < 1 else 1)

            target = w if w < h else h
            target -= target * self.padding/100
            img = pygame.transform.smoothscale(self.img,(target,target))
            sf.set_alpha(255*v)

            pygame.draw.rect(sf,(255,255,255),((w/2)-(target/2),(h/2)-(target/2),target,target))
            sf.blit(img, ((w/2)-(target/2),(h/2)-(target/2)))

        return sf
