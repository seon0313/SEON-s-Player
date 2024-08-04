import sys

import pygame
from module.ui.grid import Grid
from module.ui.album import Album
from module.ui.lyric import Lyric
from module.ui.control_bar import Control_Bar
from module.ui.background import Background

from module.api.music import Music
import glob
import os
import vlc
class App:
    def __init__(self):
        self.sc: pygame.Surface = pygame.display.set_mode((1280,720),pygame.SRCALPHA)
        self.title = 'SEON\'s Player'
        self.clock = pygame.time.Clock()
        self.fps = 60
        pygame.display.set_caption(self.title)
        self.mainMusic: Music = Music('8yXGI3kcLsw')
        self.img = {}
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new('https://www.youtube.com/watch?v='+self.mainMusic.video.videoid)
        self.media.get_mrl()
        self.player.set_media(self.media)
        self.player.play()
        #self.player.play()
        for i in glob.glob('./module/i/*.svg'):
            name = os.path.basename(i).lower().split('.')[0]
            print(i)
            a = pygame.image.load(i)
            w,h = a.get_size()
            for x in range(w):
                for y in range(h):
                    alpha = a.get_at((x,y))[3]
                    if alpha != 0:
                        a.set_at((x,y),pygame.Color(0,0,0,alpha))
            print(a.get_colorkey())
            self.img[name] = a
        print(self.img)


    def run(self):
        album = Album()
        album.setImage(self.mainMusic.getNailsImage())
        lyric = Lyric(pygame.font.Font('./module/f/font.ttf',40))
        lyric.lyric = self.mainMusic.getLyrics()
        lyric.lyric_render()
        inner = Grid([album,lyric])
        inner.percent = 40
        self.player.play()
        g = Grid([
            inner,
            Control_Bar(self.img)
        ], align=1)
        g.percent = 90
        g.max_ = 90

        background = Background()


        run_ = True
        while run_:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    run_ = False
                    break
            if not run_: break

            print(self.player.get_time())

            self.sc.fill((255,255,255))

            self.sc.blit(background.run(pygame.Surface(self.sc.get_size(),pygame.SRCALPHA)),(0,0))
            ct = g.run(pygame.Surface(self.sc.get_size(),pygame.SRCALPHA))
            self.sc.blit(ct,(0,0))

            pygame.display.flip()
            self.clock.tick(self.fps)



if __name__ == '__main__':
    pygame.init()
    a = App()
    a.run()
    pygame.quit()