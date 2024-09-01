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

    def getNextItem(self) -> Music:
        self.index += 1
        return self._items[self.index]

    def getLen(self) -> int:
        return len(self._items)

    def getMusic(self, index: int = None) -> Music:
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
        Thread(target=self._addMusic, args=code, daemon=True).start()
