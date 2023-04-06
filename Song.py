import os
import re
from pytube import Search
from YoutubeSong import YoutubeSong
import subprocess
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3  
import shutil # save img locally
import requests
from mutagen.id3 import ID3, APIC, error, TXXX
from os.path import exists
from extraUtil import *

def cleanTrackName(text):
    cleanerTrackName = re.sub('\<.*?\>', '', text)
    cleanerTrackName = re.sub('\[.*?\]', '', cleanerTrackName)
    cleanerTrackName = re.sub('\{.*?\}', '', cleanerTrackName)
    cleanerTrackName = re.sub('\(.*?\)', '', cleanerTrackName)
    cleanerTrackName = re.sub(r'[^\w\s]', '', cleanerTrackName)
    cleanerTrackName = re.sub("\s\s+", " ", cleanerTrackName)
    cleanerTrackName = cleanerTrackName.strip()
    return cleanerTrackName.lower()

def addZeros(number):
    if int(number)<10: return f'(000{number})'
    if int(number)<100: return f'(00{number})'
    if int(number)<1000: return f'(0{number})'
    return f'({number})'

class Song:
    def __init__(self,track,index):
        self.index=index
        self.destinationIndex = addZeros(self.index)
        self.albumArtists = "/".join(
            [deleteBadCharacters(artist["name"]) for artist in track["track"]["album"]["artists"]]
        )
        self.albumArtists = "NULL" if self.albumArtists is None or self.albumArtists == "" else self.albumArtists
        
        self.albumPicture = "NULL" if len(track["track"]["album"]["images"])==0 else track["track"]["album"]["images"][0]['url']
            
        self.albumName = deleteBadCharacters(track["track"]["album"]["name"])
        self.albumName = "NULL" if self.albumName is None or self.albumName == "" else self.albumName
            
        self.releaseDate = track["track"]["album"]['release_date']
        self.releaseDate = "NULL" if self.releaseDate is None or self.releaseDate == "" else self.releaseDate
            
        self.trackArtists = "/".join(
            [deleteBadCharacters(artist["name"]) for artist in track["track"]["artists"]]
        )
        self.trackArtists = "NULL" if self.trackArtists is None or self.trackArtists == "" else self.trackArtists
            
        self.trackName = deleteBadCharacters(track["track"]["name"])# annoying characters
        self.trackName = "NULL" if self.trackName is None or self.trackName == "" else self.trackName
        self.cleanTrackName=removeSymbols(self.trackName)
            
        self.discnumber = track["track"]["disc_number"]
        self.discnumber = 0 if self.discnumber is None or self.discnumber == "" else self.discnumber
            
        self.tracknumber = track["track"]["track_number"]
        self.tracknumber = 0 if self.tracknumber is None or self.tracknumber == "" else self.tracknumber
            
        self.duration_ms = track["track"]["duration_ms"]
        self.duration_ms = 0 if self.duration_ms is None or self.duration_ms == "" else self.duration_ms
            
        self.explicit = track["track"]["explicit"]
        self.explicit = False if self.explicit is None or self.explicit == "" else self.explicit
        
    def get_videos(self):
        '''Gets and returns the video ID and Title (as seen on youtube)'''        
        intitleSTANDARD = "#intitle official audio #intitle high quality #intitle HQ"
        
        if (self.explicit == "True"): 
            intitleSTANDARD += " #intitle explicit"
        querySTANDARD = self.trackArtists+" - "+self.trackName+" "
        self.youtubeVideos = []
        totalQ = querySTANDARD+intitleSTANDARD
        enoughResults = False
        while not enoughResults:
            s = Search(totalQ)
            for i in s.results:
                thisYoutubeSong = YoutubeSong(i.video_id,i.length*1000,i.title,i.views,self)
                self.youtubeVideos.append(thisYoutubeSong)

            if (len(self.youtubeVideos)<MAX_SEARCH_DEPTH):
                totalQ = querySTANDARD
                prRed("QUERY: "+querySTANDARD+intitleSTANDARD+"\nNot enough results found, retrying without intitle")
            else:
                enoughResults = True
        return
    
    def getBestVideo(self):
        found = False
        difference = 1000
        possibleSongList=[]
        while len(possibleSongList)==0:
            for i,currentYoutubeVideo in enumerate(self.youtubeVideos):
                if (i>=MAX_SEARCH_DEPTH): break
                timediff = abs(int(self.duration_ms)-int(currentYoutubeVideo.length))
                if (currentYoutubeVideo.isNotBad()):
                    cleanerTrackName = cleanTrackName(self.trackName)
                    nameInTitle = cleanerTrackName in currentYoutubeVideo.title.lower()
                    addto = 0
                    if (nameInTitle): addto = 1000000000000
                    if (currentYoutubeVideo.isVeryGood() and (timediff <= difference+(int(self.duration_ms)*0.05))):
                        addto += 1000000000000
                        possibleSongList.append([currentYoutubeVideo.views+addto,currentYoutubeVideo])
                        possibleSongList = sorted(possibleSongList,reverse=True)
                        found = True
                    elif ((timediff <= difference) or ((nameInTitle) and (timediff <= difference+(int(self.duration_ms)*0.05)))):
                        possibleSongList.append([currentYoutubeVideo.views+addto,currentYoutubeVideo])
                        possibleSongList = sorted(possibleSongList,reverse=True)
                        found = True
                    if found:
                        return possibleSongList[0][1]
                    
            prRed("No suitable video found for "+self.trackName+ " within "+str(difference)+" ms of the origninal")
            difference+=1000
    
    def setDestination(self,destination):
        self.destination = destination
    
    def setFileData(self,file):
        # print(data,file)
        print("Converting to mp3")
        audio_file = file.replace(".webm", ".mp3").replace(".m4a", ".mp3")
        if exists(audio_file) : prRed("ERROR converting "+file+" to mp3, possible duplicate");return
        subprocess.run('ffmpeg -i "'+file+'" "'+audio_file+'"',shell=True,capture_output=True)
        os.remove(file)
        prGreen(audio_file)
        print("Editing Metadata")
        audio = MP3(audio_file, ID3=EasyID3)
        audio['artist'] = self.trackArtists
        audio['title'] = self.trackName
        audio['albumartist'] = self.albumArtists
        audio['album'] = self.albumName
        audio['date'] = self.releaseDate
        audio['discnumber'] = str(self.discnumber)
        audio['tracknumber'] = str(self.tracknumber)
        
        audio.save()
        prGreen("Metadata Saved")
        
        image_file = OUTPUT_FOLDER_NAME+'\\tempImage.jfif'
        print("Downloading Album Image")
        if self.albumPicture == "NULL": prRed('Album image Couldn\'t be retrieved\n'); return
        res = requests.get(self.albumPicture, stream = True) 
        if res.status_code == 200:
            with open(image_file,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            prGreen(image_file+"")
        else:
            prRed('Album image Couldn\'t be retrieved\n')
            return
        audio = MP3(audio_file, ID3=ID3)    
        audio.tags.add(
        APIC(
            encoding=3, # 3 is for utf-8
            mime='image/jfif', # image/jpeg or image/png
            type=3, # 3 is for the cover image
            desc=u'Cover',
            data=open(image_file,'rb').read()
            )
        )
        audio.save()
        os.remove(image_file)
        return