from typing import Tuple

from module.api.music import Music
from threading import Thread


class Playlist:
    def __init__(self):
        self._items: list[Music] = []
        self.name = ''
        self.index = 0
        self.event = None

    def getItems(self) -> tuple[Music, ...]:
        return tuple(self._items)

    def getNextItem(self, reset=True) -> Music:
        if reset:
            self.index += 1
            if len(self._items)-1 < self.index: self.index = 0
        else: return self._items[0 if len(self._items)-1 < self.index+1 else self.index+1]
        return self._items[self.index]

    def isLast(self) -> bool:
        if len(self._items)-1 == self.index: return True
        else: return False

    def isFirst(self) -> bool:
        if not self.index: return True
        else: return False

    def getLen(self) -> int:
        return len(self._items)

    def getMusic(self, index: int = None, reset=True) -> Music:
        if reset: self.index = index
        if index == None:
            return self._items[self.index]
        else:
            return self._items[index]

    def addMusicEndEvent(self, code: str) -> None:
        if self.event != None:
            try:
                self.event(code)
            except:
                pass

    def _addMusic(self, code: str):
        music = Music(code, True)
        self._items.append(music)

    def addMusic(self, code: str):
        Thread(target=self._addMusic, args=(code,), daemon=True).start()

    def appendMusic(self, music: Music):
        self._items.append(music)
