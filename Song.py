import json
import os
import re
import jsonpickle
from pytube import Search
from YoutubeSong import YoutubeSong
import subprocess
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3  
import shutil
import requests
from mutagen.id3 import ID3, APIC, error, TXXX
from os.path import exists
from extraUtil import *

def removeBrackets(text):
    cleanerTrackName = re.sub('\<.*?\>', '', text)
    cleanerTrackName = re.sub('\[.*?\]', '', cleanerTrackName)
    cleanerTrackName = re.sub('\{.*?\}', '', cleanerTrackName)
    cleanerTrackName = re.sub('\(.*?\)', '', cleanerTrackName)
    return cleanerTrackName
    
def removePunctuation(text):
    cleanerTrackName = re.sub(r'[^\w\s]', '', text)
    cleanerTrackName = re.sub("\s\s+", " ", cleanerTrackName)
    return cleanerTrackName

def cleanTrackName(text):
    cleanerTrackName = removeBrackets(text)
    cleanerTrackName = removePunctuation(text)
    cleanerTrackName = cleanerTrackName.strip()
    return cleanerTrackName.lower()

def addZeros(number):
    if int(number)<10: return f'(000{number})'
    if int(number)<100: return f'(00{number})'
    if int(number)<1000: return f'(0{number})'
    return f'({number})'

