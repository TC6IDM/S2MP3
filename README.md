# S2MP3
Spotify Playlists to mp3 file

make sure you have ffmpeg installed in the proper path

copy all files in the exmaple folder and move them out, remove the example from the file name and change up the values

FATAL ERRORS:
C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pytube\__main__.py
pytube.exceptions.AgeRestrictedError: Gu6GUBT0sIw is age restricted, and can't be accessed without logging in.

BOTTLENECKS:
1. getting results
2. converting to mp3 
3. the pause before downloading starts

PACKAGE EDITS:
1. 
https://github.com/ytdl-org/youtube-dl/issues/31530
C:\Users\Owner\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\youtube_dl\extractor\youtube.py

'uploader_id': self._search_regex(r'/(?:channel|user)/([^/?&#]+)', owner_profile_url, 'uploader id') if owner_profile_url else None,

CHANGE TO --------->

'uploader_id': self._search_regex(r'/(?:channel|user)/([^/?&#]+)', owner_profile_url, 'uploader id', fatal=False) if owner_profile_url else None,

2. 
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