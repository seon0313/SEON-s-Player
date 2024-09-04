import copy
import time

import pygame
from module.ui.grid import Grid
from module.ui.album import Album
from module.ui.lyric import Lyric
from module.ui.control_bar import Control_Bar
from module.ui.background import Background
from module.ui.easing import Easing
from module.ui.next_music_popup import NextPop

from module.api.music import Music
from module.api.playlist import Playlist
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
        self.mainPlayList: Playlist = None
        self._next_pop = NextPop(pygame.font.Font('./module/f/SEON-font.ttf', 20),
                                 pygame.font.Font('./module/f/SEON-font.ttf', 25))
        self._next_pop.ani = Easing.ease_in_out_expo
        self.lyric: Lyric = Lyric(pygame.font.Font('./module/f/SEON-font.ttf', 40))
        self.controlBar = Control_Bar(self, self.img, pygame.font.Font('./module/f/SEON-font.ttf', 25),
                                      self.mainmusic_load_thread, self.music_load_end)
        self.lyric.ani = Easing.ease_in_out_expo
        self.background = Background(pygame.Surface(self.sc.get_size(), pygame.SRCALPHA))
        self.album: Album = Album()
        threading.Thread(target=self.mainmusic_load, args=('iA-NcVlqLRs',), daemon=True).start()
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
            if name == 'loop':
                b = copy.deepcopy(a)
                for x in range(w):
                    for y in range(h):
                        alpha = b.get_at((x, y))[3]
                        if alpha != 0:
                            b.set_at((x, y), pygame.Color(150, 150, 150, alpha))
                self.img[name+'2'] = b
        print(self.img)

    def mainmusic_load_thread(self, code:str):
        threading.Thread(target=self.mainmusic_load, args=(code,), daemon=True).start()
    def lyric_load(self):
        self.lyric.loaded = False
        self.lyric.lyric = self.mainMusic.getLyrics()
        self.lyric.lyric_render()
        self.lyric.loaded = True
        if not self.lyric.isreset:
            self.lyric.isreset = True
            self.lyric.reset()
        self.lyric.resetNow(self.lyric.time)

    def mainmusic_load(self, code: str):
        self.controlBar.loaded = True
        self.lyric.isreset = False
        try:
            self.mainMusic = Music(code, True)
            self.mainPlayList = Playlist()
            self.mainPlayList.appendMusic(self.mainMusic)
            self.controlBar.setPlaylist(self.mainPlayList)
            self.music_load_end()
        except Exception as e: self.controlBar.loaded = False

    def set_caption(self,title:str):
        pygame.display.set_caption(title)

    def album_img_load(self):
        self.album.setImage(self.mainMusic.getNailsBest())
    def music_load(self):
        self.vlc.pause()
        self.vlc.setMidea(self.mainMusic.getAudioURL())
        self.controlBar.mainMusic = self.mainMusic
        self.controlBar.loaded = False
        if self.lyric.loaded: self.lyric.reset()
        self.vlc.play()

    def music_load_end(self):
        threading.Thread(target=self.lyric_load, daemon=True).start()
        threading.Thread(target=self.album_img_load, daemon=True).start()
        threading.Thread(target=self.music_load, daemon=True).start()


    def run(self):
        inner = Grid([self.album, self.lyric])

        inner.percent = 40
        g = Grid([
            inner,
            self.controlBar
        ], align=1)
        g.percent = 90
        g.max_ = 90
        run_ = True
        def load(l: dict):
            while l['run_']:
                self.background.run()

        bg = threading.Thread(target=load, args=(locals(),), daemon=True)
        bg.start()
        while run_:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    run_ = False
                    break
            if not run_: break
            self.lyric.time = self.vlc.getTime()
            if not self.title in pygame.display.get_caption()[0]: self.set_caption(pygame.display.get_caption()[0]+' | '+self.title)

            self.sc.fill((255, 255, 255))
            if not self.background.sf_ or self.sc.get_size() != self.background.sf_.get_size(): self.background.sf_ = pygame.Surface(self.sc.get_size(), pygame.SRCALPHA)
            if self.background.sf: self.sc.blit(self.background.sf, (0, 0))
            x,y = pygame.mouse.get_pos()
            g.setMp(x,y)
            ct = g.run(pygame.Surface(self.sc.get_size(), pygame.SRCALPHA))
            self.sc.blit(ct, (0, 0))

            leng = self.vlc.getLength()
            if leng > 0 and leng - 5000 <= self.vlc.getTime() * 1000 and (not self.mainPlayList.isLast() or self.controlBar.loop()):
                self._next_pop.blit = True
            size = self.sc.get_size()
            self._next_pop.sec = int((leng - (leng * self.vlc.getPosition())) / 1000)
            a = self._next_pop.run(size)
            if a: self.sc.blit(a[0], (a[1], size[1]-(size[1]-(size[1]*(g.percent/100)))-a[0].get_size()[1]))

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    pygame.init()
    a = App()
    a.run()
    a.vlc.stop()
    pygame.quit()
