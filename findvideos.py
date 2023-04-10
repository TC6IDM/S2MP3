import re
from os.path import exists
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Song import Song
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
    # print("regexing playlist")
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist):
        playlist_uri = match.groups()[0]
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")
    # print("Done regex")
    # get list of tracks in a given playlist (note: max playlist length 100)
    
    playlistName =deleteBadCharacters(removeSymbols(session.user_playlist(USERNAME,playlist_uri)["name"]))
    print("Fetching spotify playlist - "+playlistName+ " https://open.spotify.com/playlist/"+playlist_uri)
    tracks = get_playlist_tracks(session,USERNAME,playlist_uri)
    songList =[]
    
    for index,track in enumerate(tracks,start=1):
        thisTrack = Song(track,index,playlistName)
        songList.append(thisTrack)
    prGreen(f'Playlist {playlistName} has ben fetched with {len(songList)} songs')
    return playlistName,songList

def removePartials(parentFolder):
    if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)
        
    for file in os.listdir(parentFolder):
        if not file.endswith(".mp3"):
            os.remove(parentFolder+"/"+file)

def downloadPlaylist (currentPlaylist):
    playlistFinished = True
    # authenticate
    # print("Loading Spotify Credentials")
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    # create spotify session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # print("done")
    validPlaylist=True if currentPlaylist.startswith("https://open.spotify.com/playlist/") else False
    if not validPlaylist: return playlistFinished
    playlistName,songList = checkPlaylist(currentPlaylist,session)
    removePartials(songList[0].parentFolder)
    for song in songList: 
        if (exists(song.destination+'.mp3')):
            prYellow("SKIP "+song.trackName+" Already Downloaded")
        else:
            song.get_videos()#function is slow
            song.getBestVideo().download()
            playlistFinished = False
    if playlistFinished: 
        prPurple("Playlist : "+playlistName+" Done\n") 
    else:
        prYellow("Playlist : "+playlistName+" Restarting\n")
    return playlistFinished


file = open(PLAYLIST_FILE_NAME,'r')
for currentPlaylist in file.readlines():
    while not downloadPlaylist(currentPlaylist): pass
prPurple("DONE ALL PLAYLISTS")