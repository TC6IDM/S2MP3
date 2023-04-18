import re
from os.path import exists
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Song import Song
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from extraUtil import *

def get_playlist_tracks(sp,username,playlist_id): #slowest part of the program
    playlistLength = sp.user_playlist(username,playlist_id)['tracks']['total']
    print(f'Fetching songs {0} / {playlistLength} {0.00}%                        ',end='\r')
    results = sp.user_playlist_tracks(username,playlist_id)
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
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist):
        playlist_uri = match.groups()[0]
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")
    # get list of tracks in a given playlist (note: max playlist length 100)
    
    playlistName =deleteBadCharacters(removeSymbols(session.user_playlist(USERNAME,playlist_uri)["name"]))
    print("Fetching spotify playlist - "+playlistName+ " https://open.spotify.com/playlist/"+playlist_uri)
    tracks = get_playlist_tracks(session,USERNAME,playlist_uri)
    songList =[]
    
    for index,track in enumerate(tracks,start=1):
        thisTrack = Song(track["track"],index,playlistName)
        songList.append(thisTrack)
    prGreen(f'Playlist {playlistName} has ben fetched with {len(songList)} songs')
    return playlistName,songList

def removePartials(songList):
    parentFolder = songList[0].parentFolder
    if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)
        
    removeFiles = []
    for i,file in enumerate(os.listdir(parentFolder),start=1):
        print(f'validating folder {i} / {len(os.listdir(parentFolder))} ({round(100 * i / len(os.listdir(parentFolder)),2)}%)     ',end='\r')
        audio_file = parentFolder+"\\"+file
        if not re.match(r"^\(\d{4}\).+\.mp3$",file):
            removeFiles.append(audio_file)
        else:
            songNumber = int(re.search(r'\((\d{4})\)', file).group(1))
            if not songList[songNumber-1].destination+'.mp3' == audio_file:
                if "$$" not in audio_file: removeFiles.append(audio_file) # https://github.com/yt-dlp/yt-dlp/issues/6847
            else:
                audio = MP3(audio_file, ID3=EasyID3)
                if audio=={}:
                    removeFiles.append(audio_file)

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
    for currentPlaylist in file.readlines():
        while not downloadPlaylist(currentPlaylist): pass
    prPurple("DONE ALL PLAYLISTS")
    
if __name__ == "__main__":
    stressTest = False
    stressTestPlaylist = "https://open.spotify.com/playlist/0gnLoConJALD8SVqZyP8I1?si=149eda709fcc4426"
    if stressTest:
        while not downloadPlaylist(stressTestPlaylist): pass
        prPurple("Stress Test Done")
    else:
        run()