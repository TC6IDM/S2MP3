# S2MP3
Spotify Playlists to mp3 file

make sure you have ffmpeg installed in the proper path

copy all files in the exmaple folder and move them out, remove the example from the file name and change up the values

for the cookie file: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp

I made a question on ytdlp! https://github.com/yt-dlp/yt-dlp/issues/6847

FATAL ERRORS:
C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\__main__.py
pytube.exceptions.AgeRestrictedError: Gu6GUBT0sIw is age restricted, and can't be accessed without logging in.

Searching Youtube for Kanye West - Moon #intitle official audio #intitle high quality #intitle HQ
Traceback (most recent call last):
  File "c:\Users\Owner\Desktop\S2MP3\SpotifyToMp3.py", line 110, in <module>
    run()
  File "c:\Users\Owner\Desktop\S2MP3\SpotifyToMp3.py", line 100, in run
    while not downloadPlaylist(currentPlaylist): pass
  File "c:\Users\Owner\Desktop\S2MP3\SpotifyToMp3.py", line 86, in downloadPlaylist
    song.get_videos()#function is slow
  File "c:\Users\Owner\Desktop\S2MP3\Song.py", line 123, in get_videos
    thisYoutubeSong = YoutubeSong(self,r)
  File "c:\Users\Owner\Desktop\S2MP3\YoutubeSong.py", line 32, in __init__
    self.length = youtubeVideo.length*1000
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\__main__.py", line 386, in length
    self.bypass_age_gate()
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\__main__.py", line 257, in bypass_age_gate
    innertube_response = innertube.player(self.video_id)
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\innertube.py", line 300, in player
    return self._call_api(endpoint, query, self.base_data)
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\innertube.py", line 242, in _call_api
    response = request._execute_request(
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\request.py", line 37, in _execute_request
    return urlopen(request, timeout=timeout)  # nosec
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.3056.0_x64__qbz5n2kfra8p0\lib\urllib\request.py", line 216, in urlopen
    return opener.open(url, data, timeout)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.3056.0_x64__qbz5n2kfra8p0\lib\urllib\request.py", line 525, in open
    response = meth(req, response)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.3056.0_x64__qbz5n2kfra8p0\lib\urllib\request.py", line 634, in http_response
    response = self.parent.error(
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.3056.0_x64__qbz5n2kfra8p0\lib\urllib\request.py", line 563, in error
    return self._call_chain(*args)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.3056.0_x64__qbz5n2kfra8p0\lib\urllib\request.py", line 496, in _call_chain
    result = func(*args)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.3056.0_x64__qbz5n2kfra8p0\lib\urllib\request.py", line 643, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 502: Bad Gateway

RROR: [youtube] lE-GhpoL3c4: Video unavailable. This video is not available


Editing Metadata
Traceback (most recent call last):
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\mutagen\_util.py", line 251, in _openfile
    fileobj = open(filename, "rb+" if writable else "rb")
FileNotFoundError: [Errno 2] No such file or directory: ''

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\Owner\Desktop\S2MP3\SpotifyToMp3.py", line 148, in <module>
    while not downloadPlaylist(stressTestPlaylist): pass
  File "c:\Users\Owner\Desktop\S2MP3\SpotifyToMp3.py", line 129, in downloadPlaylist
    song.getBestVideo().download()
  File "c:\Users\Owner\Desktop\S2MP3\YoutubeSong.py", line 127, in download
    self.parent.setFileData(newDestination)
  File "c:\Users\Owner\Desktop\S2MP3\Song.py", line 173, in setFileData
    audio = MP3(file, ID3=EasyID3)
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\mutagen\_file.py", line 48, in __init__
    self.load(*args, **kwargs)
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\mutagen\_util.py", line 154, in wrapper
    with _openfile(self, filething, filename, fileobj,
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.3056.0_x64__qbz5n2kfra8p0\lib\contextlib.py", line 135, in __enter__
    return next(self.gen)
  File "C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\mutagen\_util.py", line 272, in _openfile
    raise MutagenError(e)
mutagen.MutagenError: [Errno 2] No such file or directory: ''

BOTTLENECKS:
1. getting results
2. converting to mp3 
3. the pause before downloading starts

#cd D:\Songs\test\Road-Kill
#python -m spotdl https://open.spotify.com/playlist/24Qq6TevVwM8N8F0yjRily?si=5ff918e3c1e94d8b

PACKAGE EDITS:
1. 
C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3 10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\__main__.py

line 377-399:
    @property
    def length(self) -> int:
        """Get the video length in seconds.

        :rtype: int
        """
        Len = self.vid_info.get('videoDetails', {}).get('lengthSeconds')
        while (Len is None):
            self.bypass_age_gate()
            Len = self.vid_info.get('videoDetails', {}).get('lengthSeconds')
        return int(Len)

    @property
    def views(self) -> int:
        """Get the number of the times the video has been viewed.

        :rtype: int
        """
        views = self.vid_info.get("videoDetails", {}).get("viewCount")
        while (views is None):
            self.bypass_age_gate()
            views = self.vid_info.get("videoDetails", {}).get("viewCount")
        return int(views)

Line 264:
            pass
            # raise exceptions.AgeRestrictedError(self.video_id)

2. 
C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\eyed3\id3\frames.py

line 380:
            # core.parseError(FrameException(f"Invalid date: {self.text}"))

3. 
C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\mutagen\easyid3.py
line 276:
    return ["NULL"] if "TDRC" not in id3 else [stamp.text for stamp in id3["TDRC"].text]

4. 
C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\mutagen\_util.py
line 537:
    return ["NULL"] if key not in self.__dict else self.__dict[key]