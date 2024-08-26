import threading
import time

import pygame
from module.api.vlc import VLC, VLC_Type
from module.ui.lyric import Lyric
from module.api.music import Music
class Control_Bar:
    def __init__(self, img:dict, vlc: VLC,lyric: Lyric, font:pygame.font.Font, mainMusic: Music,load_func, color = pygame.Color(255,255,255)):
        self.color = color
        self.img:dict = img
        self.vlc = vlc
        self.old = 0
        self.lyric = lyric
        self.mp = (0,0)
        self.start = 0
        self.l = None
        self.play_bar_height = -1
        self.old_h = 0
        self.font = font
        self.mainMusic = mainMusic
        self.loaded = False
        self.search_t = 0
        self.search = False
        self.load_func = load_func
        self.search_str = ''
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

        size = self.img[img_name].get_size()
        sf.blit(self.img[img_name], (w/2-size[0]/2,h/2-size[1]/2))
        if pygame.Rect((w/2-size[0]/2,h/2-size[1]/2,size[0],size[1])).collidepoint(self.mp[0], self.mp[1]):
            if click and not self.old and not self.loaded:
                if v == VLC_Type.playing: self.vlc.pause()
                elif v == VLC_Type.paused:
                    self.vlc.play()
                else:
                    self.vlc.setMidea(self.mainMusic.getAudioURL())
                    self.vlc.play()

        if h != self.old_h:
            self.play_bar_height = max(10,int(h/6))

        pygame.draw.rect(sf, (150,150,150),(0,h-self.play_bar_height,w*self.vlc.getPosition(),self.play_bar_height))
        x,y = self.mp

        if pygame.Rect((0,0,30,h)).collidepoint(self.mp[0],self.mp[1]):
            if self.search_t <= 0: self.search_t = time.time()
            if time.time() - self.search_t >= 1:
                self.search = True
        elif self.search:
            self.search = False
            self.search_t = 0

        if self.search:
            keys = pygame.key.get_pressed()
            shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            for i in tuple(self.keys.keys()):
                if keys[i]:
                    if not self.keys_t.get(i):
                        self.keys_t[i] = True
                        key = self.keys[i]
                        if i in self.s_keys.keys():
                            self.search_str += key if not shift else self.s_keys[i]
                        elif key != '-1' and key != '-2' and len(self.search_str) < 20: self.search_str += key if not shift else key.upper()
                        elif key == '-1': self.search_str = self.search_str[:-1]
                        elif key == '-2' and not self.loaded: self.load_func(self.search_str)
                elif self.keys_t.get(i): self.keys_t.pop(i)
            print(self.loaded, self.search_str)

        if pygame.Rect((0,h-self.play_bar_height,w,self.play_bar_height)).collidepoint(x,y):
            if self.start <= 0: self.start = time.time()
            if time.time() - self.start >= .8:
                if self.l == None or not (self.l[1] <= self.vlc.getTimeOfPosition(x/w) <= self.l[2]):
                    self.l = self.lyric.getLyric(self.vlc.getTimeOfPosition(x/w))
                if self.l != None:
                    f = self.font.render(str(self.l[0]),True,(125,80,90))
                    fr = f.get_rect()
                    fr.x,fr.y = self.mp[0]+fr.w/2, self.mp[1]+fr.h
                    sf.blit(f,fr)
            if click and not self.old:
                self.vlc.setPosition(x/w)
                self.lyric.resetNow(self.vlc.getTime())
        elif self.start > 0: self.start = 0
        self.old = click
        self.old_h = h
        return sf