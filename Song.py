import json
import os
import re
import eyed3
import jsonpickle
from pytube import Search
from YoutubeSong import YoutubeSong
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3  
import shutil
import requests
from extraUtil import *
from eyed3.id3.frames import ImageFrame

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

def cleanTrackName2(text):
    cleanerTrackName = removeBrackets(text)
    cleanerTrackName = removePunctuation(cleanerTrackName)
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
        self.albumArtistsPlain = "NULL" if track is None or "album" not in track.keys() else [deleteBadCharacters(artist["name"]) for artist in track["album"]["artists"]]
        self.albumArtists = "NULL" if track is None or "album" not in track.keys() else "/".join(self.albumArtistsPlain)
        self.albumArtists = "NULL" if track is None or self.albumArtists is None or self.albumArtists == "" else self.albumArtists
        self.originalAlbumArtist = "NULL" if track is None or self.albumArtists is None or self.albumArtists == "" or self.albumArtists == "NULL" else self.albumArtistsPlain[0]
       
        self.albumPicture = "NULL" if track is None or "album" not in track.keys() or len(track["album"]["images"])==0 else track["album"]["images"][0]['url']
            
        self.albumName = "NULL" if track is None or "album" not in track.keys() else deleteBadCharacters(track["album"]["name"])
        self.albumName = "NULL" if track is None or self.albumName is None or self.albumName == "" else self.albumName
            
        self.releaseDate = "NULL" if track is None or "album" not in track.keys() else track["album"]['release_date']
        self.releaseDate = "NULL" if track is None or self.releaseDate is None or self.releaseDate == "" else self.releaseDate #re.search('^([^\\-]*)',self.releaseDate).group(1)
        
        self.trackArtistsPlain = "NULL" if track is None or "artists" not in track.keys() else [deleteBadCharacters(artist["name"]) for artist in track["artists"]]
        self.trackArtists = "NULL" if track is None or "artists" not in track.keys() else "/".join(self.trackArtistsPlain)
        self.trackArtists = "NULL" if track is None or self.trackArtists is None or self.trackArtists == "" else self.trackArtists
        self.originalTrackArtist = "NULL" if track is None or self.trackArtists is None or self.trackArtists == "" or self.trackArtists == "NULL" else self.trackArtistsPlain[0]
        
        self.trackName = "NULL" if track is None or "name" not in track.keys() else deleteBadCharacters(track["name"])# annoying characters
        self.trackName = "NULL" if track is None or self.trackName is None or self.trackName == "" else self.trackName
        self.cleanTrackName=removeSymbols(self.trackName)
        self.neatFormatTrackName = cleanTrackName2(self.trackName)
        self.discnumber = "NULL" if track is None or "disc_number" not in track.keys() else track["disc_number"]
        self.discnumber = 0 if track is None or self.discnumber is None or self.discnumber == "" else self.discnumber
            
        self.tracknumber = "NULL" if track is None or "track_number" not in track.keys() else track["track_number"]
        self.tracknumber = 0 if track is None or self.tracknumber is None or self.tracknumber == "" else self.tracknumber
            
        self.duration_ms = "NULL" if track is None or "duration_ms" not in track.keys() else track["duration_ms"]
        self.duration_ms = 0 if track is None or self.duration_ms is None or self.duration_ms == "" else self.duration_ms
            
        self.explicit = "NULL" if track is None or "explicit" not in track.keys() else track["explicit"]
        self.explicit = False if track is None or self.explicit is None or self.explicit == "" else self.explicit
        self.setFolderInformation(self.cleanTrackName)
        self.youtubeSearch = ""
        self.bestfit = None
        self.youtubeVideos = []
    
    def setFolderInformation(self,trackName):
        self.debugParentFolder = f'{DEBUG_FOLDER_NAME}\\{self.playlistName}'
        self.parentFolder = f'{OUTPUT_FOLDER_NAME}\\{self.playlistName}'
        self.destination = f'{self.parentFolder}\\{self.destinationIndex} {trackName}'
        self.debugDestination = f'{self.debugParentFolder}\\{self.destinationIndex} {trackName}.json'
        self.finalDestination = ""
            
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
            if (len(s.results)<MAX_SEARCH_DEPTH):
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
                continue
                
            enoughResults = True 
            for i,r in enumerate(s.results):
                prGreen(f'Found {i+1} of {len(s.results)} results {round(100*(i+1) / len(s.results),2)}%                        ',end='\r')
                thisYoutubeSong = YoutubeSong(self,r)
                self.youtubeVideos.append(thisYoutubeSong)
            return
            
            
        
    
    def getBestVideo(self):
        found = None
        difference = 0
        possibleSongList=[]
        oneT=10**12
        while found is None:
            for i,currentYoutubeVideo in enumerate(self.youtubeVideos):  #first 5 only
                # print(f'\nFinding Best Video {i} of {MAX_SEARCH_DEPTH} {100*i/MAX_SEARCH_DEPTH}%                        ',end='\r')
                currentYoutubeVideo.weight = currentYoutubeVideo.views
                
                timediff = abs(int(self.duration_ms)-int(currentYoutubeVideo.length))
                currentYoutubeVideo.notWithinTimeLimit = timediff > difference+(int(self.duration_ms)*0.05)
                currentYoutubeVideo.badTitle = not currentYoutubeVideo.isNotBad()
                currentYoutubeVideo.nameInTitle = self.neatFormatTrackName in currentYoutubeVideo.title.lower()
                currentYoutubeVideo.goodNameInTitle = currentYoutubeVideo.isVeryGood()
                currentYoutubeVideo.closeToTime = timediff<=difference
                if (currentYoutubeVideo.notWithinTimeLimit or currentYoutubeVideo.badTitle): continue #skip if not in bounds of time limit or has bad names in title
                
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
        print("Editing Metadata")
        audio = MP3(file, ID3=EasyID3)
        audio['artist'] = self.trackArtists
        audio['title'] = self.trackName
        audio['albumartist'] = self.albumArtists
        audio['album'] = self.albumName
        audio['date'] = self.releaseDate
        audio['discnumber'] = str(self.discnumber)
        audio['tracknumber'] = str(self.tracknumber)
        
        audio.save(v2_version = 3)
        prGreen("Metadata Saved")
        image_file = OUTPUT_FOLDER_NAME+'\\tempImage.jpg'
        
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
        audiofile = eyed3.load(file)
        if (audiofile.tag == None):
            audiofile.initTag()
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(image_file,'rb').read(), 'image/jpeg')
        audiofile.tag.save()
        prGreen("Image Saved")
        
        os.remove(image_file)
        return