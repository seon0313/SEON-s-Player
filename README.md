# SEON's Player

## 목차

* [목차](#목차)
* [개요](#개요)
* [라이센스](#라이센스)
* [라이브러리](#라이브러리)
* [작동 방식](#작동-방식)

***

## 개요
Sync 자막이 지원되는
Python - Pygame 기반 유튜브 뮤직 클라이언트.

유튜브 뮤직 / 유튜브 노래들을 플레이 할수 있습니다.
가사가 등록되있는 노래는 Musixmatch등 가사 제공업체의 소스를,
가사가 없는 노래/영상/커버는 유튜브 가사를 이용하여 표시합니다.

Musixmatch등의 API를 사용하기에 Youtube Music, Apple Music, Spotify의 서비스와 같은 가사를 보실 수 있습니다.

한국어, 일본어 지원 ( 상용한자 제외한 한자들은 표시 되지 않습니다.(중국어 및 한국어 한자) )

애니메이션이 적용되어 있는 유튜브 자막도 중복 문장 제거 알고리즘을 이용해
문제없이 표시됩니다.

이 프로그램은 실행하는 컴퓨터에 VLC 플레이어가 설치되어 있어야 합니다. 
*** 

## 라이센스

* 한국어/영어 (Base Font) 폰트:  페이퍼로지 폰트
* 일본어 폰트: Kosugi Maru

위 두 폰트를 결합하여 `SEON-font.ttf`을 제작했습니다.
폰트의 저작권은 원본을 따라갑니다.
Aphache 2.0

이 프로그램은 Aphache 2.0 License를 적용합니다.

***

## 라이브러리
| 라이브러리 명 | 비고 |
| --- | --- |
| pygame-ce | (Pygame Community Edition) |
| youtube_transcript_api | 유튜브 가사 |
| syncedlyrics | 가사 API |
| yt_dlp | |
| python-vlc | |
| pafy | |
| glob | 내장 라이브러리 |
| threading | 내장 라이브러리 |
| random | 내장 라이브러리 |
| time | 내장 라이브러리 |
| math | 내장 라이브러리 |

***

## 작동 방식
유튜브 영상이나 유튜브 뮤직의 `video-id`를 이용해 영상/노래를 로드합니다.

`pafy`, `yt-dlp`를 이용하여 영상/노래의 음원 URL와 썸네일 URL를 가져와 재생/표시 합니다.

`syncedlyrics`로 음원의 가사를 로드하고 만약 가사를 로드 하지 못할 경우 `youtube_transcript_api`를 이용해 유튜브 가사를 로드합니다.

`syncedlyrics`를 통해 로드한 경우 LRC 확장자로 로드됩니다.
LRC 가사를 `SEON's Player`의 시스템에 맞게 변한하여 저장합니다.

`youtube_transcript_api`을 통해 로드한 경우 중복된 문장을 합치고 `SEON's Player`의 시스템에 맞게 변한하여 저장합니다.
중복된 문장을 합치는 이유는 효과가 적용된 자막을 로드한 경우 하나의 문장이 몇십개씩 로드되기 때문입니다.

로드한 음원 URL을 VLC backend로 전달하여 음원을 재생시킵니다.

유튜브 로드, 자막로드는 Thread로 따로 로드합니다.

***
