import pafy
import syncedlyrics
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


class Music:
    def __init__(self, code):
        self.video = pafy.new(self.codeto(code), ydl_opts={'nocheckcertificate': True})
        pafy.set_api_key('AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30')
        self.ydl_opt = {
            'format': 'bestaudio',
            'subtitlesformat': 'srt',
        }

    def codeto(self, code):
        if not 'http' in code: code = 'https://www.youtube.com/watch?v=' + code
        return code

    def getAudioURL(self):
        b = pafy.new(self.video.videoid, ydl_opts={'nocheckcertificate': True})
        audio_url = ''
        with yt_dlp.YoutubeDL(self.ydl_opt) as v:
            #print(v.list_subtitles(b.videoid,['ko']))
            info = v.extract_info(b.watchv_url, download=False)
            v.close()
        formats = info['formats']
        minus = 0
        urls = []
        for index, i in enumerate(formats):
            if i.get('acodec') in ['none', None] or not i.get('vcodec') in ['none', None]:
                minus += 1
                continue
            url = i['url']
            format = i['format']
            audio = i['audio_ext']
            if index == 0: print(i)
            #print(f'{index+1-minus}st {format} {audio} {url}')
            urls.append({'format': audio, 'type': format, 'url': url})
        return urls[-1]['url']

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
        if data == None or data == '' or len(data) <= 0:
            data = YouTubeTranscriptApi.get_transcript(self.video.videoid, languages=['ko'])
            lyric = {}
            for index, i in enumerate(data):
                if lyric.get(index - 1) is None: lyric[index - 1] = []
                for d in i['text'].split(' '):
                    if len(d) <= 0: d = '33'
                    lyric[index - 1].append({'start': i['start'], 'end': i['start'] + i['duration'], 'msg': d})
        else:
            data = data.replace('[', '').replace(']', '').split('\n')
            lyric = {}
            ly = ''
            old_t = 0
            start = -1
            sync = True
            for index, i in enumerate(data):
                if not '<' in i: sync, start = (False,old_t)
                d = i.split(' ')
                if index > 0:
                    if lyric.get(index - 1) is None: lyric[index - 1] = []
                    lyric[index - 1].append({'start': start, 'end': self.strToTime(d[0]), 'msg': ly})

                ly = ''
                start = -1
                for index2, i in enumerate(d[1:]):
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
                        if not sync:
                            if lyric.get(index) is None: lyric[index] = []
                            lyric[index].append({'start': old_t, 'end': self.strToTime(d[0]), 'msg': ly})
                            ly = ''

                old_t = self.strToTime(d[0])
        return lyric


if __name__ == '__main__':
    a = Music(input(':\t'))
    #print(a.getAudioURL())
    #print(a.getTitle(), a.getNails())
    print(a.getLyrics())
