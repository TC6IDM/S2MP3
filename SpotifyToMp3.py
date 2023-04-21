import re
from os.path import exists
import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Song import Song
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from extraUtil import *

def get_playlist_tracks(sp,username,playlist_id,album): #slowest part of the program
    if not album: playlistLength = sp.user_playlist(username,playlist_id)['tracks']['total']
    else: playlistLength = sp.album(playlist_id)['tracks']['total']
    print(f'Fetching songs {0} / {playlistLength} {0.00}%                        ',end='\r')
    if not album: results = sp.user_playlist_tracks(username,playlist_id)
    else: results = sp.album_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
        #precent done
        print(f'Fetching songs {len(tracks)} / {playlistLength} {round(100 * len(tracks) / playlistLength,2)}%                        ',end='\r')
    print(f'Fetching songs {len(tracks)} / {playlistLength} {round(100 * len(tracks) / playlistLength,2)}%                        ',end='\r')
    print()
    return tracks

def checkPlaylist(playlist,session):
    album=False
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist):
        playlist_uri = match.groups()[0]
    else:
        if match := re.match(r"https://open.spotify.com/album/(.*)\?", playlist):
            album = True
            playlist_uri = match.groups()[0]
        else:
            raise ValueError("Expected format: https://open.spotify.com/(playlist/album)/...")
    # get list of tracks in a given playlist (note: max playlist length 100)
    
    if not album : 
        playlistName =deleteBadCharacters(removeSymbols(session.user_playlist(USERNAME,playlist_uri)["name"]))
        print("Fetching spotify playlist - "+playlistName+ " https://open.spotify.com/playlist/"+playlist_uri)
        
    else : 
        playlistName =deleteBadCharacters(removeSymbols(session.album(playlist_uri)["name"]))
        print("Fetching spotify Album - "+playlistName+ " https://open.spotify.com/album/"+playlist_uri)
        
    tracks = get_playlist_tracks(session,USERNAME,playlist_uri,album)
    
    songList =[]
    # print(tracks)
    for index,track in enumerate(tracks,start=1):
        if not album: thisTrack = Song(track["track"],index,playlistName)
        else: thisTrack = Song(track,index,playlistName)
        songList.append(thisTrack)
    prGreen(f'Playlist {playlistName} has ben fetched with {len(songList)} songs')
    return playlistName,songList

def removeIndividually(file,parentFolder,removeFiles,songList):
    audio_file = parentFolder+"\\"+file
    if not re.match(r"^\(\d{4}\).+\.mp3$",file):
        removeFiles.append(audio_file)
        return removeFiles
    songNumber = int(re.search(r'\((\d{4})\)', file).group(1))
    if not songList[songNumber-1].destination+'.mp3' == audio_file:
        if "$$" not in audio_file: 
            removeFiles.append(audio_file) # https://github.com/yt-dlp/yt-dlp/issues/6847
            return removeFiles
    # print(audio_file)
    audio = MP3(audio_file, ID3=EasyID3)
    if audio=={}:
        removeFiles.append(audio_file)
        return removeFiles
        # print(audio['date'][0] == songList[songNumber-1].releaseDate or audio['date'][0] == re.search('^([^\\-]*)',songList[songNumber-1].releaseDate).group(1))
        # if not (audio['date'][0] == songList[songNumber-1].releaseDate or audio['date'][0] == re.search('^([^\\-]*)',songList[songNumber-1].releaseDate).group(1)):
        #     print(audio['date'])
        #     print(audio['date'][0])
        #     print(songList[songNumber-1].releaseDate)
        #     print(re.search('^([^\\-]*)',songList[songNumber-1].releaseDate).group(1))
        #     time.sleep(5)
    # print(audio)
    if ('artist'  in audio and not (audio['artist'][0] == songList[songNumber-1].trackArtists) or 
        'title'  in audio and not (audio['title'][0] == songList[songNumber-1].trackName) or 
        'albumartist'  in audio and not (audio['albumartist'][0] == songList[songNumber-1].albumArtists) or 
        'album'  in audio and not (audio['album'][0] == songList[songNumber-1].albumName) or 
        'date'  in audio and not (audio['date'][0] == songList[songNumber-1].releaseDate or audio['date'][0] == re.search('^([^\\-]*)',songList[songNumber-1].releaseDate).group(1)) or 
        'discnumber'  in audio and not (audio['discnumber'][0] == str(songList[songNumber-1].discnumber)) or 
        'tracknumber'  in audio and not (audio['tracknumber'][0] == str(songList[songNumber-1].tracknumber))):
        removeFiles.append(audio_file)
        return removeFiles
    
    return removeFiles
def removePartials(songList):
    parentFolder = songList[0].parentFolder
    if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)
        
    removeFiles = []
    for i,file in enumerate(os.listdir(parentFolder),start=1):
        print(f'validating folder {i} / {len(os.listdir(parentFolder))} ({round(100 * i / len(os.listdir(parentFolder)),2)}%)     ',end='\r')                 
        removeFiles = removeIndividually(file,parentFolder,removeFiles,songList)
        
    print()
    for file in removeFiles:
        if os.path.exists(file):
            prRed("Removing "+file)
            os.remove(file)
    
    
            
def downloadPlaylist (currentPlaylist):
    playlistFinished = True
    # authenticate
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    # create spotify session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    validPlaylist=True if currentPlaylist.startswith("https://open.spotify.com/playlist/") or currentPlaylist.startswith("https://open.spotify.com/album/") else False
    validPlaylist=True if currentPlaylist.startswith("https://open.spotify.com/playlist/") else False

    if not validPlaylist: return playlistFinished
    playlistName,songList = checkPlaylist(currentPlaylist,session)
    removePartials(songList)
    for song in songList: 
        if (exists(song.destination+'.mp3') or "$$$" in song.trackName):
            prYellow("SKIP "+song.trackName+" Already Downloaded")
        else:
            song.get_videos()#function is slow
            song.saveToDebug()
            song.getBestVideo().download()
            playlistFinished = False
    if playlistFinished: 
        prPurple("Playlist : "+playlistName+" Done\n") 
    else:
        prYellow("Playlist : "+playlistName+" Restarting\n")
    return playlistFinished


def run():
    file = open(PLAYLIST_FILE_NAME,'r')
    line = ""
    for currentPlaylist in file.readlines():
        subprocess.run(["python" ,"-m" ,"spotdl", re.sub(" .*", "", currentPlaylist).strip() ])
        #regex remove everything after the first space
        # line += re.sub(" .*", "", currentPlaylist).strip()+", "
        # while not downloadPlaylist(currentPlaylist): pass
        pass
    prPurple("DONE ALL PLAYLISTS")
    # print(line)
    
if __name__ == "__main__":
    stressTest = False
    stressTestPlaylist = "https://open.spotify.com/playlist/0gnLoConJALD8SVqZyP8I1?si=149eda709fcc4426"
    if stressTest:
        while not downloadPlaylist(stressTestPlaylist): pass
        prPurple("Stress Test Done")
    else:
        run()