import vlc

class VLC:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None

    def setMidea(self, url):
        self.media = self.instance.media_new(url)
        self.media.get_mrl()
        self.player.set_media(self.media)

    def play(self):
        self.player.play()

    def getTime(self) -> float:
        return self.player.get_time() / 1000

    def getLength(self) -> float:
        return self.player.get_length()

    def isPlaying(self) -> bool:
        return self.player.is_playing()

    def setTime(self, ms:float):
        self.player.set_time(ms)

    def getVolume(self) -> int:
        return self.player.get_volume()

    def getState(self) -> int:
        return self.player.get_state()

    def getPosition(self) -> float:
        return self.player.get_position()

    def setPosition(self, val: float):
        return self.player.set_position(val)

    def stop(self):
        self.player.stop()

    def getTimeOfPosition(self, val):
        return (self.getLength()*val)/1000

class VLC_Type:
    def __init__(self):
        self.playing = 1
        self.paused = 0
        self.other = -1