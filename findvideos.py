#https://www.tunemymusic.com/Spotify-to-File.php#step5


from __future__ import unicode_literals
from distutils.log import debug
import json
import csv
from pytube import YouTube 
import secrets
import string
from time import sleep
import random
import string
import time
from tkinter import E
import urllib.request
import os
from dotenv import load_dotenv
import requests
import re
import copy
import youtube_dl
import math
import os
from os.path import exists
import csv
import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import eyed3
from eyed3.id3.frames import ImageFrame
import subprocess
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3  
import shutil # save img locally
import requests
from mutagen.id3 import ID3, APIC, error, TXXX
from pytube import Search

def prRed(skk): print("\033[91m{}\033[00m" .format(skk))
def prRed2(skk,end): print("\033[91m{}\033[00m" .format(skk),end=end)
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m{}\033[00m" .format(skk))

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            
class MyLogger(object):
    '''Logs Errors/warnigs/debugs'''
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        if "'_percent_str'" not in msg: 
            prRed(msg+"\n")

def printBar(name,percentage,eta,speed):
    '''prints a bar to see how the download is coming along'''
    bartotalstring = f'\r{name} ||{percentage} ETA: {eta} Speed: {speed} '
    fill = '█'
    length = BAR_LENGTH - len(bartotalstring) if BAR_LENGTH - len(bartotalstring) > 10 else 10
    printEnd = ""
    filledLength = int(math.floor((float(percentage[:-1])/100)*length))
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{name} |{bar}| {percentage} ETA: {eta} Speed: {speed}    ', end = printEnd)
    
def removeSymbols(text):
    # print(text,"start")
    if r'\\' in text : text = re.sub(r'\\', '(Bslash)', text)
    if '<' in text : text = re.sub('\<', '(LAbracket)', text)
    if '>' in text : text = re.sub('\>', '(RAbracket)', text)
    if '*' in text : text = re.sub('\*', '(asterisk)', text)
    if '?' in text : text = re.sub('\?', '(Qmark)', text)
    if '/' in text : text = re.sub('\/', '(Fslash)', text)
    if '"' in text : text = re.sub('\"', '(Dquote)', text)
    if ':' in text : text = re.sub('\:', '(colon)', text)
    if '|' in text : text = re.sub('\|', '(pipe)', text)
    if '%' in text : text = re.sub('\%', '(percent)', text)
    # print(text,"end")
    return text

def removeSymbolsReverse(text):
    # print(text,"start")
    text = text.replace("(Bslash)","\\")
    text = text.replace("(LAbracket)","<")
    text = text.replace("(RAbracket)",">")
    text = text.replace("(asterisk)","*")
    text = text.replace("(Qmark)","?")
    text = text.replace("(Fslash)","/")
    text = text.replace("(Dquote)",'"')
    text = text.replace("(colon)",":")
    text = text.replace("(pipe)","|")
    text = text.replace("(percent)","%")
    # print(text,"end")
    return text

def youtubeSafeSearch(text):
    # print(text,"start")
    text.replace(" ","+")
    if ' ' in text : text = re.sub(' ', '+', text)
    if '%' in text : text = re.sub('\%', '%25', text)
    if r'\\' in text : text = re.sub(r'\\', '%5C', text)
    if '?' in text : text = re.sub('\?', '%3F', text)
    if '/' in text : text = re.sub('\/', '%2F', text)
    if ':' in text : text = re.sub('\:', '%3A', text)
    if '|' in text : text = re.sub('\|', '%7C', text)
    # print(text,"end")
    return text

def deleteBadCharacters(text):
    text = text.replace(",","")
    text = text.replace("’","'")
    return text.encode('ascii', 'ignore').decode('ascii')

def get_videos(artist,song):
    '''Gets and returns the video ID and Title (as seen on youtube)'''
    # print()
    # intitle = "+%23intitle+official+audio+%23intitle+high+quality+%23intitle+HQ"
    # query = youtubeSafeSearch(artist)+"+-+"+youtubeSafeSearch(song)#Old Method
    
    intitleSTANDARD = "#intitle official audio #intitle high quality #intitle HQ"
    querySTANDARD = artist+" - "+song+" "
    
    #ATTEMPTED NEW WAY
    # data = ""
    # video_lengths=[]
    # while "items" not in data or video_lengths == []:
    
    #     load_dotenv()
    #     developer_key = os.getenv("API_KEY")
    #     url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query+intitle}&type=video&key={developer_key}'
    #     response = requests.get(url)
    #     data = response.json()
    #     video_ids = []
    #     video_titles = []
    #     video_lengths = []
    #     if ("items" not in data): 
    #         for i in range(60):
    #             seconds = 60-i
    #             prRed2(f'ERROR: RATE LIMITED, retry in {seconds} seconds',end='\r')
    #             time.sleep(1)
    #     else:
    #         for item in data["items"]:
    #             video_id = item["id"]["videoId"]
    #             video_title = item["snippet"]["title"]
    #             video_length = 0
    #             while (video_length == 0): 
    #                 yt = YouTube("https://www.youtube.com/watch?v="+video_id)
    #                 video_length = yt.length*1000 
    #                 if (video_length == 0):
    #                     for k in range(60):
    #                         seconds2 = 60-k
    #                         prRed2(f'ERROR: PYTUBE BROKEN, retry in {seconds2} seconds',end='\r')
    #                         time.sleep(1)
                        
            
    #             video_ids.append(video_id)
    #             video_titles.append(video_title)
    #             video_lengths.append(video_length)
        
    # return video_ids,video_titles,video_lengths
    video_ids = []
    video_titles = []
    video_lengths = []
    totalQ = querySTANDARD+intitleSTANDARD
    while (video_ids == [] or video_titles == [] or video_lengths == []):
        

        s = Search(totalQ)
        if (exists(DEBUG_FILE_NAME)): 
            with open(DEBUG_FILE_NAME, "a", encoding="utf-8") as file:
                writer = csv.writer(file, lineterminator = '\n')
                writer.writerow([" "," "," "])
                writer.writerow([" "," "," "])
                writer.writerow([" "," "," "])
                writer.writerow([" "," "," "])
                writer.writerow([" "," "," "])
                file.close()
                
        with open(DEBUG_FILE_NAME, "a", encoding="utf-8") as file:
            writer = csv.writer(file, lineterminator = '\n')
            writer.writerow(["VideoID","title","Length"])
            file.close()
        for i in s.results:                
            with open(DEBUG_FILE_NAME, "a", encoding="utf-8") as file:
                writer = csv.writer(file, lineterminator = '\n')
                writer.writerow([i.video_id,i.title,i.length*1000])
                # prGreen("data saved to "+DEBUG_FILE_NAME)
                file.close()

            video_ids.append(i.video_id)
            video_titles.append(i.title)
            video_lengths.append(i.length*1000)
            

        if (video_ids == [] or video_titles == [] or video_lengths == []):
            totalQ = querySTANDARD
            prRed("QUERY: "+querySTANDARD+intitleSTANDARD+"\nNo results found, retrying without intitle")
    return video_ids,video_titles,video_lengths

    #OLD WAY
    # html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+query+intitle).read().decode()
    # print("Youtube Query: https://www.youtube.com/results?search_query="+query+intitle)
    # if "No results found" in html:
    #     prRed("No results found")
    #     html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+query).read().decode()
    #     print("Youtube Query: https://www.youtube.com/results?search_query="+query)
    # video_ids = re.findall(r'"videoRenderer":{"videoId":"(\S{11})',html)
    # video_titles = re.findall(r'}]},"title":{"runs":\[{"text":"(.*?)"}]',html)
    # video_lengths = re.findall(r'{"thumbnailOverlayTimeStatusRenderer":{"text":{"accessibility":{"accessibilityData":{"label":"(.*?)"}},',html) 
    # if len(video_ids) != len(video_titles) or len(video_ids) != len(video_lengths) or len(video_titles) != len(video_lengths):
    #     prRed("Error: Lengths of video_ids, video_titles, and video_lengths are not equal")
    #     # randomString = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(25))
    #     # with open(f"C:\\Users\\Owner\\Desktop\\Youtube-DL-Code\\{randomString} html.txt","w") as kk:
    #     #     kk.write(str(urllib.request.urlopen("https://www.youtube.com/results?search_query="+query+intitle).read()))
    #     # with open(f"C:\\Users\\Owner\\Desktop\\Youtube-DL-Code\\{randomString} ids_titles_lengths.txt","w") as kk:
    #     #     kk.write(str(str(video_ids)+"\n"+str(video_titles)+"\n"+str(video_lengths)))

    # #totalRegex = re.findall(r'"videoRenderer":{"videoId":"(\S{11})|}]},"title":{"runs":\[{"text":"(.*?)"}]|{"thumbnailOverlayTimeStatusRenderer":{"text":{"accessibility":{"accessibilityData":{"label":"(.*?)"}},',html)

    # return video_ids,video_titles,video_lengths

def get_playlist_tracks(sp,username,playlist_id):
    # playlistName = sp.user_playlist(username,playlist_id)["name"]
    results = sp.user_playlist_tracks(username,playlist_id)
    # with open("C:\\Users\\Owner\\Desktop\\Youtube-DL-Code\\eell.txt","w") as fp:
    #     fp.write(str(results))
    # fp.close()
    # print(playlistName)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# def scavengeData(data,file):
#     prRed("ERROR converting "+file+" to mp3, possible duplicate")
#     load_dotenv()
#     DEBUG_FILE_NAME = os.getenv("DEBUG_FILE_NAME", "")
#     # if not exists(DEBUG_FILE_NAME): 
#     #     with open(DEBUG_FILE_NAME, "a", encoding="utf-8") as file:
#     #         writer = csv.writer(file, lineterminator = '\n')
#     #         writer.writerow(["artist","title","albumartist","album","date","image/jfif","discnumber","tracknumber","Index"])
#     #     file.close()
#     with open(DEBUG_FILE_NAME, "a", encoding="utf-8") as file:
#         writer = csv.writer(file, lineterminator = '')
#         writer.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]])
#         prGreen("File data saved to "+DEBUG_FILE_NAME+"\n")
#     file.close()
    

def setFileData(data,file):
    # print(data,file)
    print("Converting to mp3")
    audio_file = file.replace(".webm", ".mp3").replace(".m4a", ".mp3")
    if exists(audio_file) : prRed("ERROR converting "+file+" to mp3, possible duplicate");return
    subprocess.run('ffmpeg -i "'+file+'" "'+audio_file+'"',shell=True,capture_output=True)
    os.remove(file)
    prGreen(audio_file)
    print("Editing Metadata")
    audio = MP3(audio_file, ID3=EasyID3)
    audio['artist'] = data[0]
    audio['title'] = data[1]
    audio['albumartist'] = data[2]
    audio['album'] = data[3]
    audio['date'] = data[4]
    audio['discnumber'] = data[6]
    audio['tracknumber'] = data[7]
    audio.save()
    tagss = ID3(audio_file)
    tagss.add(TXXX(encoding=3, desc=u'Index', text=str(data[8].replace("\n",""))))
    audio.save()
    prGreen("Metadata Saved")

    load_dotenv()
    OUTPUT_FOLDER_NAME = os.getenv("OUTPUT_FOLDER_NAME","")
    url = data[5]
    #.replace("\n","")
    image_file = OUTPUT_FOLDER_NAME+'tempImage.jfif'
    print("Downloading Album Image")
    res = requests.get(url, stream = True)
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
    prCyan("File Done!\n")
    

    

def my_hook(d):
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
    #print(d)
    #song done
    # print(d['filename'])
    songName = ((removeSymbolsReverse(d['filename'].replace(OUTPUT_FOLDER_NAME,"").replace(".mp3", "").replace(".webm", "").replace(".m4a", ""))).split("\\",1)[1])[7:]#removes the prefix and suffix as well as swapping out the changed symbols
    #.replace(".webm", "").replace(".m4a", "")
    # print(songName)
    if d['status'] == 'finished':
        prGreen("\n"+d['filename'])
        # print(songName)
        # print('\nDone downloading',songName)
        with open(OUTPUT_FILE_NAME,"r") as fpr:
            # read an store all lines into list
            lines = fpr.readlines()
        fpr.close()
        # Write file
        with open(OUTPUT_FILE_NAME,"w") as fpw:
            # iterate each line
            firstonly=0
            for line in lines:
                linearr=line.split(",")
                # delete line with the song name
                # print(songName , line)
                # print(songName, linearr[1],d['status'])
                if (songName != linearr[1]) or firstonly:
                    fpw.write(line)
                else:
                    firstonly=1
                    # print(songName,linearr[1])
                    setFileData(linearr,d['filename'])
        fpw.close()
        # time.sleep(2)

    printBar(songName,d['_percent_str'],d['_eta_str'],d['_speed_str'])
    # print(d['status'])


def checkPlaylist(playlist):
    if (exists(OUTPUT_FILE_NAME)): os.remove(OUTPUT_FILE_NAME)
    # authenticate
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    
    # create spotify session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # get uri from https link
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist):
        playlist_uri = match.groups()[0]
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")

    # get list of tracks in a given playlist (note: max playlist length 100)
    tracks = get_playlist_tracks(session,USERNAME,playlist_uri)
    # print(tracks[417]["track"]["album"]["images"][0]['url']) 
    # create csv file
    playlistName =deleteBadCharacters(removeSymbols(session.user_playlist(USERNAME,playlist_uri)["name"]))
    print("Fetching spotify playlist - "+playlistName+ " https://open.spotify.com/playlist/"+playlist_uri)
    with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator = '\n')
            
        # extract name and artist
        index=0
        for index,track in enumerate(tracks,start=1):
            albumArtists = "/".join(
                [deleteBadCharacters(artist["name"]) for artist in track["track"]["album"]["artists"]]
            )
            #if track["track"]["album"]["images"]: 
            albumPicture = track["track"]["album"]["images"][0]['url']
            # else : 
            #     albumPicture = "NULL"
            albumName = deleteBadCharacters(track["track"]["album"]["name"])
            releaseDate = track["track"]["album"]['release_date']
            trackArtists = "/".join(
                [deleteBadCharacters(artist["name"]) for artist in track["track"]["artists"]]
            )
            trackName = deleteBadCharacters(track["track"]["name"])# annoying characters
            discnumber = track["track"]["disc_number"]
            tracknumber = track["track"]["track_number"]
            duration_ms = track["track"]["duration_ms"]
            # write to csv
            writer.writerow([trackArtists, trackName,albumArtists,albumName,releaseDate,albumPicture,discnumber,tracknumber,index,duration_ms])
        pass
    file.close()
    # print(playlistName)
    prGreen(OUTPUT_FILE_NAME)
    return playlistName
