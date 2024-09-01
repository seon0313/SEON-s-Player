import threading
import time

import pygame
from module.api.vlc import VLC, VLC_Type
from module.ui.lyric import Lyric
from module.api.music import Music
from module.api.playlist import Playlist
class Control_Bar:
    def __init__(self, img:dict, vlc: VLC,lyric: Lyric, font:pygame.font.Font, mainMusic: Music,load_func, mainPlaylist, color = pygame.Color(255,255,255)):
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
        self.color = color
        self._img:dict = img
        self.vlc = vlc
        self.old = 0
        self.lyric = lyric
        self.mp = (0,0)
        self.start = 0
        self._l = None
        self.play_bar_height = -1
        self.old_h = 0
        self.font: pygame.Font = font
        self.mainMusic: Music = mainMusic
        self._mainPlaylist: mainPlaylist = mainPlaylist
        self.loaded = False
        self.old_loaded = self.loaded
        self.search_t = 0
        self.search = False
        self._load_func = load_func
        self._loop = False
        self.search_str = ''
        self._old_playing = 0
        self.keys = {
            pygame.K_1:'1',pygame.K_2:'2',pygame.K_3:'3',pygame.K_4:'4',pygame.K_5:'5',pygame.K_6:'6',pygame.K_7:'7',
            pygame.K_8:'8',pygame.K_9:'9',pygame.K_0:'0',pygame.K_q:'q',pygame.K_w:'w',pygame.K_e:'e',pygame.K_r:'r',
            pygame.K_t:'t',pygame.K_y:'y',pygame.K_u:'u',pygame.K_i:'i',pygame.K_o:'o',pygame.K_p:'p',pygame.K_a:'a',
            pygame.K_s:'s',pygame.K_d:'d',pygame.K_f:'f',pygame.K_g:'g',pygame.K_h:'h',pygame.K_j:'j',pygame.K_k:'k',
            pygame.K_l:'l',pygame.K_z:'z',pygame.K_x:'x',pygame.K_c:'c',pygame.K_v:'v',pygame.K_b:'b',pygame.K_n:'n',
            pygame.K_m:'m',pygame.K_BACKSPACE:'-1',pygame.K_MINUS:'-',pygame.K_RETURN:'-2'
        }
        self.s_keys = {pygame.K_MINUS:'_'}
        self.keys_t = {}
    def run(self, sf:pygame.Surface) -> pygame.Surface:
        sf.fill(self.color)
        w,h = sf.get_size()
        sf.set_alpha(125)
        click = pygame.mouse.get_pressed()[0]
        v = self.vlc.getState()
        if v == VLC_Type.playing: img_name = 'pause'
        elif v == VLC_Type.paused: img_name = 'play'
        else: img_name = 'play'

        if not self.loaded and self.old_loaded: pygame.display.set_caption(f'{self.mainMusic.getTitle()} - {self.mainMusic.getAuthor()}')

        size = self._img[img_name].get_size()
        sf.blit(self._img[img_name], (w/2-size[0]/2,h/2-size[1]/2))
        loop_size = self._img['loop'].get_size()
        sf.blit(self._img['loop' if self._loop else 'loop2'], (w/2-loop_size[0]/2+100,h/2-loop_size[1]/2))
        x, y = self.mp
        if pygame.Rect((0,h-self.play_bar_height,w,self.play_bar_height)).collidepoint(x,y):
            if self.start <= 0: self.start = time.time()
            if time.time() - self.start >= .8:
                if self._l == None or not (self._l[1] <= self.vlc.getTimeOfPosition(x/w) <= self._l[2]):
                    self._l = self.lyric.getLyric(self.vlc.getTimeOfPosition(x/w))
                if self._l != None:
                    f = self.font.render(str(self._l[0]),True,(125,80,90))
                    fr = f.get_rect()
                    fr.x,fr.y = self.mp[0]-fr.w/2, h-self.play_bar_height-fr.h
                    if fr.x < 10: fr.x = 10
                    if fr.x+fr.w > w-10: fr.x = w-10-fr.w
                    sf.blit(f,fr)
            if click and not self.old:
                self.vlc.setPosition(x/w)
                self.lyric.resetNow(self.vlc.getTime())

        elif pygame.Rect((w/2-size[0]/2,h/2-size[1]/2,size[0],size[1])).collidepoint(self.mp[0], self.mp[1]):
            if click and not self.old and not self.loaded:
                if v == VLC_Type.playing: self.vlc.pause()
                elif v == VLC_Type.paused:
                    self.vlc.play()
                else:
                    self.vlc.setMidea(self.mainMusic.getAudioURL())
                    self.vlc.play()
                    self.lyric.resetNow(self.vlc.getTime())
        elif pygame.Rect((w/2-loop_size[0]/2+100,h/2-loop_size[1]/2,loop_size[0],loop_size[1])).collidepoint(self.mp[0],self.mp[1]):
            if click and not self.old and not self.loaded:
                self._loop = not self._loop

        if h != self.old_h:
            self.play_bar_height = max(10,int(h/6))

        pygame.draw.rect(sf, (150,150,150),(0,h-self.play_bar_height,w*self.vlc.getPosition(),self.play_bar_height))

        if pygame.Rect((0,0,30,h)).collidepoint(self.mp[0],self.mp[1]):
            if self.search_t <= 0: self.search_t = time.time()
            if time.time() - self.search_t >= 1:
                self.search = True
        elif self.search:
            self.search = False
            self.search_t = 0
        keys = pygame.key.get_pressed()
        if self.search and not self.loaded:
            f = self.font.render(': '+str(self.search_str), True, (125, 80, 90))
            fr = f.get_rect()
            fr.x, fr.y = (10, h/2-(fr.h/2))
            sf.blit(f,fr)

            shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            if keys[pygame.K_LCTRL] and keys[pygame.K_v]:
                copyed = pygame.scrap.get(pygame.SCRAP_TEXT)
                if copyed == None: copyed = ''
                try: copyed = str(copyed.decode('utf8')[:-1])
                except: copyed = ''
                self.search_str = copyed
            else:
                for i in tuple(self.keys.keys()):
                    if keys[i]:
                        if not self.keys_t.get(i):
                            self.keys_t[i] = True
                            key = self.keys[i]
                            if i in self.s_keys.keys():
                                self.search_str += key if not shift else self.s_keys[i]
                            elif key != '-1' and key != '-2' and len(self.search_str) < 20: self.search_str += key if not shift else key.upper()
                            elif key == '-1': self.search_str = self.search_str[:-1]
                            elif key == '-2' and not self.loaded: self._load_func(self.search_str)
                    elif self.keys_t.get(i): self.keys_t.pop(i)
        elif not self.loaded:
            for i in [pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT]:
                if keys[i]:
                    if not self.keys_t.get(i):
                        if i == pygame.K_SPACE: self.vlc.toggle()
                        elif i in [pygame.K_LEFT, pygame.K_RIGHT]:
                            v = 5 if i == pygame.K_RIGHT else -5
                            t = int(self.vlc.getLength()*self.vlc.getPosition()+(v*1000))
                            if t < 0: t = 0
                            elif t > self.vlc.getLength(): t = self.vlc.getLength()
                            self.vlc.setTime(t)
                        self.keys_t[i] = True
                elif self.keys_t.get(i):
                    self.keys_t.pop(i)
        elif self.start > 0: self.start = 0
        playing = self.vlc.isPlaying()
        if not playing and self._old_playing and self._loop and self.mainMusic != None:
            self.vlc.setMidea(self.mainMusic.getAudioURL())
            self.vlc.play()
            self.lyric.resetNow(self.vlc.getTime())

        self.old = click
        self.old_h = h
        self.old_loaded = self.loaded
        self._old_playing = playing
        return sf