class Song:
    def __init__(self,track,index,playlistName):
        self.playlistName = playlistName
        self.index=index
        self.destinationIndex = addZeros(self.index)
        self.albumArtistsPlain = [deleteBadCharacters(artist["name"]) for artist in track["track"]["album"]["artists"]]
        self.albumArtists = "/".join(self.albumArtistsPlain)
        self.albumArtists = "NULL" if self.albumArtists is None or self.albumArtists == "" else self.albumArtists
        self.originalAlbumArtist = "NULL" if self.albumArtists is None or self.albumArtists == "" or self.albumArtists == "NULL" else self.albumArtistsPlain[0]
       
        self.albumPicture = "NULL" if len(track["track"]["album"]["images"])==0 else track["track"]["album"]["images"][0]['url']
            
        self.albumName = deleteBadCharacters(track["track"]["album"]["name"])
        self.albumName = "NULL" if self.albumName is None or self.albumName == "" else self.albumName
            
        self.releaseDate = track["track"]["album"]['release_date']
        self.releaseDate = "NULL" if self.releaseDate is None or self.releaseDate == "" else self.releaseDate
        
        self.trackArtistsPlain = [deleteBadCharacters(artist["name"]) for artist in track["track"]["artists"]]
        self.trackArtists = "/".join(self.trackArtistsPlain)
        self.trackArtists = "NULL" if self.trackArtists is None or self.trackArtists == "" else self.trackArtists
        self.originalTrackArtist = "NULL" if self.trackArtists is None or self.trackArtists == "" or self.trackArtists == "NULL" else self.trackArtistsPlain[0]
        
        self.trackName = deleteBadCharacters(track["track"]["name"])# annoying characters
        self.trackName = "NULL" if self.trackName is None or self.trackName == "" else self.trackName
        self.cleanTrackName=removeSymbols(self.trackName)
        self.neatFormatTrackName = cleanTrackName(self.trackName)
        
        self.discnumber = track["track"]["disc_number"]
        self.discnumber = 0 if self.discnumber is None or self.discnumber == "" else self.discnumber
            
        self.tracknumber = track["track"]["track_number"]
        self.tracknumber = 0 if self.tracknumber is None or self.tracknumber == "" else self.tracknumber
            
        self.duration_ms = track["track"]["duration_ms"]
        self.duration_ms = 0 if self.duration_ms is None or self.duration_ms == "" else self.duration_ms
            
        self.explicit = track["track"]["explicit"]
        self.explicit = False if self.explicit is None or self.explicit == "" else self.explicit
        
        self.debugParentFolder = f'{DEBUG_FOLDER_NAME}\\{self.playlistName}'
        self.parentFolder = f'{OUTPUT_FOLDER_NAME}\\{self.playlistName}'
        self.destination = f'{self.parentFolder}\\{self.destinationIndex} {self.cleanTrackName}'
        self.debugDestination = f'{self.debugParentFolder}\\{self.destinationIndex} {self.cleanTrackName}.json'
        self.youtubeSearch = ""
        self.bestfit = None
        self.youtubeVideos = []
        # self.track = track
        
    def get_videos(self):
        '''Gets and returns the video ID and Title (as seen on youtube)'''        
        intitleSTANDARD = "#intitle official audio #intitle high quality #intitle HQ"
        
        if (self.explicit == "True"): 
            intitleSTANDARD += " #intitle explicit"
        self.youtubeSearch = self.trackArtists+" - "+self.trackName+" "+intitleSTANDARD
        enoughResults = False
        retries = 0
        while not enoughResults:
            print("Searching Youtube for "+self.youtubeSearch)
            self.youtubeVideos = []
            s = Search(self.youtubeSearch)
            for i,r in enumerate(s.results):
                prGreen(f'Found {i+1} of {len(s.results)} results {round(100*(i+1) / len(s.results),2)}%                        ',end='\r')
                thisYoutubeSong = YoutubeSong(self,r)
                self.youtubeVideos.append(thisYoutubeSong)
            
            if (len(self.youtubeVideos)<MAX_SEARCH_DEPTH):
                prRed(f'Found {len(self.youtubeVideos)} results, not enough, retrying with different query',end='\r')
                match retries:
                    case 0:
                        prYellow(f'\nQUERY: {self.youtubeSearch}\nRetrying with only the original artist')
                        self.youtubeSearch = self.originalTrackArtist+" - "+self.trackName+" "+intitleSTANDARD
                    case 1:
                        prYellow(f'\nQUERY: {self.youtubeSearch}\nRetrying with only the original artist and without brackets in the track name')
                        self.youtubeSearch = self.originalTrackArtist+" - "+removeBrackets(self.trackName)+" "+intitleSTANDARD
                    case 2:
                        prYellow(f'\nQUERY: {self.youtubeSearch}\nRetrying with only the original artist and without brackets in the track name and without #intitle')
                        self.youtubeSearch = self.originalTrackArtist+" - "+removeBrackets(self.trackName)
                    case _:
                        prRed(f'\nRetry: {retries} Song Skipped')
                retries+=1
                prYellow(f'NEW QUERY: {self.youtubeSearch}')
            else:
                enoughResults = True
        return
    
    def getBestVideo(self):
        found = None
        difference = 0
        possibleSongList=[]
        oneT=10**12
        while found is None:
            for currentYoutubeVideo in self.youtubeVideos[0:MAX_SEARCH_DEPTH]:  #first 5 only
                currentYoutubeVideo.weight = currentYoutubeVideo.views
                
                timediff = abs(int(self.duration_ms)-int(currentYoutubeVideo.length))
                currentYoutubeVideo.notWithinTimeLimit = timediff > difference+(int(self.duration_ms)*0.05)
                currentYoutubeVideo.badTitle = not currentYoutubeVideo.isNotBad()
                currentYoutubeVideo.nameInTitle = self.neatFormatTrackName in currentYoutubeVideo.title.lower()
                currentYoutubeVideo.goodNameInTitle = currentYoutubeVideo.isVeryGood()
                currentYoutubeVideo.closeToTime = timediff<=difference
                if ( currentYoutubeVideo.notWithinTimeLimit or currentYoutubeVideo.badTitle): continue #skip if not in bounds of time limit or has bad names in title
                
                #ugly ass names :barf: 
                if currentYoutubeVideo.nameInTitle: currentYoutubeVideo.weight += oneT
                if currentYoutubeVideo.goodNameInTitle: currentYoutubeVideo.weight += oneT
                if currentYoutubeVideo.closeToTime: currentYoutubeVideo.weight += oneT 
                possibleSongList.append(currentYoutubeVideo)
                
            if (len(possibleSongList)!=0):
                possibleSongList.sort(key=lambda x: x.weight, reverse=True)
                found = possibleSongList[0]
                self.bestfit = found
                print()
                return self.bestfit
            print()
            prRed(f'No suitable video found for {self.trackName} within {difference} ms of the origninal',end='\r')
            difference+=1000
              
    def saveToDebug(self):
        json_object = jsonpickle.encode(self)
        if not os.path.exists(self.debugParentFolder):
            os.makedirs(self.debugParentFolder)
        with open(self.debugDestination, "w") as outfile:
            outfile.write(json.dumps(json.loads(json_object), indent=4))
    
    def setFileData(self,file):
        # print(data,file)
        print("Converting to mp3")
        audio_file = re.sub('(\.)(?!.*\.).*$', '.mp3', file) #what the fuck
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