import time

import pygame
from module.ui.grid import Grid
from module.ui.album import Album
from module.ui.lyric import Lyric
from module.ui.control_bar import Control_Bar
from module.ui.background import Background
from module.ui.easing import Easing
from module.api.music import Music
from module.api.vlc import VLC
import glob
import os
import threading


class App:
    def __init__(self):
        self.sc: pygame.Surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.title = 'SEON\'s Player'
        self.clock = pygame.time.Clock()
        self.fps = 60
        pygame.display.set_caption(self.title)
        self.mainMusic: Music = None
        self.img = {}
        self.vlc = VLC()
        self.lyric: Lyric = Lyric(pygame.font.Font('./module/f/SEON-font.ttf', 40))
        self.controlBar: Control_Bar = Control_Bar(self.img, self.vlc, self.lyric,
                                                   pygame.font.Font('./module/f/SEON-font.ttf', 25), self.mainMusic, self.mainmusic_load_thread)
        self.lyric.ani = Easing.ease_in_out_expo
        self.album: Album = Album()
        threading.Thread(target=self.mainmusic_load, args=('iA-NcVlqLRs',)).start()
        for i in glob.glob('./module/i/*.svg'):
            name = os.path.basename(i).lower().split('.')[0]
            a = pygame.image.load(i)
            w, h = a.get_size()
            for x in range(w):
                for y in range(h):
                    alpha = a.get_at((x, y))[3]
                    if alpha != 0:
                        a.set_at((x, y), pygame.Color(0, 0, 0, alpha))
            self.img[name] = a
        print(self.img)

    def mainmusic_load_thread(self, code:str):
        threading.Thread(target=self.mainmusic_load, args=(code,)).start()
    def lyric_load(self):
        self.lyric.lyric = self.mainMusic.getLyrics()
        self.lyric.lyric_render()
        self.lyric.reset()

    def mainmusic_load(self, code: str):
        self.controlBar.loaded = True
        self.mainMusic = Music(code)
        self.music_load_end()

    def album_img_load(self):
        self.album.setImage(self.mainMusic.getNailsBest())
    def music_load(self):
        self.vlc.setMidea(self.mainMusic.getAudioURL())
        self.controlBar.mainMusic = self.mainMusic
        self.controlBar.loaded = False
        self.vlc.play()

    def music_load_end(self):
        threading.Thread(target=self.lyric_load).start()
        threading.Thread(target=self.album_img_load).start()
        threading.Thread(target=self.music_load).start()


    def run(self):
        inner = Grid([self.album, self.lyric])

        inner.percent = 40
        g = Grid([
            inner,
            self.controlBar
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
            self.lyric.time = self.vlc.getTime()

            self.sc.fill((255, 255, 255))

            self.sc.blit(background.run(pygame.Surface(self.sc.get_size(), pygame.SRCALPHA)), (0, 0))
            x,y = pygame.mouse.get_pos()
            g.setMp(x,y)
            ct = g.run(pygame.Surface(self.sc.get_size(), pygame.SRCALPHA))
            self.sc.blit(ct, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    pygame.init()
    a = App()
    a.run()
    a.vlc.stop()
    pygame.quit()
