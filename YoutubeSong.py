import math
import time
import youtube_dl
import yt_dlp
from extraUtil import *
            
class MyLogger(object):
    '''Logs Errors/warnigs/debugs'''
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        if "'_percent_str'" not in msg and "'_eta_str'" not in msg: 
            prRed(msg+"\n")

def printBar(name,percentage,eta,speed): #i am geniuenly proud of this function
    '''prints a bar to see how the download is coming along'''
    bartotalstring = f'\r{name} ||{percentage} ETA: {eta} Speed: {speed} '
    fill = '█'
    terminalSize = os.get_terminal_size().columns
    length = terminalSize - len(bartotalstring) if terminalSize - len(bartotalstring) > 10 else 10
    printEnd = ""
    filledLength = int(math.floor((float(percentage[:-1])/100)*length))
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{name} |{bar}| {percentage} ETA: {eta} Speed: {speed}', end = printEnd)

# def printBarSHIT(name,template,percentage):
#     '''prints a bar to see how the download is coming along'''
#     bartotalstring = f'\r{name} ||{template} '
#     fill = '█'
#     terminalSize = os.get_terminal_size().columns
#     length = terminalSize - len(bartotalstring) if terminalSize - len(bartotalstring) > 10 else 10
#     printEnd = ""
#     filledLength = int(math.floor((float(percentage[:-1])/100)*length))
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print(f'\r{name} |{bar}| {template}', end = printEnd)

class YoutubeSong:
    def __init__(self,parent,youtubeVideo):
        self.id = youtubeVideo.video_id
        self.youtubeLink=youtubeVideo.watch_url
        self.length = youtubeVideo.length*1000
        self.title = youtubeVideo.title
        self.views = youtubeVideo.views
        self.weight = self.views
        self.notWithinTimeLimit = False
        self.badTitle = False
        self.nameInTitle = False
        self.goodNameInTitle = False
        self.closeToTime = False
        self.parent = parent
        # self.youtubeVideo = youtubeVideo
    
    def isNotBad(self):
        blacklistDirty = ["clean"]
        blacklist = ["instrumental",
                 "8d",
                 "1 hour",
                 "full album",
                 "alternative",
                 "sped up",
                 "acapella",
                 "vocals only",
                 "radio edit",
                 "extended",
                 "slowed",
                 "reverb",
                 "bass boosted"]
        if self.parent.explicit: 
            blacklist = blacklist + blacklistDirty
        for i in blacklist:
            if (i in self.title.lower()) and (i not in self.parent.trackArtists.lower()) and (i not in self.parent.trackName.lower()): return False #if word is in the title, it must be in the artist or song name
        return True

    def isVeryGood(self):
        blacklistDirty = ["uncensored",
                    "explicit",]
        blacklist = ["official audio",
                    "high quality",
                    "hq",
                    "official visualizer",
                    "visualizer",
                    "lyrics",
                    "(audio)"]
        if self.parent.explicit: 
            blacklist = blacklist + blacklistDirty
        
        for i in blacklist:
            if (i in self.title.lower()): return True #
        return False
    
    def my_hook(self,d):
        ''''status': 'downloading', 
            'downloaded_bytes': 1319748, 
            'total_bytes': 3622010, 
            'tmpfilename': 'C:\\Songs\\All Falls Down.m4a.part', 
            'filename': 'C:\\Songs\\All Falls Down.m4a', 
            'eta': 51, 
            'speed': 44831.65774925726, 
            'elapsed': 15.69459342956543, 
            '_eta_str': '00:51', 
            '_percent_str': ' 36.4%', 
            '_speed_str': '43.78KiB/s', 
            '_total_bytes_str': '3.45MiB'
            '''
        if d['status'] == 'finished':
            prGreen("\n"+d['filename'])
            self.parent.setFileData(d['filename'])
            prCyan("File Done!\n")
        
        printBar(self.parent.trackName,d['_percent_str'].strip(),d['_eta_str'].strip(),d['_speed_str'].strip())
        
        
    def download(self):
        print(f'{self.parent.destination}\n{self.parent.debugDestination}')
        print("Now Downloading:",self.title,"| On Youtube",self.youtubeLink)
        self.parent.saveToDebug()
        ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',#highest quality
            }],
            'ignoreerrors': True, #ignore errors
            'outtmpl': self.parent.destination+'.%(ext)s', #save songs here .%(ext)s
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook],
            'cookiefile': COOKIE_FILE, #cookies for downloading age restricted videos
        }
                                    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.youtubeLink])