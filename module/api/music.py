import pafy
import syncedlyrics


class Music:
    def __init__(self, code):
        self.video = pafy.new(self.codeto(code), ydl_opts={'nocheckcertificate': True})
        pafy.set_api_key('AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30')

    def codeto(self, code):
        if not 'http' in code: code = 'https://www.youtube.com/watch?v=' + code
        return code

    def getAudioURL(self):
        b = pafy.new(self.video.videoid, ydl_opts={'nocheckcertificate': True})
        audio_url = b.getbestaudio() #preftype="m4a")
        print(audio_url.url)
        return audio_url.url

    def getTitle(self):
        return self.video.title

    def getNails(self):
        return self.video.bigthumb

    def getNailsImage(self):
        import requests, io
        r = requests.get(self.getNails())
        img = io.BytesIO(r.content)
        return img

    def getNailsBest(self):
        import requests, io
        r = requests.get(f'https://i.ytimg.com/vi/{self.video.videoid}/maxresdefault.jpg')
        img = io.BytesIO(r.content)
        return img

    def strToTime(self, s: str) -> float:
        try:
            int(s[-1])
            if len(s) > 1: int(s[-2])
        except:
            return -1
        s = s.split(':')
        sec = float(s[-1])
        if len(s) > 1: sec += 60 * float(s[-2])
        return sec

    def getLyrics(self, lang='ko'):
        data = syncedlyrics.search(f'{self.video.title} {self.video.author}', enhanced=True)
        if data == None or data == '' or len(data) <= 0: return None
        data = data.replace('[', '').replace(']', '').split('\n')
        lyric = {}
        ly = ''
        start = -1
        for index, i in enumerate(data):
            d = i.split(' ')
            if index > 0:
                if lyric.get(index - 1) is None: lyric[index - 1] = []
                lyric[index - 1].append({'start': start, 'end': self.strToTime(d[0]), 'msg': ly})

            ly = ''
            start = -1
            for i in d[1:]:
                if '<' in i:
                    t = self.strToTime(i.replace('<', '').replace('>', ''))
                    if start < 0:
                        start = t
                    else:
                        if lyric.get(index) is None: lyric[index] = []
                        lyric[index].append({'start': start, 'end': t, 'msg': ly})
                        ly = ''
                        start = -2
                else:
                    ly += i
        return lyric


if __name__ == '__main__':
    a = Music(input(':\t'))
    print(a.getAudioURL())
    #print(a.getTitle(), a.getNails())
    #print(a.getLyrics())