# o = open("C:\\Users\\Owner\\Desktop\\Youtube-DL-Code\\output.txt","w")

def sameMetadata(line,file):
    return line[0]==file['artist'][0] and line[1]==file['title'][0] and line[2]==file['albumartist'][0] and line[3]==file['album'][0] and line[4]==file['date'][0] and line[6]==file['discnumber'][0] and line[7]==file['tracknumber'][0]

def addZeros(number):
    if int(number)<10: return "(000"+number+") "
    if int(number)<100: return "(00"+number+") "
    if int(number)<1000: return "(0"+number+") "
    return"("+number+")"

def getPT(str):
    hours = re.findall(r'(\d+)[^\d]+hour',str)
    minutes = re.findall(r'(\d+)[^\d]+minute',str)
    seconds = re.findall(r'(\d+)[^\d]+second',str)
    playtime_ms = 0
    if hours:
        playtime_ms = playtime_ms + int(hours[0]) * 3600000
    if minutes:
        playtime_ms = playtime_ms + int(minutes[0]) * 60000
    if seconds:
        playtime_ms = playtime_ms + int(seconds[0]) * 1000
    return playtime_ms

#important files
load_dotenv()
DEBUG_FILE_NAME = os.getenv("DEBUG_FILE_NAME", "")
BAR_LENGTH = int(os.getenv("BAR_LENGTH"))
OUTPUT_FOLDER_NAME = os.getenv("OUTPUT_FOLDER_NAME","")
OUTPUT_FILE_NAME = os.getenv("OUTPUT_FILE_NAME", "")
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
USERNAME = os.getenv("USERNAME", "")
COOKIE_FILE = os.getenv("COOKIE_FILE", "")
PLAYLIST_FILE_NAME = os.getenv("PLAYLIST_FILE_NAME", "")

letters = string.digits

if (exists(DEBUG_FILE_NAME)): os.rename(DEBUG_FILE_NAME, 'DEBUG - ' + ' '.join(random.choice(letters) for i in range(10)) + ' .csv')

reallydone = False
while not reallydone:
    reallydone = True
    file = open(PLAYLIST_FILE_NAME,'r')
    for currentPlaylist in file.readlines():
        #removes \n from the end of the playlist
        done=False
        # if (exists(DEBUG_FILE_NAME)): os.remove(DEBUG_FILE_NAME)
        while not done: #while there is still stuff in the playlist, loop through playlist
            playlistName = checkPlaylist(currentPlaylist)
            f = open(OUTPUT_FILE_NAME,"r",encoding="utf-8")
            lines = f.readlines()
            f.close()
            #delets playlist if there is nothing on there
            if len(lines) == 0 :
                # sleep(10)
                f.close()
                os.remove(OUTPUT_FILE_NAME)
                prPurple("Playlist : "+playlistName+" Done\n") 
                done = True
                break
            for x in lines: 
                trackInfo=x.split(",")
                trackInfoRemovedSymbols=removeSymbols(trackInfo[1])
                dupe = 0
                songDestination= OUTPUT_FOLDER_NAME+playlistName+"\\"+addZeros(trackInfo[8].replace("\n",""))+trackInfoRemovedSymbols
                songname = trackInfo[1]
                
                if (exists(songDestination+'.mp3')):
                    #or exists(songDestination+'.webm') or exists(songDestination+'.m4a')
                    prYellow("SKIP "+songname+" Already Downloaded")
                    with open(OUTPUT_FILE_NAME,"r") as fpr1:
                    # read an store all lines into list
                        level = fpr1.readlines()
                    fpr1.close()
                    with open(OUTPUT_FILE_NAME,"w") as fpw1:
                    # iterate each line
                        firstonly=0
                        for line in level:
                            # delete line with the song name
                            # print(songName , line)
                            linearr=line.split(",")
                            # print(songname,linearr[1])
                            if (songname != linearr[1]) or firstonly:
                                fpw1.write(line)
                                # break
                            else:
                                firstonly=1
                                # print(songname,linearr[1])
                            # else:
                            #     setFileData(line.split(","),d['filename'])
                    fpw1.close()
                    dupe = 1
                if dupe==0:
                    reallydone = False
                    # print(trackInfo)
                    # print(youtubeSafeSearch(trackInfo[0]))
                    # editedTrackInfo= trackInfo[0]+" "+trackInfo[1] #New Method
                    # editedTrackInfo = youtubeSafeSearch(trackInfo[0])+"+-+"+youtubeSafeSearch(trackInfo[1])#Old Method
                    # print(editedTrackInfo+"+offical+audio")
                    code,title,length = get_videos(trackInfo[0],trackInfo[1]) #lists
                    
                    # currentname =re.sub(r'^.*?\+\-\+', '', x[:-1]).replace("+", " ")
                    # print(currentname)
                    #make sure that shorter list is iterated
                    found = 0
                    difference = 1000
                    # print()
                    while not found:
                        # print(len(code),len(title),len(length))
                        # if len(code)!= len(title) or len(code)!= len(length) or len(title)!= len(length):
                        #     print(code)
                        #     print(title)
                        #     print(length)
                        # if len(code)<=len(title) and len(code)<=len(length):
                        #     use = len(code)
                        # elif len(title)<=len(code) and len(title)<=len(length):
                        #     use = len(title)
                        # elif len(length)<=len(code) and len(length)<=len(title):
                        #     use = len(length)
                        maxSearchDepth = 5
                        for i in range(len(code) if len(code) < maxSearchDepth else maxSearchDepth):
                            # playtime_ms = getPT(length[i]) #old way
                            playtime_ms = str(length[i]) #new way
                            timediff = abs(int(trackInfo[9])-int(playtime_ms))
                            # print("title: " +title[i]+" length: " +str(length[i])+" url: " +"https://www.youtube.com/watch?v="+code[i]+" title: " +"SpotifyLength: " +str(trackInfo[9].replace("\n",""))+ " YoutubeLength: " +str(playtime_ms)+ " TimeDifference: " +str(timediff)+"\n")
                            if ("clean" not in title[i] and "8d" not in title[i].lower() and "1 hour" not in title[i].lower() and "full album" not in title[i].lower() and timediff <= difference): #not clean version
                                found = 1
                                if (difference!=1000):
                                    print()
                                print("Now Downloading:",title[i],"On Youtube","https://www.youtube.com/watch?v="+code[i])
                                #print(songDestination)
                                ydl_opts = {
                                    'format': 'bestaudio/best',
                                    'postprocessors': [{
                                        'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
                                        'preferredquality': '320',#highest quality
                                    }],
                                    'ignoreerrors': True, #ignore errors
                                    'outtmpl': songDestination+'.%(ext)s', #save songs here .%(ext)s
                                    'logger': MyLogger(),
                                    'progress_hooks': [my_hook],
                                    'cookiefile': COOKIE_FILE, #cookies for downloading age restricted videos
                                }
                                # print('C:/Songs/'+currentname+'.%(ext)s')
                                # o.write("https://www.youtube.com/watch?v="+code[i]+"\n")
                                # print("https://www.youtube.com/watch?v="+code[i],title[i])
                                #download
                                
                                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                    ydl.download(["https://www.youtube.com/watch?v="+code[i]])
                                
                                break
                        if not found:
                            prRed2("No suitable video found for "+trackInfo[1]+ " within "+str(difference)+" ms of the origninal",end="\r")
                            difference+=1000
            
            f = open(OUTPUT_FILE_NAME,"r",encoding="utf-8")
            lines = f.readlines()
            f.close()
            #delets playlist if there is nothing on there
            if len(lines) == 0 :
                # sleep(10)
                f.close()
                os.remove(OUTPUT_FILE_NAME)
                prPurple("Playlist : "+playlistName+" Done\n") 
                done = True
                break
            f.close()
            prYellow("RESTARTING")

# load_dotenv()
# duplicates=[]
# with open(DEBUG_FILE_NAME, "r", encoding="utf-8") as debugFile:
#     missingData = debugFile.readlines()
# debugFile.close()
# for i in missingData:
#     duplicates.append(i[1])

# def convert(old,new,data):
#     print("Converting "+old+" to mp3")
#     subprocess.run('ffmpeg -i "'+old+'" "'+new+'"',shell=True,capture_output=True)
#     os.remove(old)
#     prGreen(new)
#     print("Editing Metadata")
#     audio = MP3(new, ID3=EasyID3)
#     audio['artist'] = data[0]
#     audio['title'] = data[1]
#     audio['albumartist'] = data[2]
#     audio['album'] = data[3]
#     audio['date'] = data[4]
#     audio['discnumber'] = data[6]
#     audio['tracknumber'] = data[7]
#     audio.save()
#     tagss = ID3(new)
#     tagss.add(TXXX(encoding=3, desc=u'Index', text=str(data[8].replace("\n",""))))
#     audio.save()
#     prGreen("Metadata Saved")

#     load_dotenv()
#     OUTPUT_FOLDER_NAME = os.getenv("OUTPUT_FOLDER_NAME","")
#     url = data[5]
#     #.replace("\n","")
#     image_file = OUTPUT_FOLDER_NAME+'tempImage.jfif'
#     print("Downloading Album Image")
#     res = requests.get(url, stream = True)
#     if res.status_code == 200:
#         with open(image_file,'wb') as f:
#             shutil.copyfileobj(res.raw, f)
#         prGreen(image_file+"\n")
#     else:
#         prRed('Album image Couldn\'t be retrieved\n')
#     audio = MP3(new, ID3=ID3)    
#     audio.tags.add(
#     APIC(
#         encoding=3, # 3 is for utf-8
#         mime='image/jfif', # image/jpeg or image/png
#         type=3, # 3 is for the cover image
#         desc=u'Cover',
#         data=open(image_file,'rb').read()
#         )
#     )
#     audio.save()
#     os.remove(image_file)
#spotify
{
'album': 
    {
    'album_type': 'album', 
    'artists': 
        [{
            'external_urls': 
            {'spotify': 'https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x'}, 
            'href': 'https://api.spotify.com/v1/artists/5K4W6rqBFWDnAN6FQUkS6x', 
            'id': '5K4W6rqBFWDnAN6FQUkS6x', 
            'name': 'Kanye West', 
            'type': 'artist', 
            'uri': 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'
        }], 
    'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CG', 'CH', 'CI', 'CL', 'CM', 'CO', 'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH', 'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG', 'MH', 'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NE', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PK', 'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI', 'SK', 'SL', 'SM', 'SN', 'SR', 'ST', 'SV', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 'WS', 'XK', 'ZA', 'ZM', 'ZW'], 
    'external_urls': {'spotify': 'https://open.spotify.com/album/4Uv86qWpGTxf7fU7lG5X6F'}, 
    'href': 'https://api.spotify.com/v1/albums/4Uv86qWpGTxf7fU7lG5X6F', 
    'id': '4Uv86qWpGTxf7fU7lG5X6F', 
    'images': 
        [{
            'height': 640, 
            'url': 'https://i.scdn.co/image/ab67616d0000b27325b055377757b3cdd6f26b78', 
            'width': 640
        }, 
        {
            'height': 300, 
            'url': 'https://i.scdn.co/image/ab67616d00001e0225b055377757b3cdd6f26b78', 
            'width': 300
        }, 
        {
            'height': 64, 
            'url': 'https://i.scdn.co/image/ab67616d0000485125b055377757b3cdd6f26b78', 
            'width': 64
        }], 
    'name': 'The College Dropout', 
    'release_date': '2004-02-10', 
    'release_date_precision': 'day', 
    'total_tracks': 21, 
    'type': 'album', 
    'uri': 'spotify:album:4Uv86qWpGTxf7fU7lG5X6F'
    }, 
'artists': 
    [{
        'external_urls': {'spotify': 'https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x'}, 
        'href': 'https://api.spotify.com/v1/artists/5K4W6rqBFWDnAN6FQUkS6x', 
        'id': '5K4W6rqBFWDnAN6FQUkS6x', 
        'name': 'Kanye West', 
        'type': 'artist', 
        'uri': 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'
    }], 
'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CG', 'CH', 'CI', 'CL', 'CM', 'CO', 'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH', 'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 'KW', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG', 'MH', 'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NE', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 'PK', 'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI', 'SK', 'SL', 'SM', 'SN', 'SR', 'ST', 'SV', 'SZ', 'TD', 'TG', 'TH', 'TJ', 'TL', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 'WS', 'XK', 'ZA', 'ZM', 'ZW'], 
'disc_number': 1, 
'duration_ms': 239880, 
'episode': False, 
'explicit': True, 
'external_ids': {'isrc': 'USDJ20400032'}, 
'external_urls': {'spotify': 'https://open.spotify.com/track/0IW0qaeyxL5Et4UG2MrJKB'}, 
'href': 'https://api.spotify.com/v1/tracks/0IW0qaeyxL5Et4UG2MrJKB', 
'id': '0IW0qaeyxL5Et4UG2MrJKB', 
'is_local': False, 
'name': "We Don't Care", 
'popularity': 66, 
'preview_url': None, 
'track': True, 
'track_number': 2, 
'type': 'track', 
'uri': 'spotify:track:0IW0qaeyxL5Et4UG2MrJKB'
}

